#!/usr/bin/env python


class PacketType:
    REQUEST_PACKET = 1
    RESPONSE_PACKET = 2

class TempRequest:
    ID = 0
    Type = PacketType.REQUEST_PACKET
    def __init__(self, ID):    
        self.ID = ID  
        
class TempResponse: 
    ID = 0 
    Type = PacketType.RESPONSE_PACKET
    beanTemp = 0
    exhaustTemp = 0
    environmentTemp = 0
    humidity = 0
    pressure = 0
    otherTemp = 0
    otherTemp2 = 0
    
    def __init__(self, ID):    
        self.ID = ID    
        self.beanTemp = 0
        self.exhaustTemp = 0
        self.environment = 0
        self.humidity = 0
        self.pressure = 0
        otherTemp = 0
        otherTemp2 = 0
        Type = PacketType.RESPONSE_PACKET
        
        
    
    
    
    
