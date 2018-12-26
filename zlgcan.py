#!/usr/bin/python
#  zlgcan.py
#
#  ~~~~~~~~~~~~
#
#  ZLGCAN API
#
#  ~~~~~~~~~~~~
#
#  ------------------------------------------------------------------
#  Author : guochuangjian    
#  Last change: 25.12.2018
#
#  Language: Python 3.6
#  ------------------------------------------------------------------
#
from ctypes import *
import platform

DEVICE_HANDLE  = c_void_p
CHANNEL_HANDLE = c_void_p
CANID          = c_uint

class ZCAN_DEVICE_INFO(Structure):
    _fields_ = [("hw_Version", c_ushort),
                ("fw_Version", c_ushort),
                ("dr_Version", c_ushort), 
                ("in_Version", c_ushort), 
                ("irq_num", c_ushort),
                ("can_Num", c_ubyte),
                ("str_Serial_Num", c_ubyte * 20),
                ("str_hw_Type", c_ubyte * 40),
                ("reserved", c_ushort * 4)]

class _ZCAN_CHANNEL_CAN_INIT_CONFIG(Structure):
    _fields_ = [("acc_code", c_uint),
                ("acc_mask", c_uint),
                ("reserved", c_uint),
                ("filter",   c_ubyte),
                ("timing0",  c_ubyte),
                ("timing1",  c_ubyte),
                ("mode",     c_ubyte)]

class _ZCAN_CHANNEL_CANFD_INIT_CONFIG(Structure):
    _fields_ = [("acc_code",     c_uint),
                ("acc_mask",     c_uint),
                ("abit_timing",  c_uint),
                ("dbit_timing",  c_uint),
                ("brp",          c_uint),
                ("filter",       c_ubyte),
                ("mode",         c_ubyte),
                ("pad",          c_ushort),
                ("reserved",     c_uint)]

class _ZCAN_CHANNEL_INIT_CONFIG(Union):
    _fields_ = [("can", _ZCAN_CHANNEL_CAN_INIT_CONFIG), ("canfd", _ZCAN_CHANNEL_CANFD_INIT_CONFIG)]

class ZCAN_CHANNEL_INIT_CONFIG(Structure):
    _fields_ = [("can_type", c_uint),
                ("config", _ZCAN_CHANNEL_CAN_INIT_CONFIG)]

class ZCAN_CHANNEL_ERR_INFO(Structure):
    _fields_ = [("error_code", c_uint),
                ("passive_ErrData", c_ubyte * 3),
                ("arLost_ErrData", c_ubyte)]

class ZCAN_CHANNEL_STATUS(Structure):
    _fields_ = [("errInterrupt", c_ubyte),
                ("regMode",      c_ubyte),
                ("regStatus",    c_ubyte), 
                ("regALCapture", c_ubyte),
                ("regECCapture", c_ubyte),
                ("regEWLimit",   c_ubyte),
                ("regRECounter", c_ubyte),
                ("regTECounter", c_ubyte),
                ("Reserved",     c_ubyte)]

class ZCAN_CAN_FRAME(Structure):
    _fields_ = [("can_id",  CANID), 
                ("can_dlc", c_ubyte),
                ("__pad",   c_ubyte),
                ("__res0",  c_ubyte),
                ("__res1",  c_ubyte),
                ("data",    c_ubyte * 8)]

class ZCAN_CANFD_FRAME(Structure):
    _fields_ = [("can_id",  CANID), 
                ("len",     c_ubyte),
                ("flags",   c_ubyte),
                ("__res0",  c_ubyte),
                ("__res1",  c_ubyte),
                ("data",    c_ubyte * 64)]

class ZCAN_Transmit_Data(Structure):
    _fileds_ = [("frame", ZCAN_CAN_FRAME), ("transmit_type", c_uint)]

class ZCAN_Receive_Data(Structure):
    _fileds_ = [("frame", ZCAN_CAN_FRAME), ("timestamp", c_ulong)]

class ZCAN_TransmitFD_Data(Structure):
    _fileds_ = [("frame", ZCAN_CANFD_FRAME), ("transmit_type", c_uint)]

class ZCAN_ReceiveFD_Data(Structure):
    _fileds_ = [("frame", ZCAN_CANFD_FRAME), ("timestamp", c_ulong)]

class ZCAN_AUTO_TRANSMIT_OBJ(Structure):
    _fields_ = [("enable",   c_ushort),
                ("index",    c_ushort),
                ("interval", c_uint),
                ("obj",      ZCAN_Transmit_Data)]

class ZCANFD_AUTO_TRANSMIT_OBJ(Structure):
    _fields_ = [("enable",   c_ushort),
                ("index",    c_ushort),
                ("interval", c_uint),
                ("obj",      ZCAN_TransmitFD_Data)]

class ZCAN(object):
    def __init__(self):
        if platform.system() == "Windows":
            self.__m_dll = windll.LoadLibrary("zlgcan.dll")
        else:
            print("No support now!")
        if self.__m_dll == None
            print("DLL couldn't be loaded!")

    def OpenDevice(self, device_type, device_index, reserved):
        try:
            ret = self.__m_dll.ZCAN_OpenDevice(device_type, device_index, reserved)
            return DEVICE_HANDLE(ret)
        except:
            print("OpenDevice Failed!")
            raise

    def CloseDevice(self, device_handle):
        try:
            ret = self.__m_dll.ZCAN_CloseDevice(device_handle)
        except:
            print("CloseDevice Failed!")
            raise

    def GetDeviceInf(device_handle):
        try:
            info = ZCAN_DEVICE_INFO()
            ret = self.__m_dll.ZCAN_GetDeviceInf(device_handle, info)
            return info
        except:
            print("Exception on ZCAN_GetDeviceInf")
            raise

    def DeviceOnLine(device_handle):
        try:
            ret = self.__m_dll.ZCAN_IsDeviceOnLine(device_handle)
            return c_uint(ret)
        except:
            print("Exception on ZCAN_ZCAN_IsDeviceOnLine!")
            raise

    def InitCAN(device_handle, can_index, init_config):
        try:
            ret = self.__m_dll.ZCAN_InitCAN(device_handle, can_index, byref(init_config))
            return CHANNEL_HANDLE(ret)
        except:
            print("Exception on ZCAN_InitCAN!")
            raise

    def StartCAN(chn_handle):
        try:
            ret = self.__m_dll.ZCAN_StartCAN(chn_handle)
            return CHANNEL_HANDLE(ret)
        except:
            print("Exception on ZCAN_StartCAN!")
            raise

    def ResetCAN(chn_handle):
        try:
            ret = self.__m_dll.ZCAN_ResetCAN(chn_handle)
            return c_uint(ret)
        except:
            print("Exception on ZCAN_ResetCAN!")
            raise

    def ClearBuffer(chn_handle):
        try:
            ret = self.__m_dll.ZCAN_ClearBuffer(chn_handle)
            return c_uint(ret)
        except:
            print("Exception on ZCAN_ClearBuffer!")
            raise

    def ReadChannelErrInfo(chn_handle):
        try:
            ErrInfo = ZCAN_
            ret = self.__m_dll.ZCAN_ClearBuffer(chn_handle)
            return c_uint(ret)
        except:
            print("Exception on ZCAN_ClearBuffer!")
            raise

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