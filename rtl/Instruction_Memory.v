`timescale 1ns / 1ps
// =============================================================================
// RISC-V Instruction Memory
// Phase 3: Crypto Extensions Test Program (ROTL, ROTR, RNG)
// =============================================================================

module Instruction_Memory(
    input [31:0] A,
    output [31:0] RD
);

    reg [31:0] I_MEM_BLOCK[63:0];
    
    initial begin
        // =====================================================================
        // PHASE 3 TEST PROGRAM: Crypto Extensions Verification
        // =====================================================================
        // This program tests:
        //   1. RNG  - Random Number Generator (generates pseudo-random value)
        //   2. ROTL - Rotate Left instruction
        //   3. ROTR - Rotate Right instruction
        //   4. XOR mixing for cryptographic operations
        //   5. Store results for verification
        //
        // Custom Opcode: 7'b0001011 (0x0B)
        //   - funct3=100 (0x4): RNG
        //   - funct3=010 (0x2): ROTL  
        //   - funct3=011 (0x3): ROTR
        //
        // Encoding: funct7[6:0] | rs2[4:0] | rs1[4:0] | funct3[2:0] | rd[4:0] | opcode[6:0]
        // =====================================================================
        
        // --- Phase 1 & 2 Tests (BNE loop + JAL) ---
        I_MEM_BLOCK[0]  = 32'h00500093;  // 0x00: addi x1, x0, 5    | x1 = 5 (loop limit)
        I_MEM_BLOCK[1]  = 32'h00000113;  // 0x04: addi x2, x0, 0    | x2 = 0 (counter)
        I_MEM_BLOCK[2]  = 32'h00100193;  // 0x08: addi x3, x0, 1    | x3 = 1 (increment)
        I_MEM_BLOCK[3]  = 32'h00310133;  // 0x0C: add x2, x2, x3    | x2++ [LOOP START]
        I_MEM_BLOCK[4]  = 32'hFE209CE3;  // 0x10: bne x1, x2, -8    | if(x1!=x2) goto 0x0C
        I_MEM_BLOCK[5]  = 32'h00210533;  // 0x14: add x10, x2, x2   | x10 = 10 (verify BNE)
        
        // --- Phase 3: Crypto Extensions Demo ---
        // RNG instruction: opcode=0001011, funct3=100, rd=x11
        // Encoding: 0000000_00000_00000_100_01011_0001011 = 0x0000450B
        I_MEM_BLOCK[6]  = 32'h0000450B;  // 0x18: rng x11           | x11 = random number
        
        // ROTL instruction: opcode=0001011, funct3=010, rs1=x11, rs2=x3(=1), rd=x12
        // Encoding: 0000000_00011_01011_010_01100_0001011 = 0x0035A60B
        I_MEM_BLOCK[7]  = 32'h0035A60B;  // 0x1C: rotl x12, x11, x3 | x12 = rotl(x11, 1)
        
        // ROTR instruction: opcode=0001011, funct3=011, rs1=x11, rs2=x3(=1), rd=x13
        // Encoding: 0000000_00011_01011_011_01101_0001011 = 0x0035B68B
        I_MEM_BLOCK[8]  = 32'h0035B68B;  // 0x20: rotr x13, x11, x3 | x13 = rotr(x11, 1)
        
        // XOR mixing: x14 = x12 ^ x13 (crypto mixing)
        I_MEM_BLOCK[9]  = 32'h00D64733;  // 0x24: xor x14, x12, x13 | x14 = x12 ^ x13
        
        // Store results for verification
        I_MEM_BLOCK[10] = 32'h00B02023;  // 0x28: sw x11, 0(x0)     | mem[0] = RNG result
        I_MEM_BLOCK[11] = 32'h00C02223;  // 0x2C: sw x12, 4(x0)     | mem[4] = ROTL result
        I_MEM_BLOCK[12] = 32'h00D02423;  // 0x30: sw x13, 8(x0)     | mem[8] = ROTR result
        I_MEM_BLOCK[13] = 32'h00E02623;  // 0x34: sw x14, 12(x0)    | mem[12] = XOR result
        
        // Store expected test value (25) at address 100
        I_MEM_BLOCK[14] = 32'h01900513;  // 0x38: addi x10, x0, 25  | x10 = 25
        I_MEM_BLOCK[15] = 32'h06A02223;  // 0x3C: sw x10, 100(x0)   | mem[100] = 25
        
        // HALT
        I_MEM_BLOCK[16] = 32'h00000073;  // 0x40: ecall             | HALT
        
        // --- Fill remaining with NOPs ---
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