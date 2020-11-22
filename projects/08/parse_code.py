#!/usr/bin/python3

import asm_ops
import re

C_ARITH = ['add', 'sub', 'neg', 'eq', 'gt', 'lt', 'and', 'or', 'not']
C_BRANCH = ['label', 'goto', 'if-goto']
C_FUNCTION = ['function', 'call', 'return']
ARG_TABLE = {'local': '@LCL', 'argument': '@ARG', 'this': '@THIS', 'that': '@THAT'}
FUNC_TABLE = {}
C_PUSH = 'push'
C_POP = 'pop'
deref = '''
A=M
D=M
'''


def parse_vm_code(vmc=None, link_tbl=None, file_tag=''):
    if link_tbl is None:
        link_tbl = []
    if vmc is None:
        vmc = []
    if file_tag:
        file_tag = file_tag + '.'
    vmc_output = []
    function_name = ''

    # remove comments

    comment = '//'
    for i in range(len(vmc)):
        line = vmc[i]
        line = line.split(comment, 1)[0]
        vmc[i] = line

    # remove empty lines

    vmc = list(filter(lambda x: not re.match(r'^\s*$', x), vmc))

    links = link_tbl
    i = 0

    for line_index in range(len(vmc)):
        line = vmc[line_index]
        args = line.split()
        arg1 = args[0]
        cmd = ''
        addr = ''
        c = 'COMP' + str(i)
        ret_head = '@' + c + '\nD=A\n@R13\nM=D\n'
        ret_tail = '(' + c + ')\n'

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
            i += 1
            if asm_ops.eq not in links:
                links.append(asm_ops.eq)

        if 'gt' == arg1:
            cmd = ret_head + '@GREATER\n0;JMP\n' + ret_tail
            i += 1
            if asm_ops.gt not in links:
                links.append(asm_ops.gt)

        if 'lt' == arg1:
            cmd = ret_head + '@LESS\n0;JMP\n' + ret_tail
            i += 1
            if asm_ops.lt not in links:
                links.append(asm_ops.lt)

        if arg1 == C_PUSH or arg1 == C_POP:
            arg2 = args[1]
            index = args[2]
            dval = '@' + str(index) + '\nD=A\n'

            if arg2 in ARG_TABLE:
                addr = dval + ARG_TABLE[arg2] + '\nA=D+M\n'
            if 'static' == arg2:
                addr = '@' + function_name.split('.')[0] + '.static.' + index + '\n'
            if 'temp' == arg2:
                addr = '@R' + str(5 + int(index)) + '\n'
            if 'pointer' == arg2:
                addr = '@' + str(3 + int(index)) + '\n'
            if C_PUSH == arg1:
                if 'constant' == arg2:
                    cmd = '@' + index + '\nD=A\n' + asm_ops.push
                else:
                    cmd = addr + 'D=M\n' + asm_ops.push
            if C_POP == arg1:
                cmd = addr + 'D=A\n@R13\nM=D' + asm_ops.pop

        if arg1 in C_BRANCH:
            label = args[1]
            if function_name:
                label = file_tag + function_name + '$' + label
            if arg1 == 'label':
                cmd = '(' + label + ')\n'
            if arg1 == 'goto':
                cmd = '@' + label + '\n0;JMP\n'
            if arg1 == 'if-goto':
                cmd = '@SP\nAM=M-1\nD=M\n@' + label + '\nD;JNE\n'

        if arg1 in C_FUNCTION:
            if arg1 == 'function':
                function_name = args[1]
                n_args = args[2]

                init_pointer = '@' + function_name + '.init\n'
                init_label = '(' + function_name + '.init)\n'
                start_pointer = '@' + function_name + '.start\n'
                start_label = '(' + function_name + '.start)\n'

                cmd = init_label + '@' + n_args + '\nD=A\n' + start_pointer + 'D;JEQ\n@SP\nM=M+1\nA=M-1\nM=0\nD=D-1\n'
                cmd = cmd + init_pointer + '0;JMP\n' + start_label

            if arg1 == 'call':
                fxn = args[1]
                n_args = args[2]
                if fxn not in FUNC_TABLE:
                    FUNC_TABLE[fxn] = 0
                else:
                    FUNC_TABLE[fxn] += 1

                fxn_ret = fxn + '$ret.' + str(FUNC_TABLE[fxn])
                cmd = '@' + fxn_ret + asm_ops.save_frame + '@' + n_args
                cmd = cmd + asm_ops.arg_lcl + '@' + fxn + '.init' + '\n0;JMP\n' + '(' + fxn_ret + ')\n'

            if arg1 == 'return':
                if vmc[line_index+1].startswith('function'):
                    function_name = ''
                cmd = asm_ops.restore_caller

        vmc_output.append(cmd)
    return [vmc_output, links]
