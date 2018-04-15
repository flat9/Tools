import socket
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect(('192.168.134.129',7777))
buf = ''
i = 0
try:
   for i in range(1,500):
      buf += chr(100+i%10)
      print buf
      s.send(buf)
      s.recv(1000)
except:
   s.close()
   print 'complete'
