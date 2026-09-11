/************************************************************\
**	Copyright (c) 2012-2024 Anlogic Inc.
**	All Right Reserved.
\************************************************************/
/************************************************************\
**	Build time: Jun 17 2024 15:10:03
**	TD version	:	5.9.112797
///////////////////////////////////////////////////////////////////////////////
//	Input frequency:                50.0 MHZ
//	Clock multiplication factor: 5
//	Clock division factor:       2
//	Clock information:
//		Clock name	| Frequency 	| Phase shift 
//		C0        	| 125.000000   MHZ	    |  0 DEG 
//		C1        	| 125.000000   MHZ	    |  0 DEG 
//		C2        	| 50.000000   MHZ		|  0 DEG 
//		C3        	| 23.972603   MHZ		|  0 DEG 
///////////////////////////////////////////////////////////////////////////////
`timescale 1 ns / 100 fs 

\************************************************************/
module pll
(
  input                         refclk,
  output                        clk0_out,
  output                        clk1_out,
  output                        clk2_out,
  output                        clk3_out,
  output                        lock,
  input                         pllreset
);
  wire							  clk0_buf;
DR1_LOGIC_BUFG bufg_feedback (
 .i(clk0_buf), 
 .o(clk0_out) 
 ); 

 
 
 




  DR1_PHY_PLL_WRAPERR_c27ca599f4ef
  #(
      .FBKCLK("CLKC0_EXT"),
      .REFCLK_DIV(2),
      .FBCLK_DIV(5),
      .CLKC0_FPHASE(0),
      .CLKC1_FPHASE(0),
      .CLKC2_FPHASE(0),
      .CLKC3_FPHASE(0),
      .CLKC0_CPHASE(13),
      .CLKC1_CPHASE(13),
      .CLKC2_CPHASE(34),
      .CLKC3_CPHASE(72),
      .CLKC0_DIV(14),
      .CLKC1_DIV(14),
      .CLKC2_DIV(35),
      .CLKC3_DIV(73),
      .CLKC0_DUTY_INT(7),
      .CLKC1_DUTY_INT(7),
      .CLKC2_DUTY_INT(18),
      .CLKC3_DUTY_INT(37),
      .CLKC0_ENABLE("ENABLE"),
      .CLKC1_ENABLE("ENABLE"),
      .CLKC2_ENABLE("ENABLE"),
      .CLKC3_ENABLE("ENABLE"),
      .FIN("50.0"),
      .FEEDBK_MODE("NORMAL"),
      .PLL_USR_RST("ENABLE"),
      .PLL_FEED_TYPE("EXTERNAL"),
      .LPF_RES(3),
      .LPF_CAP(2),
      .ICP_CUR(11),
      .GMC_GAIN(1),
      .FRAC_ENABLE("DISABLE"),
      .DITHER_ENABLE("DISABLE"),
      .SDM_FRAC(0),
      .SSC_AMP(0.0000),
      .MPHASE_ENABLE("DISABLE"),
      .DYN_PHASE_PATH_SEL("DISABLE"),
      .DYN_FPHASE_EN("DISABLE"),
      .CLKC0_FPHASE_RSTSEL(0),
      .CLKC1_FPHASE_RSTSEL(0),
      .CLKC2_FPHASE_RSTSEL(0),
      .CLKC3_FPHASE_RSTSEL(0),
      .CLKC0_DUTY50("ENABLE"),
      .CLKC1_DUTY50("ENABLE"),
      .CLKC2_DUTY50("ENABLE"),
      .CLKC3_DUTY50("ENABLE"),
      .INTPI(2),
      .SSC_ENABLE("DISABLE"),
      .SSC_MODE("DOWN"),
      .SSC_FREQ_DIV(0),
      .SSC_RNGE(0),
      .HIGH_SPEED_EN("DISABLE")
  )DR1_PHY_PLL_WRAPERR_c27ca599f4ef_Inst
  (
      .clk4_en(1'b0),
      .clk4_out(),
      .clkb4_out(),
      .clk5_en(1'b0),
      .clk5_out(),
      .clkb5_out(),
      .clk6_en(1'b0),
      .clk6_out(),
      .clkb6_out(),
      .refclk(refclk),
      .ssc_en(1'b0),
      .ext_freq_mod_val(17'b00000000000000000),
      .ext_freq_mod_en(1'b0),
      .ext_freq_mod_clk(1'b0),
	  .clkc_rst(2'b00),
      .fbclk(clk0_out),
      .drp_rdata(),
      .drp_rdy(),
      .drp_err(),
      .drp_wdata(8'b00000000),
      .drp_addr(8'b00000000),
      .drp_wr(1'b0),
      .drp_rd(1'b0),
      .drp_sel(1'b0),
      .drp_rstn(1'b1),
      .drp_clk(1'b0),
      .cps_step(2'b00),
      .psclksel(3'b000),
      .psdone(),
      .psstep(1'b0),
      .psdown(1'b0),
      .psclk(1'b0),
      .pllpd(1'b0),
      .wakeup(1'b0),
      .refclk_rst(1'b0),
      .clk0_en(1'b1),
      .clkb0_out(),
      .clk0_out(clk0_buf),
      .clk1_en(1'b1),
      .clkb1_out(),
      .clk1_out(clk1_out),
      .clk2_en(1'b1),
      .clkb2_out(),
      .clk2_out(clk2_out),
      .clk3_en(1'b1),
      .clkb3_out(),
      .clk3_out(clk3_out),
      .lock(lock),
      .pllreset(pllreset)
  );
endmodule
