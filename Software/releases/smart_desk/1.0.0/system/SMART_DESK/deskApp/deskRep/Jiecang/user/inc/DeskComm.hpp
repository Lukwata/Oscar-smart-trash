/* 
 * File:   ZmqIpc.hpp
 * Author: thanh
 *
 * Created on September 24, 2015, 9:10 PM
 */

#ifndef DESKCOMM_HPP
#define	DESKCOMM_HPP
// Data Package Define
static struct mZmqPacket{
    static const uint8_t IND0_START_BYTE1  = 0;
    static const uint8_t IND1_START_BYTE2  = 1;
    static const uint8_t IND2_LENGTH  = 2;
    static const uint8_t IND3_PRODUCT_ID = 3;
    static const uint8_t IND4_COMPONENT_ID = 4;
    static const uint8_t IND5_INSTRUCTION = 5;
    static const uint8_t IND6_ADDRESS = 6;
} ZmqPacketIndex;
// Product ID Define
static struct mID{
    static const uint8_t PERSONAL_ROBOT = 1;
    static const uint8_t CLOCK = 2;
    static const uint8_t SMART_DESK = 3;
    static const uint8_t IOS = 4;
    
}ProductID;



// Component ID Define
static struct mComponentID{
    static const uint8_t PAN_MOTOR = 1;
    static const uint8_t TILT_MOTOR = 2;
    static const uint8_t UP_DOWN_MOTOR = 3;

} ComponentID;

// Instruction Define
static struct mInstruction{
    static const uint8_t INS_READ = 1;
    static const uint8_t INS_WRITE = 2;
    static const uint8_t INS_RETURN = 3;

}Instruction;
//

#define     ZMQ_TX_LENGTH           60
#define     ZMQ_RX_LENGTH           60
static struct mZmqPacketVal{
    static const uint8_t START_BYTE  = 0xFF;
    static const uint8_t STOP_BYTE  = 0xFA;
    static const uint8_t IND1_START_BYTE2  = 1;
    static const uint8_t IND2_LENGTH  = 2;
    static const uint8_t IND3_PRODUCT_ID = 3;
    static const uint8_t IND4_COMPONENT_ID = 4;
    static const uint8_t IND5_INSTRUCTION = 5;
    static const uint8_t IND6_ADDRESS = 6;
} ZmqPacketValue;
class DeskComm{
public:
    unsigned char rxBuf[ZMQ_RX_LENGTH];
    unsigned char rxLength;
    unsigned char txBuf[ZMQ_TX_LENGTH];
    unsigned char txLength;
    unsigned char rxBegin;
    unsigned char rxEnd;
    void init();
    char addData(void *p, unsigned char length);
    char isChecksumOk();
    void getAction();
private:
    char getTxChecksum();
};
#endif	/* ZMQIPC_HPP */

