import Lexical
import Syntax
import Semantics
import CodeGeneration

'''
Author: Thomas Welborn
Class: Compiler Design and Construction
Due: April 30, 2021

Assignment: Language Translator/Compiler

Purpose:
This is the driver program for the compiler. It will take a chosen input
file written in "Java 0" and perform Lexical Analysis by using a
deterministic table-driven finite state automaton. Then it will perform
Syntax Analysis using a table-driven push down automaton. Then it will generate
the assembly code from the symbol table and quads.

Source Code Text File >> Lexical.py (Output: tokenList.txt, symbolTable.txt) >>
Syntax.py (Output: quads.txt) >> Semantics.py (Output: assembly_temp.txt) >>
CodeGeneration.py (Output: assemblyFINAL.txt)
'''


def main():
    # Get the name of the source Java 0 code file.
    fileName = input("Enter the name of the file to compile: ")

    # Do Lexical Analysis 
    # Produces two files: tokenList.txt, symbolTable.txt
    Lexical.main(fileName)

    # Do Syntax Anlysis with PDA.
    # Produces one file: quads.txt
    Syntax.main(fileName)

    # Do Semantics, converts quads to some assembly.
    # Produces one file: assembly_temp.txt
    Semantics.main()

    # Generate Code, produces final assembly code file.
    # Produces one file: assemblyFINAL.txt
    CodeGeneration.main()

if __name__ == '__main__':
    main()
