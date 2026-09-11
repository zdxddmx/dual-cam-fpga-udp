module gmii_to_rgmii(
  reset_n,

  gmii_tx_clk,
  gmii_txd,
  gmii_txen,
  gmii_txer,

  rgmii_tx_clk,
  rgmii_txd,
  rgmii_txen
);
  input        reset_n;

  input        gmii_tx_clk;
  input  [7:0] gmii_txd;
  input        gmii_txen;
  input        gmii_txer;
  
  output       rgmii_tx_clk;
  output [3:0] rgmii_txd;
  output       rgmii_txen;

  genvar i;
  generate
    for(i=0;i<4;i=i+1)
    begin: rgmii_txd_o

DR1_LOGIC_ODDR #(
  .ASYNCRST     ( "ENABLE"   )  //  "ENABLE", "DISABLE".  Asynchronous reset enable.  
)ODDR_rgmii_txd(
  .q            ( rgmii_txd[i]     ), //  1-Bit output. 1 bit DDR edge output data.    
  .clk          ( gmii_tx_clk      ), //  1-Bit input. Synchronous clock.             
  .d1           ( gmii_txd[i+4]    ), //  1-Bit input. 1 bit negedge input data.      
  .d0           ( gmii_txd[i]      ), //  1-Bit input. 1 bit posedge input data.      
  .rst          ( ~reset_n         )  //  1-Bit input. Reset,high active.             
);

    end
  endgenerate

DR1_LOGIC_ODDR #(
  .ASYNCRST     ( "ENABLE"   )  //  "ENABLE", "DISABLE".  Asynchronous reset enable.  
)ODDR_rgmii_txen(
  .q            ( rgmii_txen          ), //  1-Bit output. 1 bit DDR edge output data.    
  .clk          ( gmii_tx_clk        ), //  1-Bit input. Synchronous clock.             
  .d1           ( gmii_txen^gmii_txer         ), //  1-Bit input. 1 bit negedge input data.      
  .d0           ( gmii_txen         ), //  1-Bit input. 1 bit posedge input data.      
  .rst          ( ~reset_n        )  //  1-Bit input. Reset,high active.             
);



DR1_LOGIC_ODDR #(
  .ASYNCRST     ( "ENABLE"   )  //  "ENABLE", "DISABLE".  Asynchronous reset enable.  
)ODDR_rgmii_clk(
  .q            ( rgmii_tx_clk          ), //  1-Bit output. 1 bit DDR edge output data.    
  .clk          ( gmii_tx_clk        ), //  1-Bit input. Synchronous clock.             
  .d1           ( 1'b0         ), //  1-Bit input. 1 bit negedge input data.      
  .d0           ( 1'b1         ), //  1-Bit input. 1 bit posedge input data.      
  .rst          ( ~reset_n        )  //  1-Bit input. Reset,high active.             
);


endmodule

