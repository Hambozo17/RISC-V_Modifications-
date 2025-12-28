`timescale 1ns / 1ps
//=============================================================================
// HALT Instruction Test - Instruction Memory with Simple HALT Test
//=============================================================================
// This test program verifies the HALT instruction functionality:
//   1. Load some values into registers
//   2. Perform simple ALU operations
//   3. Execute HALT to freeze the processor
//
// Expected behavior:
//   - PC should freeze at HALT instruction address
//   - No memory writes should occur after HALT
//   - No register writes should occur after HALT
//=============================================================================

module Instruction_Memory_HALT_Test(
    input [31:0] A,
    output [31:0] RD
);

    reg [31:0] I_MEM_BLOCK[63:0];
    
    initial begin
        //=====================================================================
        // HALT TEST PROGRAM
        //=====================================================================
        // Assembly:
        //   addi x1, x0, 5      # x1 = 5
        //   addi x2, x0, 10     # x2 = 10  
        //   add  x3, x1, x2     # x3 = 15
        //   addi x4, x0, 25     # x4 = 25
        //   sw   x4, 100(x0)    # Store 25 to address 100
        //   halt                # ECALL - Stop execution
        //   addi x5, x0, 99     # Should NOT execute (after HALT)
        //=====================================================================
        
        I_MEM_BLOCK[0]  = 32'h00500093;  // addi x1, x0, 5
        I_MEM_BLOCK[1]  = 32'h00A00113;  // addi x2, x0, 10
        I_MEM_BLOCK[2]  = 32'h002081B3;  // add  x3, x1, x2
        I_MEM_BLOCK[3]  = 32'h01900213;  // addi x4, x0, 25
        I_MEM_BLOCK[4]  = 32'h06402223;  // sw   x4, 100(x0)
        I_MEM_BLOCK[5]  = 32'h00000073;  // ECALL (HALT)
        I_MEM_BLOCK[6]  = 32'h06300293;  // addi x5, x0, 99 (should NOT execute)
        
        // Fill rest with NOPs
        I_MEM_BLOCK[7]  = 32'h00000013;
        I_MEM_BLOCK[8]  = 32'h00000013;
        I_MEM_BLOCK[9]  = 32'h00000013;
        I_MEM_BLOCK[10] = 32'h00000013;
        I_MEM_BLOCK[11] = 32'h00000013;
        I_MEM_BLOCK[12] = 32'h00000013;
        I_MEM_BLOCK[13] = 32'h00000013;
        I_MEM_BLOCK[14] = 32'h00000013;
        I_MEM_BLOCK[15] = 32'h00000013;
        I_MEM_BLOCK[16] = 32'h00000013;
        I_MEM_BLOCK[17] = 32'h00000013;
        I_MEM_BLOCK[18] = 32'h00000013;
        I_MEM_BLOCK[19] = 32'h00000013;
        I_MEM_BLOCK[20] = 32'h00000013;
        I_MEM_BLOCK[21] = 32'h00000013;
        I_MEM_BLOCK[22] = 32'h00000013;
        I_MEM_BLOCK[23] = 32'h00000013;
        I_MEM_BLOCK[24] = 32'h00000013;
        I_MEM_BLOCK[25] = 32'h00000013;
        I_MEM_BLOCK[26] = 32'h00000013;
        I_MEM_BLOCK[27] = 32'h00000013;
        I_MEM_BLOCK[28] = 32'h00000013;
        I_MEM_BLOCK[29] = 32'h00000013;
        I_MEM_BLOCK[30] = 32'h00000013;
        I_MEM_BLOCK[31] = 32'h00000013;
        I_MEM_BLOCK[32] = 32'h00000013;
        I_MEM_BLOCK[33] = 32'h00000013;
        I_MEM_BLOCK[34] = 32'h00000013;
        I_MEM_BLOCK[35] = 32'h00000013;
        I_MEM_BLOCK[36] = 32'h00000013;
        I_MEM_BLOCK[37] = 32'h00000013;
        I_MEM_BLOCK[38] = 32'h00000013;
        I_MEM_BLOCK[39] = 32'h00000013;
        I_MEM_BLOCK[40] = 32'h00000013;
        I_MEM_BLOCK[41] = 32'h00000013;
        I_MEM_BLOCK[42] = 32'h00000013;
        I_MEM_BLOCK[43] = 32'h00000013;
        I_MEM_BLOCK[44] = 32'h00000013;
        I_MEM_BLOCK[45] = 32'h00000013;
        I_MEM_BLOCK[46] = 32'h00000013;
        I_MEM_BLOCK[47] = 32'h00000013;
        I_MEM_BLOCK[48] = 32'h00000013;
        I_MEM_BLOCK[49] = 32'h00000013;
        I_MEM_BLOCK[50] = 32'h00000013;
        I_MEM_BLOCK[51] = 32'h00000013;
        I_MEM_BLOCK[52] = 32'h00000013;
        I_MEM_BLOCK[53] = 32'h00000013;
        I_MEM_BLOCK[54] = 32'h00000013;
        I_MEM_BLOCK[55] = 32'h00000013;
        I_MEM_BLOCK[56] = 32'h00000013;
        I_MEM_BLOCK[57] = 32'h00000013;
        I_MEM_BLOCK[58] = 32'h00000013;
        I_MEM_BLOCK[59] = 32'h00000013;
        I_MEM_BLOCK[60] = 32'h00000013;
        I_MEM_BLOCK[61] = 32'h00000013;
        I_MEM_BLOCK[62] = 32'h00000013;
        I_MEM_BLOCK[63] = 32'h00000013;
    end
    
    assign RD = I_MEM_BLOCK[A[31:2]]; // word aligned
    
endmodule
