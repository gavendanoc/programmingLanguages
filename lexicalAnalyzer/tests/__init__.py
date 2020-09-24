from lexical import main

def getLexicalOutput(code):
  data = [f"{line}\n" for line in code.split("\n")]
  out = []
  try:
    for token in main.getTokens(data):
      out.append(str(token))
  except main.LexicalError as le:
    out.append(le.message)
  return '\n'.join(out)