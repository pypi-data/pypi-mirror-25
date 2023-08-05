from elasticmon.client import ElasticmonClient
from argparse import ArgumentParser


def main():
    parser = ArgumentParser(description='Elasticsearch monitoring client')
    parser.add_argument(
        '--verbose',
        '-v',
        action='count',
        dest='verbosity',
        help=
        'verbose mode (-v for warnings, -vv for informational, -vvv for debug')
    parser.add_argument(
        '--es-hosts',
        '-e',
        dest='es_hosts',
        nargs='+',
        help='elasticsearch host(s) to retrieve information from')
    parser.add_argument(
        '--environment',
        '-n',
        dest='environment',
        nargs='?',
        help='the environment in which this tool is running')

    args = parser.parse_args()

    mon_client = ElasticmonClient(
        environment=args.environment,
        verbosity=args.verbosity,
        hosts=args.es_hosts)
    chealth = mon_client.cluster_health()
    mon_client.print_cluster_health_flattened(j=chealth)

    cstats = mon_client.cluster_stats()
    mon_client.print_cluster_stats_flattened(j=cstats)

    istats = mon_client.indices_stats()
    mon_client.print_indices_stats_flattened(j=istats)

    nstats = mon_client.node_stats()
    mon_client.print_node_stats_flattened(j=nstats)
