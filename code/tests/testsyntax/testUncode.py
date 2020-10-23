import unittest
import tests.testsyntax as test

class TestUncode(unittest.TestCase):
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

if __name__ == "__main__":
  unittest.main()