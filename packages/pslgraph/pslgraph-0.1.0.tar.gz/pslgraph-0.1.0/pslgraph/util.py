import re

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
