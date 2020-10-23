from src.lexical import Lexical, LexicalError
from src.main import SyntacticAnalizer, grammar, asd, SyntacticError, SyntacticNoEndError

def getOutput(code):
  data = [f"{line}\n" for line in code.split("\n")]
  lexical = Lexical(data)

  syntacticAnalizer = SyntacticAnalizer(grammar)
  syntacticAnalizer.generatePredictionSets()

  noEndError = SyntacticNoEndError(data)

  try:
    return asd('prog', syntacticAnalizer.noTerminals, lexical, noEndError)
  except (SyntacticError, SyntacticNoEndError, LexicalError) as error:
    return error.message