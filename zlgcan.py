#!/usr/bin/python
import ctypes

class ZCAN(object):
    def __init__(self):
        #load dll
        pass 

    def OpenDevice(self, device_type, device_index, reserved):
        pass
    
    def CloseDevice(self, device_handle):
        pass

    def GetDeviceInf(device_handle):
        return None

    def DeviceOnLine(device_handle):
        return False

    def InitCAN(device_handle, can_index, InitConfig):
        pass

    def StartCAN(chn_handle):
        pass

    def ResetCAN(chn_handle):
        pass

    def ClearBuffer(chn_handle):
        pass

    def ReadChannelErrInfo(chn_handle):
        return None

    def ReadChannelStatus(chn_handle):
        return None

    def GetReceiveNum(chn_handle, type = 0):
        return 0

    def Transmit(chn_handle, std_msg, len):
        pass

    def Receive(chn_handle, wait_time = -1):
        pass
    
    def TransmitFD(chn_handle, fd_msg, len):
        pass
    
    def ReceiveFD(chn_handle, wait_time = -1):
        pass

    #reserved 
    def GetIProperty(device_handle):
        pass

    #reserved 
    def ReleaseIProperty(property):
        pass

if __name__ == "__main__":
    pass