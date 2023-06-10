# gr_MSF60_Receiver
This is a basic MSF60 receiver for GNU Radio, containing:
1. signal demodulation and detection of the MSF60 OOK signal with an SDR using GNU Radio (and Python modules)
2. a simple live decoder of the received OOK bits provided by the GNU Radio MSF60 receiver

__MSF60__ (from the National Physics Laboratory (NPL) is one of the __UK time signals__ in Anthorn, Cumbria, UK.)

### Overview
The __flowgraphs__ are provided in the `examples` folder:
+ `MSF60_receiver.grc`
    + for SDR reception

Supplementary tools are provided in the `python` folder:
+ `DecodeMSF60.py` decodes the received OOK bits from a specified ZMQ server upon receiving them. It shows the current time, date, weekday, etc. at each new minute.

### Requirements
The MSF60 receiver was tested with:
+ gnuradio & GNU Radio Companion 3.10.1.1 (Linux)
+ Radioconda 2023.02.24 & gnuradio & GNU Radio Companion 3.10.5.1 (Windows)
+ Python 3.10.6
    + PyQt5 5.15.7
    + pyzmq 23.1.0
    + gnuradio-osmosdr 0.2.0
+ An SDR receiver capable of receiving in the range of at least 1 kHz - 1 MHz, e.g. an _Airspy Discovery HF+_ is configured and used for this project.
+ An antenna that provides a sufficiently clear MSF60 signal, e.g. a simple _YouLoop_ loop antenna was used for this project. Indoor reception should probably be possible if you are close enough (<1000 km) to the MSF60 transmitter in Anthorn, UK. You should mount the antenna close to a window or outside.
+ The user might also need some antenna cables and adapters to connect the SDR with the antenna.
+ This project has been successfully tested in:
    + Ubuntu 22.04.2 LTS (recommended)
    + Windows 11

### Instructions/Setup

#### Signal Reception with SDR

##### MSF60 On-Off-Keying (OOK) with SDR
+ Set up your SDR with your computer.
+ Ensure that the raw MSF60 signal reception at 60 kHz is good enough, e.g. using gqrx or another signal analysis tool.
+ To start the MSF60 receiver, open the flowchart in `/examples/MSF60_Receiver/MSF60_receiver.grc` with GNU Radio Companion
    + Press `run` button.
    + Set the _Recv Gain_ slider values in the MSF60 GUI so that the amplitude of __BB signal__ is centered roughly around the value 9000.
    + Adjust the _Threshold_ slider values, if needed.
    + The slider _LP width_ and _LP cut-off_ can be used to change the dense low-pass filter, but these values should rather be kept as they are.
    + After parameter adjustment, the GNU Radio Companion debug console should show a debug message each second with either '00', '01','11,'10, or '2' (for new minute).

+ Next, open a terminal or Powershell.
    + Change to your cloned repository.
    + Run _DecodeMSF60_ with ```python3 ./python/decoder/DecodeMSF60.py```.
    + The terminal should show the received bits together with a sequence of indices.
    + after approximately 2 minutes, _DecodeMSF60_ should be synchronized with the transmitter. It should provide the current time, date, etc. each minute.
    + NOTE: sometimes a bit can not be decoded correctly, e.g. due to bad reception. Then the current frame of the minute is corrupted and both the decoder and detector will produce error messages and will attempt to re-synchronize.

### REMARKS
+ This project has __not__ been tested with other SDR receivers, yet.
+ This project has __not__ been tested with a receiver setup using a sound card.
+ This project has __not__ been tested with other antennas (e.g. a ferrite antenna).
+ A Low Noise Amplifier (LNA) is not needed.
+ Even a single lost bit during reception causes the synchronization of a full minute to fail. Additional resilience of the decoder has __not__ been implemented yet.
+ Bits 01-16 carrying the difference (DUT1) between atomic and astronomical time are currently ignored by the decoder.
+ The project provides the decoded MSF60 signal more or less in real-time, but it is probably __not__ accurate in terms of milliseconds.
+ NOTE: A simulation of the MSF60 transmitter and the channel (for offline tests) might be added soon.