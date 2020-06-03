#!/usr/bin/python3
'''
Parser for Hack machine assembler
Because Python allows SymbolTable functions to be one-liners, the table and all
required functionality will be included in this script
'''

import sys
import re

#init address counter, comp table and symbol table, output list; define comment string
HACK=[]
RAM_ADDR=16
CMNT= '//'

COMP_TABLE={'0':'0101010','1':'0111111','-1':'0111010','D':'0001100','A':'0110000','M':'1110000','!D':'0001101','!A':'0110001','!M':'1110001','-D':'0001111','-A':'0110011','-M':'1110011','D+1':'0011111','1+D':'0001110','A+1':'0110111','M+1':'1110111','1+A':'0110111','1+M':'1110111','D-1':'0001110','A-1':'0110010','M-1':'1110010','D+A':'0000010','A+D':'0000010','D+M':'1000010','M+D':'1000010','D-A':'0010011','D-M':'1010011','A-D':'0000111','M-D':'1000111','D&A':'0000000','A&D':'0000000','D&M':'1000000','M&D':'1000000','D|A':'0010101','A|D':'0010101','D|M':'1010101','M|D':'1010101'}

SYM_TABLE=dict(SP=0,LCL=1,ARG=2,THIS=3,THAT=4,SCREEN=16384,KBD=24576)
for i in range(16):
	SYM_TABLE['R'+str(i)] = i


#create list of lines in input file
filename = sys.argv[1]
f = open(filename)
asm = f.readlines()

#remove whitespace and comments
for i in range(len(asm)):
	l = asm[i]
	l = l.split(CMNT, 1)[0] 
	l = re.sub(r'\s+', '', l, flags=re.UNICODE)
	asm[i] = l

#remove empty lines
asm = list(filter(lambda x:not re.match(r'^\s*$', x), asm))

###FIRST PASS: load label symbols into SYM_TABLE and remove from asm
rl = 0
lena = len(asm)
for i in range(lena):
	cmd = asm[i]
	if re.match(r'^[(](.*[)])$', cmd):
		SYM_TABLE[cmd[1:-1]] = i - rl
		rl += 1

asm = list(filter(lambda x:not re.match(r'^[(](.*[)])$', x), asm))
###SECOND PASS: parses instructions into machine code
for i in range(len(asm)):
	cmd = asm[i]

##commandType section##

#A_COMMAND & L_COMMAND section#
	if '@' is cmd[0]:
		label = cmd[1:]
		if label.isnumeric() :
			addr = '{0:015b}'.format(int(label))
		elif label in SYM_TABLE :
			addr = '{0:015b}'.format(int(SYM_TABLE[label]))
		else:
			addr = '{0:015b}'.format(RAM_ADDR)
			SYM_TABLE[label] = RAM_ADDR
			RAM_ADDR += 1

		HACK.append('0'+addr+'\n')

#C_COMMAND SECTION#
	else:
		comp = ''
		dest = ''
		jump = ''
		c = ''
		d = ''
		j = ''
		DST = '=' in cmd
		JMP = ';' in cmd

#divide mnemonic parts#
		if DST:
			d = cmd.split('=')[0]
			c = cmd.split('=')[1]
		elif JMP:
			j = cmd.split(';')[1]
			c = cmd.split(';')[0]
		else:
			c = cmd

#comp():

		comp = COMP_TABLE[c]

#define dest portion of C command
		if DST:
			d1 = 'A' in d
			d2 = 'D' in d
			d3 = 'M' in d
			dest = str(int(d1)) + str(int(d2)) + str(int(d3))
		else:
			dest = '000'

#define jump portion of C command
		if not JMP:
			jump = '000'
		elif 'JMP' == j:
			jump = '111'
		else:
			j1 = 'L' in j or 'NE' in j
			j2 = 'E' in j and not 'NE' in j
			j3 = 'G' in j or 'NE' in j
			jump = str(int(j1)) + str(int(j2)) + str(int(j3))

		HACK.append('111'+comp+dest+jump+'\n')

f.close()

#create and write lines to .hack file
hack_file = filename.split('.asm')[0] + '.hack'
hack = open(hack_file,'w')
hack.writelines(HACK)
hack.close()
