import unittest
import tests

class TestCharacters(unittest.TestCase):
  def test_sum(self):
    case = {
      "code": """+++\n""",
      "result": """<tk_incremento,1,1>
<tk_mas,1,3>"""
    }
    self.assertEqual(tests.getLexicalOutput(case["code"]), case["result"])

  def test_sum_tuple(self):
    case = {
      "code": """+++\n""",
      "result": """<tk_incremento,1,1>
<tk_mas,1,3>"""
    }
    self.assertEqual(tests.getLexicalOutput(case["code"]), case["result"])

if __name__ == "__main__":
  unittest.main()