from src.lexical import Lexical, LexicalError
from src.main import SyntacticAnalizer, grammar, asd, SyntacticError

def getOutput(code):
  data = [f"{line}\n" for line in code.split("\n")]
  lexical = Lexical(data)

  syntacticAnalizer = SyntacticAnalizer(grammar)
  syntacticAnalizer.generatePredictionSets()

  try:
    return asd('prog', syntacticAnalizer.noTerminals, lexical)
  except SyntacticError as se:
    return se.message
  except LexicalError as le:
    return le.message
  return ""