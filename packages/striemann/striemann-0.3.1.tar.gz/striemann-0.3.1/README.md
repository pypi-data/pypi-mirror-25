Send metrics to the Riemann monitoring system

## Run the tests

A `tox.ini` file is provided to run the tests with different versions of
Python.

To run the tests:

1. Install tox
2. Run `tox` from the root folder of the repository


## Changes

0.3.1 - We now reconnect if there is an exception when flushing
0.3.0 - Added missing TTL parameter to `time` method
0.2.0 - TTL is no longer converted to string.
