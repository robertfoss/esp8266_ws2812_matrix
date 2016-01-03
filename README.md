# ESP8266 WS2812 Matrix
![Alt text](/../images/IMAG0896.jpg?raw=true "Case")
![Alt text](/../images/IMAG1414.jpg?raw=true "Parts")
![Alt text](/../images/IMAG1416.jpg?raw=true "Assembled")
![Alt text](/../images/IMAG1429.jpg?raw=true "Running")

This is a project in 3 parts. Software, hardware and electronics. Together it forms a wireless led matrix.
Since it's based around the ESP8266 it supports connecting to a wifi and having animations streamed to it.

## Software
This was the first proof of concept for the software. The software comes in two parts **effect.py** which is run on a computer somewhere and generates the actual animations that will be displayed on the led matrix.

The second part, the ** *.lua** files, are a simple udp-server that runs on the led matrix and receives the animation and outputs it to the WS2812B LEDs.

This code requires the ESP8266 to be flashed with [NodeMCU](https://github.com/nodemcu/nodemcu-firmware), which then needs to have the ** *.lua** files put onto its filesystem. But the .bin image supplied with this repo will work and do everything you need.
