# The configuration and results of DoQ vs DoT DNS resolver benchmark

## dns_server_configs
contains configuration of each DNS resolver measured in this benchmark.

## systemd_configs
contains the systemd unit configuration
of the DNS resolvers. Knot Resolver does not have
a systemd unit configured because it didn't require one.
running Knot Resolver with a manager process means that
any worker failures that might occur will be resolved
simply by the manager restarting said worker.

## measurements
contain the complete benchmark results
from a test which was run on the 16th of october 2025.
The measurement directory contains many
subdirectorie which might seem to have a crypting naming.
here is the semantic meaning of the directory names

bench_\<protocol\>_\<DNS server\>_\<number of clients\>

where the DNS server is an integer number which corresponds to the
last number of the IP address the DNS resolver listens on

bench_\<protocol\>_1_...   is kresd (single worker)
bench_\<protocol\>_3_...   is Unbound
bench_\<protocol\>_4_...   is RouteDNS
bench_\<protocol\>_5_...   is Knot Resolver run with manager

these IP addresses can be found in the dns_server_configs/*.conf

## run_bench.py
is the python script used to perform the tests
the current configuration (seen at the top of the script)
runs for approximately 10 hours.
