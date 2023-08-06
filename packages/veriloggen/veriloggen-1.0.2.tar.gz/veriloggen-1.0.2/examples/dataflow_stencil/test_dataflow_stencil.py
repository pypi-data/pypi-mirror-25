from __future__ import absolute_import
from __future__ import print_function
import veriloggen
import dataflow_stencil

expected_verilog = """
module test;

  reg CLK;
  reg RST;
  reg start;
  wire busy;
  reg [4-1:0] ext_src_ram0_addr;
  wire [32-1:0] ext_src_ram0_rdata;
  reg [32-1:0] ext_src_ram0_wdata;
  reg ext_src_ram0_wenable;
  reg [4-1:0] ext_src_ram1_addr;
  wire [32-1:0] ext_src_ram1_rdata;
  reg [32-1:0] ext_src_ram1_wdata;
  reg ext_src_ram1_wenable;
  reg [4-1:0] ext_src_ram2_addr;
  wire [32-1:0] ext_src_ram2_rdata;
  reg [32-1:0] ext_src_ram2_wdata;
  reg ext_src_ram2_wenable;
  reg [4-1:0] ext_dst_ram_addr;
  wire [32-1:0] ext_dst_ram_rdata;
  reg [32-1:0] ext_dst_ram_wdata;
  reg ext_dst_ram_wenable;

  stencil
  uut
  (
    .CLK(CLK),
    .RST(RST),
    .start(start),
    .busy(busy),
    .ext_src_ram0_addr(ext_src_ram0_addr),
    .ext_src_ram0_rdata(ext_src_ram0_rdata),
    .ext_src_ram0_wdata(ext_src_ram0_wdata),
    .ext_src_ram0_wenable(ext_src_ram0_wenable),
    .ext_src_ram1_addr(ext_src_ram1_addr),
    .ext_src_ram1_rdata(ext_src_ram1_rdata),
    .ext_src_ram1_wdata(ext_src_ram1_wdata),
    .ext_src_ram1_wenable(ext_src_ram1_wenable),
    .ext_src_ram2_addr(ext_src_ram2_addr),
    .ext_src_ram2_rdata(ext_src_ram2_rdata),
    .ext_src_ram2_wdata(ext_src_ram2_wdata),
    .ext_src_ram2_wenable(ext_src_ram2_wenable),
    .ext_dst_ram_addr(ext_dst_ram_addr),
    .ext_dst_ram_rdata(ext_dst_ram_rdata),
    .ext_dst_ram_wdata(ext_dst_ram_wdata),
    .ext_dst_ram_wenable(ext_dst_ram_wenable)
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
    start = 0;
    ext_src_ram0_addr = 0;
    ext_src_ram0_wdata = 0;
    ext_src_ram0_wenable = 0;
    ext_src_ram1_addr = 0;
    ext_src_ram1_wdata = 0;
    ext_src_ram1_wenable = 0;
    ext_src_ram2_addr = 0;
    ext_src_ram2_wdata = 0;
    ext_src_ram2_wenable = 0;
    ext_dst_ram_addr = 2;
    ext_dst_ram_wdata = 0;
    ext_dst_ram_wenable = 0;
    #100;
    RST = 1;
    #100;
    RST = 0;
    #1000;
    reset_done = 1;
    @(posedge CLK);
    #1;
    #100000;
    $finish;
  end

  reg [32-1:0] fsm;
  localparam fsm_init = 0;
  reg [32-1:0] _d1_fsm;
  reg _fsm_cond_4_0_1;
  localparam fsm_1 = 1;
  localparam fsm_2 = 2;
  localparam fsm_3 = 3;
  localparam fsm_4 = 4;
  localparam fsm_5 = 5;
  localparam fsm_6 = 6;
  localparam fsm_7 = 7;

  always @(posedge CLK) begin
    if(RST) begin
      fsm <= fsm_init;
      _d1_fsm <= fsm_init;
      _fsm_cond_4_0_1 <= 0;
    end else begin
      _d1_fsm <= fsm;
      case(_d1_fsm)
        fsm_4: begin
          if(_fsm_cond_4_0_1) begin
            start <= 0;
          end 
        end
      endcase
      case(fsm)
        fsm_init: begin
          if(reset_done) begin
            fsm <= fsm_1;
          end 
        end
        fsm_1: begin
          ext_src_ram0_addr <= -1;
          ext_src_ram1_addr <= -1;
          ext_src_ram2_addr <= -1;
          fsm <= fsm_2;
        end
        fsm_2: begin
          ext_src_ram0_addr <= ext_src_ram0_addr + 1;
          ext_src_ram0_wdata <= 'sd5898240;
          ext_src_ram0_wenable <= 1;
          if(ext_src_ram0_wenable && (ext_src_ram0_addr == 15)) begin
            ext_src_ram0_wenable <= 0;
          end 
          ext_src_ram1_addr <= ext_src_ram1_addr + 1;
          ext_src_ram1_wdata <= 'sd5898240;
          ext_src_ram1_wenable <= 1;
          if(ext_src_ram1_wenable && (ext_src_ram1_addr == 15)) begin
            ext_src_ram1_wenable <= 0;
          end 
          ext_src_ram2_addr <= ext_src_ram2_addr + 1;
          ext_src_ram2_wdata <= 'sd5898240;
          ext_src_ram2_wenable <= 1;
          if(ext_src_ram2_wenable && (ext_src_ram2_addr == 15)) begin
            ext_src_ram2_wenable <= 0;
          end 
          if(ext_src_ram2_wenable && (ext_src_ram0_addr == 15)) begin
            fsm <= fsm_3;
          end 
        end
        fsm_3: begin
          if(!busy) begin
            fsm <= fsm_4;
          end 
        end
        fsm_4: begin
          start <= 1;
          _fsm_cond_4_0_1 <= 1;
          fsm <= fsm_5;
        end
        fsm_5: begin
          if(busy) begin
            fsm <= fsm_6;
          end 
        end
        fsm_6: begin
          if(!busy) begin
            fsm <= fsm_7;
          end 
        end
        fsm_7: begin
          $finish;
        end
      endcase
    end
  end


endmodule



module stencil
(
  input CLK,
  input RST,
  input start,
  output reg busy,
  input [4-1:0] ext_src_ram0_addr,
  output [32-1:0] ext_src_ram0_rdata,
  input [32-1:0] ext_src_ram0_wdata,
  input ext_src_ram0_wenable,
  input [4-1:0] ext_src_ram1_addr,
  output [32-1:0] ext_src_ram1_rdata,
  input [32-1:0] ext_src_ram1_wdata,
  input ext_src_ram1_wenable,
  input [4-1:0] ext_src_ram2_addr,
  output [32-1:0] ext_src_ram2_rdata,
  input [32-1:0] ext_src_ram2_wdata,
  input ext_src_ram2_wenable,
  input [4-1:0] ext_dst_ram_addr,
  output [32-1:0] ext_dst_ram_rdata,
  input [32-1:0] ext_dst_ram_wdata,
  input ext_dst_ram_wenable
);

  reg _tmp_0;
  reg [8-1:0] src_ram0_0_addr;
  wire [32-1:0] src_ram0_0_rdata;
  reg [32-1:0] src_ram0_0_wdata;
  reg src_ram0_0_wenable;
  reg [8-1:0] src_ram0_1_addr;
  wire [32-1:0] src_ram0_1_rdata;
  reg [32-1:0] src_ram0_1_wdata;
  reg src_ram0_1_wenable;

  src_ram0
  inst_src_ram0
  (
    .CLK(CLK),
    .src_ram0_0_addr(src_ram0_0_addr),
    .src_ram0_0_rdata(src_ram0_0_rdata),
    .src_ram0_0_wdata(src_ram0_0_wdata),
    .src_ram0_0_wenable(src_ram0_0_wenable),
    .src_ram0_1_addr(src_ram0_1_addr),
    .src_ram0_1_rdata(src_ram0_1_rdata),
    .src_ram0_1_wdata(src_ram0_1_wdata),
    .src_ram0_1_wenable(src_ram0_1_wenable)
  );

  reg [8-1:0] src_ram1_0_addr;
  wire [32-1:0] src_ram1_0_rdata;
  reg [32-1:0] src_ram1_0_wdata;
  reg src_ram1_0_wenable;
  reg [8-1:0] src_ram1_1_addr;
  wire [32-1:0] src_ram1_1_rdata;
  reg [32-1:0] src_ram1_1_wdata;
  reg src_ram1_1_wenable;

  src_ram1
  inst_src_ram1
  (
    .CLK(CLK),
    .src_ram1_0_addr(src_ram1_0_addr),
    .src_ram1_0_rdata(src_ram1_0_rdata),
    .src_ram1_0_wdata(src_ram1_0_wdata),
    .src_ram1_0_wenable(src_ram1_0_wenable),
    .src_ram1_1_addr(src_ram1_1_addr),
    .src_ram1_1_rdata(src_ram1_1_rdata),
    .src_ram1_1_wdata(src_ram1_1_wdata),
    .src_ram1_1_wenable(src_ram1_1_wenable)
  );

  reg [8-1:0] src_ram2_0_addr;
  wire [32-1:0] src_ram2_0_rdata;
  reg [32-1:0] src_ram2_0_wdata;
  reg src_ram2_0_wenable;
  reg [8-1:0] src_ram2_1_addr;
  wire [32-1:0] src_ram2_1_rdata;
  reg [32-1:0] src_ram2_1_wdata;
  reg src_ram2_1_wenable;

  src_ram2
  inst_src_ram2
  (
    .CLK(CLK),
    .src_ram2_0_addr(src_ram2_0_addr),
    .src_ram2_0_rdata(src_ram2_0_rdata),
    .src_ram2_0_wdata(src_ram2_0_wdata),
    .src_ram2_0_wenable(src_ram2_0_wenable),
    .src_ram2_1_addr(src_ram2_1_addr),
    .src_ram2_1_rdata(src_ram2_1_rdata),
    .src_ram2_1_wdata(src_ram2_1_wdata),
    .src_ram2_1_wenable(src_ram2_1_wenable)
  );

  reg [8-1:0] dst_ram_0_addr;
  wire [32-1:0] dst_ram_0_rdata;
  reg [32-1:0] dst_ram_0_wdata;
  reg dst_ram_0_wenable;
  reg [8-1:0] dst_ram_1_addr;
  wire [32-1:0] dst_ram_1_rdata;
  reg [32-1:0] dst_ram_1_wdata;
  reg dst_ram_1_wenable;

  dst_ram
  inst_dst_ram
  (
    .CLK(CLK),
    .dst_ram_0_addr(dst_ram_0_addr),
    .dst_ram_0_rdata(dst_ram_0_rdata),
    .dst_ram_0_wdata(dst_ram_0_wdata),
    .dst_ram_0_wenable(dst_ram_0_wenable),
    .dst_ram_1_addr(dst_ram_1_addr),
    .dst_ram_1_rdata(dst_ram_1_rdata),
    .dst_ram_1_wdata(dst_ram_1_wdata),
    .dst_ram_1_wenable(dst_ram_1_wenable)
  );

  wire [8-1:0] _tmp_1;
  assign _tmp_1 = ext_src_ram0_addr;

  always @(*) begin
    src_ram0_1_addr = _tmp_1;
  end

  assign ext_src_ram0_rdata = src_ram0_1_rdata;
  wire [32-1:0] _tmp_2;
  assign _tmp_2 = ext_src_ram0_wdata;

  always @(*) begin
    src_ram0_1_wdata = _tmp_2;
  end

  wire _tmp_3;
  assign _tmp_3 = ext_src_ram0_wenable;

  always @(*) begin
    src_ram0_1_wenable = _tmp_3;
  end

  wire [8-1:0] _tmp_4;
  assign _tmp_4 = ext_src_ram1_addr;

  always @(*) begin
    src_ram1_1_addr = _tmp_4;
  end

  assign ext_src_ram1_rdata = src_ram1_1_rdata;
  wire [32-1:0] _tmp_5;
  assign _tmp_5 = ext_src_ram1_wdata;

  always @(*) begin
    src_ram1_1_wdata = _tmp_5;
  end

  wire _tmp_6;
  assign _tmp_6 = ext_src_ram1_wenable;

  always @(*) begin
    src_ram1_1_wenable = _tmp_6;
  end

  wire [8-1:0] _tmp_7;
  assign _tmp_7 = ext_src_ram2_addr;

  always @(*) begin
    src_ram2_1_addr = _tmp_7;
  end

  assign ext_src_ram2_rdata = src_ram2_1_rdata;
  wire [32-1:0] _tmp_8;
  assign _tmp_8 = ext_src_ram2_wdata;

  always @(*) begin
    src_ram2_1_wdata = _tmp_8;
  end

  wire _tmp_9;
  assign _tmp_9 = ext_src_ram2_wenable;

  always @(*) begin
    src_ram2_1_wenable = _tmp_9;
  end

  wire [8-1:0] _tmp_10;
  assign _tmp_10 = ext_dst_ram_addr;

  always @(*) begin
    dst_ram_1_addr = _tmp_10;
  end

  assign ext_dst_ram_rdata = dst_ram_1_rdata;
  wire [32-1:0] _tmp_11;
  assign _tmp_11 = ext_dst_ram_wdata;

  always @(*) begin
    dst_ram_1_wdata = _tmp_11;
  end

  wire _tmp_12;
  assign _tmp_12 = ext_dst_ram_wenable;

  always @(*) begin
    dst_ram_1_wenable = _tmp_12;
  end

  reg [32-1:0] read_fsm;
  localparam read_fsm_init = 0;
  reg [32-1:0] read_count;
  reg [32-1:0] read_addr;
  reg _tmp_13;
  reg _src_ram0_cond_0_1;
  reg _src_ram0_cond_1_1;
  reg _src_ram0_cond_1_2;
  reg _tmp_14;
  reg _src_ram1_cond_0_1;
  reg _src_ram1_cond_1_1;
  reg _src_ram1_cond_1_2;
  reg _tmp_15;
  reg _src_ram2_cond_0_1;
  reg _src_ram2_cond_1_1;
  reg _src_ram2_cond_1_2;
  localparam read_fsm_1 = 1;
  localparam read_fsm_2 = 2;

  always @(posedge CLK) begin
    if(RST) begin
      read_fsm <= read_fsm_init;
      read_addr <= 0;
      read_count <= 0;
      busy <= 0;
    end else begin
      case(read_fsm)
        read_fsm_init: begin
          read_addr <= 0;
          read_count <= 0;
          busy <= 0;
          if(start) begin
            busy <= 1;
          end 
          if(start) begin
            read_fsm <= read_fsm_1;
          end 
        end
        read_fsm_1: begin
          read_addr <= read_addr + 1;
          read_count <= read_count + 1;
          if(read_count == 15) begin
            read_addr <= 0;
            read_count <= 0;
          end 
          if(read_count == 15) begin
            read_fsm <= read_fsm_2;
          end 
        end
        read_fsm_2: begin
          if(_tmp_0) begin
            busy <= 0;
          end 
          if(_tmp_0) begin
            read_fsm <= read_fsm_init;
          end 
        end
      endcase
    end
  end

  wire [32-1:0] odata;
  wire ovalid;

  stencil_pipeline_2d
  inst_stencil
  (
    .CLK(CLK),
    .RST(RST),
    .idata0(src_ram0_0_rdata),
    .ivalid0(_tmp_13),
    .idata1(src_ram1_0_rdata),
    .ivalid1(_tmp_14),
    .idata2(src_ram2_0_rdata),
    .ivalid2(_tmp_15),
    .odata(odata),
    .ovalid(ovalid)
  );

  reg [32-1:0] write_fsm;
  localparam write_fsm_init = 0;
  reg [32-1:0] write_count;
  reg [32-1:0] write_addr;
  reg _dst_ram_cond_0_1;

  always @(posedge CLK) begin
    if(RST) begin
      write_fsm <= write_fsm_init;
      _tmp_0 <= 0;
      write_addr <= 1;
      write_count <= 0;
    end else begin
      case(write_fsm)
        write_fsm_init: begin
          _tmp_0 <= 0;
          if(ovalid && (write_count > 1)) begin
            write_addr <= write_addr + 1;
          end 
          if(ovalid) begin
            write_count <= write_count + 1;
          end 
          if(write_count == 16) begin
            write_count <= 0;
            write_addr <= 1;
            _tmp_0 <= 1;
          end 
          if(write_count == 16) begin
            write_fsm <= write_fsm_init;
          end 
        end
      endcase
    end
  end


  always @(posedge CLK) begin
    if(RST) begin
      src_ram0_0_wdata <= 0;
      src_ram0_0_wenable <= 0;
      src_ram0_0_addr <= 0;
      _src_ram0_cond_0_1 <= 0;
      _tmp_13 <= 0;
      _src_ram0_cond_1_1 <= 0;
      _src_ram0_cond_1_2 <= 0;
    end else begin
      if(_src_ram0_cond_1_2) begin
        _tmp_13 <= 0;
      end 
      if(_src_ram0_cond_0_1) begin
        _tmp_13 <= 1;
      end 
      _src_ram0_cond_1_2 <= _src_ram0_cond_1_1;
      src_ram0_0_wdata <= 0;
      src_ram0_0_wenable <= 0;
      if(read_fsm == 1) begin
        src_ram0_0_addr <= read_addr;
      end 
      _src_ram0_cond_0_1 <= read_fsm == 1;
      _src_ram0_cond_1_1 <= read_fsm == 1;
    end
  end


  always @(posedge CLK) begin
    if(RST) begin
      src_ram1_0_wdata <= 0;
      src_ram1_0_wenable <= 0;
      src_ram1_0_addr <= 0;
      _src_ram1_cond_0_1 <= 0;
      _tmp_14 <= 0;
      _src_ram1_cond_1_1 <= 0;
      _src_ram1_cond_1_2 <= 0;
    end else begin
      if(_src_ram1_cond_1_2) begin
        _tmp_14 <= 0;
      end 
      if(_src_ram1_cond_0_1) begin
        _tmp_14 <= 1;
      end 
      _src_ram1_cond_1_2 <= _src_ram1_cond_1_1;
      src_ram1_0_wdata <= 0;
      src_ram1_0_wenable <= 0;
      if(read_fsm == 1) begin
        src_ram1_0_addr <= read_addr;
      end 
      _src_ram1_cond_0_1 <= read_fsm == 1;
      _src_ram1_cond_1_1 <= read_fsm == 1;
    end
  end


  always @(posedge CLK) begin
    if(RST) begin
      src_ram2_0_wdata <= 0;
      src_ram2_0_wenable <= 0;
      src_ram2_0_addr <= 0;
      _src_ram2_cond_0_1 <= 0;
      _tmp_15 <= 0;
      _src_ram2_cond_1_1 <= 0;
      _src_ram2_cond_1_2 <= 0;
    end else begin
      if(_src_ram2_cond_1_2) begin
        _tmp_15 <= 0;
      end 
      if(_src_ram2_cond_0_1) begin
        _tmp_15 <= 1;
      end 
      _src_ram2_cond_1_2 <= _src_ram2_cond_1_1;
      src_ram2_0_wdata <= 0;
      src_ram2_0_wenable <= 0;
      if(read_fsm == 1) begin
        src_ram2_0_addr <= read_addr;
      end 
      _src_ram2_cond_0_1 <= read_fsm == 1;
      _src_ram2_cond_1_1 <= read_fsm == 1;
    end
  end


  always @(posedge CLK) begin
    if(RST) begin
      dst_ram_0_addr <= 0;
      dst_ram_0_wdata <= 0;
      dst_ram_0_wenable <= 0;
      _dst_ram_cond_0_1 <= 0;
    end else begin
      if(_dst_ram_cond_0_1) begin
        dst_ram_0_wenable <= 0;
      end 
      if((write_fsm == 0) && (ovalid && (write_count > 1))) begin
        dst_ram_0_addr <= write_addr;
        dst_ram_0_wdata <= odata;
        dst_ram_0_wenable <= 1;
      end 
      _dst_ram_cond_0_1 <= (write_fsm == 0) && (ovalid && (write_count > 1));
    end
  end


endmodule



module src_ram0
(
  input CLK,
  input [8-1:0] src_ram0_0_addr,
  output [32-1:0] src_ram0_0_rdata,
  input [32-1:0] src_ram0_0_wdata,
  input src_ram0_0_wenable,
  input [8-1:0] src_ram0_1_addr,
  output [32-1:0] src_ram0_1_rdata,
  input [32-1:0] src_ram0_1_wdata,
  input src_ram0_1_wenable
);

  reg [8-1:0] src_ram0_0_daddr;
  reg [8-1:0] src_ram0_1_daddr;
  reg [32-1:0] mem [0:256-1];

  always @(posedge CLK) begin
    if(src_ram0_0_wenable) begin
      mem[src_ram0_0_addr] <= src_ram0_0_wdata;
    end 
    src_ram0_0_daddr <= src_ram0_0_addr;
  end

  assign src_ram0_0_rdata = mem[src_ram0_0_daddr];

  always @(posedge CLK) begin
    if(src_ram0_1_wenable) begin
      mem[src_ram0_1_addr] <= src_ram0_1_wdata;
    end 
    src_ram0_1_daddr <= src_ram0_1_addr;
  end

  assign src_ram0_1_rdata = mem[src_ram0_1_daddr];

endmodule



module src_ram1
(
  input CLK,
  input [8-1:0] src_ram1_0_addr,
  output [32-1:0] src_ram1_0_rdata,
  input [32-1:0] src_ram1_0_wdata,
  input src_ram1_0_wenable,
  input [8-1:0] src_ram1_1_addr,
  output [32-1:0] src_ram1_1_rdata,
  input [32-1:0] src_ram1_1_wdata,
  input src_ram1_1_wenable
);

  reg [8-1:0] src_ram1_0_daddr;
  reg [8-1:0] src_ram1_1_daddr;
  reg [32-1:0] mem [0:256-1];

  always @(posedge CLK) begin
    if(src_ram1_0_wenable) begin
      mem[src_ram1_0_addr] <= src_ram1_0_wdata;
    end 
    src_ram1_0_daddr <= src_ram1_0_addr;
  end

  assign src_ram1_0_rdata = mem[src_ram1_0_daddr];

  always @(posedge CLK) begin
    if(src_ram1_1_wenable) begin
      mem[src_ram1_1_addr] <= src_ram1_1_wdata;
    end 
    src_ram1_1_daddr <= src_ram1_1_addr;
  end

  assign src_ram1_1_rdata = mem[src_ram1_1_daddr];

endmodule



module src_ram2
(
  input CLK,
  input [8-1:0] src_ram2_0_addr,
  output [32-1:0] src_ram2_0_rdata,
  input [32-1:0] src_ram2_0_wdata,
  input src_ram2_0_wenable,
  input [8-1:0] src_ram2_1_addr,
  output [32-1:0] src_ram2_1_rdata,
  input [32-1:0] src_ram2_1_wdata,
  input src_ram2_1_wenable
);

  reg [8-1:0] src_ram2_0_daddr;
  reg [8-1:0] src_ram2_1_daddr;
  reg [32-1:0] mem [0:256-1];

  always @(posedge CLK) begin
    if(src_ram2_0_wenable) begin
      mem[src_ram2_0_addr] <= src_ram2_0_wdata;
    end 
    src_ram2_0_daddr <= src_ram2_0_addr;
  end

  assign src_ram2_0_rdata = mem[src_ram2_0_daddr];

  always @(posedge CLK) begin
    if(src_ram2_1_wenable) begin
      mem[src_ram2_1_addr] <= src_ram2_1_wdata;
    end 
    src_ram2_1_daddr <= src_ram2_1_addr;
  end

  assign src_ram2_1_rdata = mem[src_ram2_1_daddr];

endmodule



module dst_ram
(
  input CLK,
  input [8-1:0] dst_ram_0_addr,
  output [32-1:0] dst_ram_0_rdata,
  input [32-1:0] dst_ram_0_wdata,
  input dst_ram_0_wenable,
  input [8-1:0] dst_ram_1_addr,
  output [32-1:0] dst_ram_1_rdata,
  input [32-1:0] dst_ram_1_wdata,
  input dst_ram_1_wenable
);

  reg [8-1:0] dst_ram_0_daddr;
  reg [8-1:0] dst_ram_1_daddr;
  reg [32-1:0] mem [0:256-1];

  always @(posedge CLK) begin
    if(dst_ram_0_wenable) begin
      mem[dst_ram_0_addr] <= dst_ram_0_wdata;
    end 
    dst_ram_0_daddr <= dst_ram_0_addr;
  end

  assign dst_ram_0_rdata = mem[dst_ram_0_daddr];

  always @(posedge CLK) begin
    if(dst_ram_1_wenable) begin
      mem[dst_ram_1_addr] <= dst_ram_1_wdata;
    end 
    dst_ram_1_daddr <= dst_ram_1_addr;
  end

  assign dst_ram_1_rdata = mem[dst_ram_1_daddr];

endmodule



module stencil_pipeline_2d
(
  input CLK,
  input RST,
  input signed [32-1:0] idata0,
  input ivalid0,
  input signed [32-1:0] idata1,
  input ivalid1,
  input signed [32-1:0] idata2,
  input ivalid2,
  output signed [32-1:0] odata,
  output ovalid
);

  reg signed [32-1:0] __prev_data_0;
  reg signed [32-1:0] __prev_data_1;
  reg signed [32-1:0] __prev_data_2;
  reg signed [32-1:0] __prev_data_3;
  reg signed [32-1:0] __prev_data_4;
  reg signed [32-1:0] __prev_data_5;
  wire signed [32-1:0] _times_data_6;
  wire _times_valid_6;
  wire _times_ready_6;
  wire signed [46-1:0] _times_odata_6;
  reg signed [46-1:0] _times_data_reg_6;
  assign _times_data_6 = _times_data_reg_6;
  wire _times_ovalid_6;
  reg _times_valid_reg_6;
  assign _times_valid_6 = _times_valid_reg_6;
  wire _times_enable_6;
  wire _times_update_6;
  assign _times_enable_6 = (_times_ready_6 || !_times_valid_6) && 1 && ivalid0;
  assign _times_update_6 = _times_ready_6 || !_times_valid_6;

  multiplier_0
  mul6
  (
    .CLK(CLK),
    .RST(RST),
    .update(_times_update_6),
    .enable(_times_enable_6),
    .valid(_times_ovalid_6),
    .a(idata0),
    .b(14'sd7281),
    .c(_times_odata_6)
  );

  wire signed [32-1:0] _times_data_7;
  wire _times_valid_7;
  wire _times_ready_7;
  wire signed [46-1:0] _times_odata_7;
  reg signed [46-1:0] _times_data_reg_7;
  assign _times_data_7 = _times_data_reg_7;
  wire _times_ovalid_7;
  reg _times_valid_reg_7;
  assign _times_valid_7 = _times_valid_reg_7;
  wire _times_enable_7;
  wire _times_update_7;
  assign _times_enable_7 = (_times_ready_7 || !_times_valid_7) && 1 && ivalid0;
  assign _times_update_7 = _times_ready_7 || !_times_valid_7;

  multiplier_1
  mul7
  (
    .CLK(CLK),
    .RST(RST),
    .update(_times_update_7),
    .enable(_times_enable_7),
    .valid(_times_ovalid_7),
    .a(__prev_data_0),
    .b(14'sd7281),
    .c(_times_odata_7)
  );

  wire signed [32-1:0] _times_data_8;
  wire _times_valid_8;
  wire _times_ready_8;
  wire signed [46-1:0] _times_odata_8;
  reg signed [46-1:0] _times_data_reg_8;
  assign _times_data_8 = _times_data_reg_8;
  wire _times_ovalid_8;
  reg _times_valid_reg_8;
  assign _times_valid_8 = _times_valid_reg_8;
  wire _times_enable_8;
  wire _times_update_8;
  assign _times_enable_8 = (_times_ready_8 || !_times_valid_8) && 1 && ivalid0;
  assign _times_update_8 = _times_ready_8 || !_times_valid_8;

  multiplier_2
  mul8
  (
    .CLK(CLK),
    .RST(RST),
    .update(_times_update_8),
    .enable(_times_enable_8),
    .valid(_times_ovalid_8),
    .a(__prev_data_1),
    .b(14'sd7281),
    .c(_times_odata_8)
  );

  wire signed [32-1:0] _times_data_9;
  wire _times_valid_9;
  wire _times_ready_9;
  wire signed [46-1:0] _times_odata_9;
  reg signed [46-1:0] _times_data_reg_9;
  assign _times_data_9 = _times_data_reg_9;
  wire _times_ovalid_9;
  reg _times_valid_reg_9;
  assign _times_valid_9 = _times_valid_reg_9;
  wire _times_enable_9;
  wire _times_update_9;
  assign _times_enable_9 = (_times_ready_9 || !_times_valid_9) && 1 && ivalid1;
  assign _times_update_9 = _times_ready_9 || !_times_valid_9;

  multiplier_3
  mul9
  (
    .CLK(CLK),
    .RST(RST),
    .update(_times_update_9),
    .enable(_times_enable_9),
    .valid(_times_ovalid_9),
    .a(idata1),
    .b(14'sd7281),
    .c(_times_odata_9)
  );

  wire signed [32-1:0] _times_data_10;
  wire _times_valid_10;
  wire _times_ready_10;
  wire signed [46-1:0] _times_odata_10;
  reg signed [46-1:0] _times_data_reg_10;
  assign _times_data_10 = _times_data_reg_10;
  wire _times_ovalid_10;
  reg _times_valid_reg_10;
  assign _times_valid_10 = _times_valid_reg_10;
  wire _times_enable_10;
  wire _times_update_10;
  assign _times_enable_10 = (_times_ready_10 || !_times_valid_10) && 1 && ivalid1;
  assign _times_update_10 = _times_ready_10 || !_times_valid_10;

  multiplier_4
  mul10
  (
    .CLK(CLK),
    .RST(RST),
    .update(_times_update_10),
    .enable(_times_enable_10),
    .valid(_times_ovalid_10),
    .a(__prev_data_2),
    .b(14'sd7281),
    .c(_times_odata_10)
  );

  wire signed [32-1:0] _times_data_11;
  wire _times_valid_11;
  wire _times_ready_11;
  wire signed [46-1:0] _times_odata_11;
  reg signed [46-1:0] _times_data_reg_11;
  assign _times_data_11 = _times_data_reg_11;
  wire _times_ovalid_11;
  reg _times_valid_reg_11;
  assign _times_valid_11 = _times_valid_reg_11;
  wire _times_enable_11;
  wire _times_update_11;
  assign _times_enable_11 = (_times_ready_11 || !_times_valid_11) && 1 && ivalid1;
  assign _times_update_11 = _times_ready_11 || !_times_valid_11;

  multiplier_5
  mul11
  (
    .CLK(CLK),
    .RST(RST),
    .update(_times_update_11),
    .enable(_times_enable_11),
    .valid(_times_ovalid_11),
    .a(__prev_data_3),
    .b(14'sd7281),
    .c(_times_odata_11)
  );

  wire signed [32-1:0] _times_data_12;
  wire _times_valid_12;
  wire _times_ready_12;
  wire signed [46-1:0] _times_odata_12;
  reg signed [46-1:0] _times_data_reg_12;
  assign _times_data_12 = _times_data_reg_12;
  wire _times_ovalid_12;
  reg _times_valid_reg_12;
  assign _times_valid_12 = _times_valid_reg_12;
  wire _times_enable_12;
  wire _times_update_12;
  assign _times_enable_12 = (_times_ready_12 || !_times_valid_12) && 1 && ivalid2;
  assign _times_update_12 = _times_ready_12 || !_times_valid_12;

  multiplier_6
  mul12
  (
    .CLK(CLK),
    .RST(RST),
    .update(_times_update_12),
    .enable(_times_enable_12),
    .valid(_times_ovalid_12),
    .a(idata2),
    .b(14'sd7281),
    .c(_times_odata_12)
  );

  wire signed [32-1:0] _times_data_13;
  wire _times_valid_13;
  wire _times_ready_13;
  wire signed [46-1:0] _times_odata_13;
  reg signed [46-1:0] _times_data_reg_13;
  assign _times_data_13 = _times_data_reg_13;
  wire _times_ovalid_13;
  reg _times_valid_reg_13;
  assign _times_valid_13 = _times_valid_reg_13;
  wire _times_enable_13;
  wire _times_update_13;
  assign _times_enable_13 = (_times_ready_13 || !_times_valid_13) && 1 && ivalid2;
  assign _times_update_13 = _times_ready_13 || !_times_valid_13;

  multiplier_7
  mul13
  (
    .CLK(CLK),
    .RST(RST),
    .update(_times_update_13),
    .enable(_times_enable_13),
    .valid(_times_ovalid_13),
    .a(__prev_data_4),
    .b(14'sd7281),
    .c(_times_odata_13)
  );

  wire signed [32-1:0] _times_data_14;
  wire _times_valid_14;
  wire _times_ready_14;
  wire signed [46-1:0] _times_odata_14;
  reg signed [46-1:0] _times_data_reg_14;
  assign _times_data_14 = _times_data_reg_14;
  wire _times_ovalid_14;
  reg _times_valid_reg_14;
  assign _times_valid_14 = _times_valid_reg_14;
  wire _times_enable_14;
  wire _times_update_14;
  assign _times_enable_14 = (_times_ready_14 || !_times_valid_14) && 1 && ivalid2;
  assign _times_update_14 = _times_ready_14 || !_times_valid_14;

  multiplier_8
  mul14
  (
    .CLK(CLK),
    .RST(RST),
    .update(_times_update_14),
    .enable(_times_enable_14),
    .valid(_times_ovalid_14),
    .a(__prev_data_5),
    .b(14'sd7281),
    .c(_times_odata_14)
  );

  reg signed [32-1:0] _plus_data_15;
  reg _plus_valid_15;
  wire _plus_ready_15;
  assign _times_ready_6 = (_plus_ready_15 || !_plus_valid_15) && (_times_valid_6 && _times_valid_7);
  assign _times_ready_7 = (_plus_ready_15 || !_plus_valid_15) && (_times_valid_6 && _times_valid_7);
  reg signed [32-1:0] __delay_data_16;
  reg __delay_valid_16;
  wire __delay_ready_16;
  assign _times_ready_8 = (__delay_ready_16 || !__delay_valid_16) && _times_valid_8;
  reg signed [32-1:0] __delay_data_17;
  reg __delay_valid_17;
  wire __delay_ready_17;
  assign _times_ready_9 = (__delay_ready_17 || !__delay_valid_17) && _times_valid_9;
  reg signed [32-1:0] __delay_data_18;
  reg __delay_valid_18;
  wire __delay_ready_18;
  assign _times_ready_10 = (__delay_ready_18 || !__delay_valid_18) && _times_valid_10;
  reg signed [32-1:0] __delay_data_19;
  reg __delay_valid_19;
  wire __delay_ready_19;
  assign _times_ready_11 = (__delay_ready_19 || !__delay_valid_19) && _times_valid_11;
  reg signed [32-1:0] __delay_data_20;
  reg __delay_valid_20;
  wire __delay_ready_20;
  assign _times_ready_12 = (__delay_ready_20 || !__delay_valid_20) && _times_valid_12;
  reg signed [32-1:0] __delay_data_21;
  reg __delay_valid_21;
  wire __delay_ready_21;
  assign _times_ready_13 = (__delay_ready_21 || !__delay_valid_21) && _times_valid_13;
  reg signed [32-1:0] __delay_data_22;
  reg __delay_valid_22;
  wire __delay_ready_22;
  assign _times_ready_14 = (__delay_ready_22 || !__delay_valid_22) && _times_valid_14;
  reg signed [32-1:0] _plus_data_23;
  reg _plus_valid_23;
  wire _plus_ready_23;
  assign _plus_ready_15 = (_plus_ready_23 || !_plus_valid_23) && (_plus_valid_15 && __delay_valid_16);
  assign __delay_ready_16 = (_plus_ready_23 || !_plus_valid_23) && (_plus_valid_15 && __delay_valid_16);
  reg signed [32-1:0] __delay_data_24;
  reg __delay_valid_24;
  wire __delay_ready_24;
  assign __delay_ready_17 = (__delay_ready_24 || !__delay_valid_24) && __delay_valid_17;
  reg signed [32-1:0] __delay_data_25;
  reg __delay_valid_25;
  wire __delay_ready_25;
  assign __delay_ready_18 = (__delay_ready_25 || !__delay_valid_25) && __delay_valid_18;
  reg signed [32-1:0] __delay_data_26;
  reg __delay_valid_26;
  wire __delay_ready_26;
  assign __delay_ready_19 = (__delay_ready_26 || !__delay_valid_26) && __delay_valid_19;
  reg signed [32-1:0] __delay_data_27;
  reg __delay_valid_27;
  wire __delay_ready_27;
  assign __delay_ready_20 = (__delay_ready_27 || !__delay_valid_27) && __delay_valid_20;
  reg signed [32-1:0] __delay_data_28;
  reg __delay_valid_28;
  wire __delay_ready_28;
  assign __delay_ready_21 = (__delay_ready_28 || !__delay_valid_28) && __delay_valid_21;
  reg signed [32-1:0] __delay_data_29;
  reg __delay_valid_29;
  wire __delay_ready_29;
  assign __delay_ready_22 = (__delay_ready_29 || !__delay_valid_29) && __delay_valid_22;
  reg signed [32-1:0] _plus_data_30;
  reg _plus_valid_30;
  wire _plus_ready_30;
  assign _plus_ready_23 = (_plus_ready_30 || !_plus_valid_30) && (_plus_valid_23 && __delay_valid_24);
  assign __delay_ready_24 = (_plus_ready_30 || !_plus_valid_30) && (_plus_valid_23 && __delay_valid_24);
  reg signed [32-1:0] __delay_data_31;
  reg __delay_valid_31;
  wire __delay_ready_31;
  assign __delay_ready_25 = (__delay_ready_31 || !__delay_valid_31) && __delay_valid_25;
  reg signed [32-1:0] __delay_data_32;
  reg __delay_valid_32;
  wire __delay_ready_32;
  assign __delay_ready_26 = (__delay_ready_32 || !__delay_valid_32) && __delay_valid_26;
  reg signed [32-1:0] __delay_data_33;
  reg __delay_valid_33;
  wire __delay_ready_33;
  assign __delay_ready_27 = (__delay_ready_33 || !__delay_valid_33) && __delay_valid_27;
  reg signed [32-1:0] __delay_data_34;
  reg __delay_valid_34;
  wire __delay_ready_34;
  assign __delay_ready_28 = (__delay_ready_34 || !__delay_valid_34) && __delay_valid_28;
  reg signed [32-1:0] __delay_data_35;
  reg __delay_valid_35;
  wire __delay_ready_35;
  assign __delay_ready_29 = (__delay_ready_35 || !__delay_valid_35) && __delay_valid_29;
  reg signed [32-1:0] _plus_data_36;
  reg _plus_valid_36;
  wire _plus_ready_36;
  assign _plus_ready_30 = (_plus_ready_36 || !_plus_valid_36) && (_plus_valid_30 && __delay_valid_31);
  assign __delay_ready_31 = (_plus_ready_36 || !_plus_valid_36) && (_plus_valid_30 && __delay_valid_31);
  reg signed [32-1:0] __delay_data_37;
  reg __delay_valid_37;
  wire __delay_ready_37;
  assign __delay_ready_32 = (__delay_ready_37 || !__delay_valid_37) && __delay_valid_32;
  reg signed [32-1:0] __delay_data_38;
  reg __delay_valid_38;
  wire __delay_ready_38;
  assign __delay_ready_33 = (__delay_ready_38 || !__delay_valid_38) && __delay_valid_33;
  reg signed [32-1:0] __delay_data_39;
  reg __delay_valid_39;
  wire __delay_ready_39;
  assign __delay_ready_34 = (__delay_ready_39 || !__delay_valid_39) && __delay_valid_34;
  reg signed [32-1:0] __delay_data_40;
  reg __delay_valid_40;
  wire __delay_ready_40;
  assign __delay_ready_35 = (__delay_ready_40 || !__delay_valid_40) && __delay_valid_35;
  reg signed [32-1:0] _plus_data_41;
  reg _plus_valid_41;
  wire _plus_ready_41;
  assign _plus_ready_36 = (_plus_ready_41 || !_plus_valid_41) && (_plus_valid_36 && __delay_valid_37);
  assign __delay_ready_37 = (_plus_ready_41 || !_plus_valid_41) && (_plus_valid_36 && __delay_valid_37);
  reg signed [32-1:0] __delay_data_42;
  reg __delay_valid_42;
  wire __delay_ready_42;
  assign __delay_ready_38 = (__delay_ready_42 || !__delay_valid_42) && __delay_valid_38;
  reg signed [32-1:0] __delay_data_43;
  reg __delay_valid_43;
  wire __delay_ready_43;
  assign __delay_ready_39 = (__delay_ready_43 || !__delay_valid_43) && __delay_valid_39;
  reg signed [32-1:0] __delay_data_44;
  reg __delay_valid_44;
  wire __delay_ready_44;
  assign __delay_ready_40 = (__delay_ready_44 || !__delay_valid_44) && __delay_valid_40;
  reg signed [32-1:0] _plus_data_45;
  reg _plus_valid_45;
  wire _plus_ready_45;
  assign _plus_ready_41 = (_plus_ready_45 || !_plus_valid_45) && (_plus_valid_41 && __delay_valid_42);
  assign __delay_ready_42 = (_plus_ready_45 || !_plus_valid_45) && (_plus_valid_41 && __delay_valid_42);
  reg signed [32-1:0] __delay_data_46;
  reg __delay_valid_46;
  wire __delay_ready_46;
  assign __delay_ready_43 = (__delay_ready_46 || !__delay_valid_46) && __delay_valid_43;
  reg signed [32-1:0] __delay_data_47;
  reg __delay_valid_47;
  wire __delay_ready_47;
  assign __delay_ready_44 = (__delay_ready_47 || !__delay_valid_47) && __delay_valid_44;
  reg signed [32-1:0] _plus_data_48;
  reg _plus_valid_48;
  wire _plus_ready_48;
  assign _plus_ready_45 = (_plus_ready_48 || !_plus_valid_48) && (_plus_valid_45 && __delay_valid_46);
  assign __delay_ready_46 = (_plus_ready_48 || !_plus_valid_48) && (_plus_valid_45 && __delay_valid_46);
  reg signed [32-1:0] __delay_data_49;
  reg __delay_valid_49;
  wire __delay_ready_49;
  assign __delay_ready_47 = (__delay_ready_49 || !__delay_valid_49) && __delay_valid_47;
  reg signed [32-1:0] _plus_data_50;
  reg _plus_valid_50;
  wire _plus_ready_50;
  assign _plus_ready_48 = (_plus_ready_50 || !_plus_valid_50) && (_plus_valid_48 && __delay_valid_49);
  assign __delay_ready_49 = (_plus_ready_50 || !_plus_valid_50) && (_plus_valid_48 && __delay_valid_49);
  assign odata = _plus_data_50;
  assign ovalid = _plus_valid_50;
  assign _plus_ready_50 = 1;

  always @(posedge CLK) begin
    if(RST) begin
      __prev_data_0 <= 0;
      __prev_data_1 <= 0;
      __prev_data_2 <= 0;
      __prev_data_3 <= 0;
      __prev_data_4 <= 0;
      __prev_data_5 <= 0;
      _times_data_reg_6 <= 0;
      _times_valid_reg_6 <= 0;
      _times_data_reg_7 <= 0;
      _times_valid_reg_7 <= 0;
      _times_data_reg_8 <= 0;
      _times_valid_reg_8 <= 0;
      _times_data_reg_9 <= 0;
      _times_valid_reg_9 <= 0;
      _times_data_reg_10 <= 0;
      _times_valid_reg_10 <= 0;
      _times_data_reg_11 <= 0;
      _times_valid_reg_11 <= 0;
      _times_data_reg_12 <= 0;
      _times_valid_reg_12 <= 0;
      _times_data_reg_13 <= 0;
      _times_valid_reg_13 <= 0;
      _times_data_reg_14 <= 0;
      _times_valid_reg_14 <= 0;
      _plus_data_15 <= 0;
      _plus_valid_15 <= 0;
      __delay_data_16 <= 0;
      __delay_valid_16 <= 0;
      __delay_data_17 <= 0;
      __delay_valid_17 <= 0;
      __delay_data_18 <= 0;
      __delay_valid_18 <= 0;
      __delay_data_19 <= 0;
      __delay_valid_19 <= 0;
      __delay_data_20 <= 0;
      __delay_valid_20 <= 0;
      __delay_data_21 <= 0;
      __delay_valid_21 <= 0;
      __delay_data_22 <= 0;
      __delay_valid_22 <= 0;
      _plus_data_23 <= 0;
      _plus_valid_23 <= 0;
      __delay_data_24 <= 0;
      __delay_valid_24 <= 0;
      __delay_data_25 <= 0;
      __delay_valid_25 <= 0;
      __delay_data_26 <= 0;
      __delay_valid_26 <= 0;
      __delay_data_27 <= 0;
      __delay_valid_27 <= 0;
      __delay_data_28 <= 0;
      __delay_valid_28 <= 0;
      __delay_data_29 <= 0;
      __delay_valid_29 <= 0;
      _plus_data_30 <= 0;
      _plus_valid_30 <= 0;
      __delay_data_31 <= 0;
      __delay_valid_31 <= 0;
      __delay_data_32 <= 0;
      __delay_valid_32 <= 0;
      __delay_data_33 <= 0;
      __delay_valid_33 <= 0;
      __delay_data_34 <= 0;
      __delay_valid_34 <= 0;
      __delay_data_35 <= 0;
      __delay_valid_35 <= 0;
      _plus_data_36 <= 0;
      _plus_valid_36 <= 0;
      __delay_data_37 <= 0;
      __delay_valid_37 <= 0;
      __delay_data_38 <= 0;
      __delay_valid_38 <= 0;
      __delay_data_39 <= 0;
      __delay_valid_39 <= 0;
      __delay_data_40 <= 0;
      __delay_valid_40 <= 0;
      _plus_data_41 <= 0;
      _plus_valid_41 <= 0;
      __delay_data_42 <= 0;
      __delay_valid_42 <= 0;
      __delay_data_43 <= 0;
      __delay_valid_43 <= 0;
      __delay_data_44 <= 0;
      __delay_valid_44 <= 0;
      _plus_data_45 <= 0;
      _plus_valid_45 <= 0;
      __delay_data_46 <= 0;
      __delay_valid_46 <= 0;
      __delay_data_47 <= 0;
      __delay_valid_47 <= 0;
      _plus_data_48 <= 0;
      _plus_valid_48 <= 0;
      __delay_data_49 <= 0;
      __delay_valid_49 <= 0;
      _plus_data_50 <= 0;
      _plus_valid_50 <= 0;
    end else begin
      if(ivalid0) begin
        __prev_data_0 <= idata0;
      end 
      if(ivalid0) begin
        __prev_data_1 <= __prev_data_0;
      end 
      if(ivalid1) begin
        __prev_data_2 <= idata1;
      end 
      if(ivalid1) begin
        __prev_data_3 <= __prev_data_2;
      end 
      if(ivalid2) begin
        __prev_data_4 <= idata2;
      end 
      if(ivalid2) begin
        __prev_data_5 <= __prev_data_4;
      end 
      if(_times_ready_6 || !_times_valid_6) begin
        _times_data_reg_6 <= _times_odata_6 >>> 16;
      end 
      if(_times_ready_6 || !_times_valid_6) begin
        _times_valid_reg_6 <= _times_ovalid_6;
      end 
      if(_times_ready_7 || !_times_valid_7) begin
        _times_data_reg_7 <= _times_odata_7 >>> 16;
      end 
      if(_times_ready_7 || !_times_valid_7) begin
        _times_valid_reg_7 <= _times_ovalid_7;
      end 
      if(_times_ready_8 || !_times_valid_8) begin
        _times_data_reg_8 <= _times_odata_8 >>> 16;
      end 
      if(_times_ready_8 || !_times_valid_8) begin
        _times_valid_reg_8 <= _times_ovalid_8;
      end 
      if(_times_ready_9 || !_times_valid_9) begin
        _times_data_reg_9 <= _times_odata_9 >>> 16;
      end 
      if(_times_ready_9 || !_times_valid_9) begin
        _times_valid_reg_9 <= _times_ovalid_9;
      end 
      if(_times_ready_10 || !_times_valid_10) begin
        _times_data_reg_10 <= _times_odata_10 >>> 16;
      end 
      if(_times_ready_10 || !_times_valid_10) begin
        _times_valid_reg_10 <= _times_ovalid_10;
      end 
      if(_times_ready_11 || !_times_valid_11) begin
        _times_data_reg_11 <= _times_odata_11 >>> 16;
      end 
      if(_times_ready_11 || !_times_valid_11) begin
        _times_valid_reg_11 <= _times_ovalid_11;
      end 
      if(_times_ready_12 || !_times_valid_12) begin
        _times_data_reg_12 <= _times_odata_12 >>> 16;
      end 
      if(_times_ready_12 || !_times_valid_12) begin
        _times_valid_reg_12 <= _times_ovalid_12;
      end 
      if(_times_ready_13 || !_times_valid_13) begin
        _times_data_reg_13 <= _times_odata_13 >>> 16;
      end 
      if(_times_ready_13 || !_times_valid_13) begin
        _times_valid_reg_13 <= _times_ovalid_13;
      end 
      if(_times_ready_14 || !_times_valid_14) begin
        _times_data_reg_14 <= _times_odata_14 >>> 16;
      end 
      if(_times_ready_14 || !_times_valid_14) begin
        _times_valid_reg_14 <= _times_ovalid_14;
      end 
      if((_plus_ready_15 || !_plus_valid_15) && (_times_ready_6 && _times_ready_7) && (_times_valid_6 && _times_valid_7)) begin
        _plus_data_15 <= _times_data_6 + _times_data_7;
      end 
      if(_plus_valid_15 && _plus_ready_15) begin
        _plus_valid_15 <= 0;
      end 
      if((_plus_ready_15 || !_plus_valid_15) && (_times_ready_6 && _times_ready_7)) begin
        _plus_valid_15 <= _times_valid_6 && _times_valid_7;
      end 
      if((__delay_ready_16 || !__delay_valid_16) && _times_ready_8 && _times_valid_8) begin
        __delay_data_16 <= _times_data_8;
      end 
      if(__delay_valid_16 && __delay_ready_16) begin
        __delay_valid_16 <= 0;
      end 
      if((__delay_ready_16 || !__delay_valid_16) && _times_ready_8) begin
        __delay_valid_16 <= _times_valid_8;
      end 
      if((__delay_ready_17 || !__delay_valid_17) && _times_ready_9 && _times_valid_9) begin
        __delay_data_17 <= _times_data_9;
      end 
      if(__delay_valid_17 && __delay_ready_17) begin
        __delay_valid_17 <= 0;
      end 
      if((__delay_ready_17 || !__delay_valid_17) && _times_ready_9) begin
        __delay_valid_17 <= _times_valid_9;
      end 
      if((__delay_ready_18 || !__delay_valid_18) && _times_ready_10 && _times_valid_10) begin
        __delay_data_18 <= _times_data_10;
      end 
      if(__delay_valid_18 && __delay_ready_18) begin
        __delay_valid_18 <= 0;
      end 
      if((__delay_ready_18 || !__delay_valid_18) && _times_ready_10) begin
        __delay_valid_18 <= _times_valid_10;
      end 
      if((__delay_ready_19 || !__delay_valid_19) && _times_ready_11 && _times_valid_11) begin
        __delay_data_19 <= _times_data_11;
      end 
      if(__delay_valid_19 && __delay_ready_19) begin
        __delay_valid_19 <= 0;
      end 
      if((__delay_ready_19 || !__delay_valid_19) && _times_ready_11) begin
        __delay_valid_19 <= _times_valid_11;
      end 
      if((__delay_ready_20 || !__delay_valid_20) && _times_ready_12 && _times_valid_12) begin
        __delay_data_20 <= _times_data_12;
      end 
      if(__delay_valid_20 && __delay_ready_20) begin
        __delay_valid_20 <= 0;
      end 
      if((__delay_ready_20 || !__delay_valid_20) && _times_ready_12) begin
        __delay_valid_20 <= _times_valid_12;
      end 
      if((__delay_ready_21 || !__delay_valid_21) && _times_ready_13 && _times_valid_13) begin
        __delay_data_21 <= _times_data_13;
      end 
      if(__delay_valid_21 && __delay_ready_21) begin
        __delay_valid_21 <= 0;
      end 
      if((__delay_ready_21 || !__delay_valid_21) && _times_ready_13) begin
        __delay_valid_21 <= _times_valid_13;
      end 
      if((__delay_ready_22 || !__delay_valid_22) && _times_ready_14 && _times_valid_14) begin
        __delay_data_22 <= _times_data_14;
      end 
      if(__delay_valid_22 && __delay_ready_22) begin
        __delay_valid_22 <= 0;
      end 
      if((__delay_ready_22 || !__delay_valid_22) && _times_ready_14) begin
        __delay_valid_22 <= _times_valid_14;
      end 
      if((_plus_ready_23 || !_plus_valid_23) && (_plus_ready_15 && __delay_ready_16) && (_plus_valid_15 && __delay_valid_16)) begin
        _plus_data_23 <= _plus_data_15 + __delay_data_16;
      end 
      if(_plus_valid_23 && _plus_ready_23) begin
        _plus_valid_23 <= 0;
      end 
      if((_plus_ready_23 || !_plus_valid_23) && (_plus_ready_15 && __delay_ready_16)) begin
        _plus_valid_23 <= _plus_valid_15 && __delay_valid_16;
      end 
      if((__delay_ready_24 || !__delay_valid_24) && __delay_ready_17 && __delay_valid_17) begin
        __delay_data_24 <= __delay_data_17;
      end 
      if(__delay_valid_24 && __delay_ready_24) begin
        __delay_valid_24 <= 0;
      end 
      if((__delay_ready_24 || !__delay_valid_24) && __delay_ready_17) begin
        __delay_valid_24 <= __delay_valid_17;
      end 
      if((__delay_ready_25 || !__delay_valid_25) && __delay_ready_18 && __delay_valid_18) begin
        __delay_data_25 <= __delay_data_18;
      end 
      if(__delay_valid_25 && __delay_ready_25) begin
        __delay_valid_25 <= 0;
      end 
      if((__delay_ready_25 || !__delay_valid_25) && __delay_ready_18) begin
        __delay_valid_25 <= __delay_valid_18;
      end 
      if((__delay_ready_26 || !__delay_valid_26) && __delay_ready_19 && __delay_valid_19) begin
        __delay_data_26 <= __delay_data_19;
      end 
      if(__delay_valid_26 && __delay_ready_26) begin
        __delay_valid_26 <= 0;
      end 
      if((__delay_ready_26 || !__delay_valid_26) && __delay_ready_19) begin
        __delay_valid_26 <= __delay_valid_19;
      end 
      if((__delay_ready_27 || !__delay_valid_27) && __delay_ready_20 && __delay_valid_20) begin
        __delay_data_27 <= __delay_data_20;
      end 
      if(__delay_valid_27 && __delay_ready_27) begin
        __delay_valid_27 <= 0;
      end 
      if((__delay_ready_27 || !__delay_valid_27) && __delay_ready_20) begin
        __delay_valid_27 <= __delay_valid_20;
      end 
      if((__delay_ready_28 || !__delay_valid_28) && __delay_ready_21 && __delay_valid_21) begin
        __delay_data_28 <= __delay_data_21;
      end 
      if(__delay_valid_28 && __delay_ready_28) begin
        __delay_valid_28 <= 0;
      end 
      if((__delay_ready_28 || !__delay_valid_28) && __delay_ready_21) begin
        __delay_valid_28 <= __delay_valid_21;
      end 
      if((__delay_ready_29 || !__delay_valid_29) && __delay_ready_22 && __delay_valid_22) begin
        __delay_data_29 <= __delay_data_22;
      end 
      if(__delay_valid_29 && __delay_ready_29) begin
        __delay_valid_29 <= 0;
      end 
      if((__delay_ready_29 || !__delay_valid_29) && __delay_ready_22) begin
        __delay_valid_29 <= __delay_valid_22;
      end 
      if((_plus_ready_30 || !_plus_valid_30) && (_plus_ready_23 && __delay_ready_24) && (_plus_valid_23 && __delay_valid_24)) begin
        _plus_data_30 <= _plus_data_23 + __delay_data_24;
      end 
      if(_plus_valid_30 && _plus_ready_30) begin
        _plus_valid_30 <= 0;
      end 
      if((_plus_ready_30 || !_plus_valid_30) && (_plus_ready_23 && __delay_ready_24)) begin
        _plus_valid_30 <= _plus_valid_23 && __delay_valid_24;
      end 
      if((__delay_ready_31 || !__delay_valid_31) && __delay_ready_25 && __delay_valid_25) begin
        __delay_data_31 <= __delay_data_25;
      end 
      if(__delay_valid_31 && __delay_ready_31) begin
        __delay_valid_31 <= 0;
      end 
      if((__delay_ready_31 || !__delay_valid_31) && __delay_ready_25) begin
        __delay_valid_31 <= __delay_valid_25;
      end 
      if((__delay_ready_32 || !__delay_valid_32) && __delay_ready_26 && __delay_valid_26) begin
        __delay_data_32 <= __delay_data_26;
      end 
      if(__delay_valid_32 && __delay_ready_32) begin
        __delay_valid_32 <= 0;
      end 
      if((__delay_ready_32 || !__delay_valid_32) && __delay_ready_26) begin
        __delay_valid_32 <= __delay_valid_26;
      end 
      if((__delay_ready_33 || !__delay_valid_33) && __delay_ready_27 && __delay_valid_27) begin
        __delay_data_33 <= __delay_data_27;
      end 
      if(__delay_valid_33 && __delay_ready_33) begin
        __delay_valid_33 <= 0;
      end 
      if((__delay_ready_33 || !__delay_valid_33) && __delay_ready_27) begin
        __delay_valid_33 <= __delay_valid_27;
      end 
      if((__delay_ready_34 || !__delay_valid_34) && __delay_ready_28 && __delay_valid_28) begin
        __delay_data_34 <= __delay_data_28;
      end 
      if(__delay_valid_34 && __delay_ready_34) begin
        __delay_valid_34 <= 0;
      end 
      if((__delay_ready_34 || !__delay_valid_34) && __delay_ready_28) begin
        __delay_valid_34 <= __delay_valid_28;
      end 
      if((__delay_ready_35 || !__delay_valid_35) && __delay_ready_29 && __delay_valid_29) begin
        __delay_data_35 <= __delay_data_29;
      end 
      if(__delay_valid_35 && __delay_ready_35) begin
        __delay_valid_35 <= 0;
      end 
      if((__delay_ready_35 || !__delay_valid_35) && __delay_ready_29) begin
        __delay_valid_35 <= __delay_valid_29;
      end 
      if((_plus_ready_36 || !_plus_valid_36) && (_plus_ready_30 && __delay_ready_31) && (_plus_valid_30 && __delay_valid_31)) begin
        _plus_data_36 <= _plus_data_30 + __delay_data_31;
      end 
      if(_plus_valid_36 && _plus_ready_36) begin
        _plus_valid_36 <= 0;
      end 
      if((_plus_ready_36 || !_plus_valid_36) && (_plus_ready_30 && __delay_ready_31)) begin
        _plus_valid_36 <= _plus_valid_30 && __delay_valid_31;
      end 
      if((__delay_ready_37 || !__delay_valid_37) && __delay_ready_32 && __delay_valid_32) begin
        __delay_data_37 <= __delay_data_32;
      end 
      if(__delay_valid_37 && __delay_ready_37) begin
        __delay_valid_37 <= 0;
      end 
      if((__delay_ready_37 || !__delay_valid_37) && __delay_ready_32) begin
        __delay_valid_37 <= __delay_valid_32;
      end 
      if((__delay_ready_38 || !__delay_valid_38) && __delay_ready_33 && __delay_valid_33) begin
        __delay_data_38 <= __delay_data_33;
      end 
      if(__delay_valid_38 && __delay_ready_38) begin
        __delay_valid_38 <= 0;
      end 
      if((__delay_ready_38 || !__delay_valid_38) && __delay_ready_33) begin
        __delay_valid_38 <= __delay_valid_33;
      end 
      if((__delay_ready_39 || !__delay_valid_39) && __delay_ready_34 && __delay_valid_34) begin
        __delay_data_39 <= __delay_data_34;
      end 
      if(__delay_valid_39 && __delay_ready_39) begin
        __delay_valid_39 <= 0;
      end 
      if((__delay_ready_39 || !__delay_valid_39) && __delay_ready_34) begin
        __delay_valid_39 <= __delay_valid_34;
      end 
      if((__delay_ready_40 || !__delay_valid_40) && __delay_ready_35 && __delay_valid_35) begin
        __delay_data_40 <= __delay_data_35;
      end 
      if(__delay_valid_40 && __delay_ready_40) begin
        __delay_valid_40 <= 0;
      end 
      if((__delay_ready_40 || !__delay_valid_40) && __delay_ready_35) begin
        __delay_valid_40 <= __delay_valid_35;
      end 
      if((_plus_ready_41 || !_plus_valid_41) && (_plus_ready_36 && __delay_ready_37) && (_plus_valid_36 && __delay_valid_37)) begin
        _plus_data_41 <= _plus_data_36 + __delay_data_37;
      end 
      if(_plus_valid_41 && _plus_ready_41) begin
        _plus_valid_41 <= 0;
      end 
      if((_plus_ready_41 || !_plus_valid_41) && (_plus_ready_36 && __delay_ready_37)) begin
        _plus_valid_41 <= _plus_valid_36 && __delay_valid_37;
      end 
      if((__delay_ready_42 || !__delay_valid_42) && __delay_ready_38 && __delay_valid_38) begin
        __delay_data_42 <= __delay_data_38;
      end 
      if(__delay_valid_42 && __delay_ready_42) begin
        __delay_valid_42 <= 0;
      end 
      if((__delay_ready_42 || !__delay_valid_42) && __delay_ready_38) begin
        __delay_valid_42 <= __delay_valid_38;
      end 
      if((__delay_ready_43 || !__delay_valid_43) && __delay_ready_39 && __delay_valid_39) begin
        __delay_data_43 <= __delay_data_39;
      end 
      if(__delay_valid_43 && __delay_ready_43) begin
        __delay_valid_43 <= 0;
      end 
      if((__delay_ready_43 || !__delay_valid_43) && __delay_ready_39) begin
        __delay_valid_43 <= __delay_valid_39;
      end 
      if((__delay_ready_44 || !__delay_valid_44) && __delay_ready_40 && __delay_valid_40) begin
        __delay_data_44 <= __delay_data_40;
      end 
      if(__delay_valid_44 && __delay_ready_44) begin
        __delay_valid_44 <= 0;
      end 
      if((__delay_ready_44 || !__delay_valid_44) && __delay_ready_40) begin
        __delay_valid_44 <= __delay_valid_40;
      end 
      if((_plus_ready_45 || !_plus_valid_45) && (_plus_ready_41 && __delay_ready_42) && (_plus_valid_41 && __delay_valid_42)) begin
        _plus_data_45 <= _plus_data_41 + __delay_data_42;
      end 
      if(_plus_valid_45 && _plus_ready_45) begin
        _plus_valid_45 <= 0;
      end 
      if((_plus_ready_45 || !_plus_valid_45) && (_plus_ready_41 && __delay_ready_42)) begin
        _plus_valid_45 <= _plus_valid_41 && __delay_valid_42;
      end 
      if((__delay_ready_46 || !__delay_valid_46) && __delay_ready_43 && __delay_valid_43) begin
        __delay_data_46 <= __delay_data_43;
      end 
      if(__delay_valid_46 && __delay_ready_46) begin
        __delay_valid_46 <= 0;
      end 
      if((__delay_ready_46 || !__delay_valid_46) && __delay_ready_43) begin
        __delay_valid_46 <= __delay_valid_43;
      end 
      if((__delay_ready_47 || !__delay_valid_47) && __delay_ready_44 && __delay_valid_44) begin
        __delay_data_47 <= __delay_data_44;
      end 
      if(__delay_valid_47 && __delay_ready_47) begin
        __delay_valid_47 <= 0;
      end 
      if((__delay_ready_47 || !__delay_valid_47) && __delay_ready_44) begin
        __delay_valid_47 <= __delay_valid_44;
      end 
      if((_plus_ready_48 || !_plus_valid_48) && (_plus_ready_45 && __delay_ready_46) && (_plus_valid_45 && __delay_valid_46)) begin
        _plus_data_48 <= _plus_data_45 + __delay_data_46;
      end 
      if(_plus_valid_48 && _plus_ready_48) begin
        _plus_valid_48 <= 0;
      end 
      if((_plus_ready_48 || !_plus_valid_48) && (_plus_ready_45 && __delay_ready_46)) begin
        _plus_valid_48 <= _plus_valid_45 && __delay_valid_46;
      end 
      if((__delay_ready_49 || !__delay_valid_49) && __delay_ready_47 && __delay_valid_47) begin
        __delay_data_49 <= __delay_data_47;
      end 
      if(__delay_valid_49 && __delay_ready_49) begin
        __delay_valid_49 <= 0;
      end 
      if((__delay_ready_49 || !__delay_valid_49) && __delay_ready_47) begin
        __delay_valid_49 <= __delay_valid_47;
      end 
      if((_plus_ready_50 || !_plus_valid_50) && (_plus_ready_48 && __delay_ready_49) && (_plus_valid_48 && __delay_valid_49)) begin
        _plus_data_50 <= _plus_data_48 + __delay_data_49;
      end 
      if(_plus_valid_50 && _plus_ready_50) begin
        _plus_valid_50 <= 0;
      end 
      if((_plus_ready_50 || !_plus_valid_50) && (_plus_ready_48 && __delay_ready_49)) begin
        _plus_valid_50 <= _plus_valid_48 && __delay_valid_49;
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
  input [14-1:0] b,
  output [46-1:0] c
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
  input [14-1:0] b,
  output [46-1:0] c
);

  reg signed [32-1:0] _a;
  reg signed [14-1:0] _b;
  reg signed [46-1:0] _tmpval0;
  reg signed [46-1:0] _tmpval1;
  reg signed [46-1:0] _tmpval2;
  reg signed [46-1:0] _tmpval3;
  reg signed [46-1:0] _tmpval4;
  wire signed [46-1:0] rslt;
  assign rslt = _a * _b;
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



module multiplier_1
(
  input CLK,
  input RST,
  input update,
  input enable,
  output valid,
  input [32-1:0] a,
  input [14-1:0] b,
  output [46-1:0] c
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


  multiplier_core_1
  mult
  (
    .CLK(CLK),
    .update(update),
    .a(a),
    .b(b),
    .c(c)
  );


endmodule



module multiplier_core_1
(
  input CLK,
  input update,
  input [32-1:0] a,
  input [14-1:0] b,
  output [46-1:0] c
);

  reg signed [32-1:0] _a;
  reg signed [14-1:0] _b;
  reg signed [46-1:0] _tmpval0;
  reg signed [46-1:0] _tmpval1;
  reg signed [46-1:0] _tmpval2;
  reg signed [46-1:0] _tmpval3;
  reg signed [46-1:0] _tmpval4;
  wire signed [46-1:0] rslt;
  assign rslt = _a * _b;
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



module multiplier_2
(
  input CLK,
  input RST,
  input update,
  input enable,
  output valid,
  input [32-1:0] a,
  input [14-1:0] b,
  output [46-1:0] c
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


  multiplier_core_2
  mult
  (
    .CLK(CLK),
    .update(update),
    .a(a),
    .b(b),
    .c(c)
  );


endmodule



module multiplier_core_2
(
  input CLK,
  input update,
  input [32-1:0] a,
  input [14-1:0] b,
  output [46-1:0] c
);

  reg signed [32-1:0] _a;
  reg signed [14-1:0] _b;
  reg signed [46-1:0] _tmpval0;
  reg signed [46-1:0] _tmpval1;
  reg signed [46-1:0] _tmpval2;
  reg signed [46-1:0] _tmpval3;
  reg signed [46-1:0] _tmpval4;
  wire signed [46-1:0] rslt;
  assign rslt = _a * _b;
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



module multiplier_3
(
  input CLK,
  input RST,
  input update,
  input enable,
  output valid,
  input [32-1:0] a,
  input [14-1:0] b,
  output [46-1:0] c
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


  multiplier_core_3
  mult
  (
    .CLK(CLK),
    .update(update),
    .a(a),
    .b(b),
    .c(c)
  );


endmodule



module multiplier_core_3
(
  input CLK,
  input update,
  input [32-1:0] a,
  input [14-1:0] b,
  output [46-1:0] c
);

  reg signed [32-1:0] _a;
  reg signed [14-1:0] _b;
  reg signed [46-1:0] _tmpval0;
  reg signed [46-1:0] _tmpval1;
  reg signed [46-1:0] _tmpval2;
  reg signed [46-1:0] _tmpval3;
  reg signed [46-1:0] _tmpval4;
  wire signed [46-1:0] rslt;
  assign rslt = _a * _b;
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



module multiplier_4
(
  input CLK,
  input RST,
  input update,
  input enable,
  output valid,
  input [32-1:0] a,
  input [14-1:0] b,
  output [46-1:0] c
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


  multiplier_core_4
  mult
  (
    .CLK(CLK),
    .update(update),
    .a(a),
    .b(b),
    .c(c)
  );


endmodule



module multiplier_core_4
(
  input CLK,
  input update,
  input [32-1:0] a,
  input [14-1:0] b,
  output [46-1:0] c
);

  reg signed [32-1:0] _a;
  reg signed [14-1:0] _b;
  reg signed [46-1:0] _tmpval0;
  reg signed [46-1:0] _tmpval1;
  reg signed [46-1:0] _tmpval2;
  reg signed [46-1:0] _tmpval3;
  reg signed [46-1:0] _tmpval4;
  wire signed [46-1:0] rslt;
  assign rslt = _a * _b;
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



module multiplier_5
(
  input CLK,
  input RST,
  input update,
  input enable,
  output valid,
  input [32-1:0] a,
  input [14-1:0] b,
  output [46-1:0] c
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


  multiplier_core_5
  mult
  (
    .CLK(CLK),
    .update(update),
    .a(a),
    .b(b),
    .c(c)
  );


endmodule



module multiplier_core_5
(
  input CLK,
  input update,
  input [32-1:0] a,
  input [14-1:0] b,
  output [46-1:0] c
);

  reg signed [32-1:0] _a;
  reg signed [14-1:0] _b;
  reg signed [46-1:0] _tmpval0;
  reg signed [46-1:0] _tmpval1;
  reg signed [46-1:0] _tmpval2;
  reg signed [46-1:0] _tmpval3;
  reg signed [46-1:0] _tmpval4;
  wire signed [46-1:0] rslt;
  assign rslt = _a * _b;
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



module multiplier_6
(
  input CLK,
  input RST,
  input update,
  input enable,
  output valid,
  input [32-1:0] a,
  input [14-1:0] b,
  output [46-1:0] c
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


  multiplier_core_6
  mult
  (
    .CLK(CLK),
    .update(update),
    .a(a),
    .b(b),
    .c(c)
  );


endmodule



module multiplier_core_6
(
  input CLK,
  input update,
  input [32-1:0] a,
  input [14-1:0] b,
  output [46-1:0] c
);

  reg signed [32-1:0] _a;
  reg signed [14-1:0] _b;
  reg signed [46-1:0] _tmpval0;
  reg signed [46-1:0] _tmpval1;
  reg signed [46-1:0] _tmpval2;
  reg signed [46-1:0] _tmpval3;
  reg signed [46-1:0] _tmpval4;
  wire signed [46-1:0] rslt;
  assign rslt = _a * _b;
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



module multiplier_7
(
  input CLK,
  input RST,
  input update,
  input enable,
  output valid,
  input [32-1:0] a,
  input [14-1:0] b,
  output [46-1:0] c
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


  multiplier_core_7
  mult
  (
    .CLK(CLK),
    .update(update),
    .a(a),
    .b(b),
    .c(c)
  );


endmodule



module multiplier_core_7
(
  input CLK,
  input update,
  input [32-1:0] a,
  input [14-1:0] b,
  output [46-1:0] c
);

  reg signed [32-1:0] _a;
  reg signed [14-1:0] _b;
  reg signed [46-1:0] _tmpval0;
  reg signed [46-1:0] _tmpval1;
  reg signed [46-1:0] _tmpval2;
  reg signed [46-1:0] _tmpval3;
  reg signed [46-1:0] _tmpval4;
  wire signed [46-1:0] rslt;
  assign rslt = _a * _b;
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



module multiplier_8
(
  input CLK,
  input RST,
  input update,
  input enable,
  output valid,
  input [32-1:0] a,
  input [14-1:0] b,
  output [46-1:0] c
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


  multiplier_core_8
  mult
  (
    .CLK(CLK),
    .update(update),
    .a(a),
    .b(b),
    .c(c)
  );


endmodule



module multiplier_core_8
(
  input CLK,
  input update,
  input [32-1:0] a,
  input [14-1:0] b,
  output [46-1:0] c
);

  reg signed [32-1:0] _a;
  reg signed [14-1:0] _b;
  reg signed [46-1:0] _tmpval0;
  reg signed [46-1:0] _tmpval1;
  reg signed [46-1:0] _tmpval2;
  reg signed [46-1:0] _tmpval3;
  reg signed [46-1:0] _tmpval4;
  wire signed [46-1:0] rslt;
  assign rslt = _a * _b;
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
    test_module = dataflow_stencil.mkTest()
    code = test_module.to_verilog()

    from pyverilog.vparser.parser import VerilogParser
    from pyverilog.ast_code_generator.codegen import ASTCodeGenerator
    parser = VerilogParser()
    expected_ast = parser.parse(expected_verilog)
    codegen = ASTCodeGenerator()
    expected_code = codegen.visit(expected_ast)

    assert(expected_code == code)
