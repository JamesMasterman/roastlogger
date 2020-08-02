#!/usr/bin/env python
from ThermocoupleReader import ThermocoupleReader
from ReaderPacketHandler import parseReaderPacket
from ReaderPacketHandler import serialiseResponsePacket
from ReaderPackets import TempResponse
from ReaderPackets import TempRequest
from ReaderPackets import PacketType

import time
import socket

UDP_IP = "127.0.0.1"
UDP_PORT = 9753
BUFFER_SIZE = 256

def main():
    beanTemp = ThermocoupleReader(0x66)
    flueTemp = ThermocoupleReader(0x67)
    try:        
        print("starting server....")
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)        
        print("opening socket...")
        sock.bind((UDP_IP, UDP_PORT))
        
        beanTemp.start()
        
        while True:     
            try: 
                data, addr = sock.recvfrom(BUFFER_SIZE)
                readerPacket = parseReaderPacket(data)
                if readerPacket.Type == PacketType.REQUEST_PACKET:                   
                    response = TempResponse(readerPacket.ID)
                    response.beanTemp = beanTemp.getTemp()
                    response.exhaustTemp = flueTemp.getTemp()
                    #print("Bean temp {}, Flue temp {}".format(response.beanTemp, response.exhaustTemp))
                    data = serialiseResponsePacket(response)
                    dest = (addr[0], addr[1])
                    sock.sendto(data, dest)   
            except Exception as error:
                print(error)
                sock.bind((UDP_IP, UDP_PORT))
            
            
    except Exception as error:
        print(error)        
        
    finally:
        sock.close()
        beanTemp.stop()
        beanTemp.join()
        print("done")
        

if __name__ == '__main__':
    main()
        
        
