from collections import deque
import azkaban


class Graph(object):
    """
    Graph class for traversing in the graph defined by diagram file.
    """

    def __init__(self, edges, clusters, params, host, username, password, logger):
        """
        initialise the graph

        :param edges: diagram edges
        :param clusters: diagram clusters
        :param params: parameters
        :param host: azkaban host
        :param username: azkaban username
        :param password: azkaban password
        :param logger: logger
        """
        self.edges = edges
        self.clusters = clusters
        self.visited_nodes = []
        self.params = params
        self.logger = logger
        self.client = azkaban.Client(host, username, password, logger)

    def traverse(self, initial=None):
        """
        Traverse the graph from starting nodes based on node status and traverse condition
        :return path: visited nodes path
        """

        path = []
        queue = deque()

        # starting nodes
        initials = [initial] if initial else self.initials()
        queue.extend(initials)

        while len(queue) > 0:

            # get all the nodes in queue
            nodes = []
            while len(queue) > 0:
                nodes.append(queue.popleft())

            # run all the nodes and get the results
            results = self.run(nodes)
            path.extend(nodes)

            # append the results to the visited nodes list
            for result in results:
                self.visited_nodes.append({
                    'node': result['node'],
                    'status': result['status']
                })

            # for all the nodes, find the destinations
            # for each node if it can traverse to any destination
            # put that destination into the queue
            for node in nodes:
                destinations = self.destinations(node)

                for destination in destinations:
                    if all([self.can_traverse(source, destination) for source in self.sources(destination)]):
                        if destination not in queue:
                            queue.append(destination)

                # if the node is a leaf (no destinations) and the node result is false.
                # terminate the traverse
                if not destinations:
                    status = next(result['status'] for result in results if result['node'] == node)
                    if not status:
                        self.logger.error('TERMINATING  {node_name}'.format(
                            node_name=node['name'],
                        ))
                        raise Exception('Terminating')
        return path

    def initials(self):
        """
        get the starting nodes which are the nodes which do not have any source
        a -> b, c -> b: initials are a and c

        :return starting nodes
        """

        initials = []
        for edge1 in self.edges:
            initial = True
            for edge2 in self.edges:
                if edge1 != edge2:
                    if edge1['head'] == edge2['tail']:
                        initial = False
                        break
            if initial and edge1['head'] not in initials:
                initials.append(edge1['head'])

        return initials

    def destinations(self, node):
        """
        get the destinations of a node
        a->b, a->c: destinations are b and c

        :param node: node
        :return: destination nodes
        """

        return [edge['tail'] for edge in self.edges if edge['head'] == node]

    def sources(self, node):
        """
        get the sources of a node
        a -> b, c -> b: soruces are a and c

        :param node: node
        :return: source nodes
        """

        return [edge['head'] for edge in self.edges if edge['tail'] == node]

    def can_traverse(self, source, destination):
        """
        find out if traverse can happen between source and destination
        if the source is already visited in the graph and the source result is True OR
        the source result is False but traverse condition is 'soft' THEN
        it can traverse

        :param source: source node
        :param destination: destination node
        :return: True if it can traverse otherwise False
        """

        try:
            visited_node = next(visited_node for visited_node in self.visited_nodes if visited_node['node'] == source)
            source_status = visited_node['status']
        except StopIteration:
            return False

        try:
            edge = next(edge for edge in self.edges if edge['head'] == source and edge['tail'] == destination)
            traverse_condition = edge['style']
        except StopIteration:
            return False

        if (traverse_condition == 'hard' and source_status) or (traverse_condition == 'soft'):
            return True
        else:
            # if it cannot traverse because the source result is false and traverse condition is hard
            # terminates the traverse
            self.logger.error('TERMINATING  {source} -> {destination}'.format(
                source=source['name'],
                destination=destination['name']
            ))
            raise Exception('Terminating')

        return False

    def run(self, nodes):
        """
        Run all the nodes and return the result

        :param nodes: nodes needs to be run
        :return: list of node and status
        """

        exec_nodes = {}
        compiled_nodes = []

        # combine cluster nodes and normal nodes
        for node in nodes:
            if node['name'] in self.clusters:
                compiled_nodes.extend(self.clusters[node['name']])
            else:
                compiled_nodes.append(node)

        # run all the nodes
        for node in compiled_nodes:

            # prepare the params
            # if the param has a value in diagram definition use that one
            # otherwise use ones which are passing to the graph
            params = node['params']
            compiled_params = {}
            for param in params:
                key = param['name']
                value = param['value']
                if not value and key in self.params:
                    value = self.params[key]
                compiled_params[key] = value

            self.logger.info('Running   {project}:{params}'.format(project=node['name'], params=compiled_params))
            exec_id = self.client.run_pipeline(node['name'], node['name'], compiled_params)
            exec_nodes[exec_id] = node

        # check the results of all nodes
        results = []
        for exec_id, node in exec_nodes.iteritems():
            self.logger.info('Checking  {project}({exec_id})'.format(
                project=node['name'],
                exec_id=exec_id
            ))
            status = self.client.check_pipeline(exec_id)
            results.append({
                'node': node,
                'status': status
            })
            self.logger.info('{status}  {project}({exec_id})'.format(
                project=node['name'],
                exec_id=exec_id,
                status='SUCCEEDED' if status else 'FAILED'
            ))

        # compile the results based on single node and cluster nodes result
        compiled_results = []
        for node in nodes:
            # if it's cluster node
            # the final result is the combined results of all nodes in the cluster
            if node['name'] in self.clusters:
                status = True
                for result in results:
                    if result['node'] in self.clusters[node['name']]:
                        if not result['status']:
                            status = False

                compiled_result = {
                    'node': node,
                    'status': status
                }
            # if it's normal node
            # the final result is the result of the single node itself.
            else:
                for result in results:
                    if result['node'] == node:
                        compiled_result = result

            compiled_results.append(compiled_result)

        return compiled_results
