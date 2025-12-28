# ==============================================================================
# RISC-V Test Program: Crypto Demo
# ==============================================================================
# This program demonstrates all implemented features:
#   - Basic ALU operations
#   - Branching (BNE)
#   - Jumping (JAL)
#   - Custom Crypto (RNG, ROTL, ROTR)
#   - Memory operations
#   - HALT instruction
# ==============================================================================

# Initialize registers
        addi x1, x0, 5          # x1 = 5 (loop limit)
        addi x2, x0, 0          # x2 = 0 (counter)
        addi x3, x0, 1          # x3 = 1 (increment value)

# Loop: count from 0 to 5
loop:
        add  x2, x2, x3         # x2 = x2 + 1
        bne  x1, x2, loop       # if x1 != x2, goto loop

# After loop: x2 = 5
        add  x10, x2, x2        # x10 = 10 (verify loop worked)

# ==============================================================================
# Crypto Extension Demo
# ==============================================================================

        rng  x11                # x11 = random number
        rotl x12, x11, x3       # x12 = rotate left x11 by 1
        rotr x13, x11, x3       # x13 = rotate right x11 by 1
        xor  x14, x12, x13      # x14 = crypto mixing

# Store crypto results to memory
        sw   x11, 0(x0)         # mem[0] = RNG result
        sw   x12, 4(x0)         # mem[4] = ROTL result
        sw   x13, 8(x0)         # mem[8] = ROTR result
        sw   x14, 12(x0)        # mem[12] = XOR result

# Store final test value
        addi x10, x0, 25        # x10 = 25
        sw   x10, 100(x0)       # mem[100] = 25 (test verification)

# End program
        halt                    # Stop execution
