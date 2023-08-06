# A primitive to transform graphmatching-style problems into the types of graphs that the graph transformer can consume.
# This is a fairly trivial transformer.

import os
from typing import *

import networkx
from primitive_interfaces.transformer import TransformerPrimitiveBase

from .constants import *

# TODO(eriq): I am not sure how the other TA1/TA2 primitives pick up data like this.
#  For now, we will just take the path to the data dir.
Inputs = TypeVar('Inputs', bound = str)
# Graph1, Graph2, Targets
Outputs = TypeVar('Outputs', bound = Tuple[networkx.Graph, networkx.Graph, networkx.Graph])

class PSLGraphMatchingTransformer(TransformerPrimitiveBase[Inputs, Outputs]):

    def __init__(self):
        pass

    def produce(self, *, inputs: Inputs, timeout: float = None, iterations: int = None) -> Outputs:
        assert(inputs is not None)

        dataDir = inputs

        graph1 = self._readGraph(os.path.join(dataDir, 'raw_data', 'G1.gml'))
        graph2 = self._readGraph(os.path.join(dataDir, 'raw_data', 'G2.gml'))

        observedSources = self._readCSV(os.path.join(dataDir, 'trainData.csv'))
        observedTargets = self._readCSV(os.path.join(dataDir, 'trainTargets.csv'))

        return graph1, graph2, self._buildTargetGraph(observedSources, observedTargets)

    def _buildTargetGraph(self, observedSources, observedTargets):
        assert(len(observedSources) == len(observedTargets))

        graph = networkx.DiGraph()
        for i in range(len(observedSources)):
            graph.add_node(observedSources[i], label = observedSources[i])
            graph.add_node(observedTargets[i], label = observedTargets[i])
            graph.add_edge(observedSources[i], observedTargets[i], weight = 1.0)

        return graph

    def _readGraph(self, path):
        graph = networkx.read_gml(path, label = NODE_ID_LABEL)

        # NetworkX will not relabel the nodes even though we specified nodeID as the label.
        # If they actually did relabel, then this will do nothing.
        mapping = {}
        for nodeId in graph.nodes():
            mapping[nodeId] = graph.node[nodeId][NODE_ID_LABEL]
        networkx.relabel_nodes(graph, mapping, copy = False)

        return graph

    def _readCSV(self, path):
        nodeIds = []

        with open(path, 'r') as csvFile:
            # The file format is sometimes inconsistent, so pick up the header
            # so we can tell which column we want.
            header = next(csvFile)

            nodeIdColumnIndex = 2  # The normal index.
            d3mColumnIndex = 0  # The normal index.

            columnNames = header.strip().split(',')
            for i in range(len(columnNames)):
                if (columnNames[i].endswith('.' + NODE_ID_LABEL)):
                    nodeIdColumnIndex = i
                elif (columnNames[i] == D3MINDEX_COLUMN_NAME):
                    d3mColumnIndex = i

            for line in csvFile:
                parts = [part.strip() for part in line.split(',')]
                nodeIds.append(parts[nodeIdColumnIndex])

        return nodeIds
