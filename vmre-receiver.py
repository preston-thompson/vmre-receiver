#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from datetime import datetime
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser
import osmosdr
import time
import json
import os

class top_block(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "Top Block")

        config = json.load(open("vmre-config.json", "r"))
        config["datetime_started"] = datetime.now().strftime("%Y-%m-%d_%H-%M-%S.%f")

        ##################################################
        # Variables
        ##################################################
        self.pass_band = pass_band = config["bandwidth"]
        self.center_freq = center_freq = config["center_frequency"]
        self.output_path = output_path = ".//data//"
        self.transition_width = transition_width = config["transition_width"]
        self.samp_rate = samp_rate = config["sample_rate"]
        self.iq_filename = iq_filename = output_path + config["datetime_started"] + ".dat"
        self.freq_offset = freq_offset = config["frequency_offset"]

        json.dump(config, open(output_path + config["datetime_started"] + ".json", "w"))

        ##################################################
        # Blocks
        ##################################################
        self.osmosdr_source_0 = osmosdr.source( args="numchan=" + str(1) + " " + str(config["sdr"]) )
        self.osmosdr_source_0.set_sample_rate(samp_rate)
        self.osmosdr_source_0.set_center_freq(center_freq-freq_offset, 0)
        self.osmosdr_source_0.set_freq_corr(0, 0)
        self.osmosdr_source_0.set_dc_offset_mode(0, 0)
        self.osmosdr_source_0.set_iq_balance_mode(0, 0)
        self.osmosdr_source_0.set_gain_mode(False, 0)
        self.osmosdr_source_0.set_gain(15, 0)
        self.osmosdr_source_0.set_if_gain(15, 0)
        self.osmosdr_source_0.set_bb_gain(15, 0)
        self.osmosdr_source_0.set_antenna('', 0)
        self.osmosdr_source_0.set_bandwidth(0, 0)

        self.blocks_file_sink_1 = blocks.file_sink(gr.sizeof_gr_complex*1, iq_filename, False)
        self.blocks_file_sink_1.set_unbuffered(False)
        self.band_pass_filter_0 = filter.fir_filter_ccc(int(samp_rate/pass_band), firdes.complex_band_pass(
        	1, samp_rate, -pass_band/2+transition_width, pass_band/2-transition_width, transition_width, firdes.WIN_HAMMING, 6.76))

        ##################################################
        # Connections
        ##################################################
        self.connect((self.band_pass_filter_0, 0), (self.blocks_file_sink_1, 0))
        self.connect((self.osmosdr_source_0, 0), (self.band_pass_filter_0, 0))

def main(top_block_cls=top_block, options=None):

    if not os.path.exists("data"):
        os.makedirs("data")

    while True:
        tb = top_block_cls()
        start_time = time.time()
        tb.start()
        while time.time() - start_time < 24*60*60:
            time.sleep(60)
        print("Time is %s. Starting a new file..." % (datetime.now()))
        tb.stop()
        tb.wait()
        del tb

if __name__ == '__main__':
    main()
