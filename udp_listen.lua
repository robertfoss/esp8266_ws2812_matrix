function listen(s, data)
  ws2812.write(1, 3, data)
end


sock=net.createServer(net.UDP) 
sock:on("receive", listen)
sock:listen(10000)
