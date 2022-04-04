import socket
import re
import numpy as np
import time
 

localIP     = "10.42.0.1"

localPort   = 8080

bufferSize  = 1024

 

# msgFromServer       = "Hello UDP Client"

# bytesToSend         = str.encode(msgFromServer)

 

# Create a datagram socket

# UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)


 

# Bind to address and ip

UDPServerSocket.bind((localIP, localPort))

 

print("UDP server up and listening")

 

# Listen for incoming datagrams

while(True):
    tic = time.time()
    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)

    message = bytesAddressPair[0]

    # print(str(message))
    # vals = [float(f) for f in str.split(str(message[2:]))]
    address = bytesAddressPair[1]
    # clientIP  = "Client IP Address:{}".format(address)
    
    # print(vals)
    # print(clientIP)
    
    
    vals = message.decode()
    vals = vals.split(" ")
    
    vals = [float(x) for x in vals]
    tock = time.time()
    print((tock-tic)*1000)

   

    # Sending a reply to client

    # UDPServerSocket.sendto(bytesToSend, address)

