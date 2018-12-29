#ifndef ZLGCAN_H_
#define ZLGCAN_H_
#include <time.h>
#include"canframe.h"
#include "config.h"

#define ZCAN_PCI5121         1
#define ZCAN_PCI9810         2
#define ZCAN_USBCAN1         3
#define ZCAN_USBCAN2         4
#define ZCAN_PCI9820         5
#define ZCAN_CAN232          6
#define ZCAN_PCI5110         7
#define ZCAN_CANLITE         8
#define ZCAN_ISA9620         9
#define ZCAN_ISA5420         10
#define ZCAN_PC104CAN        11
#define ZCAN_CANETUDP        12
#define ZCAN_CANETE          12
#define ZCAN_DNP9810         13
#define ZCAN_PCI9840         14
#define ZCAN_PC104CAN2       15
#define ZCAN_PCI9820I        16
#define ZCAN_CANETTCP        17
#define ZCAN_PCIE_9220       18
#define ZCAN_PCI5010U        19
#define ZCAN_USBCAN_E_U      20
#define ZCAN_USBCAN_2E_U     21
#define ZCAN_PCI5020U        22
#define ZCAN_EG20T_CAN       23
#define ZCAN_PCIE9221        24
#define ZCAN_WIFICAN_TCP     25
#define ZCAN_WIFICAN_UDP     26
#define ZCAN_PCIe9120        27
#define ZCAN_PCIe9110        28
#define ZCAN_PCIe9140        29
#define ZCAN_USBCAN_4E_U     31
#define ZCAN_CANDTU_200UR    32
#define ZCAN_CANDTU_MINI     33
#define ZCAN_USBCAN_8E_U     34
#define ZCAN_CANREPLAY       35
#define ZCAN_CANDTU_NET      36
#define ZCAN_CANDTU_100UR    37
#define ZCAN_PCIE_CANFD_100U 38
#define ZCAN_PCIE_CANFD_200U 39
#define ZCAN_PCIE_CANFD_400U 40
#define ZCAN_USBCANFD_200U   41
#define ZCAN_USBCANFD_100U   42
#define ZCAN_USBCANFD_MINI   43
#define ZCAN_CANFDCOM_100IE  44
#define ZCAN_CANSCOPE        45
#define ZCAN_CLOUD           46
#define ZCAN_CANDTU_NET_400  47

#define ZCAN_VIRTUAL_DEVICE  99

#define ZCAN_ERROR_CAN_OVERFLOW            0x0001
#define ZCAN_ERROR_CAN_ERRALARM            0x0002
#define	ZCAN_ERROR_CAN_PASSIVE             0x0004
#define	ZCAN_ERROR_CAN_LOSE                0x0008
#define	ZCAN_ERROR_CAN_BUSERR              0x0010
#define ZCAN_ERROR_CAN_BUSOFF              0x0020
#define ZCAN_ERROR_CAN_BUFFER_OVERFLOW     0x0040

#define	ZCAN_ERROR_DEVICEOPENED            0x0100
#define	ZCAN_ERROR_DEVICEOPEN              0x0200
#define	ZCAN_ERROR_DEVICENOTOPEN           0x0400
#define	ZCAN_ERROR_BUFFEROVERFLOW          0x0800
#define	ZCAN_ERROR_DEVICENOTEXIST          0x1000
#define	ZCAN_ERROR_LOADKERNELDLL           0x2000
#define ZCAN_ERROR_CMDFAILED               0x4000
#define	ZCAN_ERROR_BUFFERCREATE            0x8000

#define ZCAN_ERROR_CANETE_PORTOPENED       0x00010000
#define ZCAN_ERROR_CANETE_INDEXUSED        0x00020000
#define ZCAN_ERROR_REF_TYPE_ID             0x00030001
#define ZCAN_ERROR_CREATE_SOCKET           0x00030002
#define ZCAN_ERROR_OPEN_CONNECT            0x00030003
#define ZCAN_ERROR_NO_STARTUP              0x00030004
#define ZCAN_ERROR_NO_CONNECTED            0x00030005
#define ZCAN_ERROR_SEND_PARTIAL            0x00030006
#define ZCAN_ERROR_SEND_TOO_FAST           0x00030007

#define STATUS_ERR                  0
#define	STATUS_OK                   1
#define STATUS_ONLINE               2
#define	STATUS_OFFLINE              3
#define STATUS_UNSUPPORTED          4

#define CMD_DESIP                   0
#define CMD_DESPORT                 1
#define CMD_CHGDESIPANDPORT         2
#define CMD_SRCPORT                 2
#define CMD_TCP_TYPE                4
#define TCP_CLIENT                  0
#define TCP_SERVER                  1

#define CMD_CLIENT_COUNT            5
#define CMD_CLIENT                  6
#define CMD_DISCONN_CLINET          7
#define CMD_SET_RECONNECT_TIME      8

#define TYPE_CAN   0
#define TYPE_CANFD 1

typedef void * DEVICE_HANDLE;
typedef void * CHANNEL_HANDLE;

typedef struct tagZCAN_DEVICE_INFO {
    USHORT hw_Version;
    USHORT fw_Version;
    USHORT dr_Version;
    USHORT in_Version;
    USHORT irq_Num;
    BYTE   can_Num;
    UCHAR  str_Serial_Num[20];
    UCHAR  str_hw_Type[40];
    USHORT reserved[4];
}ZCAN_DEVICE_INFO;

typedef struct tagZCAN_CHANNEL_INIT_CONFIG {
    UINT can_type; //type:TYPE_CAN TYPE_CANFD
    union
    {
        struct
        {
            UINT  acc_code;
            UINT  acc_mask;
            UINT  reserved;
            BYTE  filter;
            BYTE  timing0;
            BYTE  timing1;
            BYTE  mode;
        }can;
        struct
        {
            UINT   acc_code;
            UINT   acc_mask;
            UINT   abit_timing;
            UINT   dbit_timing;
            UINT   brp;
            BYTE   filter;
            BYTE   mode;
            USHORT pad;
            UINT   reserved;
        }canfd;
    };
}ZCAN_CHANNEL_INIT_CONFIG;

typedef struct tagZCAN_CHANNEL_ERR_INFO {
    UINT error_code;
    BYTE passive_ErrData[3];
    BYTE arLost_ErrData;
} ZCAN_CHANNEL_ERR_INFO;

typedef struct tagZCAN_CHANNEL_STATUS {
    BYTE errInterrupt;
    BYTE regMode;
    BYTE regStatus;
    BYTE regALCapture;
    BYTE regECCapture;
    BYTE regEWLimit;
    BYTE regRECounter;
    BYTE regTECounter;
    UINT Reserved;
}ZCAN_CHANNEL_STATUS;

typedef struct tagZCAN_Transmit_Data
{
    can_frame frame;
    UINT transmit_type;
}ZCAN_Transmit_Data;

typedef struct tagZCAN_Receive_Data
{
    can_frame frame;
    UINT64    timestamp;//us
}ZCAN_Receive_Data;

typedef struct tagZCAN_TransmitFD_Data
{
    canfd_frame frame;
    UINT transmit_type;
}ZCAN_TransmitFD_Data;

typedef struct tagZCAN_ReceiveFD_Data
{
    canfd_frame frame;
    UINT64      timestamp;//us
}ZCAN_ReceiveFD_Data;

typedef struct tagZCAN_AUTO_TRANSMIT_OBJ{
    USHORT enable;
    USHORT index;
    UINT   interval;
    ZCAN_Transmit_Data obj;
}ZCAN_AUTO_TRANSMIT_OBJ, *PZCAN_AUTO_TRANSMIT_OBJ;

typedef struct tagZCANFD_AUTO_TRANSMIT_OBJ{
    USHORT enable;
    USHORT index;
    UINT interval;
    ZCAN_TransmitFD_Data obj;
}ZCANFD_AUTO_TRANSMIT_OBJ, *PZCANFD_AUTO_TRANSMIT_OBJ;

//for zlg cloud
typedef struct tagZCLOUD_DEVINFO
{
    int devIndex;           
    char type[64];
    char id[64];
    char model[64];
    char fwVer[16];
    char hwVer[16];
    char serial[64];
    BYTE canNum;
    int status;             // 0:online, 1:offline
    BYTE bCanUploads[16];   // each channel enable can upload
    BYTE bGpsUpload;
}ZCLOUD_DEVINFO;

typedef struct tagZCLOUD_DEV_GROUP_INFO
{
    char groupName[64];
    char desc[128];
    char groupId[64];
    ZCLOUD_DEVINFO *pDevices;
    size_t devSize;
}ZCLOUD_DEV_GROUP_INFO;

typedef struct tagZCLOUD_USER_DATA
{
    char username[64];
    char mobile[64];
    char email[64];
    ZCLOUD_DEV_GROUP_INFO *pDevGroups;
    size_t devGroupSize;
}ZCLOUD_USER_DATA;

// GPS
typedef struct tagZCLOUD_GPS_FRAME
{
    float latitude;             
    float longitude;            
    float speed;                
    struct __gps_time {
        USHORT    year;
        USHORT    mon;
        USHORT    day;
        USHORT    hour;
        USHORT    min;
        USHORT    sec;
    }tm;                        
} ZCLOUD_GPS_FRAME;
//for zlg cloud

#ifdef __cplusplus 
#define DEF(a) = a
#else 
#define DEF(a)
#endif 

#ifdef __cplusplus
extern "C"
{
#endif

#define INVALID_DEVICE_HANDLE 0
DEVICE_HANDLE ZCAN_OpenDevice(UINT device_type, UINT device_index, UINT reserved);
UINT ZCAN_CloseDevice(DEVICE_HANDLE device_handle);
UINT ZCAN_GetDeviceInf(DEVICE_HANDLE device_handle, ZCAN_DEVICE_INFO* pInfo);

UINT ZCAN_IsDeviceOnLine(DEVICE_HANDLE device_handle);

#define INVALID_CHANNEL_HANDLE 0
CHANNEL_HANDLE ZCAN_InitCAN(DEVICE_HANDLE device_handle, UINT can_index, ZCAN_CHANNEL_INIT_CONFIG* pInitConfig);
UINT ZCAN_StartCAN(CHANNEL_HANDLE channel_handle);
UINT ZCAN_ResetCAN(CHANNEL_HANDLE channel_handle);
UINT ZCAN_ClearBuffer(CHANNEL_HANDLE channel_handle);
UINT ZCAN_ReadChannelErrInfo(CHANNEL_HANDLE channel_handle, ZCAN_CHANNEL_ERR_INFO* pErrInfo);
UINT ZCAN_ReadChannelStatus(CHANNEL_HANDLE channel_handle, ZCAN_CHANNEL_STATUS* pCANStatus);
UINT ZCAN_GetReceiveNum(CHANNEL_HANDLE channel_handle, BYTE type);//type:TYPE_CAN TYPE_CANFD
UINT ZCAN_Transmit(CHANNEL_HANDLE channel_handle, ZCAN_Transmit_Data* pTransmit, UINT len);
UINT ZCAN_Receive(CHANNEL_HANDLE channel_handle, ZCAN_Receive_Data* pReceive, UINT len, int wait_time DEF(-1));
UINT ZCAN_TransmitFD(CHANNEL_HANDLE channel_handle, ZCAN_TransmitFD_Data* pTransmit, UINT len);
UINT ZCAN_ReceiveFD(CHANNEL_HANDLE channel_handle, ZCAN_ReceiveFD_Data* pReceive, UINT len, int wait_time DEF(-1));

IProperty* GetIProperty(DEVICE_HANDLE device_handle);
UINT ReleaseIProperty(IProperty * pIProperty);

void ZCLOUD_SetServerInfo(const char* httpSvr, unsigned short httpPort, const char* mqttSvr, unsigned short mqttPort);
// return 0:success, 1:failure, 2:https error, 3:user login info error, 4:mqtt connection error
UINT ZCLOUD_ConnectServer(const char* username, const char* password);
bool ZCLOUD_IsConnected();
// return 0:success, 1:failure
UINT ZCLOUD_DisconnectServer();
const ZCLOUD_USER_DATA* ZCLOUD_GetUserData();
UINT ZCLOUD_ReceiveGPS(DEVICE_HANDLE device_handle, ZCLOUD_GPS_FRAME* pReceive, UINT len, int wait_time DEF(-1));

#ifdef __cplusplus
}
#endif

#endif //ZLGCAN_H_
