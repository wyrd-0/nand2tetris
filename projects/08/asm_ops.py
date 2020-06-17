push = '''//PUSH -- Expects D to contain value to push
@SP
M=M+1
A=M-1
M=D
'''
pop = '''//POP -- Stores output in addr at R13
@SP
AM=M-1    //decrement TOS, set RAM addr to old TOS
D=M
@R13
A=M
M=D
'''

add = '''//ADD
@SP
AM=M-1   //M,D==new top of stack
D=M       //D==value at old TOS
A=A-1     //A==new TOS
M=D+M     //value at new TOS += value at old TOS
'''

sub = '''//SUB
@SP
AM=M-1
D=M
A=A-1
M=M-D
'''

neg = '''//NEG -- Arithmetically negates value at TOS
@SP
A=M-1
M=-M
'''

eq = '''(EQUAL)
@SP
AM=M-1
D=M
A=A-1
D=M-D
@EQ
D;JEQ
@SP
A=M-1
M=0
@EQEX
0;JMP
(EQ)
@SP
A=M-1
M=-1
(EQEX)
@R13
A=M
0;JMP
'''

gt = '''(GREATER)
@SP
AM=M-1
D=M
A=A-1
D=M-D
@GT
D;JGT
@SP
A=M-1
M=0
@GTEX
0;JMP
(GT)
@SP
A=M-1
M=-1
(GTEX)
@R13
A=M
0;JMP
'''

lt = '''(LESS)
@SP
AM=M-1
D=M
A=A-1
D=M-D
@LT
D;JLT
@SP
A=M-1
M=0
@LTEX
0;JMP
(LT)
@SP
A=M-1
M=-1
(LTEX)
@R13
A=M
0;JMP
'''

conj = '''//AND -- Expects 1 or 0 as operands
@SP
AM=M-1
D=M
A=A-1
M=D&M
'''

disj = '''//OR -- Expects 1 or 0 as operands
@SP
AM=M-1
D=M
A=A-1
M=D|M
'''

boolnot = '''//NOT -- Expects 1 or 0 at TOS
@SP
A=M-1
M=!M
'''

save_frame = '''//A contains return address
D=A //Saves entire frame of caller
@SP
M=M+1
A=M-1
M=D
@LCL
D=M
@SP
M=M+1
A=M-1
M=D
@ARG
D=M
@SP
M=M+1
A=M-1
M=D
@THIS
D=M
@SP
M=M+1
A=M-1
M=D
@THAT
D=M
@SP
M=M+1
A=M-1
M=D
'''

arg_lcl = '''
D=A	//Sets ARG for
@5
D=D+A
@SP
D=M-D
@ARG
M=D
@SP
D=M
@LCL
M=D
'''
