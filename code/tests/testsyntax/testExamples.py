import unittest
import tests.testsyntax as test

class TestExamples(unittest.TestCase):
  def test_ex1(self):
    case = {
      "code": """## función min(x, y)
function @min:num (x:num, y:num)
  {
  when ((x < y) == true) do return x;
  return y;
  }

## función max(x, y)
function @max:num (x:num, y:num)
  {
  if ((x < y) == false) do
    {
    return x;
    }
  else
    {
    return y;
    }
  }

print @min(1,2);
print @max(1,2);
end""",
      "result": """"""
    }
    self.assertEqual(test.getOutput(case["code"]), case["result"])

  def test_ex2(self):
    case = {
      "code": """end""",
      "result": """"""
    }
    self.assertEqual(test.getOutput(case["code"]), case["result"])
  
  def test_ex3(self):
    case = {
      "code": """## función min(x, y)
function @min:num (x:num, y:num)
var menor:num, flag:bool;     # Las variables locales van antes del bloque
  {
  when ((x < y) == true) do return x;
  return y;
  }

## función max(x, y) El bloque debe tener, como mínimo, una sentencia
function @max:num (x:num, y:num)
  {
    print x+y;
  }

## función asignar(x, y) puede haber funciones de una única instrucción
function @asignar:num (x:num, y:num)
  x := y;

end
""",
      "result": """"""
    }
    self.assertEqual(test.getOutput(case["code"]), case["result"])

  def test_ex4(self):
    case = {
      "code": """## función retornay(x, y)
function @retornay: (x:num, y:num)
  {
  return y;
  }
end
""",
      "result": """<2:21> Error sintactico: se encontro: ‘(’; se esperaba: 'bool', 'num'."""
    }
    self.assertEqual(test.getOutput(case["code"]), case["result"])

  def test_ex5(self):
    case = {
      "code": """variable := 1;
variable;
end
""",
      "result": """<2:9> Error sintactico: se encontro: ‘;’; se esperaba: '%=', '*=', '++', '+=', '--', '-=', '/=', ':='."""
    }
    self.assertEqual(test.getOutput(case["code"]), case["result"])

  def test_ex6(self):
    case = {
      "code": """variable := ;""",
      "result": """<1:13> Error sintactico: se encontro: ‘;’; se esperaba: '(', '++', '--', 'false', 'identificador de funcion', 'identificador', 'not', 'numero', 'true'."""
    }
    self.assertEqual(test.getOutput(case["code"]), case["result"])

if __name__ == "__main__":
  unittest.main()