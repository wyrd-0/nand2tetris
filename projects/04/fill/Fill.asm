// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.
// Initialize scrn to start of screen
(FILL)
    @SCREEN
    D=A
    @scrn
    M=D
(FLOOP)
// Set pixels to black
    @0
    D=!A
    @scrn
    A=M
    M=D
// Increment scrn and repeat loop if it's not end of screen or no key press
    @scrn
	MD=M+1
	@24576
	D=D-A
    @FLOOP
    D;JLT
(NOKEY)
	@KBD
	D=M
	@NOKEY
	D;JNE
	@CLEAR
	0;JMP

//Init scrn
(CLEAR)
    @SCREEN
    D=A
    @scrn
    M=D
(CLOOP)
// Set pixels to black
    @0
    D=A
    @scrn
    A=M
    M=D
// Increment scrn and repeat loop if it's not end of screen or no key press
    @scrn
	MD=M+1
	@24576
	D=D-A
    @CLOOP
    D;JLT
(KEY)
	@KBD
	D=M
	@KEY
	D;JEQ
	@FILL
	0;JMP
