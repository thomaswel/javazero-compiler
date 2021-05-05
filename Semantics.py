'''
Student: Thomas Welborn
Class: 4316 Compiler Design and Construction

Purpose: This program utilizes takes the quads from the Syntax Analysis
        and forms the equivalent assembly code which is then written on 
        the output file called 'assembly_temp.txt'. This assembly
        Code is then fed to the CodeGenerator which will append the
        assembly to other assembly code templates.
'''

def main():
    inFile = open('quads.txt', mode='r')
    quadsList = []
    # Read the quads from the file one line at a time.
    # Store each quad in the quadsList.
    for line in inFile:
        line = line.strip('\n')
        line = line.split(" ")
        quadsList.append(line)
    inFile.close()

    outFile = open('assembly_temp.txt', mode='w')
    tempStr = ''
    for i in range (len(quadsList)):
        if quadsList[i][0] == '=':
            tempStr = '\tmov ax,[' + str(quadsList[i][2]) + ']\n'
            tempStr += '\tmov [' + str(quadsList[i][1]) + '],ax\n'
            outFile.write(tempStr)
        
        elif quadsList[i][0] == '+':
            tempStr = '\tmov ax,[' + str(quadsList[i][1]) + ']\n'
            tempStr += '\tadd ax,[' + str(quadsList[i][2]) + ']\n'
            tempStr += '\tmov [' + str(quadsList[i][3]) + '], ax\n'
            outFile.write(tempStr)

        elif quadsList[i][0] == '-':
            tempStr = '\tmov ax,[' + str(quadsList[i][1]) + ']\n'
            tempStr += '\tsub ax,[' + str(quadsList[i][2]) + ']\n'
            tempStr += '\tmov [' + str(quadsList[i][3]) + '], ax\n'
            outFile.write(tempStr)

        elif quadsList[i][0] == '/':
            tempStr = '\tmov dx,0\n'
            tempStr += '\tmov ax, [' + str(quadsList[i][1]) + ']\n'
            tempStr += '\tmov bx, [' + str(quadsList[i][2]) + ']\n'
            tempStr += '\tdiv bx\n'
            tempStr += '\tmov [' + str(quadsList[i][3]) + '],ax\n'
            outFile.write(tempStr)

        elif quadsList[i][0] == '*':
            tempStr = '\tmov ax,[' + str(quadsList[i][1]) + ']\n'
            tempStr += '\tmul word[' + str(quadsList[i][2]) + ']\n'
            tempStr += '\tmov [' + str(quadsList[i][3]) + '], ax\n'
            outFile.write(tempStr)
        
        elif quadsList[i][0] == 'IF':
            pass

        elif quadsList[i][0] == 'WHILE':
            tempStr = str(quadsList[i][1]) + ':'
            outFile.write(tempStr)

        elif ((quadsList[i][0] == '<') or (quadsList[i][0] == '<=') or (quadsList[i][0] == '>') or (quadsList[i][0] == '>=') or (quadsList[i][0] == '==') or (quadsList[i][0] == '!=')):
            tempStr = '\tmov ax,[' + str(quadsList[i][1]) + ']\n'
            tempStr += '\tcmp ax, [' + str(quadsList[i][2]) + ']\n'
            outFile.write(tempStr)

        elif (quadsList[i][0] == 'THEN'):
            tempStr = '\tJ' + str(quadsList[i][2])
            tempStr += ' ' + str(quadsList[i][1]) + '\n'
            outFile.write(tempStr)

        elif (quadsList[i][0] == 'ELSE'):
            tempStr = '\tJMP ' + str(quadsList[i][1]) + '\n'
            outFile.write(tempStr)

        elif (quadsList[i][0] == 'DO'):
            tempStr = '\tJ' + str(quadsList[i][2])
            tempStr += ' ' + str(quadsList[i][1]) + '\n'
            outFile.write(tempStr)

        # For the While Loops
        elif (quadsList[i][0][0] == 'L') and quadsList[i][1][0] == 'W':
            tempStr = '\tjmp ' + str(quadsList[i][1]) + '\n'
            tempStr += str(quadsList[i][0]) + ': nop\n'
            outFile.write(tempStr)
        
        # For the If Loops
        elif (quadsList[i][0][0] == 'L'):
            tempStr = str(quadsList[i][0]) + ':\tnop\n'
            outFile.write(tempStr)

        elif (quadsList[i][0] == 'Read'):
            tempStr = '\tcall PrintString\n'
            tempStr += '\tcall GetAnInteger\n'
            tempStr += '\tmov ax,[ReadInt]\n'
            tempStr += '\tmov [' + str(quadsList[i][1]) + '],ax\n'
            outFile.write(tempStr)

        elif (quadsList[i][0] == 'Print'):
            tempStr = '\tmov ax,[' + str(quadsList[i][1]) + ']\n'
            tempStr += '\tcall ConvertIntegerToString\n'
            tempStr += '\tmov eax, 4\n'
            tempStr += '\tmov ebx, 1\n'
            tempStr += '\tmov ecx, Result\n'
            tempStr += '\tmov edx, ResultEnd\n'
            tempStr += '\tint 80h\n'
            outFile.write(tempStr)

    outFile.close()
    

if __name__ == '__main__':
    main()
