from lexical import main

def getLexicalOutput(code):
  data = [f"{line}\n" for line in code.split("\n")]
  out = []
  lexical = main.Lexical(data)

  try:
    while(lexical.peekToken()):
      out.append(str(lexical.nextToken()))
  except main.LexicalError as le:
    out.append(le.message)
  return '\n'.join(out)
