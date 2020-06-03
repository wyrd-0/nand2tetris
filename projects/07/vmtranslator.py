#!/usr/bin/python3

import sys

insns = '''(PUSH)	//Expects ARG to contain value to push
@ARG
D=M
@SP
M=M+1
A=M
M=D
(POP)
@SP
A=M
D=M		//D==value at addr in SP
@ARG
A=M		//deref. addr in ARG
M=D
'''

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
	deref = '\nD=M'+'\n@'+index+'\nA=D+A'
	dec_stack = '@SP\nD=M\nM=M-1\nA=D\nD=M\nA=A-1'
	inc_stack = '@SP\nD=M\nM=M+1\nA=D\nD=M\nA=A-1'

	if 'add' is arg1:
		cmd = '@SP\nD=M\nM=M-1\nA=D\nD=M\nA=A-1\nM=D+M'

	if 'sub' is arg1:
		cmd = '@SP\nD=M\nM=M-1\nA=D\nD=M\nA=A-1\nM=M-D'

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


