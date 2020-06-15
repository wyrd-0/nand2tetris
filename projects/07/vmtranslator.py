#!/usr/bin/python3

import asm_ops
import sys
import re

VMC = []
filename = sys.argv[1]
f = open(filename)
vmc = f.readlines()
STATIC = filename.split('.vm')[0]

#remove comments
CMNT='//'
for i in range(len(vmc)):
  l = vmc[i]
  l = l.split(CMNT, 1)[0]
  vmc[i] = l

#remove empty lines
vmc = list(filter(lambda x:not re.match(r'^\s*$', x), vmc))


C_ARITH = ['add','sub','neg','eq','gt','lt','and','or','not']
ARG_TABLE = {'local':'@LCL','argument':'@ARG','this':'@THIS','that':'@THAT'}
C_PUSH = 'push'
C_POP = 'pop'
deref = '''
A=M
D=M
'''

links=[]
i=0

for l in vmc:
	args = l.split()
	arg1 = args[0]
	cmd = ''
	addr = ''
	c = 'COMP'+str(i)
	ret_head = '@'+c +'\nD=A\n@R13\nM=D\n'
	ret_tail = '('+c+')\n'

	if 'add' == arg1:
		cmd = asm_ops.add

	if 'sub' == arg1:
		cmd = asm_ops.sub 

	if 'neg' == arg1:
		cmd = asm_ops.neg

	if 'and' == arg1:
		cmd = asm_ops.conj

	if 'or' == arg1:
		cmd = asm_ops.disj

	if 'not' == arg1:
		cmd = asm_ops.boolnot

	if 'eq' == arg1:
		cmd = ret_head + '@EQUAL\n0;JMP\n' + ret_tail
		i+=1
		if not asm_ops.eq in links:
			links.append(asm_ops.eq)

	if 'gt' == arg1:
		cmd = ret_head + '@GREATER\n0;JMP\n' + ret_tail
		i+=1
		if not asm_ops.gt in links:
			links.append(asm_ops.gt)

	if 'lt' == arg1:
		cmd = ret_head + '@LESS\n0;JMP\n' + ret_tail
		i+=1
		if not asm_ops.lt in links:
			links.append(asm_ops.lt)

	if arg1 not in C_ARITH:
		arg2 = args[1]
		index = args[2]
		dval = '@'+str(index)+'\nD=A\n'
		deref = '\nA=D+M\n'

		if arg2 in ARG_TABLE:
			addr = dval + ARG_TABLE[arg2] + deref

		if 'static' == arg2:
			addr = '@' + STATIC + '.' + index+'\n'

		if 'temp' == arg2:
			addr = '@R' + str(5 + int(index))+'\n'

		if 'pointer' == arg2:
			addr = '@' + str(3 + int(index))+'\n'

		if C_PUSH == arg1:
			if 'constant' == arg2:
				cmd = '@'+index+'\nD=A\n' + asm_ops.push
			else:
				cmd = addr + 'D=M\n' + asm_ops.push

		if C_POP == arg1:
			cmd = addr + 'D=A\n@R13\nM=D' + asm_ops.pop

	VMC.append(cmd)

end = '(END)\n@END\n0;JMP\n'

VMC.append(end)

for m in links:
	VMC.append(m)

#create and write lines to .asm file
asm_file = STATIC+'.asm'
asm = open(asm_file,'w')
asm.writelines(VMC)
asm.close()
