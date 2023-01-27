prometheus-salt-exporter
========================

Prometheus Exporter for Salt highstate metrics run from the Salt master.
The exporter must have permissions to execute commands locally.

Note: Python 2 is not supported. Instead use Python 3.8 or higher.

Inspired by `BonnierNews/saltstack_exporter <https://github.com/BonnierNews/saltstack_exporter>`__

Prerequisites
-------------

-  Install
   `salt <https://docs.saltproject.io/salt/install-guide/en/latest/>`__
-  Be on the salt master node

Installation
------------

.. code:: shell

   pip install prometheus-salt-exporter

Configuration and Usage
-----------------------

::

   usage: prometheus_salt_exporter [-h] [--listen-addr LISTEN_ADDR] [--listen-port LISTEN_PORT] [--highstate-interval HIGHSTATE_INTERVAL] [--batch-size BATCH_SIZE]
                                 [--salt-target SALT_TARGET] [--log-level LOG_LEVEL]

   optional arguments:
   -h, --help            show this help message and exit
   --listen-addr LISTEN_ADDR
                           Address to bind to (default: 0.0.0.0)
   --listen-port LISTEN_PORT
                           Port to bind to (default: 9175)
   --highstate-interval HIGHSTATE_INTERVAL
                           Seconds between each highstate test run (default: 300)
   --batch-size BATCH_SIZE
                           Batch size to use in salt (default: 10)
   --salt-target SALT_TARGET
                           Salt target to be used (default: *)
   --log-level LOG_LEVEL
                           log level (default: 30)

Metrics
-------

Currently, the exporter exposes metrics for highstate conformity only:

+---------------------------+---------------------------------------------+
| Metric                    | Description                                 |
+===========================+=============================================+
|| saltstack_states_total   || Number of states which apply to the minion |
||                          || in highstate                               |
+---------------------------+---------------------------------------------+
|| saltstack_nonhigh_states || Number of states which would change on     |
||                          || state.highstate                            |
+---------------------------+---------------------------------------------+
|| saltstack_error_states   || Number of states which returns an error on |
||                          || highstate dry-run                          |
+---------------------------+---------------------------------------------+
| saltstack_highstate_error | Error in trying to apply highstate          |
+---------------------------+---------------------------------------------+
|| saltstack_last_highstate || Timestamp of the last highstate test run   |
||                          ||                                            |
+---------------------------+---------------------------------------------+

Output
~~~~~~

::

   # HELP saltstack_last_highstate_total Timestamp of the last highstate test run
   # TYPE saltstack_last_highstate_total counter
   saltstack_last_highstate_total 1.674730426e+09
   # HELP saltstack_states_total Number of states which apply to the minion in highstate
   # TYPE saltstack_states_total gauge
   saltstack_states_total{minion="3.mymachine"} 253.0
   # HELP saltstack_nonhigh_states Number of states which would change on state.highstate
   # TYPE saltstack_nonhigh_states gauge
   saltstack_nonhigh_states{minion="3.mymachine"} 0.0
   # HELP saltstack_error_states Number of states which returns an error on highstate dry-run
   # TYPE saltstack_error_states gauge
   saltstack_error_states{minion="3.mymachine"} 0.0
   # HELP saltstack_states_total Number of states which apply to the minion in highstate
   # TYPE saltstack_states_total gauge
   saltstack_states_total{minion="3.mymachine"} 253.0
   saltstack_states_total{minion="2.mymachine"} 253.0
   # HELP saltstack_nonhigh_states Number of states which would change on state.highstate
   # TYPE saltstack_nonhigh_states gauge
   saltstack_nonhigh_states{minion="3.mymachine"} 0.0
   saltstack_nonhigh_states{minion="2.mymachine"} 0.0
   # HELP saltstack_error_states Number of states which returns an error on highstate dry-run
   # TYPE saltstack_error_states gauge
   saltstack_error_states{minion="3.mymachine"} 0.0
   saltstack_error_states{minion="2.mymachine"} 0.0
   # HELP saltstack_states_total Number of states which apply to the minion in highstate
   # TYPE saltstack_states_total gauge
   saltstack_states_total{minion="3.mymachine"} 253.0
   saltstack_states_total{minion="2.mymachine"} 253.0
   saltstack_states_total{minion="1.mymachine"} 253.0
   # HELP saltstack_nonhigh_states Number of states which would change on state.highstate
   # TYPE saltstack_nonhigh_states gauge
   saltstack_nonhigh_states{minion="3.mymachine"} 0.0
   saltstack_nonhigh_states{minion="2.mymachine"} 0.0
   saltstack_nonhigh_states{minion="1.mymachine"} 0.0
   # HELP saltstack_error_states Number of states which returns an error on highstate dry-run
   # TYPE saltstack_error_states gauge
   saltstack_error_states{minion="3.mymachine"} 0.0
   saltstack_error_states{minion="2.mymachine"} 0.0
   saltstack_error_states{minion="1.mymachine"} 0.0
