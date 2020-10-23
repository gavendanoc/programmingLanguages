# -*- coding: utf-8 -*-
"""

Syntactic Analyzer

Members:
* Gabriel Andres Avendaño Casadiego  gavendanoc@unal.edu.co
* Santiago Duque Bernal              saduquebe@unal.edu.co
* Juan Diego Medina Naranjo          jmedinan@unal.edu.co
"""

if __name__ == "__main__":
    from lexical import Lexical, LexicalError
    from syntax.syntacticAnalizer import SyntacticAnalizer
    from syntax.syntacticError import SyntacticError
    from syntax.syntacticNoEndError import SyntacticNoEndError
    from syntax.rule import Rule
else:
    from .lexical import Lexical, LexicalError  # used when testing
    from .syntax.syntacticAnalizer import SyntacticAnalizer
    from .syntax.syntacticError import SyntacticError
    from .syntax.syntacticNoEndError import SyntacticNoEndError
    from .syntax.rule import Rule


def match(expectedSymbol, lexical):
    token = lexical.nextToken()
    # TODO : Cambiar, los tokens en realidad son objectos (Class token)
    if token.token != expectedSymbol:
        raise SyntacticError(token.row, token.col,
                             token.lexema, [expectedSymbol])


def asd(nonterminal, processedGrammar, lexical, noEndError):
    firstSymbol = lexical.peekToken()
    # print(f"Enter {nonterminal} reading symbol {firstSymbol}")
    if firstSymbol == None:
        raise noEndError  # no hay mas simbolos para leer

    rules = processedGrammar[nonterminal].rules
    # print("regla: ",nonterminal,rules,"\n")
    selectedRule = list(
        filter(lambda rule: firstSymbol.token in rule.pred, rules))
    if len(selectedRule) > 1:
        # Si el largo es mas que 1, hay muchos conjuntos de prediccion
        print("----> grammar error")
    if len(selectedRule) == 0:  # si el largo es 0, el simbolo no esta en prediccion
        predictions = {symbol for rule in rules for symbol in rule.pred}
        # print(f"  Error in {nonterminal}")
        raise SyntacticError(firstSymbol.row, firstSymbol.col,
                             firstSymbol.lexema, predictions)

    # print(f"  selected rule {selectedRule}")
    ruleSymbols = selectedRule[0].ruleSymbols
    if ruleSymbols == ['e']:
        ruleSymbols = []
    for symbol in ruleSymbols:
        if symbol not in processedGrammar.keys():
            # print(f"      {nonterminal} matching {symbol}")
            match(symbol, lexical)
        else:
            asd(symbol, processedGrammar, lexical, noEndError)
    return 'El analisis sintactico ha finalizado correctamente.'


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


grammarFile = "./grammarFile.txt" if __name__ == "__main__" else "./src/grammarFile.txt"
grammar = readGrammar(grammarFile)


if __name__ == "__main__":
    import sys
    data = sys.stdin.readlines()  # Ctrl+d para detener lectura
    lexical = Lexical(data)

    syntacticAnalizer = SyntacticAnalizer(grammar)
    syntacticAnalizer.generatePredictionSets()

    noEndError = SyntacticNoEndError(data)

    # syntacticAnalizer.showProperties() # Muestra Primeros,Siguientes, de todo

    try:
        print(asd('prog', syntacticAnalizer.noTerminals, lexical, noEndError))
    except (SyntacticError, SyntacticNoEndError, LexicalError) as se:
        print(se.message)
