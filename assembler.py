from sys import argv
import lexer
from codeWriter import *

table = {'SP':0, 'LCL':1, 'ARG':2, 'THIS':3, 'THAT':4, 'R0':0, 'R1':1, 'R2':2, 'R3':3, 'R4':4, 'R5':5, 'R6':6, 'R7':7, 'R8':8, 'R9':9, 'R10':10, 'R11':11, 'R12':12, 'R13':13, 'R14':14, 'R15':15, 'SCREEN':16384, 'KBD':24576}

#return 16 bit binary representation
def toBin(x):
    bn = bin(int(x))[2:]
    padding = 16 - len(bn)
    return '0' * padding + bn


script, file = argv

lexed = lexer.main()

lineNum = 0
memory = 16

for line in lexed:
    #add debug lin number to c and a instructions
    if line[0] != 'L':
        line.append(lineNum)
        lineNum += 1
    else:
        #add pseudo comands to the table
        table[line[2]] = lineNum

#remove label comands from the stream
for line in lexed:
    if line[0] == 'L':
        lexed.remove(line)

with open(file[:-4] + '.hack', 'w') as f:
    for line in lexed:
        if line[0] == 'A':
            #if the comand is already numeric
            if line[1]:
                print(toBin(line[2]), file=f)
            elif line[2] in table:
                print(toBin(table[line[2]]), file=f)
            else:
                table[line[2]] = memory
                print(toBin(memory), file=f)
                memory += 1
        if line[0] == 'C':
            comp = cmp(line[2])
            dest = dst(line[1])
            jump = jmp(line[3])
            print('111' + comp + dest + jump, file=f)
