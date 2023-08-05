from elasticsearch import Elasticsearch
from flatten_json import flatten
from logging import getLogger, basicConfig, ERROR, WARN, INFO, DEBUG
from logging.handlers import SysLogHandler
from urllib3 import disable_warnings


class ElasticmonClient(object):
    """ElasticmonClient is the primary client for monitoring Elasticsearch.

    This class is used to poll Elasticsearch for information about the cluster
    health, node statistics, etc. and log that to the loggig systems.

    Attributes:
        es_client (:obj:`elasticsearch.Elasticsearch`): Elasticsearch client
        logger (:obj:`logging.Logger`): Class logger.
    """

    def __init__(self, verbosity=2, hosts=[], environment=''):
        """Initialize a new ElasticmonClient instance.

        Args:
            hosts (list[str]): List of Elasticsearch hosts to connect to.
            verbosity (int): The level at which to log, higher numbers offer
                more logging.
            environment (str): The environment this is logging in.

        Returns:
            None
        """
        disable_warnings()
        self.es_client = Elasticsearch(hosts)
        self.verbosity = verbosity
        self.environment = environment
        self.logger = self.setup_logger()

    def setup_logger(self):
        """Setup the class logging instance.

        Args:
            verbose (bool): True for debug logging, False for info logging

        Returns:
            logging.Logger
        """
        log_format = '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
        basicConfig(format=log_format)
        logger = getLogger("elasticmon")
        if self.verbosity >= 3:
            logger.setLevel(DEBUG)
        elif self.verbosity == 2:
            logger.setLevel(INFO)
        elif self.verbosity == 1:
            logger.setLevel(WARN)
        else:
            logger.setLevel(ERROR)
        logger.addHandler(self.setup_syslog_handler())
        return logger

    def setup_syslog_handler(self, address='/dev/log'):
        """Setup the class logging instance.

        Args:
            address (string or tuple): Where to log syslog information to.

        Returns:
            logging.handler.SysLogHandler
        """
        handler = SysLogHandler(address=address)
        return handler

    def cluster_health(self):
        """Retrieve the cluster health information.

        Returns:
            dict: the cluster health information
        """
        self.logger.debug("start ElasticmonClient.cluster_health")
        chealth = self.es_client.cluster.health()
        self.logger.debug("end ElasticmonClient.cluster_health")
        return chealth

    def cluster_stats(self):
        """Retrieve the cluster statistics.

        Returns:
            dict: the cluster state information
        """
        self.logger.debug("start ElasticmonClient.cluster_stats")
        cstats = self.es_client.cluster.stats()
        self.logger.debug("end ElasticmonClient.cluster_stats")
        return cstats

    def node_stats(self):
        """Retrieve the node statistics information.

        Returns:
            dict: the node statistics information
        """
        self.logger.debug("start ElasticmonClient.node_stats")
        nstats = self.es_client.nodes.stats()
        self.logger.debug("end ElasticmonClient.node_stats")
        return nstats

    def print_cluster_health_flattened(self, j):
        """Print the flattened data

        Args:
            j (dict): The dictionary that should be flattened.
        """
        self.logger.debug(
            "start ElasticmonClient.print_cluster_health_flattened")
        fields = [
            'application=elasticmon', 'data_type=cluster_health',
            'environment={env}'.format(env=self.environment)
        ]
        self.print_flattened(j=j, fields=fields)
        self.logger.debug("end ElasticmonClient.print_cluster_health_flattened")

    def print_cluster_stats_flattened(self, j):
        """Print the flattened data

        Args:
            j (dict): The dictionary that should be flattened.
        """
        self.logger.debug(
            "start ElasticmonClient.print_cluster_stats_flattened")
        fields = [
            'application=elasticmon', 'data_type=cluster_stats',
            'environment={env}'.format(env=self.environment)
        ]
        self.print_flattened(j=j, fields=fields)
        self.logger.debug("end ElasticmonClient.print_cluster_stats_flattened")

    def print_node_stats_flattened(self, j):
        """Print the flattened data

        Args:
            j (dict): The dictionary that should be flattened.
        """
        self.logger.debug(
            "start ElasticmonClient.print_cluster_health_flattened")
        node_names = []
        if 'nodes' in j:
            node_names = j['nodes'].keys()

        for node in node_names:
            fields = [
                'node={node}'.format(node=node), 'application=elasticmon',
                'data_type=node_stats', 'environment={env}'.format(
                    env=self.environment)
            ]
            self.print_flattened(j=j['nodes'][node], fields=fields)
        self.logger.debug("end ElasticmonClient.print_cluster_health_flattened")

    def chunks(self, l, n):
        """Yield successive n-sized chunks from l."""
        for i in range(0, len(l), n):
            yield l[i:i + n]

    def print_flattened(self, j, fields=['application=elasticmon']):
        """Print the flattened data

        Args:
            j (dict): The dictionary that should be flattened.
        """
        syslog_line = []
        self.logger.debug("start ElasticmonClient.print_flattened")
        flat = flatten(j)
        for k, v in list(flat.items()):
            syslog_line.append('{key}={value}'.format(key=k, value=v))
            print('{key}: {value}'.format(key=k, value=v))

        for output_row in self.chunks(syslog_line, 10):
            output_row += fields
            self.logger.info(' '.join(output_row))
        self.logger.debug("end ElasticmonClient.print_flattened")
