The configuration and results of DoQ vs DoT DNS resolver benchmark

dns_server_configs contains configuration of each DNS resolver
measured in this benchmark.

systemd_configs contains the systemd unit configuration
of the DNS resolvers. Knot Resolver does not have
a systemd unit configured because it didn't require one.
running Knot Resolver with a manager process means that
any worker failures that might occur will be resolved
simply by the manager restarting said worker.

measurements contain the complete benchmark results
from a test which was run on the 16th of october 2025

run_bench.py is the python script used to perform the tests
the current configuration (seen at the top of the script)
runs for approximately 10 hours.
