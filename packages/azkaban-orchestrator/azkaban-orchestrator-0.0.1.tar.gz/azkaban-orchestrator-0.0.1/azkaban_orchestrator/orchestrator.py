import diagram
import graph


class Client(object):
    """
    Orchestrator client class
    """

    def __init__(self, diagram_file_name, host, username, password, logger):
        """
        Initialise the client with diagram file and azkaban credentials

        :param diagram_file_name: diagram file name
        :param host: azkaban host
        :param username: azkaban username
        :param password: azkaban password
        :param logger: logger
        """
        self.logger = logger
        self.diagram_file_name = diagram_file_name
        self.host = host
        self.username = username
        self.password = password

    def run(self, initial, params):
        """
        Run the orchestrator

        :param initial: initial pipeline
        :param params: parameters needed ro run pipelines
        :return:
        """
        azk_diagram = diagram.Diagram("diagram", self.diagram_file_name)
        edges, clusters = azk_diagram.parse_diagram()

        azk_graph = graph.Graph(
            edges,
            clusters,
            params,
            self.host,
            self.username,
            self.password,
            self.logger
        )

        initial = diagram.Diagram.parse_node(initial) if initial else None

        azk_graph.traverse(initial=initial)
