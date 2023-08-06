from typing import *

from primitive_interfaces.unsupervised_learning import UnsupervisedLearnerPrimitiveBase

from .graphdata import GraphData
from .util import runPSL
from .util import getTopLinksFromPSL

# TODO(eriq): The input type needs some thinking.
#   For set_training_data() we only need the graph, and produce() we only need the node ids.

Params = TypeVar('Params')
Inputs = TypeVar('Inputs', bound = Tuple[GraphData, Sequence[int]])
Outputs = TypeVar('Outputs', bound = Sequence[int])

class PSLLinkPrediction(UnsupervisedLearnerPrimitiveBase[Inputs, Outputs, Params]):

    def __init__(self, include_all_edges = False) -> None:
        self._graphData = None
        self._include_all_edges = include_all_edges
        self._bestLinks = None

    def set_training_data(self, *, inputs: Inputs) -> None:
        assert(inputs is not None)
        assert(len(inputs) > 0)
        assert(inputs[0] is not None)

        self._graphData = inputs[0]

    def fit(self, *, timeout: float = None, iterations: int = None) -> None:
        if (self._graphData is None):
            raise "Call set_training_data() before fit()."

        # Convert the GML into the PSL format.
        self._graphData.write_psl_data(include_all_edges = self._include_all_edges)

        # Run the "unified" model in PSL.
        pslOutput = runPSL('unified')

        # Parse the output and save the best links.
        # TODO(eriq): We should probably save all the links for when people want all the information.
        self._bestLinks = getTopLinksFromPSL(pslOutput)

    def produce(self, *, inputs: Inputs, timeout: float = None, iterations: int = None) -> Outputs:
        if (self._bestLinks == None):
            raise "Call fit() before produce()."

        assert(inputs is not None)
        assert(len(inputs) == 2)
        assert(inputs[1] is not None)

        results = []
        for nodeId in inputs[1]:
            results.append(self._bestLinks[nodeId][0])
            
        return results

    def get_params(self) -> Params:
        pass

    def set_params(self, *, params: Params) -> None:
        pass
