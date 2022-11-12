# -*- coding: utf-8 -*-

"""
config_webrx: configuration options for OpenWebRX

    This file is part of OpenWebRX,
    an open-source SDR receiver software with a web UI.
    Copyright (c) 2013-2015 by Andras Retzler <randras@sdr.hu>
    Copyright (c) 2019-2020 by Jakob Ketterl <dd5jfk@darc.de>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as
    published by the Free Software Foundation, either version 3 of the
    License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

    ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    In addition, as a special exception, the copyright holders
    state that config_rtl.py and config_webrx.py are not part of the
    Corresponding Source defined in GNU AGPL version 3 section 1.

    (It means that you do not have to redistribute config_rtl.py and
    config_webrx.py if you make any changes to these two configuration files,
    and use them for running your web service with OpenWebRX.)
"""

# configuration version. please only modify if you're able to perform the associated migration steps.
version = 2

# NOTE: you can find additional information about configuring OpenWebRX in the Wiki:
# https://github.com/jketterl/openwebrx/wiki/Configuration-guide

# ==== Server settings ====
web_port = 8073
max_clients = 20

# ==== Web GUI configuration ====
receiver_name = "N3FTU"
receiver_location = "Bethany Beach, Delaware USA"
receiver_asl = 0
receiver_admin = "rpsmithii@@mac.com"
receiver_gps = {"lat": 38.6100, "lon": -75.0700}
photo_title = ""
photo_desc = """
Receiver operated by: <a href="mailto:rpsmithii@@mac.com" target="_blank">Bob Smith</a><br/>
Device: SDRPlay RSPdx<br />
Antenna: MLA-30 Loop<br />
Website: <a href="http://localhost" target="_blank">http://localhost</a>
"""

# ==== DSP/RX settings ====
fft_fps = 9
fft_size = 4096  # Should be power of 2
fft_voverlap_factor = (
    0.3  # If fft_voverlap_factor is above 0, multiple FFTs will be used for creating a line on the diagram.
)
audio_compression = "adpcm"  		# valid values: "adpcm", "none"
fft_compression = "adpcm"  		# valid values: "adpcm", "none"
digimodes_enable = True  			# Decoding digimodes come with higher CPU usage.
digimodes_fft_size = 1024
digital_voice_unvoiced_quality = 1
digital_voice_dmr_id_lookup = False	# enables lookup of DMR ids using the radioid api

# ==== I/Q sources ====
sdrs = {
    "sdrplay": {
        "name": "SDRPlay RSPdx",
        "type": "sdrplay",
        "ppm": 0,
		"antenna": "Antenna B",
		"bias_tee": True,
        "profiles": {
            "20m": {
                "name": "20m",
                "center_freq": 14150000,
                "rf_gain": 0,
                "samp_rate": 500000,
                "start_freq": 14070000,
                "start_mod": "usb",
            },
            "30m": {
                "name": "30m",
                "center_freq": 10125000,
                "rf_gain": 0,
                "samp_rate": 250000,
                "start_freq": 10142000,
                "start_mod": "usb",
            },
            "40m": {
                "name": "40m",
                "center_freq": 7100000,
                "rf_gain": 0,
                "samp_rate": 500000,
                "start_freq": 7070000,
                "start_mod": "lsb",
            },
            "80m": {
                "name": "80m",
                "center_freq": 3650000,
                "rf_gain": 0,
                "samp_rate": 500000,
                "start_freq": 3570000,
                "start_mod": "lsb",
            },
            "49m": {
                "name": "49m Broadcast",
                "center_freq": 6000000,
                "rf_gain": 0,
                "samp_rate": 500000,
                "start_freq": 6070000,
                "start_mod": "am",
            },
        },
    },
}

# ==== Color themes ====
### default theme by teejez:
waterfall_colors = [0x000000FF, 0x0000FFFF, 0x00FFFFFF, 0x00FF00FF, 0xFFFF00FF, 0xFF0000FF, 0xFF00FFFF, 0xFFFFFFFF]
waterfall_min_level = -88  # in dB
waterfall_max_level = -20
waterfall_auto_level_margin = {"min": 5, "max": 40}

# === Experimental settings ===
csdr_dynamic_bufsize = False  					# change the buffering mode of csdr
csdr_print_bufsizes = False  					# prints buffer sizes used for csdr processes
csdr_through = False  							# True prints how much data is going into the DSP chains
nmux_memory = 50  								# in (mb) sets the approx size of the circular buffer used by nmux
google_maps_api_key = ""
map_position_retention_time = 2 * 60 * 60		# in seconds

decoding_queue_workers = 2
decoding_queue_length = 10
wsjt_decoding_depth = 6
wsjt_decoding_depths = {"jt65": 1}
js8_enabled_profiles = ["normal", "slow"]
js8_decoding_depth = 3
temporary_directory = "/tmp"
services_enabled = True
services_decoders = ["ft8", "ft4", "wspr", "packet"]

# === aprs igate settings ===
aprs_callsign = "N3FTU"
aprs_igate_enabled = False
aprs_igate_server = "euro.aprs2.net"
aprs_igate_password = ""
aprs_igate_beacon = False
aprs_symbols_path = "/opt/aprs-symbols/png"

# === PSK Reporter setting ===
pskreporter_enabled = False
pskreporter_callsign = "N3FTU"
