wifi.setmode(wifi.STATION)
wifi.sta.config("wifiname", "wifipassword")

-- Listens on UDP port 8888 and pushes pixels to a LED screen.
s=net.createServer(net.UDP) 
packets={}
s:on("receive",function(s,c)
  ws2812.writefast(3, c, 1) end
end)
s:listen(8888)

