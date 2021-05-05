'''
Student: Thomas Welborn
Class: 4316 Compiler Design and Construction

Purpose: This program takes the assembly code generated from the Semantics
        and appends it to pre-made assembly code templates provided by 
        the instructor that take care of user I/O. The final file produced
        by this is a fully functioning 32-bit assembly code file which can
        be translated to an executable file with NASM and GCC in Linux.
'''

def main():

    # Open file to get symbol table
    inFile = open('symbolTable.txt', mode='r')
    symbolTable = []
    # Read the symbol rows from the file one line at a time.
    # Store each 5 length list in the symbolList.
    # [Symbol, Classification, Value, Address, Segment]
    for line in inFile:
        line = line.strip('\n')
        line = line.split(" ")
        symbolTable.append(line)
    inFile.close()
    print(symbolTable)


    # Open file for writing
    outFile = open('assemblyFINAL.txt', mode='w')

    # Append template 1.
    template1 = open('assemblyTEMPLATE_1.txt', mode='r')
    for line in template1:
        outFile.write(line)
    template1.close()

    # Append constants and literals.
    #   The format is M DW 7
    #               lit12 DW 12
    for i in range(len(symbolTable)):
        if symbolTable[i][1] == '$numLit':
            myStr = '\tlit' + str(symbolTable[i][0]) + '\tDW\t' + str(symbolTable[i][0]) + '\n'
            outFile.write(myStr)
        elif symbolTable[i][1] == '<constvar>':
            myStr = '\t' + str(symbolTable[i][0]) + '\tDW\t' + str(symbolTable[i][2]) + '\n'
            outFile.write(myStr)
        else:
            pass
            
    
    # Append template 2.
    template2 = open('assemblyTEMPLATE_2.txt', mode='r')
    for line in template2:
        outFile.write(line)
    template2.close()


    # Append variables that are not initialized
    # DONT INCLUDE TEMPS
    for i in range (len(symbolTable)):
        if symbolTable[i][1] == '<var>':
            myStr = '\t' + str(symbolTable[i][0]) + '\tRESW\t1\n'
            outFile.write(myStr)


    # Append template 3
    template3 = open('assemblyTEMPLATE_3.txt', mode='r')
    for line in template3:
        outFile.write(line)
    template3.close()


    # Append the code segment from semantics.py
    codeSeg = open('assembly_temp.txt', mode='r')
    for line in codeSeg:
        outFile.write(line)
    codeSeg.close()


    # Append template 4.
    template4 = open('assemblyTEMPLATE_4.txt', mode='r')
    for line in template4:
        outFile.write(line)
    template4.close()

    # Close File.
    outFile.close()



if __name__ == '__main__':
    main()
