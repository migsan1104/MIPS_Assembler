.data
.equ BADVAL = 0x10000     # Too large for 16-bit immediate (intentional error)

.text
main:
    addiu r32, r0, 10      # Invalid register (intentional error)
    .macro M1
        addu r1, r1, r1
    # Missing .end_macro (intentional error)
    M1
    jr ra
