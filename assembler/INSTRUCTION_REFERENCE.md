# ==============================================================================
# RISC-V Assembler - Instruction Set Reference
# ==============================================================================
# Enhanced for Single Cycle Processor with Crypto Extensions
# ==============================================================================

## REGISTER NAMES
# ================
# x0/zero  - Hardwired zero
# x1/ra    - Return address
# x2/sp    - Stack pointer
# x3/gp    - Global pointer
# x4/tp    - Thread pointer
# x5-x7    - t0-t2 (temporaries)
# x8/s0/fp - Saved register / Frame pointer
# x9/s1    - Saved register
# x10-x11  - a0-a1 (function arguments / return values)
# x12-x17  - a2-a7 (function arguments)
# x18-x27  - s2-s11 (saved registers)
# x28-x31  - t3-t6 (temporaries)


## SUPPORTED INSTRUCTIONS
# ========================

# ------------------------------------------------------------------------------
# R-TYPE (Register-Register Operations)
# Syntax: INSTR rd, rs1, rs2
# ------------------------------------------------------------------------------
add   rd, rs1, rs2     # rd = rs1 + rs2
sub   rd, rs1, rs2     # rd = rs1 - rs2
and   rd, rs1, rs2     # rd = rs1 & rs2
or    rd, rs1, rs2     # rd = rs1 | rs2
xor   rd, rs1, rs2     # rd = rs1 ^ rs2
sll   rd, rs1, rs2     # rd = rs1 << rs2[4:0]
srl   rd, rs1, rs2     # rd = rs1 >> rs2[4:0] (logical)
sra   rd, rs1, rs2     # rd = rs1 >> rs2[4:0] (arithmetic)
slt   rd, rs1, rs2     # rd = (rs1 < rs2) ? 1 : 0 (signed)
sltu  rd, rs1, rs2     # rd = (rs1 < rs2) ? 1 : 0 (unsigned)

# ------------------------------------------------------------------------------
# I-TYPE (Immediate Operations)
# Syntax: INSTR rd, rs1, imm
# Immediate range: -2048 to 2047 (12-bit signed)
# ------------------------------------------------------------------------------
addi  rd, rs1, imm     # rd = rs1 + imm
andi  rd, rs1, imm     # rd = rs1 & imm
ori   rd, rs1, imm     # rd = rs1 | imm
xori  rd, rs1, imm     # rd = rs1 ^ imm
slti  rd, rs1, imm     # rd = (rs1 < imm) ? 1 : 0 (signed)
sltiu rd, rs1, imm     # rd = (rs1 < imm) ? 1 : 0 (unsigned)

# Shift Immediate (shamt: 0-31)
slli  rd, rs1, shamt   # rd = rs1 << shamt
srli  rd, rs1, shamt   # rd = rs1 >> shamt (logical)
srai  rd, rs1, shamt   # rd = rs1 >> shamt (arithmetic)

# ------------------------------------------------------------------------------
# LOAD INSTRUCTIONS (I-type)
# Syntax: INSTR rd, offset(rs1)
# ------------------------------------------------------------------------------
lw    rd, offset(rs1)  # rd = mem[rs1 + offset] (32-bit word)
lh    rd, offset(rs1)  # rd = mem[rs1 + offset] (16-bit halfword, sign-ext)
lb    rd, offset(rs1)  # rd = mem[rs1 + offset] (8-bit byte, sign-ext)
lhu   rd, offset(rs1)  # rd = mem[rs1 + offset] (16-bit halfword, zero-ext)
lbu   rd, offset(rs1)  # rd = mem[rs1 + offset] (8-bit byte, zero-ext)

# ------------------------------------------------------------------------------
# STORE INSTRUCTIONS (S-type)
# Syntax: INSTR rs2, offset(rs1)
# ------------------------------------------------------------------------------
sw    rs2, offset(rs1) # mem[rs1 + offset] = rs2 (32-bit word)
sh    rs2, offset(rs1) # mem[rs1 + offset] = rs2[15:0] (16-bit)
sb    rs2, offset(rs1) # mem[rs1 + offset] = rs2[7:0] (8-bit)

# ------------------------------------------------------------------------------
# BRANCH INSTRUCTIONS (B-type)
# Syntax: INSTR rs1, rs2, label
# Offset range: -4096 to 4094 (13-bit signed, 2-byte aligned)
# ------------------------------------------------------------------------------
beq   rs1, rs2, label  # if (rs1 == rs2) goto label
bne   rs1, rs2, label  # if (rs1 != rs2) goto label
blt   rs1, rs2, label  # if (rs1 <  rs2) goto label (signed)
bge   rs1, rs2, label  # if (rs1 >= rs2) goto label (signed)
bltu  rs1, rs2, label  # if (rs1 <  rs2) goto label (unsigned)
bgeu  rs1, rs2, label  # if (rs1 >= rs2) goto label (unsigned)

# ------------------------------------------------------------------------------
# JUMP INSTRUCTIONS
# ------------------------------------------------------------------------------
jal   rd, label        # rd = PC + 4; goto label (J-type)
jalr  rd, offset(rs1)  # rd = PC + 4; goto rs1 + offset (I-type)

# ------------------------------------------------------------------------------
# UPPER IMMEDIATE (U-type)
# Syntax: INSTR rd, imm
# Immediate: 20-bit upper immediate
# ------------------------------------------------------------------------------
lui   rd, imm          # rd = imm << 12
auipc rd, imm          # rd = PC + (imm << 12)

# ------------------------------------------------------------------------------
# SYSTEM INSTRUCTIONS
# ------------------------------------------------------------------------------
halt                   # Stop execution (ECALL with Halt signal)
ecall                  # Environment call (same as halt)

# ------------------------------------------------------------------------------
# CUSTOM CRYPTO EXTENSIONS (opcode = 0001011)
# ------------------------------------------------------------------------------
rng   rd               # rd = random number (XOR-shift LFSR)
rotl  rd, rs1, rs2     # rd = rs1 rotated left by rs2[4:0] bits
rotr  rd, rs1, rs2     # rd = rs1 rotated right by rs2[4:0] bits


## PSEUDO-INSTRUCTIONS
# ====================
nop                    # No operation (addi x0, x0, 0)
li    rd, imm          # Load immediate (addi rd, x0, imm)
mv    rd, rs           # Move register (addi rd, rs, 0)
j     label            # Jump (jal x0, label)


## SYNTAX NOTES
# ==============
# - Labels end with colon: loop:
# - Comments start with # or ;
# - Registers: x0-x31 or ABI names (zero, ra, sp, etc.)
# - Immediates: decimal (100), hex (0x64), binary (0b1100100)
# - Memory operands: offset(base) e.g., 100(x0), -4(sp)


## EXAMPLES
# ==========

# Example 1: Simple addition
        addi x1, x0, 10       # x1 = 10
        addi x2, x0, 20       # x2 = 20
        add  x3, x1, x2       # x3 = 30

# Example 2: Loop
        addi x1, x0, 5        # counter = 5
loop:
        addi x1, x1, -1       # counter--
        bne  x1, x0, loop     # while counter != 0

# Example 3: Memory access
        addi x1, x0, 42       # x1 = 42
        sw   x1, 100(x0)      # mem[100] = 42
        lw   x2, 100(x0)      # x2 = mem[100]

# Example 4: Function call
        jal  ra, function     # call function
        # ... continue here after return
function:
        addi a0, x0, 1        # return value = 1
        jalr x0, 0(ra)        # return

# Example 5: Crypto operations
        rng  x10              # x10 = random
        addi x11, x0, 4       # x11 = 4 (rotate amount)
        rotl x12, x10, x11    # x12 = x10 rotated left 4
        rotr x13, x10, x11    # x13 = x10 rotated right 4
