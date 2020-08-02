#!/usr/bin/env python
import mcp9600
import time
import threading
import statistics
from collections import deque


current_milli_time = lambda: time.time_ns() // 1000000 
threadlock = threading.Lock()

class ThermocoupleReader (threading.Thread):
    WindowSize = 5   
    SampleRate = 0.5 #0.5 seconds per __reading
    MaxRateChange = 5 #5 degrees per second
    
    def __init__(self, address):
        threading.Thread.__init__(self)
        self.mAddress = address
        self.mTempDevice  = mcp9600.MCP9600(i2c_addr=address, i2c_dev=None)
        self.mCurrentTemp = -1           
        self.mRunning = True      
        self.mLastReading=0      
        self.mRecentReadings = deque()
        self.mLastDelta = 0
        self.mBaseline = 0
        
    def stop(self):
        self.mRunning = False
        return        
        
    def __read(self):
        try:         
            threadlock.acquire()   
            self.mCurrentTemp = self.__getCleanReading()            
            threadlock.release()            
        except Exception as error:
            print(error)
            pass       
            
    def getTemp(self):
        currentTemp = 0
        threadlock.acquire()
        currentTemp = self.mCurrentTemp
        
        threadlock.release()
        return currentTemp                     
        
    def __getCleanReading(self):
        cleanReading = self.mCurrentTemp
        try:
            reading = self.mTempDevice.get_hot_junction_temperature()  
            if reading > 0:
                self.__captureReading(reading)                           
                if self.__inGradientRange(reading):
                    cleanReading = reading
                    self.mLastReading = current_milli_time()
        except Exception as error:
            print(error)
            pass   
                             
        return cleanReading   
        
    def __captureReading(self, reading):
        self.mRecentReadings.append(reading)
        if(len(self.mRecentReadings) > self.WindowSize):        
            self.mRecentReadings.popleft()   
            minValue = min(self.mRecentReadings)
            self.mBaseline = minValue            
                          
    def __inGradientRange(self, reading):
        inRange = True
        if(abs(reading - self.mBaseline) < 0.01):
            inRange = False
        else:    
            deltaTemp = reading - self.mCurrentTemp
            timeMs = current_milli_time()
            deltaTime = (timeMs - self.mLastReading)/1000 
            gradient = deltaTemp/deltaTime
            if(gradient < 0 and self.mLastDelta > 0 and abs(gradient) > self.MaxRateChange):
                inRange = False
            
            self.mLastDelta = gradient             
        return inRange
            
    def run(self):
        while self.mRunning:
            self.__read()
            time.sleep(self.SampleRate)
        
