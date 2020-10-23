class SyntacticError(Exception):
  symbolToErrorMessage = {
      'tk_diferente': '!=',
      'tk_mod': '%',
      'tk_mod_asig': '%=',
      'tk_par_izq': '(',
      'tk_par_der': ')',
      'tk_mul': '*',
      'tk_mul_asig': '*=',
      'tk_mas': '+',
      'tk_incremento': '++',
      'tk_sum_asig': '+=',
      'tk_coma': ',',
      'tk_menos': '-',
      'tk_decremento': '--',
      'tk_res_asig': '-=',
      'tk_div': '/',
      'tk_div_asig': '/=',
      'tk_dospuntos': ':',
      'tk_asignacion': ':=',
      'tk_puntoycoma': ';',
      'tk_menor': '<',
      'tk_menor_igual': '<=',
      'tk_igualdad': '==',
      'tk_mayor': '>',
      'tk_mayor_igual': '>=',
      'bool': 'bool',
      'end': 'end',
      'false': 'false',
      'id': 'identificador',
      'fid': 'identificador de funcion',
      'tk_num': 'numero',
      'true': 'true',
      'tk_llave_izq': '{',
      'tk_llave_der': '}'
  }

  def __init__(self, row, col, lexem=None, predictions=None):
    expected = sorted(map(SyntacticError.convertSymbol, predictions))
    # Quitar corchetes al inicio y final de lista
    expected = ', '.join(expected)
    self.message = "<{}:{}> Error sintactico: se encontro: '{}'; se esperaba: {}.".format(
        row, col, lexem, expected)
    super().__init__(self.message)

  @staticmethod
  def convertSymbol(symbol):
    if symbol in SyntacticError.symbolToErrorMessage.keys():
      return f"'{SyntacticError.symbolToErrorMessage[symbol]}'"
    else:
      return f"'{symbol}'"

  def __str__(self):
    return self.message
