# RISC-V Assembler for Single Cycle Processor

## Overview

This is an enhanced Python-based assembler for the RISC-V Single Cycle Processor project. It converts assembly language programs into machine code that can be loaded directly into the processor's Instruction Memory.

## Features

- **Full RV32I Base Integer Instruction Set**
- **Custom Crypto Extensions**: RNG, ROTL, ROTR
- **Label Support**: Forward and backward references
- **Pseudo-instructions**: nop, li, mv, j
- **Multiple Output Formats**: Hex, Verilog, .mem

## Files

| File | Description |
|------|-------------|
| `riscv_assembler.py` | Main assembler script |
| `run.py` | Convenience runner |
| `INSTRUCTION_REFERENCE.md` | Complete instruction set reference |
| `crypto_demo.asm` | Demo program with crypto extensions |
| `fibonacci.asm` | Fibonacci sequence example |

## Quick Start

### Basic Usage

```bash
# Assemble and show listing
python riscv_assembler.py program.asm -l

# Generate hex output
python riscv_assembler.py program.asm -o output.hex

# Generate Verilog format
python riscv_assembler.py program.asm --verilog

# Generate .mem format for $readmemh
python riscv_assembler.py program.asm --mem
```

### Using run.py

```bash
python run.py crypto_demo.asm
python run.py crypto_demo.asm --update-verilog
```

## Instruction Formats

### R-Type (Register-Register)
```
add  rd, rs1, rs2    # rd = rs1 + rs2
sub  rd, rs1, rs2    # rd = rs1 - rs2
and  rd, rs1, rs2    # rd = rs1 & rs2
or   rd, rs1, rs2    # rd = rs1 | rs2
xor  rd, rs1, rs2    # rd = rs1 ^ rs2
sll  rd, rs1, rs2    # rd = rs1 << rs2
srl  rd, rs1, rs2    # rd = rs1 >> rs2 (logical)
sra  rd, rs1, rs2    # rd = rs1 >> rs2 (arithmetic)
slt  rd, rs1, rs2    # rd = (rs1 < rs2) ? 1 : 0
```

### I-Type (Immediate)
```
addi rd, rs1, imm    # rd = rs1 + imm
andi rd, rs1, imm    # rd = rs1 & imm
ori  rd, rs1, imm    # rd = rs1 | imm
xori rd, rs1, imm    # rd = rs1 ^ imm
```

### Memory Operations
```
lw   rd, offset(rs1)    # Load word
sw   rs2, offset(rs1)   # Store word
```

### Branches
```
beq  rs1, rs2, label    # Branch if equal
bne  rs1, rs2, label    # Branch if not equal
blt  rs1, rs2, label    # Branch if less than
bge  rs1, rs2, label    # Branch if greater or equal
```

### Jumps
```
jal  rd, label          # Jump and link
jalr rd, offset(rs1)    # Jump and link register
```

### Custom Crypto Extensions
```
rng  rd                 # rd = random number
rotl rd, rs1, rs2       # rd = rotate left rs1 by rs2 bits
rotr rd, rs1, rs2       # rd = rotate right rs1 by rs2 bits
```

### System
```
halt                    # Stop execution
```

## Example Program

```asm
# Simple counter program
        addi x1, x0, 5          # limit = 5
        addi x2, x0, 0          # counter = 0
        addi x3, x0, 1          # increment = 1

loop:
        add  x2, x2, x3         # counter++
        bne  x1, x2, loop       # while counter != limit

        sw   x2, 100(x0)        # store result
        halt                    # stop
```

## Output Example

```
======================================================================
RISC-V ASSEMBLY LISTING
======================================================================
ADDR       MACHINE CODE   ASSEMBLY
----------------------------------------------------------------------
0x0000     0x00500093     addi x1, x0, 5
0x0004     0x00000113     addi x2, x0, 0
0x0008     0x00100193     addi x3, x0, 1
0x000C     0x00310133     add  x2, x2, x3
0x0010     0xFE209EE3     bne  x1, x2, loop
0x0014     0x06202223     sw   x2, 100(x0)
0x0018     0x00000073     halt
----------------------------------------------------------------------
Total: 7 instructions (28 bytes)
======================================================================
```

## Integration with Vivado

### Step 1: Generate Verilog Code
```bash
python riscv_assembler.py your_program.asm --verilog > program_init.v
```

### Step 2: Copy to Instruction_Memory.v
Copy the generated `initial begin ... end` block into your `Instruction_Memory.v` file.

### Step 3: Run Simulation
```tcl
launch_simulation
run -all
```

## Register ABI Names

| Register | ABI Name | Description |
|----------|----------|-------------|
| x0 | zero | Hard-wired zero |
| x1 | ra | Return address |
| x2 | sp | Stack pointer |
| x3 | gp | Global pointer |
| x5-x7 | t0-t2 | Temporaries |
| x10-x11 | a0-a1 | Arguments/Return values |
| x12-x17 | a2-a7 | Arguments |
| x18-x27 | s2-s11 | Saved registers |
| x28-x31 | t3-t6 | Temporaries |

## Error Handling

The assembler provides detailed error messages:

```
============================================================
ASSEMBLY ERRORS:
============================================================
  Line 5: Unknown register: x32 - 'add x32, x1, x2'
  Line 8: Immediate 5000 out of range [-2048, 2047] - 'addi x1, x0, 5000'
============================================================
```

## Author

Enhanced for RISC-V Single Cycle Processor Project
Phase 5: Python Assembler Toolchain
December 2025
