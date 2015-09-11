# led_matrix
This is a project in 3 parts. Software, hardware and electronics. Together it forms a wireless led matrix.
Since it's based around the ESP8266 it supports connecting to a wifi and having animations streamed to it.

## nodemcu_wifi_streamer
This was the first proof of concept for the software. The software comes in two parts **effect.py** which is run on a computer somewhere and generates the actual animations that will be displayed on the led matrix.
The second part is a simple udp-server that runs on the led matrix and receives the animation and outputs it to the WS2812B LEDs.
