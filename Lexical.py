'''
Student: Thomas Welborn
Class: COSC 4316 Compiler Design and Construction

Purpose: This program will take a program written in Java 0
    programming languge. It will use a table-driven finite state automaton
    in order to extract each token and its type from the program
    using the 'Scanner' class. Then it will export the tokens and their
    types into a text file called tokenList.txt. This is the Lexical analysis.

    Next it will do the first pass through the program using another
    table-driven FSA in order to create the initial symbol table. The
    symbol table will be exported from this program and used in the
    syntax analysis program.
'''


'''
The Scanner Class utilizes a table-drive finite state automaton
in order to extract each token and its type from a given
text file.
'''
class Scanner:
    # Dictionary used to map values to their corresponding
    # row/column numbers.
    dict_convert = {
        "a":0, "A":0,
        "b":0, "B":0,
        "c":0, "C":0,
        "d":0, "D":0,
        "e":0, "E":0,
        "f":0, "F":0,
        "g":0, "G":0,
        "h":0, "H":0,
        "i":0, "I":0,
        "j":0, "J":0,
        "k":0, "K":0,
        "l":0, "L":0,
        "m":0, "M":0,
        "n":0, "N":0,
        "o":0, "O":0,
        "p":0, "P":0,
        "q":0, "Q":0,
        "r":0, "R":0,
        "s":0, "S":0,
        "t":0, "T":0,
        "u":0, "U":0,
        "v":0, "V":0,
        "w":0, "W":0,
        "x":0, "X":0,
        "y":0, "Y":0,
        "z":0, "Z":0,

        "0":1, "1":1,
        "2":1, "3":1,
        "4":1, "5":1,
        "6":1, "7":1,
        "8":1, "9":1,

        "+":2,
        "-":3,
        "*":4,
        ",":5,
        ";":6,
        ")":7,
        "(":8,
        "{":9,
        "}":10,
        "/":11,
        "=":12,
        "<":13,
        ">":14,
        "!":15,

        " ":16, "\n":16, "\t":16, "\r":16
    }

    # The table used for the FSA
    table =[[13, 11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 15, 19, 22, 25, 28, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
            [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
            [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
            [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
            [6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6],
            [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7],
            [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
            [9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9],
            [10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10],
            [12, 11, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 1],
            [12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12],
            [13, 13, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 1],
            [14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14],
            [16, 16, 16, 16, 17, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 1],
            [16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16],
            [17, 17, 17, 17, 18, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17],
            [17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 0, 17, 17, 17, 17, 17, 17],
            [20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 21, 20, 20, 20, 20, 1],
            [20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20],
            [21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21],
            [23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 24, 23, 23, 23, 23, 1],
            [23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23],
            [24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24],
            [26, 26, 26, 26, 26, 26, 26, 26, 26, 26, 26, 26, 27, 26, 26, 26, 26, 1],
            [26, 26, 26, 26, 26, 26, 26, 26, 26, 26, 26, 26, 26, 26, 26, 26, 26, 26],
            [27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27],
            [29, 29, 29, 29, 29, 29, 29, 29, 29, 29, 29, 29, 30, 29, 29, 29, 29, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30]]



    # @param file is a string of all the contents of a program with
    def __init__ (self, file):
        self.file = file
        self.fileCounter = 0
        self.fileLength = len(self.file)
        self.tokenList = []
        

    #returns the next token using DFSA, table driven
    #@return a tuple of length 2, first entry is the token, second entry is its class
    def scan(self):
        done_flag = False
        curr = self.fileCounter
        #print(self.file[curr])
        final_token = ""
        final_type = ""
        next_state = 0
        if (self.fileCounter >= self.fileLength):
            print("The entire file has been read. Nothing more to scan. Goodbye.")
            return
        # Start on row 0 in FSA table
        # If the value is not in the dictionary, then report error.
        while (not done_flag):
            #go through table
            if (next_state == 0):
                final_token = ""
                next_state = Scanner.table[next_state][Scanner.dict_convert[self.file[curr]]]
                if (next_state != 0):
                    final_token += self.file[curr]
                curr += 1
            elif (next_state == 1):
                print("Error found at index " + str(curr) + " where the character is " + str(self.file[curr]) + ", returning -1.")
                done_flag = True
                self.fileCounter = curr
                return -1
            elif (next_state == 2):
                final_type = "<addop>"
                self.tokenList.append((final_token, final_type))
                done_flag = True
                self.fileCounter = curr
                return (final_token, final_type)
            elif (next_state == 3):
                final_type = "<addop>"
                self.tokenList.append((final_token, final_type))
                done_flag = True
                self.fileCounter = curr
                return (final_token, final_type)
            elif (next_state == 4):
                final_type = "<mop>"
                self.tokenList.append((final_token, final_type))
                done_flag = True
                self.fileCounter = curr
                return (final_token, final_type)
            elif (next_state == 5):
                final_type = "$comma"
                self.tokenList.append((final_token, final_type))
                done_flag = True
                self.fileCounter = curr
                return (final_token, final_type)
            elif (next_state == 6):
                final_type = "$semicol"
                self.tokenList.append((final_token, final_type))
                done_flag = True
                self.fileCounter = curr
                return (final_token, final_type)
            elif (next_state == 7):
                final_type = "$rparenth"
                self.tokenList.append((final_token, final_type))
                done_flag = True
                self.fileCounter = curr
                return (final_token, final_type)
            elif (next_state == 8):
                final_type = "$lparenth"
                self.tokenList.append((final_token, final_type))
                done_flag = True
                self.fileCounter = curr
                return (final_token, final_type)
            elif (next_state == 9):
                final_type = "$lbracket"
                self.tokenList.append((final_token, final_type))
                done_flag = True
                self.fileCounter = curr
                return (final_token, final_type)
            elif (next_state == 10):
                final_type = "$rbracket"
                self.tokenList.append((final_token, final_type))
                done_flag = True
                self.fileCounter = curr
                return (final_token, final_type)
            elif (next_state == 11):
                next_state = Scanner.table[next_state][Scanner.dict_convert[self.file[curr]]]
                if (next_state == 11):
                    final_token += self.file[curr]
                    curr += 1
            elif (next_state == 12):
                final_type = "<int>"
                self.tokenList.append((final_token, final_type))
                done_flag = True
                self.fileCounter = curr
                return (final_token, final_type)
            elif (next_state == 13):
                next_state = Scanner.table[next_state][Scanner.dict_convert[self.file[curr]]]
                if (next_state == 13):
                    final_token += self.file[curr]
                    curr += 1
            elif (next_state == 14):
                if (final_token == 'CONST'):
                    final_type = "$CONST"
                    self.tokenList.append((final_token, final_type))                    
                elif (final_token == 'IF'):
                    final_type = "$IF"
                    self.tokenList.append((final_token, final_type))
                elif (final_token == 'VAR'):
                    final_type = "$VARdeclaration"
                    self.tokenList.append((final_token, final_type))
                elif (final_token == 'THEN'):
                    final_type = "$THEN"
                    self.tokenList.append((final_token, final_type))
                elif (final_token == 'PROCEDURE'):
                    final_type = "$PROCEDURE"
                    self.tokenList.append((final_token, final_type))
                elif (final_token == 'WHILE'):
                    final_type = "$WHILE"
                    self.tokenList.append((final_token, final_type))
                elif (final_token == 'CALL'):
                    final_type = "$CALL"
                    self.tokenList.append((final_token, final_type))
                elif (final_token == 'DO'):
                    final_type = "$DO"
                    self.tokenList.append((final_token, final_type))
                elif (final_token == 'ODD'):
                    final_type = "$ODD"
                    self.tokenList.append((final_token, final_type))
                elif (final_token == 'CLASS'):
                    final_type = "$CLASS"
                    self.tokenList.append((final_token, final_type))
                elif (final_token == 'ELSE'):
                    final_type = "$ELSE"
                    self.tokenList.append((final_token, final_type))
                else:
                    final_type = "<var>"
                    self.tokenList.append((final_token, final_type))
                done_flag = True
                self.fileCounter = curr
                return (final_token, final_type)
            elif (next_state == 15):
                next_state = Scanner.table[next_state][Scanner.dict_convert[self.file[curr]]]
                if (next_state == 17):
                    final_token += self.file[curr]
                    curr += 1
            elif (next_state == 16):
                final_type = "<mop>"
                self.tokenList.append((final_token, final_type))
                done_flag = True
                self.fileCounter = curr
                return (final_token, final_type)            
            elif (next_state == 17):
                if (self.file[curr] == "*"):
                    next_state = Scanner.table[next_state][Scanner.dict_convert[self.file[curr]]]
                    curr+=1
                else:
                    final_token += self.file[curr]
                    curr += 1
            elif (next_state == 18):
                if (self.file[curr] == "/"):
                    next_state = Scanner.table[next_state][Scanner.dict_convert[self.file[curr]]]
                    curr+=1
                else:
                    next_state = 17
                    final_token += self.file[curr]
                    curr += 1  
            elif (next_state == 19):
                next_state = Scanner.table[next_state][Scanner.dict_convert[self.file[curr]]]
                if (next_state == 21):
                    final_token += self.file[curr]
                    curr += 1
            elif (next_state == 20):
                final_type = "<assign>"
                self.tokenList.append((final_token, final_type))
                done_flag = True
                self.fileCounter = curr
                return (final_token, final_type)
            elif (next_state == 21):
                final_type = "<relop>"
                self.tokenList.append((final_token, final_type))
                done_flag = True
                self.fileCounter = curr
                return (final_token, final_type)
            elif (next_state == 22):
                next_state = Scanner.table[next_state][Scanner.dict_convert[self.file[curr]]]
                if (next_state == 24):
                    final_token += self.file[curr]
                    curr += 1
            elif (next_state == 23):
                final_type = "<relop>"
                self.tokenList.append((final_token, final_type))
                done_flag = True
                self.fileCounter = curr
                return (final_token, final_type)
            elif (next_state == 24):
                final_type = "<relop>"
                self.tokenList.append((final_token, final_type))
                done_flag = True
                self.fileCounter = curr
                return (final_token, final_type)
            elif (next_state == 25):
                next_state = Scanner.table[next_state][Scanner.dict_convert[self.file[curr]]]
                if (next_state == 27):
                    final_token += self.file[curr]
                    curr += 1
            elif (next_state == 26):
                final_type = "<relop>"
                self.tokenList.append((final_token, final_type))
                done_flag = True
                self.fileCounter = curr
                return (final_token, final_type)
            elif (next_state == 27):
                final_type = "<relop>"
                self.tokenList.append((final_token, final_type))
                done_flag = True
                self.fileCounter = curr
                return (final_token, final_type)
            elif (next_state == 28):
                next_state = Scanner.table[next_state][Scanner.dict_convert[self.file[curr]]]
                if (next_state == 30):
                    final_token += self.file[curr]
                    curr += 1
            elif (next_state == 29):
                print("Error found at index " + str(curr) + " where the character is " + str(self.file[curr]) + ", returning -1.")
                done_flag = True
                self.fileCounter = curr
                return -1
            elif (next_state == 30):
                final_type = "<relop>"
                self.tokenList.append((final_token, final_type))
                done_flag = True
                self.fileCounter = curr
                return (final_token, final_type)
            else:
                print("Error, did not catch the correct next_state value :(.")
                return -1



# @param scanner_instance, a Scanner object
#returns a two-d list, each row has exactly five entries being:
#[Symbol, Classification, Value, Address, Segment]
def parse(scanner_instance):

    parse_convert = {
        "$CLASS":0,
        "<var>":1,
        "$lbracket":2,
        "$CONST":3,
        "<assign>":4,
        "<int>":5,
        "$comma":6,
        "$semicol":7,
        "$VARdeclaration":8,
        "$IF":9,
        "$THEN":10,
        "$PROCEDURE":11,
        "$WHILE":12,
        "$CALL":13,
        "$DO":14,
        "$ODD":15,
        }
    
    parse_table = [
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 10, 0, 4, 0, 0, 0, 0, 8, 10, 10, 10, 10, 10, 10, 10, 0],
        [0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 4, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 8, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [10, 10, 10, 10, 10, 11, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10],
        [10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]


    symbol_table = []

    next_state = 0
    prev_var = ''
    curr_cs_address=0
    curr_ds_address=0
    entry = None
    
    while (scanner_instance.fileCounter < scanner_instance.fileLength):
        curr_token = scanner_instance.scan()
        #print(curr_token)
        if (next_state == 0):
            next_state = parse_table[next_state][parse_convert[curr_token[1]]]
            if (curr_token[1] == '<var>'):
                prev_var = curr_token[0]
        elif (next_state == 1):
            next_state = parse_table[next_state][parse_convert[curr_token[1]]]
            if (curr_token[1] == '<var>'):
                prev_var = curr_token[0]
            entry = [str(curr_token[0]), '$programName', '?', 0, 'CS']
            symbol_table.append(entry)
            curr_cs_address += 2
        elif (next_state ==2):
            next_state = parse_table[next_state][parse_convert[curr_token[1]]]
            if (curr_token[1] == '<var>'):
                prev_var = curr_token[0]
        elif (next_state==3):
            next_state = parse_table[next_state][parse_convert[curr_token[1]]]
            if (curr_token[1] == '<var>'):
                prev_var = curr_token[0]
        elif (next_state==4):
            next_state = parse_table[next_state][parse_convert[curr_token[1]]]
            if (curr_token[1] == '<var>'):
                prev_var = curr_token[0]
        elif (next_state==5):
            next_state = parse_table[next_state][parse_convert[curr_token[1]]]
            if (curr_token[1] == '<var>'):
                prev_var = curr_token[0]

        elif (next_state==6):
            next_state = parse_table[next_state][parse_convert[curr_token[1]]]
            if (curr_token[1] == '<var>'):
                prev_var = curr_token[0]
            entry = [prev_var, '<constvar>', curr_token[0], curr_ds_address, 'DS']
            symbol_table.append(entry)
            curr_ds_address += 2
            
        elif (next_state==7):
            next_state = parse_table[next_state][parse_convert[curr_token[1]]]
            if (curr_token[1] == '<var>'):
                prev_var = curr_token[0]

        elif (next_state==8):
            next_state = parse_table[next_state][parse_convert[curr_token[1]]]
            entry = [curr_token[0], '<var>', '?', curr_ds_address, 'DS']
            symbol_table.append(entry)
            curr_ds_address += 2
            if (curr_token[1] == '<var>'):
                prev_var = curr_token[0]

        elif (next_state==9):
            next_state = parse_table[next_state][parse_convert[curr_token[1]]]
            if (curr_token[1] == '<var>'):
                prev_var = curr_token[0]

        elif (next_state==10):
            if curr_token[1] in parse_convert:
                next_state = parse_table[next_state][parse_convert[curr_token[1]]]
            else:
                next_state = 10
            if next_state == 11:
                isDuplicate = False
                for i in range (len(symbol_table)):
                    if (symbol_table[i][0] == curr_token[0]):
                        isDuplicate = True
                if not isDuplicate:
                    entry = [curr_token[0], '$numLit', curr_token[0], curr_ds_address, 'DS']
                    symbol_table.append(entry)
                    curr_ds_address += 2

        elif (next_state==11):
            next_state = 10

    for i in range(10):
        curr_temp = 'T' + str(i+1)
        curr_entry = [curr_temp, '$temp', '?', curr_ds_address, 'DS']
        symbol_table.append(curr_entry)
        curr_ds_address += 2
    return symbol_table





def main(fileName):

    # Open a file: file
    file = open(str(fileName), mode='r')
 
    # Read all lines at once and store as a string
    all_of_it = file.read()

    # Ended up deleting the re.sub.
    # The current scanner can handle \n, \t, \r, and spaces
    #myFile = re.sub(r"[\n\t]*", "", all_of_it)
    myFile = all_of_it
 
    # close the file
    file.close()

    # Create a Scanner object to write all the tokens
    # to an output file
    tokenFile = open('tokenList.txt', mode='w')
    myScannerDemo = Scanner(myFile)
    while (myScannerDemo.fileCounter < myScannerDemo.fileLength):
        currToken = myScannerDemo.scan()
        tokenFile.write(str(currToken[0]) + ' ' + str(currToken[1]) + '\n')
    tokenFile.close()

    # Create another Scanner object, this one to make the symbol table
    # Each entry in the symbol table is [Symbol, Classification, Value, Address, Segment]
    # Write the symbol table to a file
    myScanner = Scanner(myFile)
    symTable = parse(myScanner)
    symTabFile = open('symbolTable.txt', mode='w')
    for i in range (len(symTable)):
        for j in range(len(symTable[i])):
            symTabFile.write(str(symTable[i][j]) + ' ')
        symTabFile.write('\n')

 
if __name__ == '__main__':
    main('testInput.txt')
