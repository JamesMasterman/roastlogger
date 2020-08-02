#!/usr/bin/env python
from ReaderPacketHandler import parseReaderPacket
from ReaderPacketHandler import serialiseRequestPacket
from ReaderPackets import TempRequest
from ReaderPackets import TempResponse
from ReaderPackets import PacketType
import time
import socket

SERVER_IP = "127.0.0.1"
SERVER_PORT = 9753
BUFFER_SIZE = 256

def main(): 
    try:               
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)         
        packetID = 1       
        try: 
            requestPacket = TempRequest(packetID)
            sock.sendto(serialiseRequestPacket(requestPacket), (SERVER_IP, SERVER_PORT))             
            data, addr = sock.recvfrom(BUFFER_SIZE)                
            response = parseReaderPacket(data)
            if response.Type == PacketType.RESPONSE_PACKET:    
                print("{},{}".format(response.beanTemp, response.exhaustTemp))
                
        except Exception as error:
            print(error)            
            
    except Exception as error:
        print(error)        
        
    finally:
        sock.close()          

if __name__ == '__main__':
    main()
