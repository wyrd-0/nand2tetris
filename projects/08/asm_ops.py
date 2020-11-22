push = ('//PUSH -- Expects D to contain value to push\n'
        '@SP\n'
        'M=M+1\n'
        'A=M-1\n'
        'M=D\n')
pop = ('//POP -- Stores output in addr at R13\n'
       '@SP\n'
       'AM=M-1    //decrement TOS, set RAM addr to old TOS\n'
       'D=M\n'
       '@R13\n'
       'A=M\n'
       'M=D\n')

add = ('//ADD\n'
       '@SP\n'
       'AM=M-1   //M,D==new top of stack\n'
       'D=M       //D==value at old TOS\n'
       'A=A-1     //A==new TOS\n'
       'M=D+M     //value at new TOS += value at old TOS\n')

sub = ('//SUB\n'
       '@SP\n'
       'AM=M-1\n'
       'D=M\n'
       'A=A-1\n'
       'M=M-D\n')

neg = ('//NEG -- Arithmetically negates value at TOS\n'
       '@SP\n'
       'A=M-1\n'
       'M=-M\n')

eq = ('(EQUAL)\n'
      '@SP\n'
      'AM=M-1\n'
      'D=M\n'
      'A=A-1\n'
      'D=M-D\n'
      '@EQ\n'
      'D;JEQ\n'
      '@SP\n'
      'A=M-1\n'
      'M=0\n'
      '@EQEX\n'
      '0;JMP\n'
      '(EQ)\n'
      '@SP\n'
      'A=M-1\n'
      'M=-1\n'
      '(EQEX)\n'
      '@R13\n'
      'A=M\n'
      '0;JMP\n')

gt = ('(GREATER)\n'
      '@SP\n'
      'AM=M-1\n'
      'D=M\n'
      'A=A-1\n'
      'D=M-D\n'
      '@GT\n'
      'D;JGT\n'
      '@SP\n'
      'A=M-1\n'
      'M=0\n'
      '@GTEX\n'
      '0;JMP\n'
      '(GT)\n'
      '@SP\n'
      'A=M-1\n'
      'M=-1\n'
      '(GTEX)\n'
      '@R13\n'
      'A=M\n'
      '0;JMP\n')

lt = ('(LESS)\n'
      '@SP\n'
      'AM=M-1\n'
      'D=M\n'
      'A=A-1\n'
      'D=M-D\n'
      '@LT\n'
      'D;JLT\n'
      '@SP\n'
      'A=M-1\n'
      'M=0\n'
      '@LTEX\n'
      '0;JMP\n'
      '(LT)\n'
      '@SP\n'
      'A=M-1\n'
      'M=-1\n'
      '(LTEX)\n'
      '@R13\n'
      'A=M\n'
      '0;JMP\n')

conj = ('//AND -- Expects 1 or 0 as operands\n'
        '@SP\n'
        'AM=M-1\n'
        'D=M\n'
        'A=A-1\n'
        'M=D&M\n')

disj = ('//OR -- Expects 1 or 0 as operands\n'
        '@SP\n'
        'AM=M-1\n'
        'D=M\n'
        'A=A-1\n'
        'M=D|M\n')

boolnot = ('//NOT -- Expects 1 or 0 at TOS\n'
           '@SP\n'
           'A=M-1\n'
           'M=!M\n')

save_frame = ('//A contains return address\n'
              'D=A //Saves entire frame of caller\n'
              '@SP\n'
              'M=M+1\n'
              'A=M-1\n'
              'M=D\n'
              '@LCL\n'
              'D=M\n'
              '@SP\n'
              'M=M+1\n'
              'A=M-1\n'
              'M=D\n'
              '@ARG\n'
              'D=M\n'
              '@SP\n'
              'M=M+1\n'
              'A=M-1\n'
              'M=D\n'
              '@THIS\n'
              'D=M\n'
              '@SP\n'
              'M=M+1\n'
              'A=M-1\n'
              'M=D\n'
              '@THAT\n'
              'D=M\n'
              '@SP\n'
              'M=M+1\n'
              'A=M-1\n'
              'M=D\n')

arg_lcl = ('//Sets ARG and LCL for callee\n'
           'D=A\n'
           '@5\n'
           'D=D+A\n'
           '@SP\n'
           'D=M-D\n'
           '@ARG\n'
           'M=D\n'
           '@SP\n'
           'D=M\n'
           '@LCL\n'
           'M=D\n')

restore_caller = ('//Restores frame of caller\n'
                  '@5\n'
                  'D=A\n'
                  '@LCL\n'
                  'D=M-D\n'
                  'A=D\n'
                  'D=M\n'
                  '@R13\n'
                  'M=D // R13 holds return address\n'
                  '@SP\n'
                  'AM=M-1\n'
                  'D=M\n'
                  '@ARG\n'
                  'A=M\n'
                  'M=D\n'
                  'D=A\n'
                  '@SP\n'
                  'M=D+1\n'
                  '@LCL\n'
                  'A=M-1\n'
                  'D=M\n'
                  '@THAT\n'
                  'M=D\n'
                  '@2\n'
                  'D=A\n'
                  '@LCL\n'
                  'A=M-D\n'
                  'D=M\n'
                  '@THIS\n'
                  'M=D\n'
                  '@3\n'
                  'D=A\n'
                  '@LCL\n'
                  'A=M-D\n'
                  'D=M\n'
                  '@ARG\n'
                  'M=D\n'
                  '@4\n'
                  'D=A\n'
                  '@LCL\n'
                  'A=M-D\n'
                  'D=M\n'
                  '@LCL\n'
                  "M=D\n"
                  '@R13\n'
                  'A=M\n'
                  '0;JMP\n')
