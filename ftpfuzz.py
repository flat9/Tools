import socket
import sys
def first_send():
   buf = ''
   try:
     for i in range(0,220):
       buf += chr(97+i%10)
       s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
       s.connect(('192.168.134.129',7777))	
       buf_len = s.send(buf)
       print 'Send_Buff:' + str(buf_len)
       print buf
       s.close()
       #s.recv(1000)
   except:
     print "[+]FirstBuff Send Successful"
     First_Address = raw_input("[+]Please Enter The Error Address:")
     print "[+]Please Restart The Fuzz\'s Program"
     flag = raw_input("[+]Restart Successful[Y/N]")
     if flag.lower() == 'y':
       return 1
     else:
       return 0
     
def second_send():
   buf = ''
   try:
     for i in range(0,220):
       s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
       s.connect(('192.168.134.129',7777))
       buf += chr(97+i/10)
       buf_len = s.send(buf)
       print 'Send_Buff:' + str(buf_len)
       print buf
       s.close()
       #s.recv(1000)
   except:    
     print "[+]SecondBuff Send Successful"
     Second_Address = raw_input("[+]Please Enter The Error Address:")
     return Second_Address

if __name__ == '__main__':
   print 'Fuzz Start'
   flag = first_send() 
   if flag == 1:
     second_send()
