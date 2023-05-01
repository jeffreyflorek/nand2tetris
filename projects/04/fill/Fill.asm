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

// screenmax = SCREEN + 1024
@8192
D=A
@SCREEN
D=D+A
@screenmax
M=D
(WHITE)
    // n = SCREEN
    @SCREEN
    D=A
    @n
    M=D
(WLOOP)
    // if(n > screenmax) goto WHITE
    @n
    D=M
    @screenmax
    D=D-M
    @WHITE
    D;JGT
    // if(key != 0) goto BLACK
    @KBD
    D=M
    @BLACK
    D;JNE
    // *(SCREEN + n) = 0
    @SCREEN
    D=M
    @n
    A=D+M
    M=0
    // n = n + 1
    @n
    M=M+1
    // goto WLOOP
    @WLOOP
    0;JMP
(BLACK)
// n = SCREEN
    @SCREEN
    D=A
    @n
    M=D
(BLOOP)
    // if(n > screenmax) goto BLACK
    @n
    D=M
    @screenmax
    D=D-M
    @BLACK
    D;JGT
    // if(key = 0) goto WHITE
    @KBD
    D=M
    @WHITE
    D;JEQ
    // *(SCREEN + n) = -1
    @SCREEN
    D=M
    @n
    A=D+M
    M=-1
    // n = n + 1
    @n
    M=M+1
    // goto BLOOP
    @BLOOP
    0;JMP
