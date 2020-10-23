from .rule import Rule


def createNoTerminalDict(grammarText):
    grammarDict = {}
    text = grammarText.split("\n")
    for row in text:
        row = row.split()
        if len(row) == 0:
            continue
        nt = row[0]
        if nt not in grammarDict:
            grammarDict[nt] = []
        rowTks = row[2:]
        grammarDict[nt].append(Rule(rowTks, []))
    return grammarDict


def readGrammar(grammarFile):
    grammar = {}
    with open(grammarFile, 'r') as f:
        text = f.read()
        subGrammars = text.split("&")
        for g in subGrammars:
            grammar = {
                **grammar,
                **createNoTerminalDict(g)
            }
    return grammar
