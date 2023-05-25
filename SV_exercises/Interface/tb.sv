`include "interface.sv"
// Testbench Code Goes here
module arbiter_tb;
  
	logic clock;
  intf_arbiter arb_bus(clock); //reset, req_0, req_1, gnt_0, gnt_1;
  
initial begin

  $dumpfile("test.vcd");
  $dumpvars(0);

  $monitor("req0=%b, req1=%b, gnt0=%b, gnt1=%b", arb_bus.req_0, arb_bus.req_1, arb_bus.gnt_0, arb_bus.gnt_1);
  
  clock = 0;
  arb_bus.reset = 0;
  arb_bus.req_0 = 0;
  arb_bus.req_1 = 0;
  #5  arb_bus.reset = 1;
  #15 arb_bus.reset = 0;
  #10 arb_bus.req_0  = 1;
  #10 arb_bus.req_0  = 0;
  #10 arb_bus.req_1  = 1;
  #10 arb_bus.req_1  = 0;
  #10 {arb_bus.req_0,arb_bus.req_1} = 2'b11;
  #10 {arb_bus.req_0,arb_bus.req_1} = 2'b00;
  #10 $finish;
end

always begin
 #5 clock = !clock;
end
 
arbiter U0 (
  .clock (clock),
  .reset (arb_bus.reset),
  .req_0 (arb_bus.req_0),
  .req_1 (arb_bus.req_1),
  .gnt_0 (arb_bus.gnt_0),
  .gnt_1 (arb_bus.gnt_1)
);

endmodule