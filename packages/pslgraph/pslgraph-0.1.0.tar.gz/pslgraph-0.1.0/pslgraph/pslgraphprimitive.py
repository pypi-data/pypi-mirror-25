from typing import *
from gevent import os
from d3m_types.base import Graph
from primitive_interfaces.graph import GraphTransformerPrimitiveBase
import subprocess

Inputs = TypeVar('Inputs', bound=Sequence[Graph])
Outputs = TypeVar('Outputs', bound=Sequence[Graph])

class PSLGraphPrimitive(GraphTransformerPrimitiveBase[Inputs, Outputs]):

    """
    This is the main PSL Graph Primitive. The first step is to examine the input data to verify it is valid. Next
    it will be written to disk for use by the PSL program which will be invoked using the CLI interface. Once complete
    the results will be read back in from disk and returned to the caller in the expected format.
    """

    def produce(self, *, inputs: Inputs, timeout: float = None, iterations: int = None) -> Outputs:
        print("PSLGraphPrimitive::Produce Called...")

        # First, Inspect the Graph data to make sure it is usable by this Primitive
        # TODO: Are there other validation steps that we should take?
        if (inputs._directed) :
            print("Error, the primitive is unable to process directed graphs")
            return

        # Second, get the filename that the graph was loaded from
        filename = inputs._graph_filename

        # Third, pass the graph data to PSL with the CLI
        # FNULL = open(os.devnull, 'w')  # use this if you want to suppress output to stdout from the subprocess
        # args = ["java", "-jar", "/Users/daraghhartnett/Projects/D3M/code/psl-ta1/docker/psl-cli-CANARY.jar", "-infer",
        #         "-model", "graph-link-completion.psl", "-data ", "filename"]
        # subprocess.call(args, stdin=subprocess.DEVNULL, stdout=subprocess.STDOUT, stderr=FNULL, shell=False)

        # If this does not block figure out why the subprocess call above does not work
        # os.system("java -jar docker/psl-cli-CANARY.jar -infer -model graph-link-completion.psl -data " + filename)

        # Third, read the results back in and pass back to the caller.

