.data
.equ CONST = 0x0042

.text
.macro LOAD_CONST
    addiu r5, r0, CONST
.end_macro

main:
    LOAD_CONST
    jr ra
