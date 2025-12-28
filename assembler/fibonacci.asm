# ==============================================================================
# RISC-V Test Program: Fibonacci Sequence
# ==============================================================================
# Calculates the first N Fibonacci numbers and stores them in memory
# ==============================================================================

# Configuration
        addi x1, x0, 10       # N = 10 (calculate 10 Fibonacci numbers)

# Initialize first two Fibonacci numbers
        addi x2, x0, 0        # x2 = F(0) = 0
        addi x3, x0, 1        # x3 = F(1) = 1
        
# Store first two values
        sw   x2, 0(x0)        # mem[0] = 0
        sw   x3, 4(x0)        # mem[4] = 1

# Initialize loop variables
        addi x4, x0, 2        # x4 = counter (start at 2, already have F(0) and F(1))
        addi x5, x0, 8        # x5 = memory address (start at 8)

# Main Fibonacci loop
fib_loop:
        add  x6, x2, x3       # x6 = F(n-2) + F(n-1) = F(n)
        sw   x6, 0(x5)        # mem[addr] = F(n)
        
        # Shift values
        add  x2, x0, x3       # x2 = x3 (F(n-2) = old F(n-1))
        add  x3, x0, x6       # x3 = x6 (F(n-1) = new F(n))
        
        # Increment counters
        addi x4, x4, 1        # counter++
        addi x5, x5, 4        # addr += 4
        
        # Loop condition
        bne  x4, x1, fib_loop # if counter != N, continue

# End
        halt

# Expected results in memory:
# mem[0]  = 0   (F0)
# mem[4]  = 1   (F1)
# mem[8]  = 1   (F2)
# mem[12] = 2   (F3)
# mem[16] = 3   (F4)
# mem[20] = 5   (F5)
# mem[24] = 8   (F6)
# mem[28] = 13  (F7)
# mem[32] = 21  (F8)
# mem[36] = 34  (F9)
