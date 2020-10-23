import unittest
from src.main import SyntacticAnalizer, grammar
from collections import Counter


def checkLL1 (grammar):
  error = False
  errorMessages = []
  for nonterminal in grammar:
    rules = grammar[nonterminal].rules
    predictions = [symbol for rule in rules for symbol in rule.pred]
    mostCommonSymbol = Counter(predictions).most_common(1)[0]
    if mostCommonSymbol[1] != 1:
      errorMessages.append(f"'{nonterminal}' is not LL1 {mostCommonSymbol}")
      for rule in rules:
        if mostCommonSymbol[0] in rule.pred:
          errorMessages.append(f"  In {nonterminal} -> {' '.join(rule.ruleSymbols)}")
      error = True
  if error:
    return '\n'.join(errorMessages)
  else:
    return 'All ok!'


class TestUncode(unittest.TestCase):
  def test_ll1(self):
    syntacticAnalizer = SyntacticAnalizer(grammar)
    syntacticAnalizer.generatePredictionSets()
    result = checkLL1(syntacticAnalizer.noTerminals)
    
    self.assertEqual(result, 'All ok!')


if __name__ == "__main__":
  unittest.main()