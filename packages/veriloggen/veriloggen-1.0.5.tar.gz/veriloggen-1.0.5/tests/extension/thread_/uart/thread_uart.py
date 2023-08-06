from __future__ import absolute_import
from __future__ import print_function
import sys
import os
import math

# the next line can be removed after installation
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))))

from veriloggen import *
import veriloggen.thread as vthread


def mkLed(baudrate=19200, clockfreq=100 * 1000 * 1000):
    m = Module('blinkled')
    clk = m.Input('CLK')
    rst = m.Input('RST')
    sw = m.Input('sw', 16)
    led = m.OutputReg('led', 16, initval=0)
    tx = m.Output('utx')
    rx = m.Input('urx')

    uart_tx = vthread.UartTx(m, 'inst_tx', 'tx_', clk, rst, tx,
                             baudrate=baudrate, clockfreq=clockfreq)
    uart_rx = vthread.UartRx(m, 'inst_rx', 'rx_', clk, rst, rx,
                             baudrate=baudrate, clockfreq=clockfreq)

    def blink():
        while True:
            c = uart_rx.recv()
            data = c + sw
            led.value = data
            uart_tx.send(data)

    th = vthread.Thread(m, 'th_blink', clk, rst, blink)
    fsm = th.start()

    return m


def mkTest(baudrate=19200, clockfreq=19200 * 10):
    m = Module('test')

    # target instance
    led = mkLed(baudrate, clockfreq)

    uut = Submodule(m, led, name='uut', prefix='', as_wire=('utx', 'urx'))
    clk = uut['CLK']
    rst = uut['RST']
    tx = uut['utx']
    rx = uut['urx']
    sw = uut['sw']

    uart_tx = vthread.UartTx(m, 'inst_tx', 'tx_', clk, rst, as_wire='txd',
                             baudrate=baudrate, clockfreq=clockfreq)
    uart_rx = vthread.UartRx(m, 'inst_rx', 'rx_', clk, rst, as_wire='rxd',
                             baudrate=baudrate, clockfreq=clockfreq)

    txd = uart_tx['txd']
    rxd = uart_rx['rxd']
    rx.assign(txd)
    rxd.assign(tx)

    simulation.setup_waveform(m, uut, uart_tx, uart_rx)
    simulation.setup_clock(m, clk, hperiod=5)
    init = simulation.setup_reset(m, rst, m.make_reset(), period=100)

    init.add(
        sw(10),
        Delay(100000),
        Systask('finish')
    )

    def test():
        for i in range(10):
            s = 100 + i
            uart_tx.send(s)
            r = uart_rx.recv()
            if vthread.verilog.Eql(r, s + sw):
                print('OK: %d + %d === %d' % (s, sw, r))
            else:
                print('NG: %d + %d !== %d' % (s, sw, r))

    th = vthread.Thread(m, 'test', clk, rst, test)
    th.start()

    return m

if __name__ == '__main__':
    test = mkTest()
    verilog = test.to_verilog('tmp.v')
    print(verilog)

    sim = simulation.Simulator(test)
    rslt = sim.run()
    print(rslt)
