.text
main:
    addiu r1, r0, 0x01      # r1 = 1
    beq   r1, r0, done      # branch not taken
    j     skip
mid:
    addiu r2, r0, 0xFF      # skipped
skip:
    bne   r1, r0, done      # branch taken
    addiu r2, r0, 0xEE      # skipped
done:
    jr    ra
