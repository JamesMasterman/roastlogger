#!/usr/bin/env python
import mcp9600
import time
import threading
import statistics
from collections import deque


threadlock = threading.Lock()

class ThermocoupleReader (threading.Thread):
    WindowSize = 20  #5 valid readings are taken for each read() call and the median found   
    SampleRate = 0.5 #0.5 seconds per reading
    
    def __init__(self, address):
        self.mAddress = address
        self.mTempDevice  = mcp9600.MCP9600(i2c_dev=address)
        self.mCurrentTemp = -1
        self.mWindowMinTemp = 0      
        self.mRunning = True
        self.mReadings = deque()      
        self.mReadingMean = 0
        self.mReadingStdDev = 0
        
    def stop(self):
        self.mRunning = False
        return        
        
    def read(self):
        try:         
            threadlock.acquire()   
            self.mCurrentTemp = self.getCleanReading()
            threadlock.release()            
        except Exception as error:
            #print(error)
            pass       
            
    def getTemp(self):
        currentTemp = 0
        threadlock.acquire()
        currentTemp = self.mCurrentTemp
        threadlock.release()
        return currentTemp
                     
        
    def getCleanReading(self):
        cleanReading = self.mCurrentTemp
        try:
            reading = self.mTempDevice.get_hot_junction_temperature()
            delta = self.mTempDevice.get_temperature_delta()


            if(delta > 0 and reading > 0):
             self.storeReading(reading)         
             if self.mReadingMean > 0 and not self.isOutlier(reading):
                 cleanReading = reading
                 
         except Exception as error:
            #print(error)
            pass   
                             
         return cleanReading   
             
    def storeReading(self, reading):                        
          self.mReadings.append(reading)
          if len(self.mReadings) > WindowSize:
              self.mReadings.popleft()
              self.mReadingMean = mean(self.mReadings)
              self.mReadingStdDev = stdev(self.mReadings, self.mReadingMean)
             
    def isOutlier(self, reading):
        return reading <0.1 or reading > (mReadingMean + mReadingStdDev) 
               or reading < (m_ReadingMean - mReadingStDev)
            
    def run(self):
        while self.mRunning:
            self.read()
            time.sleep(SampleRate)
        
