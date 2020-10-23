from .syntacticError import SyntacticError


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
