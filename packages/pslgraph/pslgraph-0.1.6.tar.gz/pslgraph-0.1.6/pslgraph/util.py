import os
import re
import subprocess

from .constants import *

# Run the PSL model using the CLI and return the output (stdout).
def runPSL(model = 'unified', postgresDBName = DEFAULT_POSTRGES_DB_NAME):
    rulesPath = os.path.join(PSL_CLI_DIR, "%s.psl" % (model))
    dataPath = os.path.join(PSL_CLI_DIR, "%s.data" % (model))

    dbOption = ''
    if (postgresDBName and postgresDatabaseAvailable(postgresDBName)):
        dbOption = "--postgres '%s'" % (postgresDBName)

    pslCommand = "java -jar '%s' --infer --model '%s' --data '%s' %s" % (PSL_CLI_JAR, rulesPath, dataPath, dbOption)
    pslOutput = str(subprocess.check_output(pslCommand, shell = True), 'utf-8')

    return pslOutput

# See if we can get a response for the named database.
def postgresDatabaseAvailable(postgresDBName):
    command = "psql '%s' -c ''" % (postgresDBName)

    try:
        subprocess.check_call(command, stdout = subprocess.DEVNULL, stderr = subprocess.DEVNULL, shell = True)
    except subprocess.CalledProcessError:
        return False

    return True

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

def writeTSV(path, rows):
    with open(path, 'w') as file:
        # TODO(eriq): Batch
        for row in rows:
            file.write("\t".join(row) + "\n")
