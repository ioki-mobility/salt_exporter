import os
import signal
import sys
import threading
import time

from prometheus_client.core import CounterMetricFamily, GaugeMetricFamily
from salt.exceptions import AuthenticationError, SaltClientError, SaltClientTimeout


class SaltHighstateCollector:
    def __init__(self, caller, params, log):
        self.caller = caller
        self.params = params
        self.log = log
        self.breaking_errors = [
            "The salt master could not be contacted. Is master running?",
            "Authentication error occurred.",
        ]

        self.statedata = None

        self.states_last_highstate = lambda sample: CounterMetricFamily(
            "saltstack_last_highstate",
            "Timestamp of the last highstate test run",
            value=sample,
        )

        # Start worker thread that will collect metrics async
        thread = threading.Thread(target=self.collect_worker)
        try:
            thread.daemon = True
            thread.start()
        except (KeyboardInterrupt, SystemExit):
            thread.join(0)
            sys.exit()

    def collect_worker(self):
        """A method only run once every `--highstate-interval`
        This allows us to not rerun salt state.highstate on every request to /metrics

        Especially on larger saltstacks, calling salt might take some time.
        Hence, it makes sense to collect the data independently of HTTP calls to
        the Prometheus Salt exporter.
        """
        while True:
            try:
                self.log.info(f"Reading highstate for target '{self.params.salt_target}'")
                self.statedata = list(self.caller.cmd_batch(
                    tgt=self.params.salt_target,
                    fun="state.highstate",
                    batch=self.params.batch_size,
                    kwarg={
                        "test": True,
                        "batch-wait": self.params.batch_wait,
                    },
                ))
                self.log.info(f"Done reading highstate for target '{self.params.salt_target}'")
            except (SaltClientError, SaltClientTimeout, AuthenticationError) as ex:
                self.log.error(ex)
                # exit with error code if the master is not running at all
                if ex.message in self.breaking_errors:
                    os.kill(os.getpid(), signal.SIGINT)
                # wait before retrying after an error
                time.sleep(self.params.wait_on_error_interval)
                continue
            self.last_highstate = int(time.time())
            time.sleep(self.params.highstate_interval)

    def collect(self):
        self.log.info("Received request to send out metrics.")

        try:
            yield self.states_last_highstate(self.last_highstate)
        except AttributeError:
            # the first collection of metrics by the worker is not done yet
            # only available metrics in the prometheus registry will be returned to the user
            return

        for statedict in self.statedata:
            instance, state = next(iter(statedict.items()))
            success = isinstance(state, dict) and len(statedict) == 1

            if not success:
                metrics_states_apply_error = GaugeMetricFamily(
                    "saltstack_highstate_error",
                    "Error in trying to apply highstate",
                    labels=["minion"],
                )
                self.log.error(f"Failed to collect Highstate. Return data: {state}")
                metrics_states_apply_error.add_metric([instance], 1)
                yield metrics_states_apply_error
                continue

            metrics_states_total = GaugeMetricFamily(
                "saltstack_states_total",
                "Number of states which apply to the minion in highstate",
                labels=["minion"],
            )
            metrics_states_nonhigh = GaugeMetricFamily(
                "saltstack_nonhigh_states",
                "Number of states which would change on state.highstate",
                labels=["minion"],
            )
            metrics_states_error = GaugeMetricFamily(
                "saltstack_error_states",
                "Number of states which returns an error on highstate dry-run",
                labels=["minion"],
            )

            states_nonhigh, states_error = 0, 0
            for value in state.values():
                if value["result"] is None:
                    states_nonhigh += 1
                if value["result"] is False:
                    states_error += 1

            metrics_states_total.add_metric([instance], len(state))
            yield metrics_states_total

            metrics_states_nonhigh.add_metric([instance], states_nonhigh)
            yield metrics_states_nonhigh

            metrics_states_error.add_metric([instance], states_error)
            yield metrics_states_error
