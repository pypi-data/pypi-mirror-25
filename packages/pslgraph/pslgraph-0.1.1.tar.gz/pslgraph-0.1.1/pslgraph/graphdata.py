from d3m_types.base import Graph
import networkx as nx
import numpy as np

class GraphData(Graph) :
    """
    This is the concrete implementation of the D3M abstract type. This class is used by the PSLGraphPrimitive class to
    represtent the graph input and output data. This class inherits the following attributes

    Attributes
    ----------
    adjacency_matrix : scipy csr matrix

    _num_vertices : int
        Number of vertices

    _num_edges : int
        Number of edges

    _directed : boolean
        Declares if it is a directed graph or not

    _weighted : boolean
        Declares if it is a weighted graph or not

    _dangling_nodes : int numpy array
        Nodes with zero edges

    d : float64 numpy vector
        Degrees vector

    dn : float64 numpy vector
        Component-wise reciprocal of degrees vector

    d_sqrt : float64 numpy vector
        Component-wise square root of degrees vector

    dn_sqrt : float64 numpy vector
        Component-wise reciprocal of sqaure root degrees vector

    vol_G : float64 numpy vector
        Volume of graph

    components : list of sets
        Each set contains the indices of a connected component of the graph

    number_of_components : int
        Number of connected components of the graph

    bicomponents : list of sets
        Each set contains the indices of a biconnected component of the graph

    number_of_bicomponents : int
        Number of connected components of the graph

    core_numbers : dictionary
        Core number for each vertex
    """

    def __init__(self, filename, file_type='gml', separator='\t'):
        """
        Initializes the graph from a gml or a edgelist file and initializes the attributes of the class.

        Parameters
        ----------
        filename : string
            Name of the file, for example 'JohnsHopkins.edgelist' or 'JohnsHopkins.gml'.

        dtype : string
            Type of file. Currently only 'edgelist' and 'gml' are supported.
            Default = 'gml'

        separator : string
            used if file_type = 'edgelist'
            Default = '\t'
        """
        super().__init__(filename, file_type, separator)
        self.read_graph(filename, file_type, separator)
        self._graph_filename = filename

    def biconnected_components(self):
        pass

    def import_text(self, filename, separator):
        pass

    def connected_components(self):
        pass

    def compute_statistics(self):
        pass

    def core_number(self):
        pass

    def is_disconnected(self):
        pass

    def read_graph(self, filename, file_type='gml', separator='\t'):
        """
        Reads the graph from a gml or a edgelist file and initializes the class attribute adjacency_matrix.

        Parameters
        ----------
        filename : string
            Name of the file, for example 'JohnsHopkins.edgelist' or 'JohnsHopkins.gml'.

        dtype : string
            Type of file. Currently only 'edgelist' and 'gml' are supported.
            Default = 'gml'

        separator : string
            used if file_type = 'edgelist'
            Default = '\t'
        """
        graph = nx.read_gml(filename)
        self.adjacency_matrix = nx.adjacency_matrix(graph).astype(np.float64)
        self._num_edges = nx.number_of_edges(graph)
        self._num_vertices = nx.number_of_nodes(graph)
        self._directed = nx.is_directed(graph)
        self._graph_filename = filename

        print("Nodes: ", graph.node)
        print("Edges: ", graph.edges)
