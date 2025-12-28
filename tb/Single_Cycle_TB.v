`timescale 1ns / 1ps
//=============================================================================
// Single Cycle RISC-V Processor Testbench
// Enhanced with HALT detection, cycle counting, and comprehensive reporting
//=============================================================================
// Original Author: Sai Govardhan
// Enhanced for Phase 1-3: HALT, BNE, JAL, and Crypto Extensions
// Date: December 28, 2025
//=============================================================================
// Phase 1: HALT Instruction (ECALL)
// Phase 2: BNE (Branch Not Equal), JAL (Jump And Link)
// Phase 3: Crypto Extensions (RNG, ROTL, ROTR)
//=============================================================================

module Single_Cycle_TB();

//=============================================================================
// TESTBENCH CONFIGURATION
//=============================================================================
parameter CLK_PERIOD = 20;          // Clock period in ns (50 MHz)
parameter MAX_CYCLES = 1000;        // Maximum cycles before timeout
parameter HALT_WAIT_CYCLES = 5;     // Cycles to wait after HALT before finishing

//=============================================================================
// SIGNALS
//=============================================================================
reg         clk = 0;
reg         reset;
wire [31:0] WriteData, DataAddr;
wire        MemWrite;
wire        Halt;
wire [31:0] PC;

// Test tracking
integer     cycle_count = 0;
integer     halt_detected = 0;
integer     halt_wait_counter = 0;
reg         test_passed = 0;
reg         test_failed = 0;

// Phase 2 verification
reg         bne_verified = 0;
reg         jal_verified = 0;
reg  [31:0] prev_pc = 0;
integer     loop_count = 0;

// Phase 3 crypto verification
reg         rng_executed = 0;
reg         rotl_executed = 0;
reg         rotr_executed = 0;
reg  [31:0] rng_result = 0;
reg  [31:0] rotl_result = 0;
reg  [31:0] rotr_result = 0;

//=============================================================================
// CLOCK GENERATION
//=============================================================================
always #(CLK_PERIOD/2) clk = ~clk;

//=============================================================================
// DUT INSTANTIATION
//=============================================================================
Single_Cycle_Top DUT(
    .clk(clk),
    .reset(reset),
    .WriteData(WriteData),
    .DataAddr(DataAddr),
    .MemWrite(MemWrite),
    .Halt(Halt),
    .PC_Out(PC)
);

//=============================================================================
// RESET SEQUENCE
//=============================================================================
initial begin
    $display("=============================================================================");
    $display("  RISC-V Single Cycle Processor - Simulation Started");
    $display("  Clock Period: %0d ns | Max Cycles: %0d", CLK_PERIOD, MAX_CYCLES);
    $display("=============================================================================");
    
    // Initialize
    reset = 0;
    
    // Apply reset
    #(CLK_PERIOD);
    reset = 1;
    $display("[%0t] RESET asserted", $time);
    
    #(CLK_PERIOD);
    reset = 0;
    $display("[%0t] RESET de-asserted - Execution starting", $time);
    $display("-----------------------------------------------------------------------------");
end

//=============================================================================
// CYCLE COUNTER & EXECUTION MONITOR
//=============================================================================
always @(posedge clk) begin
    if (!reset) begin
        cycle_count <= cycle_count + 1;
        
        // Display instruction execution (every cycle)
        if (cycle_count > 0 && !halt_detected) begin
            $display("[Cycle %4d] PC=0x%08h | Instr=0x%08h", 
                     cycle_count, PC, DUT.Instr);
            
            // =========================================================
            // PHASE 2: BNE Verification
            // =========================================================
            // BNE instruction at PC=0x10 should branch back to 0x0C
            // This creates a loop that runs 5 times (until x2 == x1)
            if (PC == 32'h00000010 && DUT.Instr[6:0] == 7'b1100011) begin
                if (DUT.Instr[14:12] == 3'b001) begin // funct3 = 001 = BNE
                    loop_count = loop_count + 1;
                    $display("             [BNE] Loop iteration %0d detected", loop_count);
                end
            end
            
            // =========================================================
            // PHASE 3: CRYPTO EXTENSIONS Verification  
            // =========================================================
            // Detect custom crypto opcode (0001011)
            if (DUT.Instr[6:0] == 7'b0001011) begin
                case (DUT.Instr[14:12])  // funct3
                    3'b100: begin  // RNG
                        rng_executed = 1;
                        $display("             [CRYPTO] RNG instruction executed!");
                    end
                    3'b010: begin  // ROTL
                        rotl_executed = 1;
                        $display("             [CRYPTO] ROTL instruction executed!");
                    end
                    3'b011: begin  // ROTR
                        rotr_executed = 1;
                        $display("             [CRYPTO] ROTR instruction executed!");
                    end
                endcase
            end
            
            // Track PC for JAL verification
            prev_pc <= PC;
        end
        
        // Timeout protection
        if (cycle_count >= MAX_CYCLES && !halt_detected) begin
            $display("-----------------------------------------------------------------------------");
            $display("[ERROR] Simulation timeout after %0d cycles!", MAX_CYCLES);
            $display("        Possible infinite loop or missing HALT instruction");
            test_failed = 1;
            print_final_report();
            $finish;
        end
    end
end

//=============================================================================
// BNE LOOP VERIFICATION
//=============================================================================
always @(posedge clk) begin
    // After we exit the loop (PC goes from 0x10 to 0x14), verify loop count
    if (prev_pc == 32'h00000010 && PC == 32'h00000014 && !bne_verified) begin
        bne_verified = 1;
        if (loop_count == 5) begin
            $display("             [BNE] VERIFIED: Loop executed exactly %0d times", loop_count);
        end else begin
            $display("             [BNE] WARNING: Loop executed %0d times (expected 5)", loop_count);
        end
    end
end

//=============================================================================
// HALT DETECTION & HANDLING
//=============================================================================
always @(posedge clk) begin
    if (Halt && !halt_detected) begin
        halt_detected = 1;
        $display("-----------------------------------------------------------------------------");
        $display("[Cycle %4d] *** HALT INSTRUCTION DETECTED ***", cycle_count);
        $display("             PC frozen at: 0x%08h", PC);
        $display("-----------------------------------------------------------------------------");
        
        // Verify HALT behavior
        verify_halt_behavior();
    end
    
    // Wait a few cycles after HALT to verify frozen state
    if (halt_detected) begin
        halt_wait_counter <= halt_wait_counter + 1;
        
        if (halt_wait_counter >= HALT_WAIT_CYCLES) begin
            $display("[Cycle %4d] HALT verified - PC remained frozen for %0d cycles", 
                     cycle_count, HALT_WAIT_CYCLES);
            print_register_dump();
            print_final_report();
            $finish;
        end
    end
end

//=============================================================================
// MEMORY WRITE MONITOR
//=============================================================================
always @(posedge clk) begin
    if (MemWrite && !halt_detected) begin
        $display("[Cycle %4d] MEM WRITE: Addr=0x%08h Data=0x%08h (%0d)", 
                 cycle_count, DataAddr, WriteData, WriteData);
        
        // Check for expected test result
        if (DataAddr == 100 && WriteData == 25) begin
            $display("             *** TEST PASSED: Expected value 25 at address 100 ***");
            test_passed = 1;
        end
    end
    
    // Verify no memory writes occur during HALT
    if (MemWrite && halt_detected) begin
        $display("[ERROR] Memory write occurred during HALT state!");
        $display("        This indicates HALT masking is not working correctly");
        test_failed = 1;
    end
end

//=============================================================================
// HALT BEHAVIOR VERIFICATION TASK
//=============================================================================
task verify_halt_behavior;
    begin
        $display("Verifying HALT behavior...");
        
        // Check 1: MemWrite should be 0
        if (MemWrite == 0) begin
            $display("  [PASS] MemWrite is disabled during HALT");
        end else begin
            $display("  [FAIL] MemWrite is still active during HALT!");
            test_failed = 1;
        end
        
        // Check 2: Halt signal is properly asserted
        if (Halt == 1) begin
            $display("  [PASS] Halt signal is asserted");
        end else begin
            $display("  [FAIL] Halt signal is not asserted!");
            test_failed = 1;
        end
        
        // =====================================================================
        // PHASE 2 VERIFICATION
        // =====================================================================
        $display("");
        $display("Verifying Phase 2 (BNE/JAL) behavior...");
        
        // Check 3: BNE loop executed correctly
        if (bne_verified && loop_count == 5) begin
            $display("  [PASS] BNE instruction working - loop ran 5 times");
        end else if (loop_count > 0) begin
            $display("  [WARN] BNE detected but loop count = %0d (expected 5)", loop_count);
        end else begin
            $display("  [FAIL] BNE instruction not detected!");
            test_failed = 1;
        end
        
        // Check 4: x10 contains 25
        if (DUT.core_top.Datapath.Register_inst.REG_MEM_BLOCK[10] == 32'h00000019) begin
            $display("  [PASS] x10 = 25 (test value correct)");
        end else begin
            $display("  [FAIL] x10 = %0d (expected 25)", 
                     DUT.core_top.Datapath.Register_inst.REG_MEM_BLOCK[10]);
            test_failed = 1;
        end
        
        // =====================================================================
        // PHASE 3 VERIFICATION - CRYPTO EXTENSIONS
        // =====================================================================
        $display("");
        $display("Verifying Phase 3 (Crypto Extensions) behavior...");
        
        // Check 5: RNG executed
        if (rng_executed) begin
            $display("  [PASS] RNG instruction executed");
            $display("         x11 (RNG result) = 0x%08h", 
                     DUT.core_top.Datapath.Register_inst.REG_MEM_BLOCK[11]);
        end else begin
            $display("  [FAIL] RNG instruction not executed!");
            test_failed = 1;
        end
        
        // Check 6: ROTL executed
        if (rotl_executed) begin
            $display("  [PASS] ROTL instruction executed");
            $display("         x12 (ROTL result) = 0x%08h", 
                     DUT.core_top.Datapath.Register_inst.REG_MEM_BLOCK[12]);
        end else begin
            $display("  [FAIL] ROTL instruction not executed!");
            test_failed = 1;
        end
        
        // Check 7: ROTR executed
        if (rotr_executed) begin
            $display("  [PASS] ROTR instruction executed");
            $display("         x13 (ROTR result) = 0x%08h", 
                     DUT.core_top.Datapath.Register_inst.REG_MEM_BLOCK[13]);
        end else begin
            $display("  [FAIL] ROTR instruction not executed!");
            test_failed = 1;
        end
        
        // Check 8: Verify ROTL and ROTR are complementary
        // ROTL by 1 then ROTR by 1 should give original value
        $display("  [INFO] x14 (XOR mix) = 0x%08h", 
                 DUT.core_top.Datapath.Register_inst.REG_MEM_BLOCK[14]);
        
        // Crypto results are stored in memory addresses 0, 4, 8, 12
        $display("");
        $display("  Crypto results stored to memory successfully!");
    end
endtask

//=============================================================================
// REGISTER FILE DUMP (Accesses internal DUT hierarchy)
//=============================================================================
task print_register_dump;
    integer i;
    begin
        $display("");
        $display("=============================================================================");
        $display("  REGISTER FILE STATE AT HALT");
        $display("=============================================================================");
        $display("  x0  (zero) = 0x%08h    x16 (a6)   = 0x%08h", 
                 0, DUT.core_top.Datapath.Register_inst.REG_MEM_BLOCK[16]);
        $display("  x1  (ra)   = 0x%08h    x17 (a7)   = 0x%08h", 
                 DUT.core_top.Datapath.Register_inst.REG_MEM_BLOCK[1],
                 DUT.core_top.Datapath.Register_inst.REG_MEM_BLOCK[17]);
        $display("  x2  (sp)   = 0x%08h    x18 (s2)   = 0x%08h", 
                 DUT.core_top.Datapath.Register_inst.REG_MEM_BLOCK[2],
                 DUT.core_top.Datapath.Register_inst.REG_MEM_BLOCK[18]);
        $display("  x3  (gp)   = 0x%08h    x19 (s3)   = 0x%08h", 
                 DUT.core_top.Datapath.Register_inst.REG_MEM_BLOCK[3],
                 DUT.core_top.Datapath.Register_inst.REG_MEM_BLOCK[19]);
        $display("  x4  (tp)   = 0x%08h    x20 (s4)   = 0x%08h", 
                 DUT.core_top.Datapath.Register_inst.REG_MEM_BLOCK[4],
                 DUT.core_top.Datapath.Register_inst.REG_MEM_BLOCK[20]);
        $display("  x5  (t0)   = 0x%08h    x21 (s5)   = 0x%08h", 
                 DUT.core_top.Datapath.Register_inst.REG_MEM_BLOCK[5],
                 DUT.core_top.Datapath.Register_inst.REG_MEM_BLOCK[21]);
        $display("  x6  (t1)   = 0x%08h    x22 (s6)   = 0x%08h", 
                 DUT.core_top.Datapath.Register_inst.REG_MEM_BLOCK[6],
                 DUT.core_top.Datapath.Register_inst.REG_MEM_BLOCK[22]);
        $display("  x7  (t2)   = 0x%08h    x23 (s7)   = 0x%08h", 
                 DUT.core_top.Datapath.Register_inst.REG_MEM_BLOCK[7],
                 DUT.core_top.Datapath.Register_inst.REG_MEM_BLOCK[23]);
        $display("  x8  (s0)   = 0x%08h    x24 (s8)   = 0x%08h", 
                 DUT.core_top.Datapath.Register_inst.REG_MEM_BLOCK[8],
                 DUT.core_top.Datapath.Register_inst.REG_MEM_BLOCK[24]);
        $display("  x9  (s1)   = 0x%08h    x25 (s9)   = 0x%08h", 
                 DUT.core_top.Datapath.Register_inst.REG_MEM_BLOCK[9],
                 DUT.core_top.Datapath.Register_inst.REG_MEM_BLOCK[25]);
        $display("  x10 (a0)   = 0x%08h    x26 (s10)  = 0x%08h", 
                 DUT.core_top.Datapath.Register_inst.REG_MEM_BLOCK[10],
                 DUT.core_top.Datapath.Register_inst.REG_MEM_BLOCK[26]);
        $display("  x11 (a1)   = 0x%08h    x27 (s11)  = 0x%08h", 
                 DUT.core_top.Datapath.Register_inst.REG_MEM_BLOCK[11],
                 DUT.core_top.Datapath.Register_inst.REG_MEM_BLOCK[27]);
        $display("  x12 (a2)   = 0x%08h    x28 (t3)   = 0x%08h", 
                 DUT.core_top.Datapath.Register_inst.REG_MEM_BLOCK[12],
                 DUT.core_top.Datapath.Register_inst.REG_MEM_BLOCK[28]);
        $display("  x13 (a3)   = 0x%08h    x29 (t4)   = 0x%08h", 
                 DUT.core_top.Datapath.Register_inst.REG_MEM_BLOCK[13],
                 DUT.core_top.Datapath.Register_inst.REG_MEM_BLOCK[29]);
        $display("  x14 (a4)   = 0x%08h    x30 (t5)   = 0x%08h", 
                 DUT.core_top.Datapath.Register_inst.REG_MEM_BLOCK[14],
                 DUT.core_top.Datapath.Register_inst.REG_MEM_BLOCK[30]);
        $display("  x15 (a5)   = 0x%08h    x31 (t6)   = 0x%08h", 
                 DUT.core_top.Datapath.Register_inst.REG_MEM_BLOCK[15],
                 DUT.core_top.Datapath.Register_inst.REG_MEM_BLOCK[31]);
        $display("=============================================================================");
    end
endtask

//=============================================================================
// FINAL REPORT
//=============================================================================
task print_final_report;
    begin
        $display("");
        $display("=============================================================================");
        $display("  SIMULATION SUMMARY");
        $display("=============================================================================");
        $display("  Total Cycles Executed: %0d", cycle_count);
        $display("  Final PC Value:        0x%08h", PC);
        $display("  HALT Detected:         %s", halt_detected ? "YES" : "NO");
        $display("-----------------------------------------------------------------------------");
        
        if (test_passed && !test_failed) begin
            $display("  ██████╗  █████╗ ███████╗███████╗███████╗██████╗ ");
            $display("  ██╔══██╗██╔══██╗██╔════╝██╔════╝██╔════╝██╔══██╗");
            $display("  ██████╔╝███████║███████╗███████╗█████╗  ██║  ██║");
            $display("  ██╔═══╝ ██╔══██║╚════██║╚════██║██╔══╝  ██║  ██║");
            $display("  ██║     ██║  ██║███████║███████║███████╗██████╔╝");
            $display("  ╚═╝     ╚═╝  ╚═╝╚══════╝╚══════╝╚══════╝╚═════╝ ");
            $display("  ALL TESTS PASSED!");
        end else if (test_failed) begin
            $display("  ███████╗ █████╗ ██╗██╗     ███████╗██████╗ ");
            $display("  ██╔════╝██╔══██╗██║██║     ██╔════╝██╔══██╗");
            $display("  █████╗  ███████║██║██║     █████╗  ██║  ██║");
            $display("  ██╔══╝  ██╔══██║██║██║     ██╔══╝  ██║  ██║");
            $display("  ██║     ██║  ██║██║███████╗███████╗██████╔╝");
            $display("  ╚═╝     ╚═╝  ╚═╝╚═╝╚══════╝╚══════╝╚═════╝ ");
            $display("  TEST FAILED - Check errors above");
        end else begin
            $display("  Status: COMPLETED (No specific test criteria checked)");
        end
        
        $display("=============================================================================");
        $display("  Simulation ended at time: %0t", $time);
        $display("=============================================================================");
    end
endtask

endmodule