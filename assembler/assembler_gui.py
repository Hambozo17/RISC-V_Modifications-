#!/usr/bin/env python3
"""
================================================================================
RISC-V Assembler GUI
================================================================================
A graphical interface for the RISC-V Single Cycle Processor Assembler

Features:
- Write/Edit assembly code
- Real-time assembly
- View machine code output
- Generate Verilog code
- Save/Load programs
================================================================================
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox
import os
import sys

# Import the assembler
from riscv_assembler import RISCVAssembler

class RISCVAssemblerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("RISC-V Assembler - Single Cycle Processor")
        self.root.geometry("1200x800")
        self.root.configure(bg='#2b2b2b')
        
        # Configure style
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.configure_styles()
        
        # Current file
        self.current_file = None
        
        # Create GUI
        self.create_menu()
        self.create_toolbar()
        self.create_main_layout()
        self.create_status_bar()
        
        # Load sample program
        self.load_sample_program()
        
        # Bind shortcuts
        self.root.bind('<Control-s>', lambda e: self.save_file())
        self.root.bind('<Control-o>', lambda e: self.open_file())
        self.root.bind('<F5>', lambda e: self.assemble())
        self.root.bind('<Control-n>', lambda e: self.new_file())
    
    def configure_styles(self):
        """Configure ttk styles for dark theme"""
        self.style.configure('TFrame', background='#2b2b2b')
        self.style.configure('TLabel', background='#2b2b2b', foreground='#ffffff')
        self.style.configure('TButton', background='#3c3f41', foreground='#ffffff')
        self.style.configure('Header.TLabel', font=('Consolas', 12, 'bold'), 
                           background='#3c3f41', foreground='#6897bb')
    
    def create_menu(self):
        """Create menu bar"""
        menubar = tk.Menu(self.root, bg='#3c3f41', fg='white')
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0, bg='#3c3f41', fg='white')
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New", command=self.new_file, accelerator="Ctrl+N")
        file_menu.add_command(label="Open...", command=self.open_file, accelerator="Ctrl+O")
        file_menu.add_command(label="Save", command=self.save_file, accelerator="Ctrl+S")
        file_menu.add_command(label="Save As...", command=self.save_file_as)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        # Build menu
        build_menu = tk.Menu(menubar, tearoff=0, bg='#3c3f41', fg='white')
        menubar.add_cascade(label="Build", menu=build_menu)
        build_menu.add_command(label="Assemble", command=self.assemble, accelerator="F5")
        build_menu.add_separator()
        build_menu.add_command(label="Export Hex...", command=self.export_hex)
        build_menu.add_command(label="Export Verilog...", command=self.export_verilog)
        build_menu.add_command(label="Export .mem...", command=self.export_mem)
        
        # Examples menu
        examples_menu = tk.Menu(menubar, tearoff=0, bg='#3c3f41', fg='white')
        menubar.add_cascade(label="Examples", menu=examples_menu)
        examples_menu.add_command(label="Crypto Demo", command=lambda: self.load_example('crypto'))
        examples_menu.add_command(label="Fibonacci", command=lambda: self.load_example('fibonacci'))
        examples_menu.add_command(label="Simple Loop", command=lambda: self.load_example('loop'))
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0, bg='#3c3f41', fg='white')
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="Instruction Reference", command=self.show_reference)
        help_menu.add_command(label="About", command=self.show_about)
    
    def create_toolbar(self):
        """Create toolbar"""
        toolbar = ttk.Frame(self.root)
        toolbar.pack(fill=tk.X, padx=5, pady=5)
        
        # Buttons
        ttk.Button(toolbar, text="📄 New", command=self.new_file).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="📂 Open", command=self.open_file).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="💾 Save", command=self.save_file).pack(side=tk.LEFT, padx=2)
        
        ttk.Separator(toolbar, orient=tk.VERTICAL).pack(side=tk.LEFT, padx=10, fill=tk.Y)
        
        ttk.Button(toolbar, text="▶ Assemble (F5)", command=self.assemble).pack(side=tk.LEFT, padx=2)
        
        ttk.Separator(toolbar, orient=tk.VERTICAL).pack(side=tk.LEFT, padx=10, fill=tk.Y)
        
        ttk.Button(toolbar, text="📤 Export Verilog", command=self.export_verilog).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="📤 Export Hex", command=self.export_hex).pack(side=tk.LEFT, padx=2)
    
    def create_main_layout(self):
        """Create main layout with paned windows"""
        # Main paned window (horizontal)
        main_pane = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        main_pane.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Left panel - Source code
        left_frame = ttk.Frame(main_pane)
        main_pane.add(left_frame, weight=1)
        
        ttk.Label(left_frame, text="📝 Assembly Source Code", style='Header.TLabel').pack(fill=tk.X)
        
        # Source code editor
        self.source_text = scrolledtext.ScrolledText(
            left_frame,
            wrap=tk.NONE,
            font=('Consolas', 11),
            bg='#1e1e1e',
            fg='#d4d4d4',
            insertbackground='white',
            selectbackground='#264f78',
            padx=10,
            pady=10
        )
        self.source_text.pack(fill=tk.BOTH, expand=True)
        
        # Add horizontal scrollbar
        h_scroll = ttk.Scrollbar(left_frame, orient=tk.HORIZONTAL, command=self.source_text.xview)
        h_scroll.pack(fill=tk.X)
        self.source_text.configure(xscrollcommand=h_scroll.set)
        
        # Right panel - Output
        right_frame = ttk.Frame(main_pane)
        main_pane.add(right_frame, weight=1)
        
        # Output notebook (tabs)
        self.output_notebook = ttk.Notebook(right_frame)
        self.output_notebook.pack(fill=tk.BOTH, expand=True)
        
        # Tab 1: Listing
        listing_frame = ttk.Frame(self.output_notebook)
        self.output_notebook.add(listing_frame, text="📋 Listing")
        
        self.listing_text = scrolledtext.ScrolledText(
            listing_frame,
            wrap=tk.NONE,
            font=('Consolas', 10),
            bg='#1e1e1e',
            fg='#9cdcfe',
            state=tk.DISABLED,
            padx=10,
            pady=10
        )
        self.listing_text.pack(fill=tk.BOTH, expand=True)
        
        # Tab 2: Hex Output
        hex_frame = ttk.Frame(self.output_notebook)
        self.output_notebook.add(hex_frame, text="🔢 Hex")
        
        self.hex_text = scrolledtext.ScrolledText(
            hex_frame,
            wrap=tk.NONE,
            font=('Consolas', 10),
            bg='#1e1e1e',
            fg='#ce9178',
            state=tk.DISABLED,
            padx=10,
            pady=10
        )
        self.hex_text.pack(fill=tk.BOTH, expand=True)
        
        # Tab 3: Verilog Output
        verilog_frame = ttk.Frame(self.output_notebook)
        self.output_notebook.add(verilog_frame, text="📟 Verilog")
        
        self.verilog_text = scrolledtext.ScrolledText(
            verilog_frame,
            wrap=tk.NONE,
            font=('Consolas', 10),
            bg='#1e1e1e',
            fg='#4ec9b0',
            state=tk.DISABLED,
            padx=10,
            pady=10
        )
        self.verilog_text.pack(fill=tk.BOTH, expand=True)
        
        # Tab 4: Console/Errors
        console_frame = ttk.Frame(self.output_notebook)
        self.output_notebook.add(console_frame, text="🖥 Console")
        
        self.console_text = scrolledtext.ScrolledText(
            console_frame,
            wrap=tk.WORD,
            font=('Consolas', 10),
            bg='#1e1e1e',
            fg='#ffffff',
            state=tk.DISABLED,
            padx=10,
            pady=10
        )
        self.console_text.pack(fill=tk.BOTH, expand=True)
    
    def create_status_bar(self):
        """Create status bar"""
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        
        status_bar = ttk.Label(self.root, textvariable=self.status_var, 
                              relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(fill=tk.X, side=tk.BOTTOM)
    
    def log_console(self, message, clear=False):
        """Log message to console"""
        self.console_text.configure(state=tk.NORMAL)
        if clear:
            self.console_text.delete(1.0, tk.END)
        self.console_text.insert(tk.END, message + "\n")
        self.console_text.see(tk.END)
        self.console_text.configure(state=tk.DISABLED)
    
    def set_output_text(self, widget, text):
        """Set text in output widget"""
        widget.configure(state=tk.NORMAL)
        widget.delete(1.0, tk.END)
        widget.insert(tk.END, text)
        widget.configure(state=tk.DISABLED)
    
    def assemble(self):
        """Assemble the source code"""
        source = self.source_text.get(1.0, tk.END)
        
        self.log_console("=" * 60, clear=True)
        self.log_console("RISC-V Assembler")
        self.log_console("=" * 60)
        
        try:
            asm = RISCVAssembler()
            asm.assemble(source)
            
            if asm.errors:
                # Show errors
                error_text = "ASSEMBLY ERRORS:\n" + "=" * 40 + "\n"
                for error in asm.errors:
                    error_text += f"  {error}\n"
                self.set_output_text(self.listing_text, error_text)
                self.log_console("❌ Assembly failed with errors")
                self.status_var.set("Assembly failed - see errors")
                self.output_notebook.select(3)  # Switch to console
                messagebox.showerror("Assembly Error", f"{len(asm.errors)} error(s) found")
                return
            
            # Generate listing
            listing = self.generate_listing(asm)
            self.set_output_text(self.listing_text, listing)
            
            # Generate hex
            hex_output = asm.to_hex()
            self.set_output_text(self.hex_text, hex_output)
            
            # Generate Verilog
            verilog_output = asm.to_verilog()
            self.set_output_text(self.verilog_text, verilog_output)
            
            # Log success
            self.log_console(f"✅ Assembly successful!")
            self.log_console(f"   Instructions: {len(asm.machine_code)}")
            self.log_console(f"   Size: {len(asm.machine_code) * 4} bytes")
            if asm.labels:
                self.log_console(f"   Labels: {', '.join(asm.labels.keys())}")
            
            self.status_var.set(f"Assembly successful - {len(asm.machine_code)} instructions")
            self.output_notebook.select(0)  # Switch to listing
            
        except Exception as e:
            self.log_console(f"❌ Error: {str(e)}")
            self.status_var.set("Assembly failed")
            messagebox.showerror("Error", str(e))
    
    def generate_listing(self, asm):
        """Generate assembly listing"""
        lines = []
        lines.append("=" * 70)
        lines.append("RISC-V ASSEMBLY LISTING")
        lines.append("=" * 70)
        lines.append(f"{'ADDR':<10} {'MACHINE CODE':<14} {'ASSEMBLY':<40}")
        lines.append("-" * 70)
        
        for code, (addr, instr, line_num) in zip(asm.machine_code, asm.instructions):
            lines.append(f"0x{addr:04X}     0x{code:08X}     {instr}")
        
        lines.append("-" * 70)
        lines.append(f"Total: {len(asm.machine_code)} instructions ({len(asm.machine_code) * 4} bytes)")
        lines.append("=" * 70)
        
        if asm.labels:
            lines.append("")
            lines.append("LABELS:")
            for label, addr in asm.labels.items():
                lines.append(f"  {label}: 0x{addr:04X}")
        
        return '\n'.join(lines)
    
    def new_file(self):
        """Create new file"""
        self.source_text.delete(1.0, tk.END)
        self.current_file = None
        self.root.title("RISC-V Assembler - New File")
        self.status_var.set("New file created")
    
    def open_file(self):
        """Open file dialog"""
        filename = filedialog.askopenfilename(
            title="Open Assembly File",
            filetypes=[("Assembly files", "*.asm"), ("All files", "*.*")]
        )
        if filename:
            try:
                with open(filename, 'r') as f:
                    content = f.read()
                self.source_text.delete(1.0, tk.END)
                self.source_text.insert(1.0, content)
                self.current_file = filename
                self.root.title(f"RISC-V Assembler - {os.path.basename(filename)}")
                self.status_var.set(f"Opened: {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Could not open file: {e}")
    
    def save_file(self):
        """Save current file"""
        if self.current_file:
            try:
                with open(self.current_file, 'w') as f:
                    f.write(self.source_text.get(1.0, tk.END))
                self.status_var.set(f"Saved: {self.current_file}")
            except Exception as e:
                messagebox.showerror("Error", f"Could not save file: {e}")
        else:
            self.save_file_as()
    
    def save_file_as(self):
        """Save file as dialog"""
        filename = filedialog.asksaveasfilename(
            title="Save Assembly File",
            defaultextension=".asm",
            filetypes=[("Assembly files", "*.asm"), ("All files", "*.*")]
        )
        if filename:
            try:
                with open(filename, 'w') as f:
                    f.write(self.source_text.get(1.0, tk.END))
                self.current_file = filename
                self.root.title(f"RISC-V Assembler - {os.path.basename(filename)}")
                self.status_var.set(f"Saved: {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Could not save file: {e}")
    
    def export_hex(self):
        """Export hex file"""
        # First assemble
        source = self.source_text.get(1.0, tk.END)
        try:
            asm = RISCVAssembler()
            asm.assemble(source)
            
            if asm.errors:
                messagebox.showerror("Error", "Cannot export - assembly has errors")
                return
            
            filename = filedialog.asksaveasfilename(
                title="Export Hex File",
                defaultextension=".hex",
                filetypes=[("Hex files", "*.hex"), ("All files", "*.*")]
            )
            if filename:
                with open(filename, 'w') as f:
                    f.write(asm.to_hex())
                self.status_var.set(f"Exported: {filename}")
                messagebox.showinfo("Success", f"Hex file exported to:\n{filename}")
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def export_verilog(self):
        """Export Verilog file"""
        source = self.source_text.get(1.0, tk.END)
        try:
            asm = RISCVAssembler()
            asm.assemble(source)
            
            if asm.errors:
                messagebox.showerror("Error", "Cannot export - assembly has errors")
                return
            
            filename = filedialog.asksaveasfilename(
                title="Export Verilog File",
                defaultextension=".v",
                filetypes=[("Verilog files", "*.v"), ("All files", "*.*")]
            )
            if filename:
                with open(filename, 'w') as f:
                    f.write(asm.to_verilog())
                self.status_var.set(f"Exported: {filename}")
                messagebox.showinfo("Success", f"Verilog file exported to:\n{filename}")
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def export_mem(self):
        """Export .mem file"""
        source = self.source_text.get(1.0, tk.END)
        try:
            asm = RISCVAssembler()
            asm.assemble(source)
            
            if asm.errors:
                messagebox.showerror("Error", "Cannot export - assembly has errors")
                return
            
            filename = filedialog.asksaveasfilename(
                title="Export .mem File",
                defaultextension=".mem",
                filetypes=[("Memory files", "*.mem"), ("All files", "*.*")]
            )
            if filename:
                with open(filename, 'w') as f:
                    f.write(asm.to_mem())
                self.status_var.set(f"Exported: {filename}")
                messagebox.showinfo("Success", f".mem file exported to:\n{filename}")
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def load_example(self, example_name):
        """Load example program"""
        examples = {
            'crypto': '''# Crypto Demo Program
# ====================

# Initialize
        addi x1, x0, 5          # limit = 5
        addi x2, x0, 0          # counter = 0
        addi x3, x0, 1          # increment = 1

# Loop 5 times
loop:
        add  x2, x2, x3         # counter++
        bne  x1, x2, loop       # while counter != limit

# Crypto operations
        rng  x11                # x11 = random
        rotl x12, x11, x3       # rotate left
        rotr x13, x11, x3       # rotate right
        xor  x14, x12, x13      # XOR mix

# Store results
        sw   x11, 0(x0)         # mem[0] = RNG
        sw   x12, 4(x0)         # mem[4] = ROTL
        sw   x13, 8(x0)         # mem[8] = ROTR
        sw   x14, 12(x0)        # mem[12] = XOR

# Store test value
        addi x10, x0, 25
        sw   x10, 100(x0)       # mem[100] = 25

# End
        halt
''',
            'fibonacci': '''# Fibonacci Sequence
# ==================

# Calculate first 10 Fibonacci numbers
        addi x1, x0, 10       # N = 10

# Initialize F(0) and F(1)
        addi x2, x0, 0        # F(0) = 0
        addi x3, x0, 1        # F(1) = 1

# Store first two values
        sw   x2, 0(x0)        # mem[0] = 0
        sw   x3, 4(x0)        # mem[4] = 1

# Loop setup
        addi x4, x0, 2        # counter = 2
        addi x5, x0, 8        # addr = 8

# Main loop
fib:
        add  x6, x2, x3       # F(n) = F(n-2) + F(n-1)
        sw   x6, 0(x5)        # store F(n)
        add  x2, x0, x3       # shift values
        add  x3, x0, x6
        addi x4, x4, 1        # counter++
        addi x5, x5, 4        # addr += 4
        bne  x4, x1, fib      # loop

        halt
''',
            'loop': '''# Simple Loop Example
# ===================

# Count from 1 to 10
        addi x1, x0, 10       # limit = 10
        addi x2, x0, 0        # sum = 0
        addi x3, x0, 1        # i = 1

loop:
        add  x2, x2, x3       # sum += i
        addi x3, x3, 1        # i++
        bne  x3, x1, loop     # while i != limit

# Result: x2 = 1+2+3+...+9 = 45
        sw   x2, 0(x0)        # store sum

        halt
'''
        }
        
        if example_name in examples:
            self.source_text.delete(1.0, tk.END)
            self.source_text.insert(1.0, examples[example_name])
            self.current_file = None
            self.root.title(f"RISC-V Assembler - {example_name}.asm")
            self.status_var.set(f"Loaded example: {example_name}")
    
    def load_sample_program(self):
        """Load initial sample program"""
        self.load_example('crypto')
    
    def show_reference(self):
        """Show instruction reference"""
        ref_window = tk.Toplevel(self.root)
        ref_window.title("RISC-V Instruction Reference")
        ref_window.geometry("600x500")
        ref_window.configure(bg='#2b2b2b')
        
        text = scrolledtext.ScrolledText(
            ref_window,
            wrap=tk.WORD,
            font=('Consolas', 10),
            bg='#1e1e1e',
            fg='#d4d4d4',
            padx=10,
            pady=10
        )
        text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        reference = """
RISC-V INSTRUCTION REFERENCE
=============================

R-TYPE (Register-Register)
--------------------------
add  rd, rs1, rs2    # rd = rs1 + rs2
sub  rd, rs1, rs2    # rd = rs1 - rs2
and  rd, rs1, rs2    # rd = rs1 & rs2
or   rd, rs1, rs2    # rd = rs1 | rs2
xor  rd, rs1, rs2    # rd = rs1 ^ rs2
sll  rd, rs1, rs2    # rd = rs1 << rs2
srl  rd, rs1, rs2    # rd = rs1 >> rs2 (logical)
sra  rd, rs1, rs2    # rd = rs1 >> rs2 (arithmetic)
slt  rd, rs1, rs2    # rd = (rs1 < rs2) ? 1 : 0

I-TYPE (Immediate)
------------------
addi rd, rs1, imm    # rd = rs1 + imm
andi rd, rs1, imm    # rd = rs1 & imm
ori  rd, rs1, imm    # rd = rs1 | imm
xori rd, rs1, imm    # rd = rs1 ^ imm

MEMORY
------
lw   rd, offset(rs1)    # Load word
sw   rs2, offset(rs1)   # Store word

BRANCHES
--------
beq  rs1, rs2, label    # Branch if equal
bne  rs1, rs2, label    # Branch if not equal
blt  rs1, rs2, label    # Branch if less than
bge  rs1, rs2, label    # Branch if greater/equal

JUMPS
-----
jal  rd, label          # Jump and link
jalr rd, offset(rs1)    # Jump and link register

CRYPTO EXTENSIONS
-----------------
rng  rd                 # rd = random number
rotl rd, rs1, rs2       # rd = rotate left
rotr rd, rs1, rs2       # rd = rotate right

SYSTEM
------
halt                    # Stop execution

REGISTERS
---------
x0/zero  - Always zero
x1/ra    - Return address
x2/sp    - Stack pointer
x10-x17  - a0-a7 (arguments)
x5-x7    - t0-t2 (temporaries)
"""
        text.insert(1.0, reference)
        text.configure(state=tk.DISABLED)
    
    def show_about(self):
        """Show about dialog"""
        messagebox.showinfo("About", 
            "RISC-V Assembler GUI\n"
            "Version 1.0\n\n"
            "For Single Cycle Processor Project\n"
            "Phase 5: Python Assembler\n\n"
            "Features:\n"
            "• Full RV32I Base ISA\n"
            "• Custom Crypto Extensions\n"
            "• Verilog Code Generation\n\n"
            "December 2025"
        )


def main():
    root = tk.Tk()
    app = RISCVAssemblerGUI(root)
    root.mainloop()


if __name__ == '__main__':
    main()
