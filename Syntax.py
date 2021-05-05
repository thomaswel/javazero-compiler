import Lexical
'''
Student: Thomas Welborn
Class: 4316 Compiler Design and Construction

Purpose: This program utilizes a Push Down Automoton in order to do Syntax Analysis
        for the compilation of a source Java 0 program. The input for this program
        is the source code written in Java 0, and the output is a text file (quads.txt)
        containing the quads formed from the table-driven PDA. This will be
        used to generate the assembly code.
'''


'''
The PushDownAutomaton Class utilizes a table-driven push down
automoton to generate quads from the tokens extracted from the 
source text file.
'''
class PushDownAutomaton:
    # Dictionary used to convert token classes to their corresponding
    # row or column number.
    dict_convert = {
        '$semicol':0,
        '<assign>':1,
        '<addop>':2,
        '$lparenth':3,
        '$rparenth':4,
        '<mop>':5,
        '$IF':6,
        '$THEN':7,
        '$ODD':8,
        '<relop>':9,
        '$lbracket':10,
        '$rbracket':11,
        '$CALL':12,
        '$WHILE':13,
        '$DO':14,
        '$ELSE':15}

    # Table used for the Push Down Automoton.
    # The table is the Operator Precedence Matrix.
    table = [
        [0, '<', 0, '<', 0, 0, '<', 0, 0, 0, 0, '>', 0, '<', 0, 0],
        ['>', 0, '<', '<', 0, '<', 0, 0, 0, 0, 0, 0, 0, 0, 0, '>'],
        ['>', 0, '>', '<', '>', '<', 0, '>', 0, '>', 0, 0, 0, 0, '>', '>'],
        [0, 0, '<', '<', '=', '<', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        ['>', 0, '>', 0, '>', '>', 0, 0, 0, 0, 0, 0, 0, 0, 0, '>'],
        ['>', 0, '>', '<', '>', '>', 0, '>', 0, '>', 0, 0, 0, 0, '>', '>'],
        [0, 0, '<', '<', 0, '<', 0, '=', '<', '<', 0, 0, 0, 0, 0, 0],
        ['>', '<', 0, '<', 0, 0, '<', 0, 0, 0, '<', 0, '<', 0, 0, '='],
        [0, 0, '<', '<', 0, '<', 0, '>', 0, 0, 0, 0, 0, 0, 0, '>'],
        [0, 0, '<', '<', 0, '<', 0, '>', 0, 0, 0, 0, 0, 0, '>', '>'],
        [0, '<', 0, 0, 0, 0, '<', 0, 0, 0, '<', '=', '<', '<', 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, '<', '<', 0, '<', 0, 0, '<', '<', 0, 0, 0, 0, '=', 0],
        ['>', '<', 0, '<', 0, 0, 0, 0, 0, 0, '<', 0, '<', '<', 0, 0],
        ['>', '<', 0, '<', 0, 0, '<', 0, 0, 0, '<', 0, '<', 0, 0, 0]]


    def __init__(self, scanner, symbol_table):
        self.scanner = scanner
        self.symbolTable = symbol_table
        self.statementList = []
        self.quadList = []
        # A counter for label generation since they are not repeated.
        self.labelCount = 1
        # A counter for while loop labels
        self.whileCount = 1
        # A list for the Read Statements.
        # Will only append at the end. No PDA for these.
        self.readQuads = []
        # a list for the Print Statements.
        self.printQuads = []

    
    '''
    @param None.
    @returns Separates all of the statements by semicolons/brackets
            and appends them to self.statementList.
    '''
    def get_statements(self):
        self.scanner.scan() # Returns $CLASS, throwaway.
        self.scanner.scan() # Returns <var> $programName, throw away.
        self.scanner.scan() # Returns $lbracket, throw away.
        
        # Iterate through all of the tokens produced from Lexical Analysis.
        while (self.scanner.fileCounter < self.scanner.fileLength):
            curr_token = self.scanner.scan()
            curr_statement = []
            # Bracket count will be used for compound statements:
            #   IF-THEN{coumpound}, IF-THEN{compound}ELSE{compound}, WHILE-DO{compound}
            # If a left bracket is found, add 1
            # If a right bracket is found, subtract 1
            # The coumpound statement will continue to go until the bracket count is balanced (==0)
            bracket_count = 0
            #print(curr_token)

            # Skip over the CONST and VAR declarations.
            # These should already be in the symbol table from the first pass.
            if (curr_token[1] == '$CONST') or (curr_token[1] == '$VARdeclaration'):
                while curr_token[1] != '$semicol':
                    curr_token = self.scanner.scan()

            # Get all the Read statements, add to self.readQuads.
            elif (curr_token[0] == 'Read'):
                curr_token = self.scanner.scan() # Get the variable to read
                curr_statement = ['Read',str(curr_token[0]), 'None', 'None']
                self.readQuads.append(curr_statement)
                while curr_token[1] != '$semicol':
                    curr_token = self.scanner.scan()

            # Get all the Print statements, add to self.printQuads.
            elif (curr_token[0] == 'Print'):
                curr_token = self.scanner.scan() # Get the variable to print
                curr_statement = ['Print',str(curr_token[0]), 'None', 'None']
                self.printQuads.append(curr_statement)
                while curr_token[1] != '$semicol':
                    curr_token = self.scanner.scan()
            
            # If a statement starts with a variable, assume its a non-compound assignment.
            elif curr_token[1] == '<var>':
                while curr_token[1] != '$semicol':
                    curr_statement.append(curr_token)
                    curr_token = self.scanner.scan()
                # Get the semicolon/bracket on the end
                curr_statement.append(curr_token)
                self.statementList.append(curr_statement)

            elif curr_token[1] == '$IF':
                # Just do non-compound statements right now
                while curr_token[1] != '$semicol':
                    if curr_token[1] == '$lbracket':
                        bracket_count += 1
                    curr_statement.append(curr_token)
                    curr_token = self.scanner.scan()
                # If bracket count is 0, then it is NOT a compound statement
                if bracket_count == 0:
                    curr_statement.append(curr_token)
                    self.statementList.append(curr_statement)
                    continue
                else:
                    while bracket_count != 0:
                        if curr_token[1] == '$lbracket':
                            bracket_count += 1
                        if curr_token[1] == '$rbracket':
                            bracket_count -= 1
                        curr_statement.append(curr_token)

                        if bracket_count != 0:
                            curr_token = self.scanner.scan()
                    # Done UNLESS there is an $ELSE attached to the end.
                    # Will handle this in a new elif.
                    self.statementList.append(curr_statement)


            # This elif is only for compound else statements.
            # The simple IF-THEN-ELSE should be caught in the 
            #   previous elif statement since there's only one semicolon.
            elif curr_token[1] == '$ELSE':
                # Retreive the last list in the statementList.
                # It should be an if-then statement.
                # self.statementList[-1].append to add to it
                while curr_token[1] != '$semicol':
                    if curr_token[1] == '$lbracket':
                        bracket_count += 1
                    curr_statement.append(curr_token)
                    curr_token = self.scanner.scan()
                # If bracket count is 0, then it is NOT a compound ELSE statement
                if bracket_count == 0:
                    curr_statement.append(curr_token)
                    for i in range (len(curr_statement)):
                        self.statementList[-1].append(curr_statement[i])
                    continue
                else:
                    while bracket_count != 0:
                        if curr_token[1] == '$lbracket':
                            bracket_count += 1
                        if curr_token[1] == '$rbracket':
                            bracket_count -= 1
                        curr_statement.append(curr_token)

                        if bracket_count != 0:
                            curr_token = self.scanner.scan()
                    # Done 
                    for i in range (len(curr_statement)):
                        self.statementList[-1].append(curr_statement[i])


            
            elif curr_token[1] == '$WHILE':
                while curr_token[1] != '$semicol':
                    if curr_token[1] == '$lbracket':
                        bracket_count += 1
                    curr_statement.append(curr_token)
                    curr_token = self.scanner.scan()
                # Exit loop when semicolon encountered.
                # Check the bracket_count to see if it is compound.
                if bracket_count == 0:
                    curr_statement.append(curr_token)
                    self.statementList.append(curr_statement)
                    continue
                else:
                    while bracket_count != 0:
                        if curr_token[1] == '$lbracket':
                            bracket_count += 1
                        if curr_token[1] == '$rbracket':
                            bracket_count -= 1
                        curr_statement.append(curr_token)

                        if bracket_count != 0:
                            curr_token = self.scanner.scan()
                    # Done
                    self.statementList.append(curr_statement)                
            
            else:
                print('Error at ' + str(self.scanner.fileCounter) + 'in the file.')

        print('--------------------------')
        for i in range (len(self.statementList)):
            print(self.statementList[i])






    '''
    The method get_quads() iterates through each of the statements in self.statementList
    from the get_statements() method and uses the PDA to convert them into 
    quads.
    '''
    def get_quads(self):
        # List of the finished quads.
        fin_quads = []
        # Iterate through each statement from get_statements().
        for i in range (len(self.statementList)):
            curr_stack = [(';', '$semicol')]
            prev_ops = [(';', '$semicol')]
            tempGenerator = []
            fixUpCounter = 0
            curr_quad = []
            curr_quad_0='?'
            curr_quad_1='?'
            curr_quad_2='?'
            curr_quad_3='?'
            # Labels for the if and while statements
            labelGenerator = []
            # Labels for the while loops
            whileLabelGen = []


            
            for j in range (len(self.statementList[i])):
                curr_token = self.statementList[i][j]
                
                if curr_token[1] not in self.dict_convert:
                    print(str(curr_token) + ' not in dictionary, is a non-term')
                    curr_stack.append(curr_token)
                
                elif self.table[self.dict_convert[prev_ops[-1][1]]][self.dict_convert[curr_token[1]]] == '<':
                    curr_stack.append(curr_token)
                    prev_ops.append(curr_token)

                    if curr_token[1] == '$IF':
                        theNone = ('None', 'None')
                        thing = ('IF', '$IF')             
                        fin_quads.append([thing, theNone, theNone, theNone])

                    if curr_token[1] == '$WHILE':
                        theNone = ('None', 'None')
                        thing = ('WHILE', '$WHILE')
                        whileLabelGen.append('W' + str(self.whileCount))
                        self.whileCount += 1
                        fin_quads.append([thing, (whileLabelGen[-1], '<whileLabel>'), theNone, theNone])



                elif self.table[self.dict_convert[prev_ops[-1][1]]][self.dict_convert[curr_token[1]]] == '>':
                    while self.table[self.dict_convert[prev_ops[-1][1]]][self.dict_convert[curr_token[1]]] == '>':
                        popped_op = prev_ops.pop()

                        if popped_op[1] == '<addop>' or popped_op[1] == '<mop>':
                            curr_quad_2 = curr_stack.pop()
                            curr_stack.pop() #should be the <addop> or <mop> operator
                            curr_quad_1 = curr_stack.pop()
                            tempGenerator.append('T' + str(len(tempGenerator)+1))
                            curr_quad_3 = (tempGenerator[-1], '$temp')
                            curr_quad = [popped_op, curr_quad_1, curr_quad_2, curr_quad_3]
                            fin_quads.append(curr_quad)

                            # Now push the temp back onto the curr_stack
                            curr_stack.append(curr_quad_3)

                        elif popped_op[1] == '<assign>':
                            curr_quad_2 = curr_stack.pop()
                            curr_stack.pop() #should be the <assign> operator
                            curr_quad_1 = curr_stack.pop()
                            curr_quad_3 = ('None', 'None')
                            curr_quad = [popped_op, curr_quad_1, curr_quad_2, curr_quad_3]
                            fin_quads.append(curr_quad)
                            #Nothing to push since it was an assign. Just continue

                        elif popped_op[1] == '<relop>':
                            curr_quad_2 = curr_stack.pop()
                            curr_stack.pop() #the relop
                            curr_quad_1 = curr_stack.pop()
                            curr_quad_3 = ('None', 'None')
                            curr_quad = [popped_op, curr_quad_1, curr_quad_2, curr_quad_3]
                            fin_quads.append(curr_quad)

                        elif popped_op[1] == '$THEN':
                            prev_ops.pop() #pop IF out of operator stack
                            curr_stack.pop() #THEN popped
                            curr_stack.pop() #IF popped
                            theLabel = (labelGenerator[-1], '<label>')
                            theThing = ('None', 'None')
                            fin_quads.append([theLabel, theThing, theThing, theThing])

                        
                        elif popped_op[1] == '$ELSE':
                            prev_ops.pop() #pop THEN out of operator stack
                            prev_ops.pop() #pop IF out of operator stack
                            curr_stack.pop() #ELSE popped
                            curr_stack.pop() #THEN popped
                            curr_stack.pop() #IF popped
                            theLabel = (labelGenerator[-1], '<label>')
                            theThing = ('None', 'None')
                            fin_quads.append([theLabel, theThing, theThing, theThing])



                        elif popped_op[1] == '$DO':
                            prev_ops.pop() #pop WHILE out of operator stack
                            curr_stack.pop() #DO popped
                            curr_stack.pop() #WHILE popped
                            theLabel = (labelGenerator[-1], '<label>')
                            theWhileLabel = (whileLabelGen[-1], '<whileLabel>')
                            theThing = ('None', 'None')
                            # Need the two labels that will be converted in semantics.
                            fin_quads.append([theLabel, theWhileLabel, theThing, theThing])
                            #Pop the label out too so next label will be correct
                            labelGenerator.pop()    
                            whileLabelGen.pop()                      

                        elif popped_op[1] == '$semicol':
                            curr_stack.pop() #pop the semicol out of the stack
                        
                    # Once the while loop has been exited, it is safe to push the curr_tokens operator
                    curr_stack.append(curr_token)
                    prev_ops.append(curr_token)

                    # For compound statements, the stack could be {}, so need to pop those if they exist
                    if curr_stack[-1][1] == '$rbracket':
                        curr_stack.pop() #pop }
                        curr_stack.pop() #pop {
                        prev_ops.pop() #pop }
                        prev_ops.pop() #pop {
                        # The top of the stack and the operator stack should now be THEN
                        # if we are dealing with just an IF-THEN compound statement with no else.
                        # Also if its a while-DO then its the same as IF-THEN.
                        # So just redo the elif statement from above
                        if (j == (len(self.statementList[i]) - 1)) and (prev_ops[-1][1] == '$THEN'):
                            prev_ops.pop() #pop THEN out of op stack
                            prev_ops.pop() #pop IF out of operator stack
                            curr_stack.pop() #THEN popped
                            curr_stack.pop() #IF popped
                            theLabel = (labelGenerator[-1], '<label>')
                            theThing = ('None', 'None')
                            fin_quads.append([theLabel, theThing, theThing, theThing])
                        if (j == (len(self.statementList[i]) - 1)) and (prev_ops[-1][1] == '$ELSE'):
                            prev_ops.pop() #pop THEN out of operator stack
                            prev_ops.pop() #pop IF out of operator stack
                            curr_stack.pop() #ELSE popped
                            curr_stack.pop() #THEN popped
                            curr_stack.pop() #IF popped
                            theLabel = (labelGenerator[-1], '<label>')
                            theThing = ('None', 'None')
                            fin_quads.append([theLabel, theThing, theThing, theThing])
                        if (j == (len(self.statementList[i]) - 1)) and (prev_ops[-1][1] == '$DO'):
                            prev_ops.pop() #pop DO out of op stack
                            prev_ops.pop() #pop WHILE out of operator stack
                            curr_stack.pop() #DO popped
                            curr_stack.pop() #WHILE popped
                            theLabel = (labelGenerator[-1], '<label>')
                            labelGenerator.pop()
                            theWhileLabel = (whileLabelGen[-1], '<whileLabel>')
                            whileLabelGen.pop()
                            theThing = ('None', 'None')
                            fin_quads.append([theLabel, theWhileLabel, theThing, theThing])
                            

                        
                    # Take into account if the pushed thing was $THEN, because need to generate the quad for that
                    if curr_token[1] == '$THEN':
                        labelGenerator.append('L' + str(self.labelCount))
                        self.labelCount += 1
                        zero = ('THEN', '$THEN')
                        one = (labelGenerator[-1], '<label>')
                        three = ('None', 'None')
                        if fin_quads[-1][0][0] == '>':
                            two = ('LE', '<jumpCondition>')
                        elif fin_quads[-1][0][0] == '>=':
                            two = ('L', '<jumpCondition>')
                        elif fin_quads[-1][0][0] == '<':
                            two = ('GE', '<jumpCondition>')
                        elif fin_quads[-1][0][0] == '<=':
                            two = ('G', '<jumpCondition>')
                        elif fin_quads[-1][0][0] == '==':
                            two = ('NE', '<jumpCondition>')
                        elif fin_quads[-1][0][0] == '!=':
                            two = ('E', '<jumpCondition>')
                        else:
                            print('THEN WAS PUSHED BUT COULDNT FIND THE RIGHT CONDITIONAL')
                            two = ('?', '<jumpCondition>')
                        fin_quads.append([zero, one, two, three])

                    if curr_token[1] == '$ELSE':
                        labelGenerator.append('L' + str(self.labelCount))
                        self.labelCount += 1
                        zero = ('ELSE', '$ELSE')
                        one = (labelGenerator[-1], '<label>')
                        two = ('None', 'None')
                        three = ('None', 'None')
                        fin_quads.append([zero, one, two, three])
                        # Also add the label from the previous IF-THEN.
                        # Using the self.fixUp location within the labelGenerator.
                        theLabel = (labelGenerator[fixUpCounter], '<label>')
                        theThing = ('None', 'None')
                        fin_quads.append([theLabel, theThing, theThing, theThing])
                        fixUpCounter += 1

                    
                    # Take into account if the pushed thing was $DO, because need to generate the quad for that
                    if curr_token[1] == '$DO':
                        labelGenerator.append('L' + str(self.labelCount))
                        self.labelCount += 1
                        zero = ('DO', '$DO')
                        one = (labelGenerator[-1], '<label>')
                        three = ('None', 'None')
                        if fin_quads[-1][0][0] == '>':
                            two = ('LE', '<jumpCondition>')
                        elif fin_quads[-1][0][0] == '>=':
                            two = ('L', '<jumpCondition>')
                        elif fin_quads[-1][0][0] == '<':
                            two = ('GE', '<jumpCondition>')
                        elif fin_quads[-1][0][0] == '<=':
                            two = ('G', '<jumpCondition>')
                        elif fin_quads[-1][0][0] == '==':
                            two = ('NE', '<jumpCondition>')
                        elif fin_quads[-1][0][0] == '!=':
                            two = ('E', '<jumpCondition>')
                        else:
                            print('THEN WAS PUSHED BUT COULDNT FIND THE RIGHT CONDITIONAL')
                            two = ('?', '<jumpCondition>')
                        fin_quads.append([zero, one, two, three])


                    if curr_token[1] == '$rparenth':
                        prev_ops.pop() #pop )
                        prev_ops.pop() #pop (
                        curr_stack.pop() #pop )
                        meTemp = curr_stack.pop() #whatever temp is still in the parenthesis, or its a open parenthesis
                        if curr_stack[-1][1] =='$lparenth':
                            curr_stack.pop()
                        if meTemp[1] != '$lparenth':
                            curr_stack.append(meTemp)

                    if curr_token[1] == '$semicol':
                        prev_ops.pop() #pop the semicolon and throw away
                        curr_stack.pop() #pop the semicol and throw away

                        
                        
                elif self.table[self.dict_convert[prev_ops[-1][1]]][self.dict_convert[curr_token[1]]] == '=':
                    curr_stack.append(curr_token)
                    prev_ops.append(curr_token)
                    if curr_token[1] == '$ELSE':
                        labelGenerator.append('L' + str(self.labelCount))
                        self.labelCount += 1
                        zero = ('ELSE', '$ELSE')
                        one = (labelGenerator[-1], '<label>')
                        two = ('None', 'None')
                        three = ('None', 'None')
                        fin_quads.append([zero, one, two, three])
                        # Also add the label from the previous IF-THEN.
                        # Using the self.fixUp location within the labelGenerator.
                        theLabel = (labelGenerator[fixUpCounter], '<label>')
                        theThing = ('None', 'None')
                        fin_quads.append([theLabel, theThing, theThing, theThing])
                        fixUpCounter += 1
                    
                    
                    if curr_stack[-1][1] == '$rbracket':
                        curr_stack.pop() #pop }
                        curr_stack.pop() #pop {
                        prev_ops.pop() #pop }
                        prev_ops.pop() # pop {
                        if curr_stack[-1][1] == '$DO':
                            curr_stack.pop() #pop DO
                            curr_stack.pop() #pop WHILE
                            prev_ops.pop() #pop DO
                            prev_ops.pop() #pop WHILE

                            theLabel = (labelGenerator[-1], '<label>')
                            theWhileLabel = (whileLabelGen[-1], '<whileLabel>')
                            theThing = ('None', 'None')
                            # Need the two labels that will be converted in semantics.
                            fin_quads.append([theLabel, theWhileLabel, theThing, theThing])
                            #Pop the label out too so next label will be correct
                            labelGenerator.pop()    
                            whileLabelGen.pop()    
                        if curr_stack[-1][1] == '$ELSE':
                            curr_stack.pop() # pop ELSE
                            curr_stack.pop() # pop THEN
                            curr_stack.pop() # pop IF
                            prev_ops.pop() # pop ELSE
                            prev_ops.pop() # pop THEN
                            prev_ops.pop() # pop IF

                            theLabel = (labelGenerator[-1], '<label>')
                            theThing = ('None', 'None')
                            # Need the two labels that will be converted in semantics.
                            fin_quads.append([theLabel, theThing, theThing, theThing])
                            #Pop the label out too so next label will be correct
                            labelGenerator.pop()    
                    

                else:
                    print('Error, no op matrix relation found.')

            print('remaining stack after statement ' + str(i) + 'finished')
                         

            for x in range (len(curr_stack)):
                print (curr_stack[x])
            print('----------------------')
            '''
                if table[dict_convert[curr_stack[-1][1]]][curr_token[1]] == '>':
                if table[dict_convert[curr_stack[-1][1]]][curr_token[1]] == '=':
            '''
        self.quadList = fin_quads
        return fin_quads
            
        







def main(fileName):
    # Open a file: file
    file = open(str(fileName),mode='r')
 
    # Read all lines at once and store as a string
    all_of_it = file.read()
    myFile = all_of_it
    #myFile = re.sub(r"[\n\t]*", "", all_of_it)
 
    # close the file
    file.close()

    # Create 2 Scanner instances. 
    # One for the syntax analysis, one to get the symbol table.
    myScanner = Lexical.Scanner(myFile)
    myScanner2 = Lexical.Scanner(myFile)
    mySymbolTable = Lexical.parse(myScanner2)

    # First parse into statements. Each statement will be handled
    # individually in order to produce the quads.
    myPDA = PushDownAutomaton(myScanner, mySymbolTable)
    myPDA.get_statements()
    
    print('--------------------- NOW ONTO QUADS -----------------------------------')
    quads = myPDA.get_quads()
    for i in range (len(quads)):
        print(quads[i])
    
    quadsFile = open('quads.txt', mode='w')
    # 1) Write all the Read quads.
    for i in range (len(myPDA.readQuads)):
        for j in range (3):
            quadsFile.write(str(myPDA.readQuads[i][j]) + " ")
        quadsFile.write(str(myPDA.readQuads[i][3]))
        quadsFile.write('\n')
    # 2) Write all the normal quads.
    for i in range (len(quads)):
        for j in range (3):
            if quads[i][j][1] == '<int>':
                quadsFile.write('lit' + str(quads[i][j][0]) + " ")
            else:
                quadsFile.write(str(quads[i][j][0]) + " ")

        if quads[i][3][1] == '<int>':
            quadsFile.write('lit' + str(quads[i][3][0]))
        else:
            quadsFile.write(str(quads[i][3][0]))
        quadsFile.write('\n')
    # 3) Write all the Print quads.
    for i in range (len(myPDA.printQuads)):
        for j in range (3):
            quadsFile.write(str(myPDA.printQuads[i][j]) + " ")
        quadsFile.write(str(myPDA.printQuads[i][3]))
        quadsFile.write('\n')
    # 4. Close the file.
    quadsFile.close()
    

if __name__ == '__main__':
    main('testInput.txt')
        
    
