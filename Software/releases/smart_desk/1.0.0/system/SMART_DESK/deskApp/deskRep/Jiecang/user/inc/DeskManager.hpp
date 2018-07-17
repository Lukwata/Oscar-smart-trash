/* 
 * File:   DeskManager.hpp
 * Author: thanh
 *
 * Created on September 11, 2015, 5:23 PM
 */

#ifndef DESKMANAGER_HPP
#define DESKMANAGER_HPP

#include "DeskComm.hpp"


// Package Define
/**/
// Functions Define
// Send to control box



#define     DESK_TX_BUFFER_LENGTH    15
#define     DESK_RX_BUFFER_LENGTH    15
#define     MAX_RX_LENGTH        120
#define     MAX_TX_LENGTH        20

#define DEFAULT_HEIGHT      800
//#define DESK_MAX_HEIGHT    492
//#define DESK_MIN_HEIGHT     250
#define DESK_MAX_HEIGHT    1250
#define DESK_MIN_HEIGHT     630
#define EEPROM_SECOND_USE   100
#define DEFAULT_VERSION         2





#define UID                      0x00010001
static struct mMode{
    static const unsigned short MODE_AUTO = 2 ;
    static const unsigned short MODE_MANUAL = 1;
} Mode;
static struct mState{
    static const uint8_t STATE_STOP = 0;
    static const uint8_t STATE_UP = 1;
    static const uint8_t STATE_DOWN = 2 ;
    static const uint8_t STATE_FREE = 3;
    static const uint8_t STATE_ERROR = 4;
    static const uint8_t STATE_SET_DATA = 5;
    static const uint8_t STATE_GET_DATA = 6 ;
    static const uint8_t STATE_RETURN = 7;
    static const uint8_t STATE_RESET = 8;
    static const uint8_t STATE_BUSY = 9;
    static const uint8_t STATE_SAVE2POS1 = 10;
    static const uint8_t STATE_MOVE2POS1 = 11;
    static const uint8_t STATE_SAVE2POS2 = 12;
    static const uint8_t STATE_MOVE2POS2 = 13;
    static const uint8_t STATE_GET_MINMAX = 14;
    static const uint8_t STATE_ALL = 255;
} State;
static struct mAddress{
    static const uint8_t ADR_VERSION = 0x01; //1
    static const uint8_t ADR_HEIGHT = 0x02;  //2
    static const uint8_t ADR_UP = 0x03;         //3
    static const uint8_t ADR_DOWN = 0x04;
    static const uint8_t ADR_STOP = 0x05;
    static const uint8_t ADR_SAVE2POS1 = 0x06;
    static const uint8_t ADR_MOVE2POS1 = 0x07;
    static const uint8_t ADR_SAVE2POS2 = 0x08;
    static const uint8_t ADR_MOVE2POS2 = 0x09;
    static const uint8_t ADR_USER5 = 0x0A;
    static const uint8_t ADR_USER6 = 0x0B;
    static const uint8_t ADR_USER7 = 0x0C;
    static const uint8_t ADR_USER8 = 0x0D;
    static const uint8_t ADR_USER9 = 0x0E;
    static const uint8_t ADR_USER10 = 0x0F;
    static const uint8_t ADR_MIN_HEIGHT = 0x10;
    static const uint8_t ADR_MAX_HEIGHT = 0x11;
    static const uint8_t ADR_HEIGHT_SP = 0x12;
    static const uint8_t ADR_OPERATE_MODE = 0x13;
    static const uint8_t ADR_UID = 0x14;
    static const uint8_t ADR_BOX_STATUS = 0x15;
    static const uint8_t ADR_STATE = 0x16;
    static const uint8_t ADR_DIR = 0x17;
    /*
     add address to control table
     
     */
    
    
    static const uint8_t ADR_RAM_LENGTH = 0x18;
    
} Address;
static struct mDeskPacket{
    static const uint8_t IND_START_BYTE1 =  0;
    static const uint8_t IND_START_BYTE2 =  1;
    static const uint8_t IND_FUNCTION =     2;
    static const uint8_t IND_DATA_LENGTH =  3;

}DeskPacket;
static struct mCtrBoxFcn{
    static const uint8_t   CURENT_HEIGHT = 0x01;
    static const uint8_t   ERROR_CODE   = 0x02;
    static const uint8_t   RESET_MODE   = 0x04;
    static const uint8_t   MAX_MIN_HEIGHT  = 0x07;
    static const uint8_t RX_START_BYTE1   =   0xF2;
    static const uint8_t RX_START_BYTE2   =   0xF2;
    static const uint8_t RX_STOP_BYTE   =   0x7E;
} CtrBoxFcn;




class DeskManager{
public:
    DeskComm Comm;
    char txBuf[MAX_TX_LENGTH];
    unsigned char txDataLength;
    char rxBuf[MAX_RX_LENGTH];
    unsigned char rxDataLength;
    void init();
    void moveUp();
    void moveDown();
    void stopMove();
    void getDeskStatus();
    void getDeskMinMax();
    void getDeskAction();
    void getHeight();
    char isCheckSumOK();
    void setState(unsigned char state);
    void resetState(unsigned char state);
    void addDataRxBuf(char c);
    void initControlTable();
    void saveToPos1();
    void saveToPos2();
    void saveToPos3();
    void saveToPos4();
    void moveToPos1();
    void moveToPos2();
    void moveToPos3();
    void moveToPos4();
    unsigned short mm2in(unsigned short mm);
    unsigned short in2mm(unsigned short in);
    unsigned char currentState;
    unsigned char preState;
    uint16_t up_state_count;
    uint16_t down_state_count;
    uint16_t stop_state_count;
    uint16_t free_state_count;
    uint16_t reset_state_count;
    uint16_t max_state_count;
    uint16_t error_state_count;
    uint8_t move2pos1_state_count;
    uint8_t move2pos2_state_count;
    unsigned char rx_begin;
    unsigned char rx_end;
    unsigned char rx_data_updated;
    unsigned short data[Address.ADR_RAM_LENGTH];
    bool memFlag;
    bool en_checksum;
    uint8_t num_checksum_fail;
    void addToLog( const char *p);
    int16_t direction;
    int16_t currentHeigh;
    bool data_changed;
};



#endif	/* DESKMANAGER_HPP */

