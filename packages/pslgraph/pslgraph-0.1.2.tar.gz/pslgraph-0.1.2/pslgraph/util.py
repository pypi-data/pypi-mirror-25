import os
import re
import subprocess

PSL_CLI_DIR = os.path.join(os.path.dirname(__file__), 'psl-cli')
PSL_CLI_JAR = os.path.join(PSL_CLI_DIR, 'psl-cli-CANARY.jar')

# Run the PSL model using the CLI and return the output (stdout).
def runPSL(model = 'unified'):
    rulesPath = os.path.join(PSL_CLI_DIR, "%s.psl" % (model))
    dataPath = os.path.join(PSL_CLI_DIR, "%s.data" % (model))

    pslCommand = "java -jar '%s' -infer -model '%s' -data '%s'" % (PSL_CLI_JAR, rulesPath, dataPath)
    pslOutput = str(subprocess.check_output(pslCommand, shell = True), 'utf-8')

    return pslOutput

# Returns the strongest links found from the PSL output.
# Returns: {G1Id: (G2Id, Score), ...}
def getTopLinksFromPSL(pslOutput):
    # The strongest link for each source (G1) node.
    # {G1Id: (G2Id, Score), ...}
    strongestLinks = {}

    for line in pslOutput.splitlines():
        line = line.strip()

        match = re.match(r"^LINK\('(\d+)::(\w+)', '(\d+)::(\w+)'\) = (\d+\.\d+)", line)
        if (match != None):
            g1Id = match.group(2)
            g2Id = match.group(4)
            score = float(match.group(5))

            if (not (g1Id in strongestLinks) or score > strongestLinks[g1Id][1]):
                strongestLinks[g1Id] = (g2Id, score)

    return strongestLinks
