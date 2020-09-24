from lexical import practica1

def getLexicalOutput(code):
  data = [f"{line}\n" for line in code.split("\n")]
  out = []
  try:
    for token in practica1.getTokens(data):
      out.append(str(token))
  except practica1.LexicalError as le:
    out.append(le.message)
  return '\n'.join(out)