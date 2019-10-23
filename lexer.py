from sys import argv

script, file = argv

#used to move the file on
def advance():
    global currentLine
    currentLine = source.readline()

#determines what type of comman is on that line
def commandType(currentLine):
    if currentLine[0] == '(':
        return 'L'
    elif currentLine[0] == '@':
        return 'A'
    else:
        return 'C'

#returns the symbol for L and A commands
def symbol(currentLine):
    #handles L commands to return whatever is in parentheses
    if currentLine[0] == '(':
        symbol = currentLine[1:-1]
        return symbol
    #handles a commands to return whatever is after the at symbol
    if currentLine[0] == '@':
        symbol = currentLine[1:]
        return symbol

#returns the destination memonic for a c command
def dest(currentLine):
    if currentLine.count('=') > 0:
        dest = currentLine.split('=')
        return dest[0]
    else:
        return None

#returns the computation memonic for C commands. handles 4 cases
def comp(currentLine):
    #all cases that have a destination or a jump
    if currentLine.count('=') > 0 or currentLine.count(';') > 0:
        #if both are present
        if currentLine.count('=') > 0 and currentLine.count(';') > 0:
            comp = currentLine.split('=')
            comp = comp[1].split(';')
            return comp[0]
        #if only jump is present
        if currentLine.count(';') > 0:
            comp = currentLine.split(';')
            return comp[0]
        #if only destination is present
        else:
            comp = currentLine.split('=')
            return comp[1]
    #no destination or jump
    else:
        return currentLine

#returns the jump field in a C command
def jump(currentLine):
    if currentLine.count(';') > 0:
        jump = currentLine.split(';')
        return jump[1]
    else:
        return None




source = open(file)
numLines = len(source.readlines())
source.seek(0)
#list to store the output with comments stripped
tokenStream = []
for line in range(numLines):
    advance()
    #makes a list out of the string split at the coment symbol
    currentLine = currentLine.split('//')
    #if a coment was present removes it from the list created by the split
    if len(currentLine) > 1:
        currentLine.pop(1)
    currentLine = currentLine[0].strip()
    #handles lines with only comments by only appending non empty strings
    if currentLine != '':
        tokenStream.append(currentLine)
source.seek(0)

out = []

#main processing loop. Takes each line and splits it into a list of its components which is appended to the master list
for line in tokenStream:
    if commandType(line) == 'C':
        temp = ['C', dest(line), comp(line), jump(line)]
        out.append(temp)
    else:
        temp = [commandType(line), symbol(line).isdigit(), symbol(line)]
        out.append(temp)

def main():
    return out
