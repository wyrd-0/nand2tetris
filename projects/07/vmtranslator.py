#!/usr/bin/python3

import sys

push = '''(PUSH)	//Expects ARG to contain value to push
@ARG
D=M
@SP
M=M+1
A=M-1
M=D
'''
pop = '''(POP)		//Stores output in D
@SP
AM=M-1		//decrement TOS, set RAM addr to old TOS
D=M
'''

add = '''(ADD)
@SP
AMD=M-1		//M,D==new top of stack
D=M				//D==value at old TOS
A=A-1			//A==new TOS
M=M+D			//value at new TOS += value at old TOS
'''

sub = '''(SUB)
@SP
AMD=M-1
D=M
A=A-1
M=M-D
'''

neg = '''(NEG)
@SP
A=M
M=-M
'''

tf_jmp = '''(TF_JMP)
@SP
A=M-1
M=0
@exit
0;JMP
(true)
@SP
A=M-1
M=1
(exit)
'''

eq = '''(EQNE)
@SP
AM=M-1
D=M
A=A-1
D=M-D
@true
D;JEQ
''' + tf_jmp

gt = '''(GT)
@SP
AM=M-1
D=M
A=A-1
D=M-D
@true
D;JGT
''' + tf_jmp

lt = '''(LT)
@SP
AM=M-1
D=M
A=A-1
D=M-D
@true
D;JLT
''' + tf_jmp

conj = '''(AND)
@SP
AMD=M-1
A=A-1
M=D&M
'''

disj = '''(OR)
@SP
AMD=M-1
A=A-1
M=D|M
'''

bitnot = '''(NOT)
@SP
A=M-1
D=M
@true
D;JEQ
''' + tf_jmp

ASM = []
filename = sys.argv[1]
f = open(filename)
STATIC = filename.split('.vm')[0]

C_ARITH = ['add','sub','neg','eq','gt','lt','and','or','not']
C_PUSH = 'push'
C_POP = 'pop'

vm = f.readlines()

for l in vm:
	args = l.split(' ')
	arg1 = args[0]
	addr = ''

	if 'add' is arg1:
		cmd = add

	if 'sub' is arg1:
		cmd = sub 

	if 'neg' is arg1:
		cmd = '@SP\nA=M\nM=-M'

	if not arg1 in C_ARITH:
		arg2 = args[1]
		index = args[2]

		if 'local' is arg2:
			addr = '@LCL' + deref

		if 'arg' is arg2:
			addr = '@ARG' + deref

		if 'this' is arg2:
			addr = '@THIS' + deref

		if 'that' is arg2:
			addr = '@THAT' + deref

		if 'constant' is arg2:
			addr = '@' + index

		if 'static' is arg2:
			addr = '@' + STATIC + '.' + index

		if 'temp' is arg2:
			addr = '@' + str(5 + int(index))

		if 'pointer' is arg2:
			addr = '@' + str(3 + int(index)) + deref


