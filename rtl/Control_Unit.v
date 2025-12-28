`timescale 1ns / 1ps
/*
 * Copyright (c) 2023 Govardhan
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 * THE SOFTWARE.
 */
module Control_Unit(
		    input wire [6:0]  op,
		    input wire [2:0]  funct3,
		    input wire	      funct7b5, Zero, // function 7 is the 5th bit

		    output wire [1:0] ResultSrc,
		    output wire	      MemWrite, PCSrc, ALUSrc, RegWrite, Jump,
		    output wire [1:0] ImmSrc,
		    output wire [3:0] ALUControl,
		    output wire       Halt

		    );

   // Internal signals before HALT masking
   wire MemWrite_internal;
   wire RegWrite_internal;

   wire [1:0]			      ALUop;
   wire				      Branch;
   
   Main_Decoder Main_Decoder(
  			     .op(op),
			     .ResultSrc(ResultSrc),
			     .MemWrite(MemWrite_internal),
			     .Branch(Branch),
  			     .ALUSrc(ALUSrc),
			     .RegWrite(RegWrite_internal),
  			     .Jump(Jump),
			     .ImmSrc(ImmSrc),
			     .ALUop(ALUop) );
   
   ALU_Decoder ALU_Decoder(
  			   .opb5(op[5]),
			   .funct3(funct3),
			   .funct7b5(funct7b5),
			   .ALUOp(ALUop),
			   .ALUControl(ALUControl) );
   
   //for branches beq, bne, blt, bge, bltu, bgeu
   //make modifications later - get sign from ALU, make conditions for all branches  
  
   // =========================================================================
   // PHASE 2: BRANCH INSTRUCTION SUPPORT
   // =========================================================================
   // Branch types based on funct3:
   //   000 = BEQ  (Branch if Equal)          -> branch if Zero=1
   //   001 = BNE  (Branch if Not Equal)      -> branch if Zero=0
   //   100 = BLT  (Branch if Less Than)      -> TODO: need sign bit
   //   101 = BGE  (Branch if Greater/Equal)  -> TODO: need sign bit
   //   110 = BLTU (Branch if Less Unsigned)  -> TODO: need carry bit
   //   111 = BGEU (Branch if Greater Unsigned) -> TODO: need carry bit
   // =========================================================================
   
   reg BranchTaken;
   
   always @(*) begin
       case (funct3)
           3'b000:  BranchTaken = Zero;      // BEQ: branch if equal
           3'b001:  BranchTaken = ~Zero;     // BNE: branch if not equal
           default: BranchTaken = Zero;      // Default to BEQ behavior
       endcase
   end
   
   assign PCSrc = (Branch & BranchTaken) | Jump;
   
   // =========================================================================
   // HALT INSTRUCTION SUPPORT (ECALL opcode: 7'b1110011)
   // =========================================================================
   // When HALT is active:
   //   - PC stops incrementing (handled externally via PCEn)
   //   - Memory writes are disabled
   //   - Register writes are disabled
   //   - CPU enters frozen state
   // =========================================================================
   assign Halt = (op == 7'b1110011); // ECALL treated as HALT
   
   // Mask write enables when processor is halted
   // This prevents any unintended state changes after HALT
   assign MemWrite = MemWrite_internal & ~Halt;
   assign RegWrite = RegWrite_internal & ~Halt;

   
endmodule
