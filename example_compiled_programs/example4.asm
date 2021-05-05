;PgmEx1Nasm32Linux.asm
;$ nasm -f elf PgmEx1Nasm32Linux.asm
; elf means extended linking format
; Default to <pgm name>.o
;$ gcc -o PgmEx1Nasm32Linux PgmEx1Nasm32Linux.o
;$ ./PgmEx1Nasm32Linux
; Link defaults to <pgm name>.exe or a.out
sys_exit	equ	1
sys_read	equ	3
sys_write	equ	4
stdin		equ	0 ; default keyboard | I/O redirection
stdout		equ	1 ; default terminal screen
stderr		equ	3


section .data	;used to declare constants	
	userMsg		db 'Enter an integer(less than 32,765): '
	lenUserMsg	equ	$-userMsg
	displayMsg	db	'You entered: '
	lenDisplayMsg	equ	$-displayMsg
	newline		db	0xA 	; 0xA 0xD is ASCII <LF><CR>

	Ten        DW      10  ;Used converting to base ten.
	;printTempchar	 db	'Tempchar = : '
	;lenprintTempchar	equ 	$-printTempchar


	Result          db 'Ans = '
	ResultValue		 db	'aaaaa'
	db	 0xA		;return
	ResultEnd       equ 	$-Result   
	; $=> here - address Result = length to print

	num			times 6	 db 'ABCDEF' ;cheat NASM
	numEnd		equ	$-num
	lit9	DW	9
	lit10	DW	10
	lit1	DW	1
	;.bss RESB 1 – byte, RESW 1 – 2 bytes
    ; RESD 1 – 4 bytes, RESQ 1 - 8 bytes 
	; W word, D double, Q quad
; Start of user variable area    ----------

section	.bss	;used to declare uninitialized variables

	TempChar        RESB    1
	;1 byte temp space	
	; for use by GetNextChar
	testchar        RESB    1	
	;Temporary storage GetAnInteger.	
	ReadInt         RESW    1 
	;2 bytes
	;Used in converting to base ten.
	tempint         RESW	1              
	negflag         RESB    1              
	;P=positive, N=negative	
	a	RESW	1
	b	RESW	1
	sum	RESW	1
	T1		RESW	1
	T2		RESW	1
	T3		RESW	1
	T4		RESW	1
	T5		RESW	1
	T6		RESW	1
	T7		RESW	1
	T8		RESW	1
	T9		RESW	1
	T10		RESW	1


	;Start program code.
section .text	
	global main 
;start address (main)for elf linker (extended linking format)
main:	nop
	; prompt user for positive number	
Again:	call PrintString
	call GetAnInteger
	mov ax,[ReadInt]
	mov [a],ax
	call PrintString
	call GetAnInteger
	mov ax,[ReadInt]
	mov [b],ax
	mov ax,[a]
	add ax,[b]
	mov [T1], ax
	mov ax,[T1]
	mov [sum],ax
	mov ax,[sum]
	cmp ax, [lit9]
	JLE L1
	mov ax,[a]
	mul [lit10]
	mov [T1], ax
	mov ax,[T1]
	mov [a],ax
	mov ax,[b]
	mul [lit10]
	mov [T2], ax
	mov ax,[T2]
	mov [b],ax
	mov ax,[a]
	add ax,[b]
	mov [T3], ax
	mov ax,[T3]
	mov [sum],ax
	JMP L2
L1:	nop
	mov ax,[a]
	mul [lit1]
	mov [T4], ax
	mov ax,[T4]
	mov [a],ax
	mov ax,[b]
	mul [lit1]
	mov [T5], ax
	mov ax,[T5]
	mov [b],ax
	mov ax,[a]
	add ax,[b]
	mov [T6], ax
	mov ax,[T6]
	mov [sum],ax
L2:	nop
	mov ax,[sum]
	call ConvertIntegerToString
	mov eax, 4
	mov ebx, 1
	mov ecx, Result
	mov edx, ResultEnd
	int 80h
; exit code
fini:
	mov eax,sys_exit ;terminate, sys_exit = 1
	xor ebx,ebx	      ;zero in ebx indicates success
	int 80h

;	ENDP main

;
;    Subroutine to print a string on the display
;
; Input:
;       DS:BX = pointer to the string to print
;
; Output: None
;
; Registers destroyed: none
;
;PrintString     PROC
PrintString:
	push    ax              ;Save registers;
	push    dx
; subpgm:
	; prompt user	
	mov eax, 4		;Linux print device register
; conventions
	mov ebx, 1		; print default output device
	mov ecx, userMsg	; pointer to string
	mov edx, lenUserMsg	
	int	80h		; interrupt 80 hex, call kernel
	pop     dx              ;Restore registers.
	pop     ax
	ret
;PrintString     ENDP

;%NEWPAGE

;

; Subroutine to get an integer 
;(character string) from the keyboard buffer
; and convert it to a 16 bit binary number.
;
; Input: none
;
; Output: The integer is returned in the AX
;  register as well as the global
;         variable ReadInt .
;
; Registers Destroyed: AX, BX, CX, DX, SI
;
; Globals Destroyed: ReadInt, TempChar, tempint, negflag
;
;GetAnInteger    PROC

GetAnInteger:	;Get an integer as a string
	;get response
	mov eax,3	;read
	mov ebx,2	;device
	mov ecx, num	;buffer address
	mov edx,6	;max characters
	int 0x80	;gets an integer, reads as string

	;print number    ;works
	mov edx,eax 	; eax contains the number of 
; character read including <lf>
	mov eax, 4
	mov ebx, 1
	mov ecx, num
	int 80h

ConvertStringToInteger:
	mov ax,0	;hold integer
	mov [ReadInt],ax ;initialize 16 bit number to zero
	mov ecx,num	;pt - 1st or next digit of number as a string 
				;terminated by <lf>.
	mov bx,0	
	mov bl, byte [ecx] ;contains first or next digit
Next:	sub bl,'0'	;convert character to number
	mov ax,[ReadInt]
	mov dx,10
	mul dx		;eax = eax * 10
	add ax,bx
	mov [ReadInt], ax

	mov bx,0
	add ecx,1 	;pt = pt + 1
	mov bl, byte[ecx]

	cmp bl,0xA	;is it a <lf>
	jne Next	; get next digit   
	ret
;	ENDP GetAnInteger



;%NEWPAGE
;
; Subroutine to convert a 16 bit integer to a text string
;
; input:
;       AX = number to convert
;       DS:BX = pointer to end of string to store text
;       CX = number of digits to convert
;
; output: none
;
; Registers destroyed: AX, BX, CX, DX, SI
; Globals destroyed negflag 
;
;ConvertIntegerToString PROC

ConvertIntegerToString:
	mov ebx, ResultValue + 4   ;Store the integer as a
; five digit char string at Result for printing

ConvertLoop:
	sub dx,dx  ; repeatedly divide dx:ax by 10
; to obtain last digit of number
	mov cx,10  ; as the remainder in the DX
; register.  Quotient in AX.
	div cx
	add dl,'0' ; Add '0' to dl to 
;convert from binary to character.
	mov [ebx], dl
	dec ebx
	cmp ebx,ResultValue
	jge ConvertLoop

	ret

;ConvertIntegerToString  ENDP
