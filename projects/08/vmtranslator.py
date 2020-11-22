#!/usr/bin/python3

import parse_code
import sys
import os

START = ('//INIT STACK\n'
         '@256\n'
         'D=A\n'
         '@SP\n'
         'M=D\n'
         '//INIT LOCAL\n'
         '@300\n'
         'D=A\n'
         '@LCL\n'
         'M=D\n'
         '//INIT ARG\n'
         '@400\n'
         'D=A\n'
         '@ARG\n'
         'M=D\n'
         '//INIT THIS\n'
         '@3000\n'
         'D=A\n'
         '@THIS\n'
         'M=D\n'
         '//INIT THAT\n'
         '@3010\n'
         'D=A\n'
         '@THAT\n'
         'M=D\n')

end = '(END)\n@END\n0;JMP\n'
filename = sys.argv[1]
file = ''
init_ram = ''
bootstrap = ''

ASMBLY = []
ASMCODE = []
VMCODE = []
LINK_TABLE = []

if os.path.isdir(filename):
    init_ram = START
    with os.scandir(filename) as contents:
        for entry in contents:
            if '.vm' in entry.name:
                file = filename.split('/')[0] + '/' + entry.name
                VMCODE = VMCODE + open(file).readlines()
    FILETAG = ''
    bootstrap = 'call Sys.init 0\n'
    VMCODE.insert(0, bootstrap)
#    print(VMCODE)
else:
    VMCODE = open(filename).readlines()
    FILETAG = filename.split('.vm')[0]

ASMBLY = parse_code.parse_vm_code(VMCODE, LINK_TABLE, FILETAG)
ASMCODE = list(init_ram) + ASMBLY[0]
LINK_TABLE = ASMBLY[1]

ASMCODE.append(end)

for m in LINK_TABLE:
    ASMCODE.append(m)

# create .asm file and write lines

if os.path.isdir(filename):
    pathway = filename.split('/')[0]
    asm_file = pathway + '/' + pathway + '.asm'
else:
    asm_file = FILETAG + '.asm'
asm = open(asm_file, 'w')
asm.writelines(ASMCODE)
asm.close()
