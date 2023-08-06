from __future__ import absolute_import
from __future__ import print_function
import veriloggen
import dataflow_reduceadd_valid_enable

expected_verilog = """
module test;

  reg CLK;
  reg RST;
  reg [32-1:0] xdata;
  reg xvalid;
  wire xready;
  reg [1-1:0] resetdata;
  reg resetvalid;
  wire resetready;
  reg [1-1:0] enabledata;
  reg enablevalid;
  wire enableready;
  wire [32-1:0] zdata;
  wire zvalid;
  reg zready;
  wire [1-1:0] vdata;
  wire vvalid;
  reg vready;

  main
  uut
  (
    .CLK(CLK),
    .RST(RST),
    .xdata(xdata),
    .xvalid(xvalid),
    .xready(xready),
    .resetdata(resetdata),
    .resetvalid(resetvalid),
    .resetready(resetready),
    .enabledata(enabledata),
    .enablevalid(enablevalid),
    .enableready(enableready),
    .zdata(zdata),
    .zvalid(zvalid),
    .zready(zready),
    .vdata(vdata),
    .vvalid(vvalid),
    .vready(vready)
  );

  reg reset_done;

  initial begin
    $dumpfile("uut.vcd");
    $dumpvars(0, uut);
  end


  initial begin
    CLK = 0;
    forever begin
      #5 CLK = !CLK;
    end
  end


  initial begin
    RST = 0;
    reset_done = 0;
    xdata = 0;
    xvalid = 0;
    enabledata = 0;
    enablevalid = 0;
    resetdata = 0;
    resetvalid = 0;
    zready = 0;
    #100;
    RST = 1;
    #100;
    RST = 0;
    #1000;
    reset_done = 1;
    @(posedge CLK);
    #1;
    #10000;
    $finish;
  end

  reg [32-1:0] xfsm;
  localparam xfsm_init = 0;
  reg [32-1:0] _tmp_0;
  localparam xfsm_1 = 1;
  localparam xfsm_2 = 2;
  localparam xfsm_3 = 3;
  localparam xfsm_4 = 4;
  localparam xfsm_5 = 5;
  localparam xfsm_6 = 6;
  localparam xfsm_7 = 7;
  localparam xfsm_8 = 8;
  localparam xfsm_9 = 9;
  localparam xfsm_10 = 10;
  localparam xfsm_11 = 11;
  localparam xfsm_12 = 12;
  localparam xfsm_13 = 13;
  localparam xfsm_14 = 14;
  localparam xfsm_15 = 15;
  localparam xfsm_16 = 16;
  localparam xfsm_17 = 17;
  localparam xfsm_18 = 18;
  localparam xfsm_19 = 19;
  localparam xfsm_20 = 20;
  localparam xfsm_21 = 21;
  localparam xfsm_22 = 22;
  localparam xfsm_23 = 23;
  localparam xfsm_24 = 24;

  always @(posedge CLK) begin
    if(RST) begin
      xfsm <= xfsm_init;
      _tmp_0 <= 0;
    end else begin
      case(xfsm)
        xfsm_init: begin
          xvalid <= 0;
          if(reset_done) begin
            xfsm <= xfsm_1;
          end 
        end
        xfsm_1: begin
          xfsm <= xfsm_2;
        end
        xfsm_2: begin
          xfsm <= xfsm_3;
        end
        xfsm_3: begin
          xfsm <= xfsm_4;
        end
        xfsm_4: begin
          xfsm <= xfsm_5;
        end
        xfsm_5: begin
          xfsm <= xfsm_6;
        end
        xfsm_6: begin
          xfsm <= xfsm_7;
        end
        xfsm_7: begin
          xfsm <= xfsm_8;
        end
        xfsm_8: begin
          xfsm <= xfsm_9;
        end
        xfsm_9: begin
          xfsm <= xfsm_10;
        end
        xfsm_10: begin
          xfsm <= xfsm_11;
        end
        xfsm_11: begin
          xvalid <= 1;
          xfsm <= xfsm_12;
        end
        xfsm_12: begin
          if(xready) begin
            xdata <= xdata + 1;
          end 
          if(xready) begin
            _tmp_0 <= _tmp_0 + 1;
          end 
          if((_tmp_0 == 5) && xready) begin
            xvalid <= 0;
          end 
          if((_tmp_0 == 5) && xready) begin
            xfsm <= xfsm_13;
          end 
        end
        xfsm_13: begin
          xfsm <= xfsm_14;
        end
        xfsm_14: begin
          xfsm <= xfsm_15;
        end
        xfsm_15: begin
          xfsm <= xfsm_16;
        end
        xfsm_16: begin
          xfsm <= xfsm_17;
        end
        xfsm_17: begin
          xfsm <= xfsm_18;
        end
        xfsm_18: begin
          xfsm <= xfsm_19;
        end
        xfsm_19: begin
          xfsm <= xfsm_20;
        end
        xfsm_20: begin
          xfsm <= xfsm_21;
        end
        xfsm_21: begin
          xfsm <= xfsm_22;
        end
        xfsm_22: begin
          xfsm <= xfsm_23;
        end
        xfsm_23: begin
          xvalid <= 1;
          if(xready) begin
            xdata <= xdata + 1;
          end 
          if(xready) begin
            _tmp_0 <= _tmp_0 + 1;
          end 
          if((_tmp_0 == 100) && xready) begin
            xvalid <= 0;
          end 
          if((_tmp_0 == 100) && xready) begin
            xfsm <= xfsm_24;
          end 
        end
      endcase
    end
  end

  reg [32-1:0] zfsm;
  localparam zfsm_init = 0;
  localparam zfsm_1 = 1;
  localparam zfsm_2 = 2;
  localparam zfsm_3 = 3;
  localparam zfsm_4 = 4;
  localparam zfsm_5 = 5;
  localparam zfsm_6 = 6;
  localparam zfsm_7 = 7;
  localparam zfsm_8 = 8;

  always @(posedge CLK) begin
    if(RST) begin
      zfsm <= zfsm_init;
    end else begin
      case(zfsm)
        zfsm_init: begin
          zready <= 0;
          if(reset_done) begin
            zfsm <= zfsm_1;
          end 
        end
        zfsm_1: begin
          zfsm <= zfsm_2;
        end
        zfsm_2: begin
          if(zvalid && vvalid) begin
            zready <= 1;
          end 
          if(zvalid && vvalid) begin
            zfsm <= zfsm_3;
          end 
        end
        zfsm_3: begin
          zready <= 0;
          zfsm <= zfsm_4;
        end
        zfsm_4: begin
          zready <= 0;
          zfsm <= zfsm_5;
        end
        zfsm_5: begin
          zready <= 0;
          zfsm <= zfsm_6;
        end
        zfsm_6: begin
          zready <= 0;
          zfsm <= zfsm_7;
        end
        zfsm_7: begin
          zready <= 0;
          zfsm <= zfsm_8;
        end
        zfsm_8: begin
          zfsm <= zfsm_2;
        end
      endcase
    end
  end

  reg [32-1:0] vfsm;
  localparam vfsm_init = 0;
  localparam vfsm_1 = 1;
  localparam vfsm_2 = 2;
  localparam vfsm_3 = 3;
  localparam vfsm_4 = 4;
  localparam vfsm_5 = 5;
  localparam vfsm_6 = 6;
  localparam vfsm_7 = 7;
  localparam vfsm_8 = 8;

  always @(posedge CLK) begin
    if(RST) begin
      vfsm <= vfsm_init;
    end else begin
      case(vfsm)
        vfsm_init: begin
          vready <= 0;
          if(reset_done) begin
            vfsm <= vfsm_1;
          end 
        end
        vfsm_1: begin
          vfsm <= vfsm_2;
        end
        vfsm_2: begin
          if(zvalid && vvalid) begin
            vready <= 1;
          end 
          if(zvalid && vvalid) begin
            vfsm <= vfsm_3;
          end 
        end
        vfsm_3: begin
          vready <= 0;
          vfsm <= vfsm_4;
        end
        vfsm_4: begin
          vready <= 0;
          vfsm <= vfsm_5;
        end
        vfsm_5: begin
          vready <= 0;
          vfsm <= vfsm_6;
        end
        vfsm_6: begin
          vready <= 0;
          vfsm <= vfsm_7;
        end
        vfsm_7: begin
          vready <= 0;
          vfsm <= vfsm_8;
        end
        vfsm_8: begin
          vfsm <= vfsm_2;
        end
      endcase
    end
  end

  reg [32-1:0] enable;
  localparam enable_init = 0;
  reg [32-1:0] enable_count;
  localparam enable_1 = 1;
  localparam enable_2 = 2;

  always @(posedge CLK) begin
    if(RST) begin
      enable <= enable_init;
      enable_count <= 0;
    end else begin
      case(enable)
        enable_init: begin
          if(reset_done) begin
            enable <= enable_1;
          end 
        end
        enable_1: begin
          enablevalid <= 1;
          if(enablevalid && enableready) begin
            enable_count <= enable_count + 1;
          end 
          if(enablevalid && enableready && (enable_count == 2)) begin
            enabledata <= 1;
          end 
          if(enablevalid && enableready && (enable_count == 2)) begin
            enable <= enable_2;
          end 
        end
        enable_2: begin
          if(enablevalid && enableready) begin
            enabledata <= 0;
          end 
          enable_count <= 0;
          if(enablevalid && enableready) begin
            enable <= enable_1;
          end 
        end
      endcase
    end
  end

  reg [32-1:0] reset;
  localparam reset_init = 0;
  reg [32-1:0] reset_count;
  localparam reset_1 = 1;
  localparam reset_2 = 2;

  always @(posedge CLK) begin
    if(RST) begin
      reset <= reset_init;
      reset_count <= 0;
    end else begin
      case(reset)
        reset_init: begin
          if(reset_done) begin
            reset <= reset_1;
          end 
        end
        reset_1: begin
          resetvalid <= 1;
          if(resetvalid && resetready) begin
            reset_count <= reset_count + 1;
          end 
          if(resetvalid && resetready && (reset_count == 2)) begin
            resetdata <= 0;
          end 
          if(resetvalid && resetready && (reset_count == 2)) begin
            reset <= reset_2;
          end 
        end
        reset_2: begin
          if(resetvalid && resetready) begin
            resetdata <= 0;
          end 
          reset_count <= 0;
          if(resetvalid && resetready) begin
            reset <= reset_1;
          end 
        end
      endcase
    end
  end


  always @(posedge CLK) begin
    if(reset_done) begin
      if(xvalid && xready) begin
        $display("xdata=%d", xdata);
      end 
      if(zvalid && zready) begin
        $display("zdata=%d", zdata);
      end 
      if(vvalid && vready) begin
        $display("vdata=%d", vdata);
      end 
    end 
  end


endmodule



module main
(
  input CLK,
  input RST,
  input [32-1:0] xdata,
  input xvalid,
  output xready,
  input [1-1:0] resetdata,
  input resetvalid,
  output resetready,
  input [1-1:0] enabledata,
  input enablevalid,
  output enableready,
  output [32-1:0] zdata,
  output zvalid,
  input zready,
  output [1-1:0] vdata,
  output vvalid,
  input vready
);

  wire [32-1:0] _times_data_0;
  wire _times_valid_0;
  wire _times_ready_0;
  wire [64-1:0] _times_odata_0;
  reg [64-1:0] _times_data_reg_0;
  assign _times_data_0 = _times_data_reg_0;
  wire _times_ovalid_0;
  reg _times_valid_reg_0;
  assign _times_valid_0 = _times_valid_reg_0;
  wire _times_enable_0;
  wire _times_update_0;
  assign _times_enable_0 = (_times_ready_0 || !_times_valid_0) && (xready && xready) && (xvalid && xvalid);
  assign _times_update_0 = _times_ready_0 || !_times_valid_0;

  multiplier_0
  mul0
  (
    .CLK(CLK),
    .RST(RST),
    .update(_times_update_0),
    .enable(_times_enable_0),
    .valid(_times_ovalid_0),
    .a(xdata),
    .b(xdata),
    .c(_times_odata_0)
  );

  assign xready = (_times_ready_0 || !_times_valid_0) && (xvalid && xvalid) && ((_times_ready_0 || !_times_valid_0) && (xvalid && xvalid));
  reg [1-1:0] __delay_data_1;
  reg __delay_valid_1;
  wire __delay_ready_1;
  assign enableready = (__delay_ready_1 || !__delay_valid_1) && enablevalid;
  reg [1-1:0] __delay_data_2;
  reg __delay_valid_2;
  wire __delay_ready_2;
  assign resetready = (__delay_ready_2 || !__delay_valid_2) && resetvalid;
  reg [1-1:0] __delay_data_3;
  reg __delay_valid_3;
  wire __delay_ready_3;
  assign __delay_ready_1 = (__delay_ready_3 || !__delay_valid_3) && __delay_valid_1;
  reg [1-1:0] __delay_data_4;
  reg __delay_valid_4;
  wire __delay_ready_4;
  assign __delay_ready_2 = (__delay_ready_4 || !__delay_valid_4) && __delay_valid_2;
  reg [1-1:0] __delay_data_5;
  reg __delay_valid_5;
  wire __delay_ready_5;
  assign __delay_ready_3 = (__delay_ready_5 || !__delay_valid_5) && __delay_valid_3;
  reg [1-1:0] __delay_data_6;
  reg __delay_valid_6;
  wire __delay_ready_6;
  assign __delay_ready_4 = (__delay_ready_6 || !__delay_valid_6) && __delay_valid_4;
  reg [1-1:0] __delay_data_7;
  reg __delay_valid_7;
  wire __delay_ready_7;
  assign __delay_ready_5 = (__delay_ready_7 || !__delay_valid_7) && __delay_valid_5;
  reg [1-1:0] __delay_data_8;
  reg __delay_valid_8;
  wire __delay_ready_8;
  assign __delay_ready_6 = (__delay_ready_8 || !__delay_valid_8) && __delay_valid_6;
  reg [1-1:0] __delay_data_9;
  reg __delay_valid_9;
  wire __delay_ready_9;
  assign __delay_ready_7 = (__delay_ready_9 || !__delay_valid_9) && __delay_valid_7;
  reg [1-1:0] __delay_data_10;
  reg __delay_valid_10;
  wire __delay_ready_10;
  assign __delay_ready_8 = (__delay_ready_10 || !__delay_valid_10) && __delay_valid_8;
  reg [1-1:0] __delay_data_11;
  reg __delay_valid_11;
  wire __delay_ready_11;
  assign __delay_ready_9 = (__delay_ready_11 || !__delay_valid_11) && __delay_valid_9;
  reg [1-1:0] __delay_data_12;
  reg __delay_valid_12;
  wire __delay_ready_12;
  assign __delay_ready_10 = (__delay_ready_12 || !__delay_valid_12) && __delay_valid_10;
  reg [1-1:0] __delay_data_13;
  reg __delay_valid_13;
  wire __delay_ready_13;
  assign __delay_ready_11 = (__delay_ready_13 || !__delay_valid_13) && __delay_valid_11;
  reg [1-1:0] __delay_data_14;
  reg __delay_valid_14;
  wire __delay_ready_14;
  assign __delay_ready_12 = (__delay_ready_14 || !__delay_valid_14) && __delay_valid_12;
  reg [32-1:0] _reduceadd_data_15;
  reg _reduceadd_valid_15;
  wire _reduceadd_ready_15;
  reg [5-1:0] _reduceadd_count_15;
  reg [1-1:0] _pulse_data_16;
  reg _pulse_valid_16;
  wire _pulse_ready_16;
  reg [5-1:0] _pulse_count_16;
  assign __delay_ready_13 = (_reduceadd_ready_15 || !_reduceadd_valid_15) && (_times_valid_0 && __delay_valid_13 && __delay_valid_14) && ((_pulse_ready_16 || !_pulse_valid_16) && (_times_valid_0 && __delay_valid_13 && __delay_valid_14));
  assign _times_ready_0 = (_reduceadd_ready_15 || !_reduceadd_valid_15) && (_times_valid_0 && __delay_valid_13 && __delay_valid_14) && ((_pulse_ready_16 || !_pulse_valid_16) && (_times_valid_0 && __delay_valid_13 && __delay_valid_14));
  assign __delay_ready_14 = (_reduceadd_ready_15 || !_reduceadd_valid_15) && (_times_valid_0 && __delay_valid_13 && __delay_valid_14) && ((_pulse_ready_16 || !_pulse_valid_16) && (_times_valid_0 && __delay_valid_13 && __delay_valid_14));
  assign zdata = _reduceadd_data_15;
  assign zvalid = _reduceadd_valid_15;
  assign _reduceadd_ready_15 = zready;
  assign vdata = _pulse_data_16;
  assign vvalid = _pulse_valid_16;
  assign _pulse_ready_16 = vready;

  always @(posedge CLK) begin
    if(RST) begin
      _times_data_reg_0 <= 0;
      _times_valid_reg_0 <= 0;
      __delay_data_1 <= 0;
      __delay_valid_1 <= 0;
      __delay_data_2 <= 0;
      __delay_valid_2 <= 0;
      __delay_data_3 <= 0;
      __delay_valid_3 <= 0;
      __delay_data_4 <= 0;
      __delay_valid_4 <= 0;
      __delay_data_5 <= 0;
      __delay_valid_5 <= 0;
      __delay_data_6 <= 0;
      __delay_valid_6 <= 0;
      __delay_data_7 <= 0;
      __delay_valid_7 <= 0;
      __delay_data_8 <= 0;
      __delay_valid_8 <= 0;
      __delay_data_9 <= 0;
      __delay_valid_9 <= 0;
      __delay_data_10 <= 0;
      __delay_valid_10 <= 0;
      __delay_data_11 <= 0;
      __delay_valid_11 <= 0;
      __delay_data_12 <= 0;
      __delay_valid_12 <= 0;
      __delay_data_13 <= 0;
      __delay_valid_13 <= 0;
      __delay_data_14 <= 0;
      __delay_valid_14 <= 0;
      _reduceadd_data_15 <= 1'sd0;
      _reduceadd_count_15 <= 0;
      _reduceadd_valid_15 <= 0;
      _pulse_data_16 <= 1'sd0;
      _pulse_count_16 <= 0;
      _pulse_valid_16 <= 0;
    end else begin
      if(_times_ready_0 || !_times_valid_0) begin
        _times_data_reg_0 <= _times_odata_0;
      end 
      if(_times_ready_0 || !_times_valid_0) begin
        _times_valid_reg_0 <= _times_ovalid_0;
      end 
      if((__delay_ready_1 || !__delay_valid_1) && enableready && enablevalid) begin
        __delay_data_1 <= enabledata;
      end 
      if(__delay_valid_1 && __delay_ready_1) begin
        __delay_valid_1 <= 0;
      end 
      if((__delay_ready_1 || !__delay_valid_1) && enableready) begin
        __delay_valid_1 <= enablevalid;
      end 
      if((__delay_ready_2 || !__delay_valid_2) && resetready && resetvalid) begin
        __delay_data_2 <= resetdata;
      end 
      if(__delay_valid_2 && __delay_ready_2) begin
        __delay_valid_2 <= 0;
      end 
      if((__delay_ready_2 || !__delay_valid_2) && resetready) begin
        __delay_valid_2 <= resetvalid;
      end 
      if((__delay_ready_3 || !__delay_valid_3) && __delay_ready_1 && __delay_valid_1) begin
        __delay_data_3 <= __delay_data_1;
      end 
      if(__delay_valid_3 && __delay_ready_3) begin
        __delay_valid_3 <= 0;
      end 
      if((__delay_ready_3 || !__delay_valid_3) && __delay_ready_1) begin
        __delay_valid_3 <= __delay_valid_1;
      end 
      if((__delay_ready_4 || !__delay_valid_4) && __delay_ready_2 && __delay_valid_2) begin
        __delay_data_4 <= __delay_data_2;
      end 
      if(__delay_valid_4 && __delay_ready_4) begin
        __delay_valid_4 <= 0;
      end 
      if((__delay_ready_4 || !__delay_valid_4) && __delay_ready_2) begin
        __delay_valid_4 <= __delay_valid_2;
      end 
      if((__delay_ready_5 || !__delay_valid_5) && __delay_ready_3 && __delay_valid_3) begin
        __delay_data_5 <= __delay_data_3;
      end 
      if(__delay_valid_5 && __delay_ready_5) begin
        __delay_valid_5 <= 0;
      end 
      if((__delay_ready_5 || !__delay_valid_5) && __delay_ready_3) begin
        __delay_valid_5 <= __delay_valid_3;
      end 
      if((__delay_ready_6 || !__delay_valid_6) && __delay_ready_4 && __delay_valid_4) begin
        __delay_data_6 <= __delay_data_4;
      end 
      if(__delay_valid_6 && __delay_ready_6) begin
        __delay_valid_6 <= 0;
      end 
      if((__delay_ready_6 || !__delay_valid_6) && __delay_ready_4) begin
        __delay_valid_6 <= __delay_valid_4;
      end 
      if((__delay_ready_7 || !__delay_valid_7) && __delay_ready_5 && __delay_valid_5) begin
        __delay_data_7 <= __delay_data_5;
      end 
      if(__delay_valid_7 && __delay_ready_7) begin
        __delay_valid_7 <= 0;
      end 
      if((__delay_ready_7 || !__delay_valid_7) && __delay_ready_5) begin
        __delay_valid_7 <= __delay_valid_5;
      end 
      if((__delay_ready_8 || !__delay_valid_8) && __delay_ready_6 && __delay_valid_6) begin
        __delay_data_8 <= __delay_data_6;
      end 
      if(__delay_valid_8 && __delay_ready_8) begin
        __delay_valid_8 <= 0;
      end 
      if((__delay_ready_8 || !__delay_valid_8) && __delay_ready_6) begin
        __delay_valid_8 <= __delay_valid_6;
      end 
      if((__delay_ready_9 || !__delay_valid_9) && __delay_ready_7 && __delay_valid_7) begin
        __delay_data_9 <= __delay_data_7;
      end 
      if(__delay_valid_9 && __delay_ready_9) begin
        __delay_valid_9 <= 0;
      end 
      if((__delay_ready_9 || !__delay_valid_9) && __delay_ready_7) begin
        __delay_valid_9 <= __delay_valid_7;
      end 
      if((__delay_ready_10 || !__delay_valid_10) && __delay_ready_8 && __delay_valid_8) begin
        __delay_data_10 <= __delay_data_8;
      end 
      if(__delay_valid_10 && __delay_ready_10) begin
        __delay_valid_10 <= 0;
      end 
      if((__delay_ready_10 || !__delay_valid_10) && __delay_ready_8) begin
        __delay_valid_10 <= __delay_valid_8;
      end 
      if((__delay_ready_11 || !__delay_valid_11) && __delay_ready_9 && __delay_valid_9) begin
        __delay_data_11 <= __delay_data_9;
      end 
      if(__delay_valid_11 && __delay_ready_11) begin
        __delay_valid_11 <= 0;
      end 
      if((__delay_ready_11 || !__delay_valid_11) && __delay_ready_9) begin
        __delay_valid_11 <= __delay_valid_9;
      end 
      if((__delay_ready_12 || !__delay_valid_12) && __delay_ready_10 && __delay_valid_10) begin
        __delay_data_12 <= __delay_data_10;
      end 
      if(__delay_valid_12 && __delay_ready_12) begin
        __delay_valid_12 <= 0;
      end 
      if((__delay_ready_12 || !__delay_valid_12) && __delay_ready_10) begin
        __delay_valid_12 <= __delay_valid_10;
      end 
      if((__delay_ready_13 || !__delay_valid_13) && __delay_ready_11 && __delay_valid_11) begin
        __delay_data_13 <= __delay_data_11;
      end 
      if(__delay_valid_13 && __delay_ready_13) begin
        __delay_valid_13 <= 0;
      end 
      if((__delay_ready_13 || !__delay_valid_13) && __delay_ready_11) begin
        __delay_valid_13 <= __delay_valid_11;
      end 
      if((__delay_ready_14 || !__delay_valid_14) && __delay_ready_12 && __delay_valid_12) begin
        __delay_data_14 <= __delay_data_12;
      end 
      if(__delay_valid_14 && __delay_ready_14) begin
        __delay_valid_14 <= 0;
      end 
      if((__delay_ready_14 || !__delay_valid_14) && __delay_ready_12) begin
        __delay_valid_14 <= __delay_valid_12;
      end 
      if((_reduceadd_ready_15 || !_reduceadd_valid_15) && (_times_ready_0 && __delay_ready_13 && __delay_ready_14) && (_times_valid_0 && __delay_valid_13 && __delay_valid_14) && __delay_data_13) begin
        _reduceadd_data_15 <= _reduceadd_data_15 + _times_data_0;
      end 
      if((_reduceadd_ready_15 || !_reduceadd_valid_15) && (_times_ready_0 && __delay_ready_13 && __delay_ready_14) && (_times_valid_0 && __delay_valid_13 && __delay_valid_14) && __delay_data_13) begin
        _reduceadd_count_15 <= (_reduceadd_count_15 == 4'sd4 - 1)? 0 : _reduceadd_count_15 + 1;
      end 
      if(_reduceadd_valid_15 && _reduceadd_ready_15) begin
        _reduceadd_valid_15 <= 0;
      end 
      if((_reduceadd_ready_15 || !_reduceadd_valid_15) && (_times_ready_0 && __delay_ready_13 && __delay_ready_14)) begin
        _reduceadd_valid_15 <= _times_valid_0 && __delay_valid_13 && __delay_valid_14;
      end 
      if((_reduceadd_ready_15 || !_reduceadd_valid_15) && (_times_ready_0 && __delay_ready_13 && __delay_ready_14) && (_times_valid_0 && __delay_valid_13 && __delay_valid_14) && __delay_data_14) begin
        _reduceadd_data_15 <= 1'sd0;
      end 
      if((_reduceadd_ready_15 || !_reduceadd_valid_15) && (_times_ready_0 && __delay_ready_13 && __delay_ready_14) && (_times_valid_0 && __delay_valid_13 && __delay_valid_14) && __delay_data_13 && __delay_data_14) begin
        _reduceadd_data_15 <= 1'sd0 + _times_data_0;
      end 
      if((_reduceadd_ready_15 || !_reduceadd_valid_15) && (_times_ready_0 && __delay_ready_13 && __delay_ready_14) && (_times_valid_0 && __delay_valid_13 && __delay_valid_14) && __delay_data_13 && __delay_data_14) begin
        _reduceadd_count_15 <= 0;
      end 
      if((_reduceadd_ready_15 || !_reduceadd_valid_15) && (_times_ready_0 && __delay_ready_13 && __delay_ready_14) && (_times_valid_0 && __delay_valid_13 && __delay_valid_14) && __delay_data_13 && (_reduceadd_count_15 == 0)) begin
        _reduceadd_data_15 <= 1'sd0 + _times_data_0;
      end 
      if((_pulse_ready_16 || !_pulse_valid_16) && (_times_ready_0 && __delay_ready_13 && __delay_ready_14) && (_times_valid_0 && __delay_valid_13 && __delay_valid_14) && __delay_data_13) begin
        _pulse_data_16 <= _pulse_count_16 == 4'sd4 - 1;
      end 
      if((_pulse_ready_16 || !_pulse_valid_16) && (_times_ready_0 && __delay_ready_13 && __delay_ready_14) && (_times_valid_0 && __delay_valid_13 && __delay_valid_14) && __delay_data_13) begin
        _pulse_count_16 <= (_pulse_count_16 == 4'sd4 - 1)? 0 : _pulse_count_16 + 1;
      end 
      if(_pulse_valid_16 && _pulse_ready_16) begin
        _pulse_valid_16 <= 0;
      end 
      if((_pulse_ready_16 || !_pulse_valid_16) && (_times_ready_0 && __delay_ready_13 && __delay_ready_14)) begin
        _pulse_valid_16 <= _times_valid_0 && __delay_valid_13 && __delay_valid_14;
      end 
      if((_pulse_ready_16 || !_pulse_valid_16) && (_times_ready_0 && __delay_ready_13 && __delay_ready_14) && (_times_valid_0 && __delay_valid_13 && __delay_valid_14) && __delay_data_14) begin
        _pulse_data_16 <= 1'sd0;
      end 
      if((_pulse_ready_16 || !_pulse_valid_16) && (_times_ready_0 && __delay_ready_13 && __delay_ready_14) && (_times_valid_0 && __delay_valid_13 && __delay_valid_14) && __delay_data_13 && __delay_data_14) begin
        _pulse_data_16 <= _pulse_count_16 == 4'sd4 - 1;
      end 
      if((_pulse_ready_16 || !_pulse_valid_16) && (_times_ready_0 && __delay_ready_13 && __delay_ready_14) && (_times_valid_0 && __delay_valid_13 && __delay_valid_14) && __delay_data_13 && __delay_data_14) begin
        _pulse_count_16 <= 0;
      end 
      if((_pulse_ready_16 || !_pulse_valid_16) && (_times_ready_0 && __delay_ready_13 && __delay_ready_14) && (_times_valid_0 && __delay_valid_13 && __delay_valid_14) && __delay_data_13 && (_pulse_count_16 == 0)) begin
        _pulse_data_16 <= _pulse_count_16 == 4'sd4 - 1;
      end 
    end
  end


endmodule



module multiplier_0
(
  input CLK,
  input RST,
  input update,
  input enable,
  output valid,
  input [32-1:0] a,
  input [32-1:0] b,
  output [64-1:0] c
);

  reg valid_reg0;
  reg valid_reg1;
  reg valid_reg2;
  reg valid_reg3;
  reg valid_reg4;
  reg valid_reg5;
  assign valid = valid_reg5;

  always @(posedge CLK) begin
    if(RST) begin
      valid_reg0 <= 0;
      valid_reg1 <= 0;
      valid_reg2 <= 0;
      valid_reg3 <= 0;
      valid_reg4 <= 0;
      valid_reg5 <= 0;
    end else begin
      if(update) begin
        valid_reg0 <= enable;
        valid_reg1 <= valid_reg0;
        valid_reg2 <= valid_reg1;
        valid_reg3 <= valid_reg2;
        valid_reg4 <= valid_reg3;
        valid_reg5 <= valid_reg4;
      end 
    end
  end


  multiplier_core_0
  mult
  (
    .CLK(CLK),
    .update(update),
    .a(a),
    .b(b),
    .c(c)
  );


endmodule



module multiplier_core_0
(
  input CLK,
  input update,
  input [32-1:0] a,
  input [32-1:0] b,
  output [64-1:0] c
);

  reg [32-1:0] _a;
  reg [32-1:0] _b;
  reg signed [64-1:0] _tmpval0;
  reg signed [64-1:0] _tmpval1;
  reg signed [64-1:0] _tmpval2;
  reg signed [64-1:0] _tmpval3;
  reg signed [64-1:0] _tmpval4;
  wire signed [64-1:0] rslt;
  assign rslt = $signed({ 1'd0, _a }) * $signed({ 1'd0, _b });
  assign c = _tmpval4;

  always @(posedge CLK) begin
    if(update) begin
      _a <= a;
      _b <= b;
      _tmpval0 <= rslt;
      _tmpval1 <= _tmpval0;
      _tmpval2 <= _tmpval1;
      _tmpval3 <= _tmpval2;
      _tmpval4 <= _tmpval3;
    end 
  end


endmodule
"""


def test():
    veriloggen.reset()
    test_module = dataflow_reduceadd_valid_enable.mkTest()
    code = test_module.to_verilog()

    from pyverilog.vparser.parser import VerilogParser
    from pyverilog.ast_code_generator.codegen import ASTCodeGenerator
    parser = VerilogParser()
    expected_ast = parser.parse(expected_verilog)
    codegen = ASTCodeGenerator()
    expected_code = codegen.visit(expected_ast)

    assert(expected_code == code)
