.data
.equ SIZE = 4

array: .word 0x11223344, 0x55667788
start_byte: .byte 0xAB, 0xCD

.space 2
.org 16
extra: .byte 0xEF

.text
main:
    addiu r1, r0, SIZE     # r1 = SIZE
    addiu r2, r0, 0x02     # r2 = 2
    beq r1, r2, skip
    lw r3, array(r0)
    j exit

skip:
    addiu r3, r0, 0x99

exit:
    jr ra
