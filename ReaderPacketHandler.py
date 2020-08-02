#!/usr/bin/python

from ReaderPackets import TempRequest
from ReaderPackets import TempResponse
from ReaderPackets import PacketType
import array
import jsonpickle

PARSE_STATE_INIT = 0
PARSE_STATE_GOT_INIT = 1
PARSE_STATE_GOT_ID = 2
PARSE_STATE_GOT_TYPE = 3
PARSE_STATE_GOT_LENGTH = 4
PARSE_STATE_GOT_STRING = 5
PARSE_STATE_DONE = 6

START_PACKET = 254

def parseReaderPacket(rawPacket):
	packet = None
	state = PARSE_STATE_INIT
	ubyteData = array.array("B",rawPacket)
	ubyteLen = len(ubyteData)

	pos = 0
	dataLength = 0
	dataPos = 0
	packetID = 0
	packetType = PacketType.REQUEST_PACKET
	data = bytearray(200)
	
	while state != PARSE_STATE_DONE:
		if(state == PARSE_STATE_INIT):
			if(ubyteData[pos] != START_PACKET):
				return packet
					
			state = PARSE_STATE_GOT_INIT
			pos +=1
		elif(state == PARSE_STATE_GOT_INIT):
			packetID = ubyteData[pos]
			pos +=1		
			state = PARSE_STATE_GOT_ID
		elif(state == PARSE_STATE_GOT_ID):
			packetType = ubyteData[pos]			
			if(packetType == PacketType.REQUEST_PACKET):				
				packet = TempRequest(packetID)
				state = PARSE_STATE_DONE
			else:
				pos +=1
				state = PARSE_STATE_GOT_TYPE
		elif(state == PARSE_STATE_GOT_TYPE):			
			dataLength = ubyteData[pos]
			if dataLength == 0:
				state = PARSE_STATE_DONE				
			else:
				pos +=1
				state = PARSE_STATE_GOT_LENGTH
				data = bytearray(dataLength)
		elif(state == PARSE_STATE_GOT_LENGTH):
			data[dataPos] = ubyteData[pos];
			dataPos+=1
			pos+=1
			if(dataPos >= dataLength):
				state = PARSE_STATE_DONE
				data.strip()
				packet = jsonpickle.decode(data.decode("ascii"))
			
	return packet
	
def createRequest(ID):
	request = TempRequest(ID)
	return request
	
def serialiseRequestPacket(reqPacket):	
	data = bytearray(4)
	data[0] = START_PACKET
	data[1] = reqPacket.ID
	data[2] = reqPacket.Type
	data[3] = 0	
	return data
	
	
def createResponse(ID):
	response = TempResponse(ID)
	return response
	
	
def serialiseResponsePacket(respPacket):
	jsonEncoded = jsonpickle.encode(respPacket)	
	data = jsonEncoded.encode()
	packetLen = len(data)
	header = bytearray(4)
	header[0] = START_PACKET
	header[1] = respPacket.ID
	header[2] = respPacket.Type
	header[3] = packetLen
	fullData = header + data
	return fullData
	
	

		

