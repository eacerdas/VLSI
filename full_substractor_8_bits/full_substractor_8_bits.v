module r_c_1_bit (x,y,z,d,b);
    // Ports
    input x, y, z;
    output d, b;

    //Data flow
    assign d = (~x & ~y & z) | (~x & y & ~z) | (x & ~y & ~z) | (x & y & z);
    assign b = (~x & y) | (~x & z) | (y & z);
endmodule

module estimulo_1_bit;
    // Inputs
    reg X, Y, Z;
    // Outputs
    wire D, B;

    // Instance of 1 bit substractor
    r_c_1_bit substractor_1bit (X, Y, Z, D, B);

    initial begin
        $display("x y z | D B");
        $monitor($time, ": X=%b, Y=%b, Z=%b, --- PRESTAMO=%b,RESTA=%b\n",X,Y,Z,B,D);

        // Stimulus inputs
        X = 0; Y = 0; Z = 0; #5;
        X = 0; Y = 0; Z = 1; #5;
        X = 0; Y = 1; Z = 0; #5;
        X = 0; Y = 1; Z = 1; #5;
        X = 1; Y = 0; Z = 0; #5;
        X = 1; Y = 0; Z = 1; #5;
        X = 1; Y = 1; Z = 0; #5;
        X = 1; Y = 1; Z = 1; #5;

        $finish;
    end

endmodule

module r_c_8_bit_subtractor(x, y, z, d, b);
  // Inputs
  input [7:0] x, y;
  input z;
  // Outputs
  output [7:0] d;
  output b;

  // Internal Nets
  wire [7:0] d_int;
  wire [6:0] b_int;

  // 1-bit subtractor instances
  r_c_1_bit subtractor_0(x[0], y[0],        z, d_int[0], b_int[0]);
  r_c_1_bit subtractor_1(x[1], y[1], b_int[0], d_int[1], b_int[1]);
  r_c_1_bit subtractor_2(x[2], y[2], b_int[1], d_int[2], b_int[2]);
  r_c_1_bit subtractor_3(x[3], y[3], b_int[2], d_int[3], b_int[3]);
  r_c_1_bit subtractor_4(x[4], y[4], b_int[3], d_int[4], b_int[4]);
  r_c_1_bit subtractor_5(x[5], y[5], b_int[4], d_int[5], b_int[5]);
  r_c_1_bit subtractor_6(x[6], y[6], b_int[5], d_int[6], b_int[6]);
  r_c_1_bit subtractor_7(x[7], y[7], b_int[6], d_int[7], b);

  // Output connections
  assign d = d_int;
  assign b = b_int[6];

endmodule

module estimulo_8_bit;
  
    // Inputs
    reg [7:0] X, Y;
    reg Z;
    
    // Outputs
    wire [7:0] D;
    wire B;

    r_c_8_bit_subtractor substractor_8bits (X, Y, Z, D, B);

    initial begin
        $display("X Y Z | D B");
        $monitor($time, ": X=%b, Y=%b, Z=%b, --- PRESTAMO=%b,RESTA=%b\n",X,Y,Z,B,D);

        // Combinaciones de entradas
        X = 8'b00000000; Y = 8'b00000000; Z = 0; #5;
        X = 8'b00000000; Y = 8'b11111111; Z = 0; #5;
        X = 8'b11111111; Y = 8'b00000000; Z = 0; #5;
        X = 8'b11111111; Y = 8'b11111111; Z = 0; #5;
        X = 8'b00000000; Y = 8'b00000000; Z = 1; #5;
        X = 8'b00000000; Y = 8'b11111111; Z = 1; #5;
        X = 8'b11111111; Y = 8'b00000000; Z = 1; #5;
        X = 8'b11111111; Y = 8'b11111111; Z = 1; #5;

        $finish;
    end

endmodule


