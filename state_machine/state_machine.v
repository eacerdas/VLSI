module pattern_detector_EC (
    input InputLSB,
    input InputMSB,
    input clk,
    output reg second_letter_detected,
    output reg first_letter_detected
);

    // States definition
    parameter waiting_first_half_E = 0;                 //3'b000;
    parameter waiting_second_half_E = 1;                //3'b001;
    parameter waiting_first_half_C_and_E_detected = 2;  //3'b010;
    parameter waiting_second_half_C = 3;                //3'b011;
    parameter C_detected = 4;                           //3'b100;

    // Current and next state variables definition
    reg [2:0] current_state = waiting_first_half_E;
    reg [2:0] next_state = waiting_first_half_E;

    // Manages the next state logic
    always @(posedge clk) begin 
        current_state <= next_state;
    end

    // Manages the current state logic
    always @(posedge clk) begin 
        case(current_state)

            waiting_first_half_E: begin // waiting for a 11
                if((InputMSB == 1) && (InputLSB == 1)) begin
                    next_state = waiting_second_half_E; // Go to state 2
                end else begin
                    next_state = waiting_first_half_E; // Go to state 1
                end
            end

            waiting_second_half_E: begin // waiting for a 10
                if((InputMSB == 1) && (InputLSB == 0)) begin
                        next_state = waiting_first_half_C_and_E_detected; // Go to state 3
                    end else if ((InputMSB == 1) && (InputLSB == 1)) begin
                        next_state = waiting_second_half_E; // Go to state 2
                    end else begin
                        next_state = waiting_first_half_E; // Go to state 1
                    end
            end

            waiting_first_half_C_and_E_detected: begin // waiting for a 11
                if((InputMSB == 1) && (InputLSB == 1)) begin
                        next_state = waiting_second_half_C; // Go to state 4
                    end else begin
                        next_state = waiting_first_half_C_and_E_detected; // Go to state 3 --> don't turn first_letter_detected off
                    end
            end

            waiting_second_half_C: begin // waiting for a 00
                if((InputMSB == 0) && (InputLSB == 0)) begin
                        next_state = C_detected; // Go to state 5
                    end else if((InputMSB == 1) && (InputLSB == 1)) begin
                        next_state = waiting_second_half_C; // Go to state 4 
                    end else begin
                        next_state = waiting_first_half_C_and_E_detected; // Go to state 3 --> don't turn first_letter_detected off
                    end
            end

            C_detected: begin 
                next_state = waiting_first_half_E; // Go to state 1 --> start again
            end

            default: begin
                current_state = waiting_first_half_E;
            end

        endcase
    end

    // Manages the outputs
    always @(current_state) begin 

        case(current_state)
            waiting_first_half_E: begin // State 1
                second_letter_detected <= 0; first_letter_detected <= 0;
            end

            waiting_first_half_C_and_E_detected: begin // State 3
                second_letter_detected <= 0; first_letter_detected <= 1;
            end

            C_detected: begin // State 5
                second_letter_detected <= 1; first_letter_detected <= 1;
            end
            
        endcase
    end

endmodule

module testbench;
    // Inputs definition
    reg InputLSB, InputMSB, clk;
    // Outputs definition
    wire second_letter_detected, first_letter_detected;

    // pattern_detector_EC instance
    pattern_detector_EC pattern_detector_EC_1 (
        .InputLSB(InputLSB),
        .InputMSB(InputMSB),
        .second_letter_detected(second_letter_detected),
        .first_letter_detected(first_letter_detected),
        .clk(clk) 
    );

    initial begin
        $dumpfile("pattern_detector_EC.vcd");
        $dumpvars(0, testbench);
    end

    // Clock 
    initial begin
        clk = 0;
    end

    always begin
    #5 clk = ~clk;
    end


    // Stimulus
    initial begin

        #20; InputMSB <= 0; InputLSB <= 0; 
        #20; InputMSB <= 0; InputLSB <= 0; 
        #20; InputMSB <= 1; InputLSB <= 1; 
        #20; InputMSB <= 1; InputLSB <= 0; 
        #20; InputMSB <= 0; InputLSB <= 0; 
        #20; InputMSB <= 0; InputLSB <= 0; 
        #20; InputMSB <= 1; InputLSB <= 1; 
        #20; InputMSB <= 0; InputLSB <= 0;
        #20; InputMSB <= 0; InputLSB <= 0; 
        #20; InputMSB <= 0; InputLSB <= 0;
        #20; InputMSB <= 0; InputLSB <= 0; 
        #20; InputMSB <= 0; InputLSB <= 0; 
        #20; InputMSB <= 1; InputLSB <= 1; 
        #20; InputMSB <= 1; InputLSB <= 0; 
        #20; InputMSB <= 0; InputLSB <= 0; 
        #20; InputMSB <= 0; InputLSB <= 0; 
        #20; InputMSB <= 1; InputLSB <= 1; 
        #20; InputMSB <= 0; InputLSB <= 0;
        #20; InputMSB <= 0; InputLSB <= 0; 
        #20; InputMSB <= 0; InputLSB <= 0;

        #50
        
        $finish; // End of simulation
    end

    // Printing variables in console
    always @(posedge clk) begin
        $display("InputLSB=%b, InputMSB=%b, second_letter_detected=%b, first_letter_detected=%b", InputLSB, InputMSB, second_letter_detected, first_letter_detected);
    end

endmodule
