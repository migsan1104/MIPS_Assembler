.data
.byte 0x3F, 0x3F           # 00 00 3F 3F
.byte 0x3F, 0x3F, 0x3F, 0x3F, 0x1B  # 3F 3F 3F 3F, then 00 00 00 1B
.space 1                   # pad 1 word = 00 00 00 00
.org 0x10
.byte 0xAA, 0xBB, 0xCC     # pad left = 00 AA BB CC

.text
main:
    jr ra