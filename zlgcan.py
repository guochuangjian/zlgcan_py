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
ZCAN_STATUS    = c_uint
ZCAN_DEVICE_TYPE = c_uint

ZCAN_PCI5121        = ZCAN_DEVICE_TYPE(1)
ZCAN_PCI9810        = ZCAN_DEVICE_TYPE(2)
ZCAN_USBCAN1        = ZCAN_DEVICE_TYPE(3)
ZCAN_USBCAN2        = ZCAN_DEVICE_TYPE(4)
ZCAN_PCI9820        = ZCAN_DEVICE_TYPE(5)

ZCAN_USBCANFD_200U  = ZCAN_DEVICE_TYPE(41)
ZCAN_USBCANFD_100U  = ZCAN_DEVICE_TYPE(42)
ZCAN_USBCANFD_MINI  = ZCAN_DEVICE_TYPE(43)

ZCAN_STATUS_ERR         = ZCAN_STATUS(0)
ZCAN_STATUS_OK          = ZCAN_STATUS(1)
ZCAN_STATUS_ONLINE      = ZCAN_STATUS(2)
ZCAN_STATUS_OFFLINE     = ZCAN_STATUS(3)
ZCAN_STATUS_UNSUPPORTED = ZCAN_STATUS(4)

ZCAN_TYPE_CAN           = c_ubyte(0)
ZCAN_TYPE_CANFD         = c_ubyte(1)

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
        if self.__m_dll == None:
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
            return ZCAN_STATUS(ret), info
        except:
            print("Exception on ZCAN_GetDeviceInf")
            raise

    def DeviceOnLine(device_handle):
        try:
            ret = self.__m_dll.ZCAN_IsDeviceOnLine(device_handle)
            return ZCAN_STATUS(ret)
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
            return ZCAN_STATUS(ret)
        except:
            print("Exception on ZCAN_ResetCAN!")
            raise

    def ClearBuffer(chn_handle):
        try:
            ret = self.__m_dll.ZCAN_ClearBuffer(chn_handle)
            return ZCAN_STATUS(ret)
        except:
            print("Exception on ZCAN_ClearBuffer!")
            raise

    def ReadChannelErrInfo(chn_handle):
        try:
            ErrInfo = ZCAN_CHANNEL_ERR_INFO()
            ret = self.__m_dll.ZCAN_ReadChannelErrInfo(chn_handle)
            return ZCAN_STATUS(ret), ErrInfo
        except:
            print("Exception on ZCAN_ReadChannelErrInfo!")
            raise

    def ReadChannelStatus(chn_handle):
        try:
            status = ZCAN_CHANNEL_STATUS()
            ret = self.__m_dll.ZCAN_ReadChannelStatus(chn_handle, byref(status))
            return ZCAN_STATUS(ret), status 
        except:
            print("Exception on ZCAN_ReadChannelStatus!")
            raise

    def GetReceiveNum(chn_handle, can_type = ZCAN_TYPE_CAN):
        try:
            ret = self.__m_dll.ZCAN_GetReceiveNum(chn_handle, can_type)
            return c_uint(ret)
        except:
            print("Exception on ZCAN_GetReceiveNum!")
            raise

    def Transmit(chn_handle, std_msg, len):
        try:
            ret = self.__m_dll.ZCAN_Transmit(chn_handle, byref(std_msg), len)
            return ZCAN_STATUS(ret)
        except:
            print("Exception on ZCAN_Transmit!")
            raise

    def Receive(chn_handle, rcv_num, wait_time = c_int(-1)):
        try:
            rcv_can_msgs = ZCAN_Receive_Data() * rcv_num
            ret = self.__m_dll.ZCAN_Receive(chn_handle, byref(rcv_can_msgs), rcv_num, wait_time)
            return rcv_can_msgs, ret
        except:
            print("Exception on ZCAN_Receive!")
            raise
    
    def TransmitFD(chn_handle, fd_msg, len):
        try:
            ret = self.__m_dll.ZCAN_TransmitFD(chn_handle, byref(fd_msg), len)
            return ZCAN_STATUS(ret)
        except:
            print("Exception on ZCAN_TransmitFD!")
            raise
    
    def ReceiveFD(chn_handle, rcv_num, wait_time = c_int(-1)):
        try:
            rcv_canfd_msgs = ZCAN_ReceiveFD_Data() * rcv_num
            ret = self.__m_dll.ZCAN_Receive(chn_handle, byref(rcv_can_msgs), rcv_num, wait_time)
            return rcv_canfd_msgs, ret
        except:
            print("Exception on ZCAN_ReceiveFD!")
            raise

    #reserved 
    def GetIProperty(device_handle):
        pass

    #reserved 
    def ReleaseIProperty(property):
        pass

if __name__ == "__main__":
    pass
