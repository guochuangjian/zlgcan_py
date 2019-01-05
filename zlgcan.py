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


INVALID_DEVICE_HANDLE = DEVICE_HANDLE(None)
INVALID_CHANNEL_HANDLE = CHANNEL_HANDLE(None)

ZCAN_PCI5121        = ZCAN_DEVICE_TYPE(1)
ZCAN_PCI9810        = ZCAN_DEVICE_TYPE(2)
ZCAN_USBCAN1        = ZCAN_DEVICE_TYPE(3)
ZCAN_USBCAN2        = ZCAN_DEVICE_TYPE(4)
ZCAN_PCI9820        = ZCAN_DEVICE_TYPE(5)

ZCAN_USBCANFD_200U  = ZCAN_DEVICE_TYPE(41)
ZCAN_USBCANFD_100U  = ZCAN_DEVICE_TYPE(42)
ZCAN_USBCANFD_MINI  = ZCAN_DEVICE_TYPE(43)

ZCAN_STATUS_ERR         = 0
ZCAN_STATUS_OK          = 1
ZCAN_STATUS_ONLINE      = 2
ZCAN_STATUS_OFFLINE     = 3
ZCAN_STATUS_UNSUPPORTED = 4

ZCAN_TYPE_CAN           = c_uint(0)
ZCAN_TYPE_CANFD         = c_uint(1)

class ZCAN_DEVICE_INFO(Structure):
    _fields_ = [("hw_Version", c_ushort),
                ("fw_Version", c_ushort),
                ("dr_Version", c_ushort), 
                ("in_Version", c_ushort), 
                ("irq_Num", c_ushort),
                ("can_Num", c_ubyte),
                ("str_Serial_Num", c_ubyte * 20),
                ("str_hw_Type", c_ubyte * 40),
                ("reserved", c_ushort * 4)]

    def __str__(self):
        serial = ''
        for i in range(len(self.str_Serial_Num)):
            serial = serial + chr(self.str_Serial_Num[i])
        hw_type = ''
        for i in range(len(self.str_hw_Type)):
            hw_type = hw_type + chr(self.str_hw_Type[i])
        return '硬件版本号：V%d.%02d\r\n固件版本号：V%d.%02d\r\n驱动程序版本号：V%d.%02d\r\n接口库版本号：V%d.%02d\r\n' \
               '中断号：%s\r\nCAN通道数：%s\r\n序列号：%s\r\n硬件类型：%s' % ( \
                self.hw_Version / 0xFF, self.hw_Version & 0xFF,  \
                self.fw_Version / 0xFF, self.fw_Version & 0xFF,  \
                self.dr_Version / 0xFF, self.dr_Version & 0xFF,  \
                self.in_Version / 0xFF, self.in_Version & 0xFF,  \
                self.irq_Num, self.can_Num,  \
                serial, hw_type)


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
                ("config", _ZCAN_CHANNEL_INIT_CONFIG)]

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
            # self.__m_dll = cdll.LoadLibrary("zlgcan.dll")
        else:
            print("No support now!")
        if self.__m_dll == None:
            print("DLL couldn't be loaded!")

    def OpenDevice(self, device_type, device_index, reserved):
        try:
            return self.__m_dll.ZCAN_OpenDevice(device_type, device_index, reserved)
        except:
            print("OpenDevice Failed!")
            raise

    def CloseDevice(self, device_handle):
        try:
            return self.__m_dll.ZCAN_CloseDevice(device_handle)
        except:
            print("CloseDevice Failed!")
            raise

    def GetDeviceInf(self, device_handle):
        try:
            info = ZCAN_DEVICE_INFO()
            ret = self.__m_dll.ZCAN_GetDeviceInf(device_handle, byref(info))
            return info if ret == ZCAN_STATUS_OK else None
        except:
            print("Exception on ZCAN_GetDeviceInf")
            raise

    def DeviceOnLine(self, device_handle):
        try:
            return self.__m_dll.ZCAN_IsDeviceOnLine(device_handle)
        except:
            print("Exception on ZCAN_ZCAN_IsDeviceOnLine!")
            raise

    def InitCAN(self, device_handle, can_index, init_config):
        try:
            ret = self.__m_dll.ZCAN_InitCAN(device_handle, can_index, byref(init_config))
            return CHANNEL_HANDLE(ret)
        except:
            print("Exception on ZCAN_InitCAN!")
            raise

    def StartCAN(self, chn_handle):
        try:
            return self.__m_dll.ZCAN_StartCAN(chn_handle)
        except:
            print("Exception on ZCAN_StartCAN!")
            raise

    def ResetCAN(self, chn_handle):
        try:
            return self.__m_dll.ZCAN_ResetCAN(chn_handle)
        except:
            print("Exception on ZCAN_ResetCAN!")
            raise

    def ClearBuffer(self, chn_handle):
        try:
            return self.__m_dll.ZCAN_ClearBuffer(chn_handle)
        except:
            print("Exception on ZCAN_ClearBuffer!")
            raise

    def ReadChannelErrInfo(self, chn_handle):
        try:
            ErrInfo = ZCAN_CHANNEL_ERR_INFO()
            ret = self.__m_dll.ZCAN_ReadChannelErrInfo(chn_handle)
            return ErrInfo if ret == ZCAN_STATUS_OK else None
        except:
            print("Exception on ZCAN_ReadChannelErrInfo!")
            raise

    def ReadChannelStatus(self, chn_handle):
        try:
            status = ZCAN_CHANNEL_STATUS()
            ret = self.__m_dll.ZCAN_ReadChannelStatus(chn_handle, byref(status))
            return status if ret == ZCAN_STATUS_OK else None
        except:
            print("Exception on ZCAN_ReadChannelStatus!")
            raise

    def GetReceiveNum(self, chn_handle, can_type = ZCAN_TYPE_CAN):
        try:
            return self.__m_dll.ZCAN_GetReceiveNum(chn_handle, can_type)
        except:
            print("Exception on ZCAN_GetReceiveNum!")
            raise

    def Transmit(self, chn_handle, std_msg, len):
        try:
            return self.__m_dll.ZCAN_Transmit(chn_handle, byref(std_msg), len)
        except:
            print("Exception on ZCAN_Transmit!")
            raise

    def Receive(self, chn_handle, rcv_num, wait_time = c_int(-1)):
        try:
            rcv_can_msgs = ZCAN_Receive_Data() * rcv_num
            ret = self.__m_dll.ZCAN_Receive(chn_handle, byref(rcv_can_msgs), rcv_num, wait_time)
            return rcv_can_msgs, ret
        except:
            print("Exception on ZCAN_Receive!")
            raise
    
    def TransmitFD(self, chn_handle, fd_msg, len):
        try:
            return self.__m_dll.ZCAN_TransmitFD(chn_handle, byref(fd_msg), len)
        except:
            print("Exception on ZCAN_TransmitFD!")
            raise
    
    def ReceiveFD(self, chn_handle, rcv_num, wait_time = c_int(-1)):
        try:
            rcv_canfd_msgs = ZCAN_ReceiveFD_Data() * rcv_num
            ret = self.__m_dll.ZCAN_Receive(chn_handle, byref(rcv_can_msgs), rcv_num, wait_time)
            return rcv_canfd_msgs, ret
        except:
            print("Exception on ZCAN_ReceiveFD!")
            raise

    #reserved 
    def GetIProperty(self, device_handle):
        pass

    #reserved 
    def ReleaseIProperty(self, property):
        pass

if __name__ == "__main__":
    can_cfg = _ZCAN_CHANNEL_CAN_INIT_CONFIG(0,1,2,3,4,5, mode = 6)
    canfd_cfg = _ZCAN_CHANNEL_CANFD_INIT_CONFIG(0,1,2,3,4,5,6,7,8)
    _chn_cfg = _ZCAN_CHANNEL_INIT_CONFIG(canfd = canfd_cfg)
    chn_cfg = ZCAN_CHANNEL_INIT_CONFIG(ZCAN_TYPE_CANFD, _chn_cfg)
    print(chn_cfg)
    #sys.path.append(".")
    # os.environ["PATH"] = os.getcwd() + ";" + os.environ["PATH"]
    # print(os.environ["PATH"])
    # zcanlib = ZCAN() 
    # handle = zcanlib.OpenDevice(ZCAN_USBCANFD_MINI, 0,0)
    # print(handle)

    # info = zcanlib.GetDeviceInf(handle)
    # print(info)

    # chn_cfg = ZCAN_CHANNEL_INIT_CONFIG(ZCAN_TYPE_CANFD)
    # chn_handle = zcanlib.InitCAN(handle, 0, chn_cfg)
    # if chn_handle == 0:
    #     print("open failed")
    # else:
    #     zcanlib.StartCAN(chn_handle)

    # zcanlib.CloseDevice(handle)

