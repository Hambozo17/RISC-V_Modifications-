#!/usr/bin/env python3
"""
================================================================================
RISC-V Assembler Runner
================================================================================
Quick script to assemble and generate Verilog output

Usage:
    python run.py program.asm
    python run.py crypto_demo.asm --update-verilog

This will:
1. Assemble the program
2. Show the listing
3. Optionally update Instruction_Memory.v
================================================================================
"""

import sys
import os
import shutil
from riscv_assembler import RISCVAssembler

def main():
    if len(sys.argv) < 2:
        print("Usage: python run.py <program.asm> [--update-verilog]")
        print("\nExamples:")
        print("  python run.py crypto_demo.asm")
        print("  python run.py crypto_demo.asm --update-verilog")
        sys.exit(1)
    
    input_file = sys.argv[1]
    update_verilog = '--update-verilog' in sys.argv
    
    # Read source
    try:
        with open(input_file, 'r') as f:
            source = f.read()
    except FileNotFoundError:
        print(f"Error: File not found: {input_file}")
        sys.exit(1)
    
    print("=" * 70)
    print("RISC-V ASSEMBLER")
    print("=" * 70)
    print(f"Input: {input_file}")
    print()
    
    # Assemble
    asm = RISCVAssembler()
    asm.assemble(source)
    
    # Print listing
    asm.print_listing()
    
    # Generate outputs
    hex_file = input_file.replace('.asm', '.hex')
    with open(hex_file, 'w') as f:
        f.write(asm.to_hex())
    print(f"\nHex file written to: {hex_file}")
    
    mem_file = input_file.replace('.asm', '.mem')
    with open(mem_file, 'w') as f:
        f.write(asm.to_mem())
    print(f"Mem file written to: {mem_file}")
    
    # Generate Verilog initialization
    verilog_init = asm.to_verilog()
    verilog_file = input_file.replace('.asm', '_verilog_init.v')
    with open(verilog_file, 'w') as f:
        f.write(verilog_init)
    print(f"Verilog init written to: {verilog_file}")
    
    # Optionally update Instruction_Memory.v
    if update_verilog:
        rtl_path = os.path.join(os.path.dirname(__file__), '..', 'rtl', 'Instruction_Memory.v')
        if os.path.exists(rtl_path):
            # Backup original
            backup_path = rtl_path + '.backup'
            shutil.copy(rtl_path, backup_path)
            print(f"\nBackup created: {backup_path}")
            
            # Read original file
            with open(rtl_path, 'r') as f:
                content = f.read()
            
            # Find and replace the initial block
            import re
            pattern = r'(initial begin\s*\n)(.*?)(^\s*end\s*$)'
            
            new_init = "initial begin\n"
            for i, (code, (addr, instr, _)) in enumerate(zip(asm.machine_code, asm.instructions)):
                new_init += f"        I_MEM_BLOCK[{i}]  = 32'h{code:08X};  // 0x{addr:02X}: {instr}\n"
            
            # Add NOPs
            new_init += "\n        // Fill remaining with NOPs\n"
            for i in range(len(asm.machine_code), min(len(asm.machine_code) + 5, 64)):
                new_init += f"        I_MEM_BLOCK[{i}] = 32'h00000013;\n"
            
            # Note: Manual replacement might be needed for complex cases
            print("\n" + "=" * 70)
            print("VERILOG INITIALIZATION CODE:")
            print("=" * 70)
            print(verilog_init)
            print("=" * 70)
            print("\nCopy the above 'initial begin...end' block to Instruction_Memory.v")
        else:
            print(f"\nWarning: Could not find {rtl_path}")
    
    print("\n" + "=" * 70)
    print("ASSEMBLY COMPLETE!")
    print("=" * 70)


if __name__ == '__main__':
    main()
