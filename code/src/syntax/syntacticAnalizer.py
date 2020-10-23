from .noTerminal import NoTerminal
from .rule import Rule


class SyntacticAnalizer:
    def __init__(self, grammar):
        self.grammar = grammar.copy()
        self.noTerminals = {}
        self.__makeNoTerminals()

    def __makeNoTerminals(self):
        for key in self.grammar:
            nt = NoTerminal(key, firsts=[], next=[], rules=self.grammar[key])
            self.noTerminals[key] = nt

    def makeFirsts(self):
        for noTerminalSymbol, rules in self.grammar.items():
            if self.noTerminals[noTerminalSymbol].firsts == []:
                self.__calculateFirsts(noTerminalSymbol, rules)
        # print(self.noTerminals)

    def __calculateFirsts(self, noTerminalSymbol, rules):
        for rule in rules:  # analiza regla por regla
            if rule.ruleSymbols[0] == "e":
                self.noTerminals[noTerminalSymbol].addFirst("e")
            else:
                for symbol in rule.ruleSymbols:
                    if symbol not in self.grammar:
                        self.noTerminals[noTerminalSymbol].addFirst(symbol)
                        break
                    elif symbol in self.grammar:
                        if self.noTerminals[symbol].firsts == []:
                            symbolRules = self.grammar.get(symbol)
                            self.__calculateFirsts(symbol, symbolRules)
                        symbolFirsts = self.noTerminals[symbol].firsts
                        addToTerminal = set(symbolFirsts).difference("e")
                        self.noTerminals[noTerminalSymbol].addFirst(
                            list(addToTerminal))
                        if "e" in symbolFirsts:
                            length = len(rule.ruleSymbols)
                            if length == 1:
                                self.noTerminals[noTerminalSymbol].addFirst(
                                    "e")
                            elif length > 1:
                                continue
                        else:
                            break

    def makeNext(self):
        completed = False
        changes = {k: 0 for k in self.noTerminals}
        while not completed:
            completed = True  # paso 3 verificar si hubo cambios
            for noTerminalSymbol, rules in self.grammar.items():
                if noTerminalSymbol == 'prog':  # paso 1
                    self.noTerminals[noTerminalSymbol].addNext("$")
                for rule in rules:
                    symbols = rule.ruleSymbols
                    for i, symbol in enumerate(symbols):
                        if symbol in self.grammar:  # verifica que sea no terminal
                            if i == len(symbols)-1:  # ultimo elemento de la regla
                                nextNoTerminalSymbol = self.noTerminals[noTerminalSymbol].next
                                self.noTerminals[symbol].addNext(
                                    nextNoTerminalSymbol)
                                break
                            nextSymbol = symbols[i+1]
                            if nextSymbol in self.grammar:  # siguiente es no terminal
                                nextSymbolFirsts = self.__getRuleFirsts(
                                    Rule(symbols[i+1:], []))
                                nextFirsts = list(
                                    set(nextSymbolFirsts).difference({"e"}))
                                self.noTerminals[symbol].addNext(nextFirsts)
                                if "e" in nextSymbolFirsts:
                                    nextNoTerminalSymbol = self.noTerminals[noTerminalSymbol].next
                                    self.noTerminals[symbol].addNext(
                                        nextNoTerminalSymbol)
                            else:  # siguiente es no terminal
                                self.noTerminals[symbol].addNext(nextSymbol)
                if changes[noTerminalSymbol] < len(self.noTerminals[noTerminalSymbol].next):
                    changes[noTerminalSymbol] = len(
                        self.noTerminals[noTerminalSymbol].next)
                    completed = False

    def __getRuleFirsts(self, rule):
        firsts = set()
        for symbol in rule.ruleSymbols:
            if symbol not in self.grammar:
                firsts.add(symbol)
                if symbol == "e":
                    return firsts
                return firsts.difference({"e"})
            else:
                noTerminalFirsts = self.noTerminals[symbol].firsts
                for nt in noTerminalFirsts:
                    firsts.add(nt)
                if "e" not in noTerminalFirsts:
                    return firsts.difference({"e"})
        return firsts  # cambiado por GAbriel

    def makePredictionSets(self):
        for noTerminalSymbol, noTerminal in self.noTerminals.items():
            rules = noTerminal.rules
            for rule in rules:
                ruleFirsts = self.__getRuleFirsts(rule)
                if "e" in ruleFirsts:
                    nextNoTerminal = self.noTerminals[noTerminalSymbol].next
                    predSet = ruleFirsts.difference(
                        {"e"}).union(set(nextNoTerminal))
                    rule.pred = tuple(sorted(predSet))
                else:
                    rule.pred = tuple(sorted(tuple(ruleFirsts)))

    def generatePredictionSets(self):
        self.makeFirsts()
        self.makeNext()
        self.makePredictionSets()

    def showProperties(self):
        for nt in self.noTerminals:
            print(nt, syntacticAnalizer.noTerminals[nt])
