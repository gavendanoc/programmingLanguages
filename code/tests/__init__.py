from src.lexical import Lexical, LexicalError

def getLexicalOutput(code):
  data = [f"{line}\n" for line in code.split("\n")]
  out = []
  lexical = Lexical(data)

  try:
    while(lexical.peekToken()):
      out.append(str(lexical.nextToken()))
  except LexicalError as le:
    out.append(le.message)
  return '\n'.join(out)
