.text
main:
    addiu r1, r0, 10        # r1 = 10
    addiu r2, r0, 5         # r2 = 5
    addu  r3, r1, r2        # r3 = r1 + r2
    subu  r4, r1, r2        # r4 = r1 - r2
    and   r5, r1, r2        # r5 = r1 & r2
    or    r6, r1, r2        # r6 = r1 | r2
    xor   r7, r1, r2        # r7 = r1 ^ r2
    jr    ra                # return
