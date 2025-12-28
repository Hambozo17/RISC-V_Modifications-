# 🔧 Non-Pipelined RISC-V Processor with Crypto Extensions

[![RISC-V](https://img.shields.io/badge/RISC--V-RV32I-blue)](https://riscv.org/)
[![Verilog](https://img.shields.io/badge/HDL-Verilog-orange)](https://en.wikipedia.org/wiki/Verilog)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

A **Single-Cycle RISC-V Processor** with custom cryptographic extensions, developed for ECEN432 - Introduction to Computer Architecture at NILE University.

## 🎯 Features

- ✅ **RV32I Base Integer Instruction Set**
- ✅ **Custom HALT Instruction** - Clean program termination
- ✅ **Branch (BNE) & Jump (JAL)** - Control flow instructions
- ✅ **Crypto Extensions**:
  - `RNG` - Random Number Generator (LFSR-based)
  - `ROTL` - Rotate Left
  - `ROTR` - Rotate Right
- ✅ **Python Assembler with GUI**

## 📁 Project Structure

```
RISC_V_Arch/
├── rtl/                          # Verilog RTL source files
│   ├── Single_Cycle_Top.v        # Top-level module
│   ├── Single_Cycle_Core.v       # Core processor
│   ├── Control_Unit.v            # Control unit
│   ├── ALU.v                     # Arithmetic Logic Unit
│   ├── Register_File.v           # 32x32 register file
│   ├── Instruction_Memory.v      # Instruction memory
│   ├── Data_Memory.v             # Data memory
│   └── ...                       # Other modules
├── tb/                           # Testbenches
│   └── Single_Cycle_TB.v         # Main testbench
├── assembler/                    # Python assembler
│   ├── riscv_assembler.py        # Command-line assembler
│   ├── assembler_gui.py          # GUI application
│   ├── crypto_demo.asm           # Demo program
│   └── fibonacci.asm             # Example program
├── Images/                       # Simulation screenshots
├── docs/                         # Documentation
│   └── RISCV_Project_Report.pdf  # Full project report
└── README.md
```

## 🏗️ Architecture

```
                    ┌─────────────────────────────────────┐
                    │          Single_Cycle_Top           │
                    │  ┌─────────────────────────────┐   │
                    │  │      Single_Cycle_Core      │   │
                    │  │  ┌───────────┬───────────┐  │   │
                    │  │  │  Control  │  Datapath │  │   │
                    │  │  │   Unit    │    (ALU,  │  │   │
                    │  │  │           │  RegFile, │  │   │
                    │  │  │           │    PC)    │  │   │
                    │  │  └───────────┴───────────┘  │   │
                    │  └─────────────────────────────┘   │
                    │  ┌─────────────┐ ┌─────────────┐   │
                    │  │ Instruction │ │    Data     │   │
                    │  │   Memory    │ │   Memory    │   │
                    │  └─────────────┘ └─────────────┘   │
                    └─────────────────────────────────────┘
```

## 📋 Supported Instructions

### Standard RV32I
| Type | Instructions |
|------|-------------|
| R-Type | `add`, `sub`, `and`, `or`, `xor`, `sll`, `srl`, `sra`, `slt` |
| I-Type | `addi`, `andi`, `ori`, `xori`, `lw` |
| S-Type | `sw` |
| B-Type | `beq`, `bne`, `blt`, `bge` |
| J-Type | `jal`, `jalr` |

### Custom Extensions
| Instruction | Encoding | Description |
|-------------|----------|-------------|
| `halt` | `0x00000073` | Stop execution |
| `rng rd` | Custom opcode | Random number generation |
| `rotl rd, rs1, rs2` | Custom opcode | Rotate left |
| `rotr rd, rs1, rs2` | Custom opcode | Rotate right |

## 🚀 Quick Start

### Simulation (Vivado)

1. Create new project in Vivado
2. Add RTL files from `rtl/` folder
3. Add testbench from `tb/` folder
4. Set `Single_Cycle_TB` as top module for simulation
5. Run simulation:
```tcl
launch_simulation
run -all
```

### Python Assembler

```bash
# Command line
python assembler/riscv_assembler.py program.asm -l

# Generate Verilog output
python assembler/riscv_assembler.py program.asm --verilog

# GUI application
python assembler/assembler_gui.py
```

## 📊 Simulation Results

All tests pass successfully:
- ✅ HALT instruction working
- ✅ BNE loop (5 iterations verified)
- ✅ JAL jump verified
- ✅ RNG, ROTL, ROTR crypto operations
- ✅ Memory read/write operations

### Sample Test Output
```
=============================================================================
  RISC-V Single Cycle Processor - Simulation Started
=============================================================================
[Cycle   19] [CRYPTO] RNG instruction executed!
[Cycle   20] [CRYPTO] ROTL instruction executed!
[Cycle   21] [CRYPTO] ROTR instruction executed!
[Cycle   28] *** TEST PASSED: Expected value 25 at address 100 ***
[Cycle   29] *** HALT INSTRUCTION DETECTED ***
             PC frozen at: 0x00000040
=============================================================================
  ALL TESTS PASSED!
=============================================================================
```

## 👥 Team Members

| Name | ID |
|------|-----|
| Hossam Aqeel | 221001590 |
| Farah Khaled | 221001643 |
| Mohamed Mohsen | 221001411 |
| Omar Sherif | 221000161 |
| Yahia Yasser | 221001502 |

## 📚 Course Information

- **Course**: ECEN432 - Introduction to Computer Architecture
- **University**: Nile University
- **Faculty**: Faculty of Engineering - Electronics and Communications Dept.
- **Supervisor**: Dr. Ahmed Soltan
- **Teaching Assistant**: Eng. Silvana Atef
- **Semester**: Fall 2025

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔗 References

- [RISC-V Specification](https://riscv.org/specifications/)
- Patterson & Hennessy - Computer Organization and Design RISC-V Edition
- Harris & Harris - Digital Design and Computer Architecture RISC-V Edition
