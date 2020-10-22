if __name__ == "__main__": 
  from lexical import Lexical, LexicalError
else:
  from .lexical import Lexical, LexicalError # used when testing

class Rule:
  def __init__(self, ruleSymbols, pred):
    if isinstance(ruleSymbols, str):
      self.ruleSymbols = ruleSymbols.split()
    else:
      self.ruleSymbols = ruleSymbols
    self.pred = pred
  
  
  def __repr__(self):
    return f"<{' '.join(self.ruleSymbols)} : {self.pred}>"

class NoTerminal:
  def __init__(self, symbol,firsts=[],next=[],rules=[]):
    self.symbol = symbol
    self.firsts = firsts
    self.next = next
    self.rules = rules

  def addNext(self,n):
    if type(n) != list:
      n = [n]
    self.next+= n
    temp = set(self.next) # quitar elementos repetidos
    self.next = sorted(list(temp))
  
  def addFirst(self, first):
    if type(first) != list: 
      first = [first]
    self.firsts += first
    temp = set(self.firsts)
    self.firsts = sorted(list(temp))

  def __repr__(self):
    # return f"{self.symbol}: \n  Firsts: {self.firsts} \n  Next:   {self.next} \n  Rules:  {self.rules}"
    return f" \n  Firsts: {self.firsts} \n  Next:   {self.next} \n  Rules:  {self.rules}"

class SyntacticAnalizer:
  def __init__(self,grammar):
    self.grammar = grammar.copy()
    self.noTerminals = {}
    self.__makeNoTerminals()

  def __makeNoTerminals(self):
    for key in self.grammar:
      nt = NoTerminal(key,firsts=[],next=[],rules=self.grammar[key])    
      self.noTerminals[key] = nt

  def makeFirsts(self):
    for noTerminalSymbol,rules in self.grammar.items():
      if self.noTerminals[noTerminalSymbol].firsts == []:
        self.__calculateFirsts(noTerminalSymbol, rules)
    # print(self.noTerminals)

  def __calculateFirsts(self,noTerminalSymbol, rules):
    for rule in rules: #analiza regla por regla
      for i, symbol in enumerate(rule.ruleSymbols):
        if symbol == "e" and i == 0 : #paso 1
          self.noTerminals[noTerminalSymbol].addFirst("e")
        elif symbol not in self.grammar and i == 0: #paso 2-a
          self.noTerminals[noTerminalSymbol].addFirst(symbol)
        elif symbol in self.grammar and i == 0: #paso 2-b
          symbolRules = self.grammar.get(symbol)
          if self.noTerminals[symbol].firsts == []:
            self.__calculateFirsts(symbol, symbolRules)
          symbolFirsts = self.noTerminals[symbol].firsts
          addToTerminal = set(symbolFirsts).difference("e")
          self.noTerminals[noTerminalSymbol].addFirst(list(addToTerminal))
          if "e" in symbolFirsts: #paso 2-c
            length = len(rule.ruleSymbols)
            if length == 1:
              self.noTerminals[noTerminalSymbol].addFirst("e")
            elif length > 1:
              if rule.ruleSymbols[i+1] in self.grammar:
                remaining = self.noTerminals[rule.ruleSymbols[i+1]].firsts
                if remaining != []:
                  self.noTerminals[noTerminalSymbol].addFirst(remaining)
                else:
                  remRules = self.grammar.get(rule.ruleSymbols[i+1])
                  self.__calculateFirsts(rule.ruleSymbols[i+1],remRules)
                  remaining = self.noTerminals[rule.ruleSymbols[i+1]].firsts
                  self.noTerminals[noTerminalSymbol].addFirst(remaining)
              elif rule.ruleSymbols[i+1] not in self.grammar:
                self.noTerminals[noTerminalSymbol].addFirst(rule.ruleSymbols[i+1])

  def makeNext(self):
    first = True
    completed = False
    changes  = {k:0 for k in self.noTerminals} # almacema el tamaño de cada conjunto de siguientes para verificar si hubo cambios despues de la iteracion
    while not completed:
      completed = True # paso 3 verificar si hubo cambios
      for noTerminalSymbol,rules in self.grammar.items():
        if first: # paso 1
          self.noTerminals[noTerminalSymbol].addNext("$")
          first = False 
        for rule in rules:
          symbols = rule.ruleSymbols
          for i,symbol in enumerate(symbols):
            if symbol in self.grammar: # verifica que sea no terminal
              if i == len(symbols)-1: # ultimo elemento de la regla
                nextNoTerminalSymbol= self.noTerminals[noTerminalSymbol].next
                self.noTerminals[symbol].addNext(nextNoTerminalSymbol)
                break
              nextSymbol = symbols[i+1]
              if nextSymbol in self.grammar: # siguiente es no terminal
                nextSymbolFirsts = self.__getRuleFirsts(Rule(symbols[i+1:],[]))     
                # nextSymbolFirsts = self.noTerminals[nextSymbol].firsts # primeros del siguiente simbolo
                nextFirsts = list(set(nextSymbolFirsts).difference({"e"})) # quitar epsilon si lo hay
                self.noTerminals[symbol].addNext(nextFirsts)
                if "e" in nextSymbolFirsts:
                  nextNoTerminalSymbol = self.noTerminals[noTerminalSymbol].next
                  self.noTerminals[symbol].addNext(nextNoTerminalSymbol) # agregar siguientes del la regla del no terminal
              else: #siguiente es no terminal
                self.noTerminals[symbol].addNext(nextSymbol)
        if changes[noTerminalSymbol] < len(self.noTerminals[noTerminalSymbol].next):
          changes[noTerminalSymbol] = len(self.noTerminals[noTerminalSymbol].next)
          completed = False
  
  def __getRuleFirsts(self,rule):
    firsts = set()
    for symbol in rule.ruleSymbols:
      if symbol not in self.grammar:
        firsts.add(symbol)
        if symbol == "e": return firsts
        return firsts.difference({"e"})
      else:
        noTerminalFirsts = self.noTerminals[symbol].firsts
        for nt in noTerminalFirsts:
            firsts.add(nt)
        if "e" not in noTerminalFirsts:
          return firsts.difference({"e"})
    return firsts # cambiado por GAbriel

  def makePredictionSets(self):
    for noTerminalSymbol,noTerminal in self.noTerminals.items():
      rules = noTerminal.rules
      for rule in rules:
        ruleFirsts = self.__getRuleFirsts(rule)
        if "e" in ruleFirsts:
          nextNoTerminal = self.noTerminals[noTerminalSymbol].next
          predSet = ruleFirsts.difference({"e"}).union(set(nextNoTerminal))
          rule.pred = tuple(sorted(predSet))
        else:
          rule.pred = tuple(sorted(tuple(ruleFirsts)))
    

  def generatePredictionSets(self):
    self.makeFirsts()
    self.makeNext()
    self.makePredictionSets()

class SyntacticError(Exception):
  symbolToErrorMessage = {
    'tk_diferente' : '!=',
    'tk_mod' : '%',
    'tk_mod_asig' : '%=',
    'tk_par_izq' : '(',
    'tk_par_der' : ')',
    'tk_mul' : '*',
    'tk_mul_asig' : '*=',
    'tk_mas': '+',
    'tk_incremento' : '++',
    'tk_sum_asig' : '+=',
    'tk_coma' : ',',
    'tk_menos' : '-',
    'tk_decremento' : '--', 
    'tk_res_asig' : '-=',
    'tk_div' : '/',
    'tk_div_asig' : '/=',
    'tk_dospuntos' : ':' ,
    'tk_asignacion' : ':=',
    'tk_puntoycoma' : ';',
    'tk_menor' : '<',
    'tk_menor_igual' : '<=',
    'tk_igualdad' : '==',
    'tk_mayor' : '>',
    'tk_mayor_igual' : '>=' , 
    'bool' : 'bool' ,
    'end' : 'end' ,
    'false' : 'false' ,
    'id' : 'identificador',
    'fid' : 'identificador de funcion',
    'tk_num' : 'numero',
    'true' : 'true',
    'tk_llave_izq' : '{',
    'tk_llave_der' : '}'
  } 

  def __init__(self, lexem, predictions, row=1, col=1, message=None):
    if message != None:
      self.message = message
      super().__init__(self.message)
      return

    expected = sorted(map(SyntacticError.convertSymbol, predictions))
    for i,v in enumerate(expected):
      if i == len(expected)-1:
        break
      if v in expected[i+1]:
        expected[i] = expected[i+1]
        expected[i+1] = v
    expected = str(expected)[1:-1] # Quitar corchetes al inicio y final de lista
    self.message = "<{}:{}> Error sintactico: se encontro: '{}'; se esperaba: {}.".format(row, col, lexem, expected)
    super().__init__(self.message)

  def convertSymbol (symbol):
    if symbol in SyntacticError.symbolToErrorMessage.keys():
      return SyntacticError.symbolToErrorMessage[symbol]
    else:
      return symbol

  def __str__(self):
    return self.message

def match(expectedSymbol, lexical):
  token = lexical.nextToken()
  # TODO : Cambiar, los tokens en realidad son objectos (Class token)
  if token.token != expectedSymbol: 
    raise SyntacticError(token.lexema, [expectedSymbol], token.row, token.col)

def asd(nonterminal, processedGrammar, lexical):
  firstSymbol = lexical.peekToken()
  # print(f"Enter {nonterminal} reading symbol {firstSymbol}")
  if firstSymbol == None: 
    raise SyntacticError(None, None, message="Error sintactico: se encontro final de archivo; se esperaba ‘end’.") # no hay mas simbolos para leer
  
  rules = processedGrammar[nonterminal].rules
  selectedRule = list(filter(lambda rule : firstSymbol.token in rule.pred, rules))
  if len(selectedRule) > 1: print("----> grammar error") # Si el largo es mas que 1, hay muchos conjuntos de prediccion
  if len(selectedRule) == 0: # si el largo es 0, el simbolo no esta en prediccion
    predictions = {symbol for rule in rules for symbol in rule.pred}
    # print(f"  Error in {nonterminal}")
    raise SyntacticError(firstSymbol.lexema, predictions, firstSymbol.row, firstSymbol.col)

  # print(f"  selected rule {selectedRule}")
  ruleSymbols = selectedRule[0].ruleSymbols
  if ruleSymbols == ['e']: ruleSymbols = []
  for symbol in ruleSymbols: 
    if symbol not in processedGrammar.keys():
      # print(f"      {nonterminal} matching {symbol}")
      match(symbol, lexical)
    else: 
      asd(symbol, processedGrammar, lexical)

def createGrammarDict(grammarText):
  grammarDict = {}
  text = grammarText.split("\n")
  for row in text:
    row = row.split()
    if len(row) == 0 : continue
    nt = row[0]
    if nt not in grammarDict:
      grammarDict[nt] = []
    rowTks = row[2:]
    grammarDict[nt].append(Rule(rowTks,[]))
  return grammarDict

grammarFile = "./grammarFile.txt"
grammar = {}
with open(grammarFile,'r') as f:
  text = f.read()
  grammarRules = text.split("&")
  for g in grammarRules:
    grammar = {
        **grammar,
        **createGrammarDict(g)
    }

if __name__ == "__main__":
  import sys 
  data = sys.stdin.readlines() # Ctrl+d para detener lectura
  lexical = Lexical(data)

  syntacticAnalizer = SyntacticAnalizer(grammar)
  syntacticAnalizer.generatePredictionSets()

  try:
    asd('prog', syntacticAnalizer.noTerminals, lexical)
    print('El analisis sintactico ha finalizado correctamente.')
  except SyntacticError as se:
    print(se.message)
  except LexicalError as le:
    print(le.message)
  
