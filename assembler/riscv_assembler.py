#!/usr/bin/env python3
"""
================================================================================
RISC-V Assembler for Single Cycle Processor
Phase 5: Python Assembler Toolchain
================================================================================
Author: Enhanced for RISC-V Project
Date: December 28, 2025

Supports:
  - Standard RV32I: add, addi, sub, and, or, xor, sll, srl, sra, slt, sltu
  - Memory: lw, sw
  - Branches: beq, bne, blt, bge, bltu, bgeu
  - Jumps: jal, jalr
  - Upper Immediate: lui, auipc
  - System: halt (ecall), nop
  - Custom Crypto: rotl, rotr, rng

Usage:
  python riscv_assembler.py program.asm
  python riscv_assembler.py program.asm -o output.hex
  python riscv_assembler.py program.asm --verilog

Output:
  - .hex file (Intel HEX format)
  - Verilog Instruction_Memory initialization
================================================================================
"""

import sys
import re
import argparse
from typing import Dict, List, Tuple, Optional

# ==============================================================================
# REGISTER MAPPINGS
# ==============================================================================
REGISTERS = {
    'x0': 0,  'zero': 0,
    'x1': 1,  'ra': 1,
    'x2': 2,  'sp': 2,
    'x3': 3,  'gp': 3,
    'x4': 4,  'tp': 4,
    'x5': 5,  't0': 5,
    'x6': 6,  't1': 6,
    'x7': 7,  't2': 7,
    'x8': 8,  's0': 8, 'fp': 8,
    'x9': 9,  's1': 9,
    'x10': 10, 'a0': 10,
    'x11': 11, 'a1': 11,
    'x12': 12, 'a2': 12,
    'x13': 13, 'a3': 13,
    'x14': 14, 'a4': 14,
    'x15': 15, 'a5': 15,
    'x16': 16, 'a6': 16,
    'x17': 17, 'a7': 17,
    'x18': 18, 's2': 18,
    'x19': 19, 's3': 19,
    'x20': 20, 's4': 20,
    'x21': 21, 's5': 21,
    'x22': 22, 's6': 22,
    'x23': 23, 's7': 23,
    'x24': 24, 's8': 24,
    'x25': 25, 's9': 25,
    'x26': 26, 's10': 26,
    'x27': 27, 's11': 27,
    'x28': 28, 't3': 28,
    'x29': 29, 't4': 29,
    'x30': 30, 't5': 30,
    'x31': 31, 't6': 31,
}

# ==============================================================================
# OPCODES
# ==============================================================================
OPCODES = {
    # R-type (opcode = 0110011)
    'add':  0b0110011, 'sub':  0b0110011, 'and':  0b0110011,
    'or':   0b0110011, 'xor':  0b0110011, 'sll':  0b0110011,
    'srl':  0b0110011, 'sra':  0b0110011, 'slt':  0b0110011,
    'sltu': 0b0110011,
    
    # I-type ALU (opcode = 0010011)
    'addi': 0b0010011, 'andi': 0b0010011, 'ori':  0b0010011,
    'xori': 0b0010011, 'slti': 0b0010011, 'sltiu':0b0010011,
    'slli': 0b0010011, 'srli': 0b0010011, 'srai': 0b0010011,
    
    # Load (opcode = 0000011)
    'lw':   0b0000011, 'lh': 0b0000011, 'lb': 0b0000011,
    'lhu':  0b0000011, 'lbu': 0b0000011,
    
    # Store (opcode = 0100011)
    'sw':   0b0100011, 'sh': 0b0100011, 'sb': 0b0100011,
    
    # Branch (opcode = 1100011)
    'beq':  0b1100011, 'bne':  0b1100011, 'blt':  0b1100011,
    'bge':  0b1100011, 'bltu': 0b1100011, 'bgeu': 0b1100011,
    
    # JAL (opcode = 1101111)
    'jal':  0b1101111,
    
    # JALR (opcode = 1100111)
    'jalr': 0b1100111,
    
    # LUI (opcode = 0110111)
    'lui':  0b0110111,
    
    # AUIPC (opcode = 0010111)
    'auipc': 0b0010111,
    
    # System (opcode = 1110011)
    'ecall': 0b1110011, 'halt': 0b1110011,
    
    # Custom Crypto (opcode = 0001011)
    'rotl': 0b0001011, 'rotr': 0b0001011, 'rng': 0b0001011,
}

# ==============================================================================
# FUNCT3 CODES
# ==============================================================================
FUNCT3 = {
    # R-type
    'add': 0b000, 'sub': 0b000, 'sll': 0b001, 'slt': 0b010,
    'sltu': 0b011, 'xor': 0b100, 'srl': 0b101, 'sra': 0b101,
    'or': 0b110, 'and': 0b111,
    
    # I-type ALU
    'addi': 0b000, 'slti': 0b010, 'sltiu': 0b011, 'xori': 0b100,
    'ori': 0b110, 'andi': 0b111, 'slli': 0b001, 'srli': 0b101,
    'srai': 0b101,
    
    # Load
    'lb': 0b000, 'lh': 0b001, 'lw': 0b010, 'lbu': 0b100, 'lhu': 0b101,
    
    # Store
    'sb': 0b000, 'sh': 0b001, 'sw': 0b010,
    
    # Branch
    'beq': 0b000, 'bne': 0b001, 'blt': 0b100, 'bge': 0b101,
    'bltu': 0b110, 'bgeu': 0b111,
    
    # JALR
    'jalr': 0b000,
    
    # Custom Crypto
    'rotl': 0b010, 'rotr': 0b011, 'rng': 0b100,
}

# ==============================================================================
# FUNCT7 CODES
# ==============================================================================
FUNCT7 = {
    'add': 0b0000000, 'sub': 0b0100000,
    'sll': 0b0000000, 'slt': 0b0000000, 'sltu': 0b0000000,
    'xor': 0b0000000, 'srl': 0b0000000, 'sra': 0b0100000,
    'or': 0b0000000, 'and': 0b0000000,
    'slli': 0b0000000, 'srli': 0b0000000, 'srai': 0b0100000,
    'rotl': 0b0000000, 'rotr': 0b0000000, 'rng': 0b0000000,
}


class RISCVAssembler:
    """RISC-V Assembler for Single Cycle Processor"""
    
    def __init__(self):
        self.labels: Dict[str, int] = {}
        self.instructions: List[Tuple[int, str, int]] = []  # (address, line, line_num)
        self.machine_code: List[int] = []
        self.current_address = 0
        self.errors: List[str] = []
        
    def parse_register(self, reg_str: str) -> int:
        """Parse register name to number"""
        reg_str = reg_str.strip().lower().replace(',', '')
        if reg_str in REGISTERS:
            return REGISTERS[reg_str]
        raise ValueError(f"Unknown register: {reg_str}")
    
    def parse_immediate(self, imm_str: str, bits: int = 12, signed: bool = True) -> int:
        """Parse immediate value with bounds checking"""
        imm_str = imm_str.strip().replace(',', '')
        
        # Handle hex, binary, or decimal
        if imm_str.startswith('0x') or imm_str.startswith('0X'):
            value = int(imm_str, 16)
        elif imm_str.startswith('0b') or imm_str.startswith('0B'):
            value = int(imm_str, 2)
        else:
            value = int(imm_str)
        
        # Check bounds
        if signed:
            min_val = -(1 << (bits - 1))
            max_val = (1 << (bits - 1)) - 1
        else:
            min_val = 0
            max_val = (1 << bits) - 1
            
        if value < min_val or value > max_val:
            raise ValueError(f"Immediate {value} out of range [{min_val}, {max_val}]")
        
        # Convert to unsigned for encoding
        if value < 0:
            value = value & ((1 << bits) - 1)
            
        return value
    
    def parse_memory_operand(self, operand: str) -> Tuple[int, int]:
        """Parse memory operand like '100(x0)' -> (offset, base_reg)"""
        match = re.match(r'(-?\d+)\s*\(\s*(\w+)\s*\)', operand.strip())
        if not match:
            raise ValueError(f"Invalid memory operand: {operand}")
        
        offset = self.parse_immediate(match.group(1))
        base_reg = self.parse_register(match.group(2))
        return offset, base_reg
    
    # ==========================================================================
    # INSTRUCTION ENCODERS
    # ==========================================================================
    
    def encode_r_type(self, instr: str, rd: int, rs1: int, rs2: int) -> int:
        """Encode R-type instruction"""
        opcode = OPCODES[instr]
        funct3 = FUNCT3[instr]
        funct7 = FUNCT7[instr]
        
        return (funct7 << 25) | (rs2 << 20) | (rs1 << 15) | (funct3 << 12) | (rd << 7) | opcode
    
    def encode_i_type(self, instr: str, rd: int, rs1: int, imm: int) -> int:
        """Encode I-type instruction"""
        opcode = OPCODES[instr]
        funct3 = FUNCT3[instr]
        
        # Handle shift instructions (imm is shamt, funct7 in upper bits)
        if instr in ['slli', 'srli', 'srai']:
            funct7 = FUNCT7[instr]
            imm = (funct7 << 5) | (imm & 0x1F)
        
        return ((imm & 0xFFF) << 20) | (rs1 << 15) | (funct3 << 12) | (rd << 7) | opcode
    
    def encode_s_type(self, instr: str, rs2: int, rs1: int, imm: int) -> int:
        """Encode S-type instruction (stores)"""
        opcode = OPCODES[instr]
        funct3 = FUNCT3[instr]
        
        imm_11_5 = (imm >> 5) & 0x7F
        imm_4_0 = imm & 0x1F
        
        return (imm_11_5 << 25) | (rs2 << 20) | (rs1 << 15) | (funct3 << 12) | (imm_4_0 << 7) | opcode
    
    def encode_b_type(self, instr: str, rs1: int, rs2: int, imm: int) -> int:
        """Encode B-type instruction (branches)"""
        opcode = OPCODES[instr]
        funct3 = FUNCT3[instr]
        
        # B-type immediate encoding: imm[12|10:5|4:1|11]
        imm_12 = (imm >> 12) & 0x1
        imm_11 = (imm >> 11) & 0x1
        imm_10_5 = (imm >> 5) & 0x3F
        imm_4_1 = (imm >> 1) & 0xF
        
        return (imm_12 << 31) | (imm_10_5 << 25) | (rs2 << 20) | (rs1 << 15) | \
               (funct3 << 12) | (imm_4_1 << 8) | (imm_11 << 7) | opcode
    
    def encode_u_type(self, instr: str, rd: int, imm: int) -> int:
        """Encode U-type instruction (LUI, AUIPC)"""
        opcode = OPCODES[instr]
        return ((imm & 0xFFFFF) << 12) | (rd << 7) | opcode
    
    def encode_j_type(self, instr: str, rd: int, imm: int) -> int:
        """Encode J-type instruction (JAL)"""
        opcode = OPCODES[instr]
        
        # J-type immediate encoding: imm[20|10:1|11|19:12]
        imm_20 = (imm >> 20) & 0x1
        imm_19_12 = (imm >> 12) & 0xFF
        imm_11 = (imm >> 11) & 0x1
        imm_10_1 = (imm >> 1) & 0x3FF
        
        return (imm_20 << 31) | (imm_10_1 << 21) | (imm_11 << 20) | \
               (imm_19_12 << 12) | (rd << 7) | opcode
    
    def encode_crypto(self, instr: str, rd: int, rs1: int = 0, rs2: int = 0) -> int:
        """Encode custom crypto instruction"""
        opcode = OPCODES[instr]
        funct3 = FUNCT3[instr]
        funct7 = FUNCT7[instr]
        
        return (funct7 << 25) | (rs2 << 20) | (rs1 << 15) | (funct3 << 12) | (rd << 7) | opcode
    
    # ==========================================================================
    # FIRST PASS: Collect Labels
    # ==========================================================================
    
    def first_pass(self, lines: List[str]):
        """First pass: collect all labels and their addresses"""
        self.current_address = 0
        
        for line_num, line in enumerate(lines, 1):
            # Remove comments
            line = re.sub(r'[#;].*', '', line).strip()
            if not line:
                continue
            
            # Check for label
            if ':' in line:
                parts = line.split(':', 1)
                label = parts[0].strip()
                self.labels[label] = self.current_address
                line = parts[1].strip() if len(parts) > 1 else ''
            
            if line:
                self.instructions.append((self.current_address, line, line_num))
                self.current_address += 4
    
    # ==========================================================================
    # SECOND PASS: Generate Machine Code
    # ==========================================================================
    
    def second_pass(self):
        """Second pass: generate machine code"""
        for addr, line, line_num in self.instructions:
            try:
                code = self.assemble_instruction(line, addr)
                self.machine_code.append(code)
            except Exception as e:
                self.errors.append(f"Line {line_num}: {e} - '{line}'")
    
    def assemble_instruction(self, line: str, current_addr: int) -> int:
        """Assemble a single instruction"""
        parts = line.replace(',', ' ').split()
        instr = parts[0].lower()
        
        # Handle pseudo-instructions
        if instr == 'nop':
            return self.encode_i_type('addi', 0, 0, 0)
        
        if instr == 'li':  # Load immediate (pseudo)
            rd = self.parse_register(parts[1])
            imm = self.parse_immediate(parts[2], bits=12)
            return self.encode_i_type('addi', rd, 0, imm)
        
        if instr == 'mv':  # Move (pseudo)
            rd = self.parse_register(parts[1])
            rs = self.parse_register(parts[2])
            return self.encode_i_type('addi', rd, rs, 0)
        
        if instr == 'j':  # Jump (pseudo for jal x0, offset)
            if parts[1] in self.labels:
                offset = self.labels[parts[1]] - current_addr
            else:
                offset = self.parse_immediate(parts[1], bits=21, signed=True)
            return self.encode_j_type('jal', 0, offset)
        
        # R-type instructions
        if instr in ['add', 'sub', 'and', 'or', 'xor', 'sll', 'srl', 'sra', 'slt', 'sltu']:
            rd = self.parse_register(parts[1])
            rs1 = self.parse_register(parts[2])
            rs2 = self.parse_register(parts[3])
            return self.encode_r_type(instr, rd, rs1, rs2)
        
        # I-type ALU
        if instr in ['addi', 'andi', 'ori', 'xori', 'slti', 'sltiu']:
            rd = self.parse_register(parts[1])
            rs1 = self.parse_register(parts[2])
            imm = self.parse_immediate(parts[3])
            return self.encode_i_type(instr, rd, rs1, imm)
        
        # Shift immediate
        if instr in ['slli', 'srli', 'srai']:
            rd = self.parse_register(parts[1])
            rs1 = self.parse_register(parts[2])
            shamt = self.parse_immediate(parts[3], bits=5, signed=False)
            return self.encode_i_type(instr, rd, rs1, shamt)
        
        # Load instructions
        if instr in ['lw', 'lh', 'lb', 'lhu', 'lbu']:
            rd = self.parse_register(parts[1])
            offset, base = self.parse_memory_operand(parts[2])
            return self.encode_i_type(instr, rd, base, offset)
        
        # Store instructions
        if instr in ['sw', 'sh', 'sb']:
            rs2 = self.parse_register(parts[1])
            offset, base = self.parse_memory_operand(parts[2])
            return self.encode_s_type(instr, rs2, base, offset)
        
        # Branch instructions
        if instr in ['beq', 'bne', 'blt', 'bge', 'bltu', 'bgeu']:
            rs1 = self.parse_register(parts[1])
            rs2 = self.parse_register(parts[2])
            if parts[3] in self.labels:
                offset = self.labels[parts[3]] - current_addr
            else:
                offset = self.parse_immediate(parts[3], bits=13, signed=True)
            return self.encode_b_type(instr, rs1, rs2, offset)
        
        # JAL
        if instr == 'jal':
            rd = self.parse_register(parts[1])
            if parts[2] in self.labels:
                offset = self.labels[parts[2]] - current_addr
            else:
                offset = self.parse_immediate(parts[2], bits=21, signed=True)
            return self.encode_j_type(instr, rd, offset)
        
        # JALR
        if instr == 'jalr':
            rd = self.parse_register(parts[1])
            if '(' in parts[2]:
                offset, rs1 = self.parse_memory_operand(parts[2])
            else:
                rs1 = self.parse_register(parts[2])
                offset = self.parse_immediate(parts[3]) if len(parts) > 3 else 0
            return self.encode_i_type(instr, rd, rs1, offset)
        
        # LUI
        if instr == 'lui':
            rd = self.parse_register(parts[1])
            imm = self.parse_immediate(parts[2], bits=20, signed=False)
            return self.encode_u_type(instr, rd, imm)
        
        # AUIPC
        if instr == 'auipc':
            rd = self.parse_register(parts[1])
            imm = self.parse_immediate(parts[2], bits=20, signed=False)
            return self.encode_u_type(instr, rd, imm)
        
        # HALT / ECALL
        if instr in ['halt', 'ecall']:
            return 0x00000073
        
        # Custom Crypto: RNG
        if instr == 'rng':
            rd = self.parse_register(parts[1])
            return self.encode_crypto(instr, rd, 0, 0)
        
        # Custom Crypto: ROTL
        if instr == 'rotl':
            rd = self.parse_register(parts[1])
            rs1 = self.parse_register(parts[2])
            rs2 = self.parse_register(parts[3])
            return self.encode_crypto(instr, rd, rs1, rs2)
        
        # Custom Crypto: ROTR
        if instr == 'rotr':
            rd = self.parse_register(parts[1])
            rs1 = self.parse_register(parts[2])
            rs2 = self.parse_register(parts[3])
            return self.encode_crypto(instr, rd, rs1, rs2)
        
        raise ValueError(f"Unknown instruction: {instr}")
    
    # ==========================================================================
    # ASSEMBLER MAIN
    # ==========================================================================
    
    def assemble(self, source: str) -> List[int]:
        """Assemble source code to machine code"""
        lines = source.split('\n')
        
        # First pass: collect labels
        self.first_pass(lines)
        
        # Second pass: generate machine code
        self.second_pass()
        
        if self.errors:
            print("=" * 60)
            print("ASSEMBLY ERRORS:")
            print("=" * 60)
            for error in self.errors:
                print(f"  {error}")
            print("=" * 60)
            sys.exit(1)
        
        return self.machine_code
    
    # ==========================================================================
    # OUTPUT GENERATORS
    # ==========================================================================
    
    def to_hex(self) -> str:
        """Generate hex file content"""
        lines = []
        lines.append("// RISC-V Machine Code - Generated by riscv_assembler.py")
        lines.append(f"// Total instructions: {len(self.machine_code)}")
        lines.append("// Format: ADDRESS: MACHINE_CODE  // ASM")
        lines.append("")
        
        for i, (code, (addr, asm, _)) in enumerate(zip(self.machine_code, self.instructions)):
            lines.append(f"0x{addr:08X}: 0x{code:08X}  // {asm}")
        
        return '\n'.join(lines)
    
    def to_verilog(self) -> str:
        """Generate Verilog memory initialization"""
        lines = []
        lines.append("// =============================================================================")
        lines.append("// RISC-V Instruction Memory - Auto-generated by riscv_assembler.py")
        lines.append("// =============================================================================")
        lines.append("")
        lines.append("    initial begin")
        
        for i, (code, (addr, asm, _)) in enumerate(zip(self.machine_code, self.instructions)):
            lines.append(f"        I_MEM_BLOCK[{i}]  = 32'h{code:08X};  // 0x{addr:02X}: {asm}")
        
        # Fill remaining with NOPs
        lines.append("")
        lines.append("        // Fill remaining with NOPs")
        for i in range(len(self.machine_code), min(len(self.machine_code) + 5, 64)):
            lines.append(f"        I_MEM_BLOCK[{i}] = 32'h00000013;  // nop")
        
        lines.append("    end")
        
        return '\n'.join(lines)
    
    def to_mem(self) -> str:
        """Generate .mem file for $readmemh"""
        lines = []
        for code in self.machine_code:
            lines.append(f"{code:08X}")
        return '\n'.join(lines)
    
    def print_listing(self):
        """Print assembly listing"""
        print("=" * 70)
        print("RISC-V ASSEMBLY LISTING")
        print("=" * 70)
        print(f"{'ADDR':<10} {'MACHINE CODE':<14} {'ASSEMBLY':<30}")
        print("-" * 70)
        
        for code, (addr, asm, line_num) in zip(self.machine_code, self.instructions):
            print(f"0x{addr:04X}     0x{code:08X}     {asm}")
        
        print("-" * 70)
        print(f"Total: {len(self.machine_code)} instructions ({len(self.machine_code) * 4} bytes)")
        print("=" * 70)
        
        if self.labels:
            print("\nLABELS:")
            for label, addr in self.labels.items():
                print(f"  {label}: 0x{addr:04X}")


def main():
    parser = argparse.ArgumentParser(
        description='RISC-V Assembler for Single Cycle Processor',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  python riscv_assembler.py program.asm
  python riscv_assembler.py program.asm -o output.hex
  python riscv_assembler.py program.asm --verilog > Instruction_Memory_init.v
  python riscv_assembler.py program.asm --mem > program.mem
        '''
    )
    parser.add_argument('input', help='Input assembly file (.asm)')
    parser.add_argument('-o', '--output', help='Output hex file')
    parser.add_argument('--verilog', action='store_true', help='Output Verilog format')
    parser.add_argument('--mem', action='store_true', help='Output .mem format for $readmemh')
    parser.add_argument('-l', '--listing', action='store_true', help='Print assembly listing')
    
    args = parser.parse_args()
    
    # Read input file
    try:
        with open(args.input, 'r') as f:
            source = f.read()
    except FileNotFoundError:
        print(f"Error: File not found: {args.input}")
        sys.exit(1)
    
    # Assemble
    asm = RISCVAssembler()
    asm.assemble(source)
    
    # Print listing if requested
    if args.listing:
        asm.print_listing()
    
    # Output
    if args.verilog:
        print(asm.to_verilog())
    elif args.mem:
        print(asm.to_mem())
    elif args.output:
        with open(args.output, 'w') as f:
            f.write(asm.to_hex())
        print(f"Output written to: {args.output}")
    else:
        # Default: print hex and listing
        asm.print_listing()
        print("\n" + asm.to_hex())


if __name__ == '__main__':
    main()
