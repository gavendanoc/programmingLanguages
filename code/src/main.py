# -*- coding: utf-8 -*-
"""

Syntactic Analyzer

Members:
* Gabriel Andres Avendaño Casadiego  gavendanoc@unal.edu.co
* Santiago Duque Bernal              saduquebe@unal.edu.co
* Juan Diego Medina Naranjo          jmedinan@unal.edu.co
"""

if __name__ == "__main__":
    from lexical import Lexical, LexicalError
    from syntax.syntacticAnalizer import SyntacticAnalizer
    from syntax.syntacticError import SyntacticError
    from syntax.syntacticNoEndError import SyntacticNoEndError
    from syntax.asd import asd
    from syntax.readGrammar import readGrammar
else:  # used when testing
    from .lexical import Lexical, LexicalError
    from .syntax.syntacticAnalizer import SyntacticAnalizer
    from .syntax.syntacticError import SyntacticError
    from .syntax.syntacticNoEndError import SyntacticNoEndError
    from .syntax.asd import asd
    from .syntax.readGrammar import readGrammar


grammarFile = "./grammarFile.txt" if __name__ == "__main__" else "./src/grammarFile.txt"
grammar = readGrammar(grammarFile)


if __name__ == "__main__":
    import sys
    data = sys.stdin.readlines()  # Ctrl+d para detener lectura
    lexical = Lexical(data)

    syntacticAnalizer = SyntacticAnalizer(grammar)
    syntacticAnalizer.generatePredictionSets()

    noEndError = SyntacticNoEndError(data)

    # syntacticAnalizer.showProperties() # Muestra Primeros,Siguientes, de todo

    try:
        print(asd('prog', syntacticAnalizer.noTerminals, lexical, noEndError))
    except (SyntacticError, SyntacticNoEndError, LexicalError) as se:
        print(se.message)
