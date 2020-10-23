import unittest
import tests.testsyntax as test

class TestUncode(unittest.TestCase):
  def test_1(self):
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
      "result": """El analisis sintactico ha finalizado correctamente."""
    }
    self.assertEqual(test.getOutput(case["code"]), case["result"])
  
  def test_2(self):
    case = {
      "code": """var flag:bool;

flag:=true;
flag := not (flag and (not(false) or true)) + ;
end""",
      "result": """<4:45> Error sintactico: se encontro: '+'; se esperaba: ';'."""
    }
    self.assertEqual(test.getOutput(case["code"]), case["result"])

  def test_3(self):
    case = {
      "code": """loop{
    repeat 10:
    {    print(100);

}
""",
      "result": """<7:1> Error sintactico: se encontro final de archivo; se esperaba 'end'."""
    }
    self.assertEqual(test.getOutput(case["code"]), case["result"])

  def test_4(self):
    case = {
      "code": """end""",
      "result": """El analisis sintactico ha finalizado correctamente."""
    }
    self.assertEqual(test.getOutput(case["code"]), case["result"])
  
  def test_5(self):
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
      "result": """El analisis sintactico ha finalizado correctamente."""
    }
    self.assertEqual(test.getOutput(case["code"]), case["result"])

  def test_6(self):
    case = {
      "code": """## función retornay(x, y)
function @retornay: (x:num, y:num)
  {
  return y;
  }
end""",
      "result": """<2:21> Error sintactico: se encontro: '('; se esperaba: 'bool', 'num'."""
    }
    self.assertEqual(test.getOutput(case["code"]), case["result"])

  def test_7(self):
    case = {
      "code": """variable := ;""",
      "result": """<1:13> Error sintactico: se encontro: ';'; se esperaba: '(', '++', '--', 'false', 'identificador de funcion', 'identificador', 'not', 'numero', 'true'."""
    }
    self.assertEqual(test.getOutput(case["code"]), case["result"])

  def test_8(self):
    case = {
      "code": """
var z:num;
z := 0;
while (z < 10)
  {
  z := z + 1;
  print z;
  }
end
# salida: 1 2 3 4 5 6 7 8 9 10""",
      "result": """<5:3> Error sintactico: se encontro: '{'; se esperaba: 'do'."""
    }
    self.assertEqual(test.getOutput(case["code"]), case["result"])

  def test_9(self):
    case = {
      "code": """var z:num;
z := 0;
while (z < 10) do
  {
  z := z + 1;
  print z;
  }
end
# salida: 1 2 3 4 5 6 7 8 9 10""",
      "result": """El analisis sintactico ha finalizado correctamente."""
    }
    self.assertEqual(test.getOutput(case["code"]), case["result"])
  
  def test_10(self):
    case = {
      "code": """loop{
    repeat 10:
    {    print(100);
    }
}
end""",
      "result": """El analisis sintactico ha finalizado correctamente."""
    }
    self.assertEqual(test.getOutput(case["code"]), case["result"])

  def test_11(self):
    case = {
      "code": """loop{
    repeat 10:
    {    print(100);

}
end""",
      "result": """<6:1> Error sintactico: se encontro: 'end'; se esperaba: '++', '--', 'break', 'do', 'for', 'identificador', 'if', 'input', 'loop', 'next', 'print', 'repeat', 'return', 'unless', 'until', 'when', 'while', '}'."""
    }
    self.assertEqual(test.getOutput(case["code"]), case["result"])

if __name__ == "__main__":
  unittest.main()