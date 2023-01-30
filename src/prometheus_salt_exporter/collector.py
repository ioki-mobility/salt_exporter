import sys
import threading
import time

from prometheus_client.core import CounterMetricFamily, GaugeMetricFamily
from salt.exceptions import SaltClientError, SaltClientTimeout


class SaltHighstateCollector:
    def __init__(self, caller, params, log):
        self.caller = caller
        self.params = params
        self.log = log

        self.statedata = None

        self.states_total = GaugeMetricFamily(
            "saltstack_states_total",
            "Number of states which apply to the minion in highstate",
            labels=["minion"],
        )
        self.states_nonhigh = GaugeMetricFamily(
            "saltstack_nonhigh_states",
            "Number of states which would change on state.highstate",
            labels=["minion"],
        )
        self.states_error = GaugeMetricFamily(
            "saltstack_error_states",
            "Number of states which returns an error on highstate dry-run",
            labels=["minion"],
        )
        self.states_apply_error = GaugeMetricFamily(
            "saltstack_highstate_error",
            "Error in trying to apply highstate",
            labels=["minion"],
        )
        self.states_last_highstate = lambda sample: CounterMetricFamily(
            "saltstack_last_highstate",
            "Timestamp of the last highstate test run",
            value=sample,
        )

        # Start worker thread that will collect metrics async
        thread = threading.Thread(target=self.collect_worker, args=(params.highstate_interval,))
        try:
            thread.daemon = True
            thread.start()
        except (KeyboardInterrupt, SystemExit):
            thread.join(0)
            sys.exit()

    def collect_worker(self, highstate_interval):
        """A method only run once every `--highstate-interval`
        This allows us to not rerun salt state.highstate on every request to /metrics

        Especially on larger saltstacks, calling salt might take some time.
        Hence, it makes sense to collect the data independently of HTTP calls to
        the Prometheus Salt exporter.
        """
        while True:
            try:
                self.statedata = list(self.caller.cmd_batch(
                    tgt=self.params.salt_target,
                    fun="state.highstate",
                    batch=self.params.batch_size,
                    kwarg={"test": True},
                ))
            except (SaltClientError, SaltClientTimeout) as ex:
                self.log.error(ex)
                # wait before retrying after an error
                time.sleep(300)
                continue
            self.last_highstate = int(time.time())
            time.sleep(highstate_interval)

    def describe(self):
        """Running highstate on startup can be slow, so we describe instead
        """
        yield self.states_total
        yield self.states_nonhigh
        yield self.states_error
        yield self.states_apply_error
        yield self.states_last_highstate(None)

    def collect(self):
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
                self.log.error(f"Failed to collect Highstate. Return data: {state}")
                self.states_apply_error.add_metric([instance], 1)
                yield self.states_apply_error
                continue

            states_nonhigh, states_error = 0, 0
            for value in state.values():
                if value["result"] is None:
                    states_nonhigh += 1
                if value["result"] is False:
                    states_error += 1

            self.states_total.add_metric([instance], len(state))
            yield self.states_total

            self.states_nonhigh.add_metric([instance], states_nonhigh)
            yield self.states_nonhigh

            self.states_error.add_metric([instance], states_error)
            yield self.states_error
