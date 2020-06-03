// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

// Put your code here.
	@2
	M=0		//R2 (sum)=0
	@0
	D=M		//D=R0
	@i
	M=D		//i=R0
(LOOP)
	@1
	D=D-A	//D=i-1
	@END
	D;JLT	//End if i<1
	@i
	M=D		//i=i-1
	@1
	D=M		//D=R1
	@2
	M=D+M	//sum=sum+R1
	@i
	D=M		//D=i
	@LOOP
	0;JMP	//Goto LOOP
(END)
	@END
	0;JMP
