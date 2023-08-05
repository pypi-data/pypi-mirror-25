import hashlib
from graphviz import Digraph


class Diagram(object):
    """
    Diagram class to parse and render the diagram file.
    """

    def __init__(self, diagram_name, diagram_file_name):
        """
        initialize the diagram

        :param diagram_name: name of the diagram
        :param diagram_file_name: diagram file path
        """
        self.diagram_file_name = diagram_file_name
        self.diagram_name = diagram_name

    def parse_diagram(self):
        """
        Parse the diagram file and get the edges and clusters

        clr: a,b
        clr -> c
        c .> d

        edges: [{head:clr,tail:c,style:hard},{head:c,tail:d,style:soft}
        clusters: {clr: [a,b]}

        each node is a dictionary itself

        :return: edges and clusters
        """
        with open(self.diagram_file_name) as diagram_file:
            lines = diagram_file.read().splitlines()

        edges = []
        clusters = {}
        for line in lines:
            # if there is a '->' or '.>' in a line then it's an edge.
            if '->' in line or '.>' in line:
                if '->' in line:
                    head, tail = line.split('->')
                else:
                    head, tail = line.split('.>')

                edge = {
                    'head': self.parse_node(head),
                    'tail': self.parse_node(tail),
                    'style': 'hard' if '->' in line else 'soft'
                }

                edges.append(edge)

            # if there is ':' in a line then it's a cluster
            elif ':' in line:
                cluster, nodes = line.split(':')
                clusters[cluster.strip()] = [self.parse_node(node) for node in nodes.split(',')]

        return edges, clusters

    @staticmethod
    def parse_node(node_str):
        """
        parse a node and find out the elements as following

        parsing

        apple_news(date, status=2)

        return

        {
          'name': 'apple_news
          'unique_name': ##### some unique id based on node name and node params
          'params': [{'name': 'date','value':''},{'name':'status','value':'2'}]
          'pretty_params': date, status=2
        }

        :param node_str: node to be parsed
        :return: dictionary of elements
        """
        node_name = node_str.strip()
        name_values = []
        unique_name = node_name
        pretty_params = ''

        if '(' in node_str and ')' in node_str:

            node_name = node_str[:node_str.index('(')].strip()
            params_str = node_str[node_str.index('(') + 1:node_str.index(')')]
            params = params_str.split('|')
            for param in params:
                value = ''
                name = param
                if '=' in param:
                    name, value = param.split('=')
                name_values.append({
                    'name': name.strip(),
                    'value': value.strip()
                })

            unique_name = node_name + hashlib.md5(str(name_values)).hexdigest()

            pretty_params = ', '.join([
                name_value['name'] + (' = ' if name_value['value'] else '') + name_value['value']
                for name_value in name_values
            ])

        return {
            'name': node_name,
            'unique_name': unique_name,
            'params': name_values,
            'pretty_params': pretty_params,
        }

    def render(self, edges, clusters):
        """
        render the graph using Graphviz library

        :param edges: edges e.g.
        [{head:clr,tail:c,style:hard},{head:c,tail:d,style:soft}
        clr, c and d are dictionary
        :param clusters: clusters e.g. {clr: [a,b]}
        """

        dot = Digraph(comment=self.diagram_name)
        # for drawing line between clusters
        dot.attr(compound='true')

        # draw the clusters and the nodes in each of them
        for cluster in clusters:
            with dot.subgraph(name='cluster_{}'.format(cluster)) as cls:
                for node in clusters[cluster]:
                    cls.node(node['unique_name'], node['name'] + '\n' + node['pretty_params'])

        # find out all nodes from the edges
        nodes = []
        for edge in edges:
            if edge['head'] not in nodes and edge['head']['unique_name'] not in clusters:
                nodes.append(edge['head'])
            if edge['tail'] not in nodes and edge['tail']['unique_name'] not in clusters:
                nodes.append(edge['tail'])

        # draw all the nodes
        # unique_name is used for the name of the node
        # which is generated uniquely based on params and name of the node
        for node in nodes:
            dot.node(node['unique_name'], node['name'] + '\n' + node['pretty_params'])

        for edge in edges:

            style = 'dashed' if edge['style'] == 'soft' else 'solid'
            lhead = None
            ltail = None
            head_unique_name = edge['head']['unique_name']
            tail_unique_name = edge['tail']['unique_name']

            # if the edge is between clusters we need to do a trick
            # the middle node in each clusters is found
            # and edge is drawn between middle nodes
            # then we draw the edge starting and ending the clusters not the node itself
            # it looks nicer!
            if edge['head']['name'] in clusters:
                mid_index = lambda cluster_name: len(clusters[cluster_name]) / 2
                head_mid_index = mid_index(edge['head']['name'])
                head = clusters[edge['head']['name']][head_mid_index]
                head_unique_name = head['unique_name']
                ltail = 'cluster_{}'.format(edge['head']['name'])
            if edge['tail']['name'] in clusters:
                mid_index = lambda cluster_name: len(clusters[cluster_name]) / 2
                tail_mid_index = mid_index(edge['tail']['name'])
                tail = clusters[edge['tail']['name']][tail_mid_index]
                tail_unique_name = tail['unique_name']
                lhead = 'cluster_{}'.format(edge['tail']['name'])

            dot.edge(
                head_unique_name, tail_unique_name,
                style=style,
                ltail=ltail,
                lhead=lhead
            )

        dot.render('diagram.gv', view=True)

    def show(self):
        """
        parse diagram and render it
        """

        edges, clusters = self.parse_diagram()
        self.render(edges, clusters)
