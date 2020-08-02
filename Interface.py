#!/usr/bin/env python
from Thermocouple import ThermocoupleReader


def main():
    
    beanTempReader = ThermocoupleReader(0x66)
    beanTemp, fluTemp = beanTempReader.read()
    print("{}".format(beanTemp))
    
if __name__ == '__main__':
    main()
