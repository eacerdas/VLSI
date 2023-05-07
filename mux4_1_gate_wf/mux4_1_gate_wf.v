module mux4_1 (i0,i1,i2,i3,s1,s2,out);
//Declaración de puertos
output out;
input i0, i1, i2, i3;
input s1, s2;

//Nets internas
wire s1n, s2n;
wire y0, y1, y2, y3;

//Definición de compuertas
not (s1n, s1);
not (s2n, s2);

and (y0, i0, s1n, s2n);
and (y1, i1, s1n, s2);
and (y2, i2, s1, s2n);
and (y3, i3, s1, s2);

or (out, y0, y1, y2, y3);

endmodule

//Root module, sin puertos
module estimulo;

//Declaración de variables para conectar a las entradas
reg IN0, IN1, IN2, IN3;
reg S1, S2;

//Declaración de net de salida
wire OUTPUT;

//Instancia de multiplexor
mux4_1 mymux(IN0, IN1, IN2, IN3, S1, S2, OUTPUT);

initial
begin
	$dumpfile("estimulo.vcd");
	$dumpvars(0,estimulo);
end

//Estimular las entradas
initial
begin
  	//Definición de valores para entradas
	IN0 = 1; IN1 = 0; IN2 = 1; IN3 = 0;
	#1 $display("IN0= %b, IN1= %b, IN2= %b, IN3= %b\n",IN0,IN1,IN2,IN3);
	
	S1 = 0; S2 = 0;
	#1 $display("S1 = %b, S2 = %b, OUTPUT = %b \n", S1, S2, OUTPUT);

	S1 = 0; S2 = 1;
	#1 $display("S1 = %b, S2 = %b, OUTPUT = %b \n", S1, S2, OUTPUT);

	S1 = 1; S2 = 0;
	#1 $display("S1 = %b, S2 = %b, OUTPUT = %b \n", S1, S2, OUTPUT);

	S1 = 1; S2 = 1;
	#1 $display("S1 = %b, S2 = %b, OUTPUT = %b \n", S1, S2, OUTPUT);
end

endmodule