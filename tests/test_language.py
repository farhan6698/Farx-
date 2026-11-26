import unittest
from farx.lexer import Lexer
from farx.parser import Parser
from farx.runtime import Interpreter

def execute(src):
    out=[]
    tree=Parser(Lexer(src).tokens()).parse()
    Interpreter(output=out.append).run(tree)
    return out

class LanguageTests(unittest.TestCase):
    def test_arithmetic(self):
        self.assertEqual(execute('MODE CODE\nPRINT 6 * 7\nEND MODE'),[42])
    def test_variables(self):
        self.assertEqual(execute('LET x = 4\nSET x = x + 3\nPRINT x'),[7])
    def test_if(self):
        self.assertEqual(execute('IF 2 < 3 THEN\nPRINT "yes"\nELSE\nPRINT "no"\nEND IF'),["yes"])
    def test_while(self):
        self.assertEqual(execute('LET x=0\nWHILE x < 3 DO\nSET x=x+1\nEND WHILE\nPRINT x'),[3])
    def test_function(self):
        self.assertEqual(execute('FUNCTION twice(x)\nRETURN x*2\nEND FUNCTION\nPRINT twice(8)'),[16])
    def test_list_builtin(self):
        self.assertEqual(execute('PRINT LEN([1,2,3])'),[3])

if __name__ == "__main__": unittest.main()
