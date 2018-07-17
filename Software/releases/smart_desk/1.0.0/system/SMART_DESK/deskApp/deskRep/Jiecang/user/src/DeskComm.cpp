#include"main.hpp"
void DeskComm::init(){
    memset(this->rxBuf,0, sizeof(this->rxBuf));
    memset(this->txBuf,0, sizeof(this->txBuf));
    txBuf[ZmqPacketIndex.IND0_START_BYTE1] = ZmqPacketValue.START_BYTE;
    txBuf[ZmqPacketIndex.IND1_START_BYTE2] = ZmqPacketValue.START_BYTE;
    this->rxLength = 0;
    this->txLength = 0;  
}
char DeskComm::addData(void *p, unsigned char length){
    
    this->rxLength = length;
    memcpy(rxBuf,p,length);
    rxBegin = 0;
    rxEnd = length -1;
    return 0;
}
char DeskComm::isChecksumOk(){
    short sum = rxBuf[rxBegin + ZmqPacketIndex.IND2_LENGTH] +
    rxBuf[rxBegin + ZmqPacketIndex.IND3_PRODUCT_ID] +
    rxBuf[rxBegin + ZmqPacketIndex.IND4_COMPONENT_ID] +
    rxBuf[rxBegin + ZmqPacketIndex.IND5_INSTRUCTION] + 
    rxBuf[rxBegin + ZmqPacketIndex.IND6_ADDRESS];
    if(rxBuf[rxBegin + ZmqPacketIndex.IND2_LENGTH] > 0){
        int tem = rxBegin + ZmqPacketIndex.IND6_ADDRESS +1;
        for(int i = tem; i < tem + rxBuf[rxBegin + ZmqPacketIndex.IND2_LENGTH]; i++){
            sum += rxBuf[i];
        
        }
    }
    if(sum > 255){
        sum = sum%255;
    }
    if(sum == rxBuf[rxEnd - 2]) 
        return true;
    else return false;
}
void DeskComm::getAction(){
    // this function is called when a valid packet got from ZMQ
    extern DeskManager mDesk;
    extern volatile char USE_INCH;
    unsigned char temState = mDesk.currentState;
    unsigned char temMode = rxBuf[rxBegin + ZmqPacketIndex.IND5_INSTRUCTION];
    unsigned char temAddr = rxBuf[rxBegin + ZmqPacketIndex.IND6_ADDRESS];
    unsigned short temData;
    if(rxBuf[rxBegin + ZmqPacketIndex.IND2_LENGTH] == 2){
        
        temData = ((unsigned short)rxBuf[rxEnd - 4])*256;
        temData += (unsigned short)rxBuf[rxEnd - 3];
    } else{
        temData = rxBuf[rxEnd - 3];
    }
    // mode = write/read
    if(temMode == Instruction.INS_WRITE){
        #ifdef CONSOLE
                printf("-I-Received Instruction Write Data\n");
        #endif
        memset(txBuf,0,sizeof(txBuf));
        txLength = 0;
        // update temData to control table with addrsss: temAddr
        mDesk.data[temAddr] = temData;
        //mDesk.resetState(State.STATE_ALL);
        // Check the address to have some modify
        switch(temAddr){
            case Address.ADR_UP:
                // Update state
                temState = State.STATE_UP;
                mDesk.data[Address.ADR_BOX_STATUS] = 1;
                mDesk.direction = 0;
                #ifdef CONSOLE
                    printf("-I-Set to UP_STATE\n");
                #endif
                mDesk.setState(temState);
                break;
            case Address.ADR_DOWN:
            {
                temState = State.STATE_DOWN;
                mDesk.data[Address.ADR_BOX_STATUS] = 1;
                mDesk.direction = 0;
                #ifdef CONSOLE
                    printf("-I-Set to DOWN_STATE\n");
                #endif
                mDesk.setState(temState);
                break;
            }
            case Address.ADR_STOP:
            {
                temState = State.STATE_STOP;
                mDesk.data[Address.ADR_OPERATE_MODE] = Mode.MODE_MANUAL;
                #ifdef CONSOLE
                    printf("-I-Set to STOP_STATE\n");
                #endif
                mDesk.setState(temState);
                break;
            }
            case Address.ADR_HEIGHT_SP:
            {
                mDesk.direction = 0;
                mDesk.data[Address.ADR_BOX_STATUS] = 1;
                #ifdef CONSOLE
                    printf("-I-Set height\n");
                #endif
                if (mDesk.data[Address.ADR_HEIGHT_SP] > mDesk.data[Address.ADR_MAX_HEIGHT])
                    mDesk.data[Address.ADR_HEIGHT_SP] = mDesk.data[Address.ADR_MAX_HEIGHT];
                if (mDesk.data[Address.ADR_HEIGHT_SP] < mDesk.data[Address.ADR_MIN_HEIGHT])
                    mDesk.data[Address.ADR_HEIGHT_SP] = mDesk.data[Address.ADR_MIN_HEIGHT];
                if (USE_INCH == true){
                    mDesk.data[Address.ADR_HEIGHT_SP] = mDesk.mm2in(mDesk.data[Address.ADR_HEIGHT_SP]);
                    
                }                
                mDesk.data[Address.ADR_OPERATE_MODE ] = Mode.MODE_AUTO;
                #ifdef EN_DESK_LOG
                                printf("SP = %d  \n",mDesk.data[Address.ADR_HEIGHT_SP]);
                #endif
                break;
            }
            case Address.ADR_SAVE2POS1:
            {
                mDesk.data[Address.ADR_BOX_STATUS] = 1;
                temState = State.STATE_SAVE2POS1;
                mDesk.setState(temState);
                break;
            }
            case Address.ADR_MOVE2POS1:
            {
                if(mDesk.currentState == State.STATE_FREE){
                    mDesk.data[Address.ADR_BOX_STATUS] = 1;
                    temState = State.STATE_MOVE2POS1;
                    mDesk.setState(temState);
                }
                
                break;
            }
            case Address.ADR_SAVE2POS2:
            {
                mDesk.data[Address.ADR_BOX_STATUS] = 1;
                temState = State.STATE_SAVE2POS2;
                mDesk.setState(temState);
                break;
            }
            case Address.ADR_MOVE2POS2:
            {
                if(mDesk.currentState == State.STATE_FREE){
                    mDesk.data[Address.ADR_BOX_STATUS] = 1;
                    temState = State.STATE_MOVE2POS2; 
                    printf("OK\n");
                    mDesk.setState(temState);
                }
                
                break;
            }
            default:
            {
                //temState = mDesk.currentState;
                #ifdef CONSOLE
                    printf("-I-Set to FREE_STATE\n");
                    mDesk.addToLog("-I-Set to FREE_STATE");
                #endif
                break;  
            }
        }
        // prepare packet to send to requester.
        txBuf[ZmqPacketIndex.IND0_START_BYTE1] = ZmqPacketValue.START_BYTE;
        txBuf[ZmqPacketIndex.IND1_START_BYTE2] = ZmqPacketValue.START_BYTE;
        txBuf[ZmqPacketIndex.IND2_LENGTH] = 2; // 2 bytes data
        txBuf[ZmqPacketIndex.IND3_PRODUCT_ID] = ProductID.SMART_DESK;
        txBuf[ZmqPacketIndex.IND4_COMPONENT_ID] = ComponentID.UP_DOWN_MOTOR;
        txBuf[ZmqPacketIndex.IND5_INSTRUCTION] = Instruction.INS_RETURN;
        txBuf[ZmqPacketIndex.IND6_ADDRESS] = temAddr;
        txBuf[ZmqPacketIndex.IND6_ADDRESS + 1] = (uint8_t)(mDesk.data[temAddr] >> 8);
        txBuf[ZmqPacketIndex.IND6_ADDRESS + 2] = (uint8_t)(mDesk.data[temAddr]);
        txLength = ZmqPacketIndex.IND6_ADDRESS + 4 + txBuf[ZmqPacketIndex.IND2_LENGTH];
        #ifdef CONSOLE
            printf("TX Length = %d\n",txLength);
        #endif
        txBuf[txLength - 3] = getTxChecksum();
        txBuf[txLength - 2] = ZmqPacketValue.STOP_BYTE;
        txBuf[txLength - 1] = ZmqPacketValue.STOP_BYTE;
     
    } 
    
    
    else if(temMode == Instruction.INS_READ){
        #ifdef CONSOLE
            printf("-I-Received Instruction Read Data\n");
            mDesk.addToLog("-I-Received Instruction Read Data");
        #endif
        // prepare packet to return
        txBuf[ZmqPacketIndex.IND0_START_BYTE1] = ZmqPacketValue.START_BYTE;
        txBuf[ZmqPacketIndex.IND1_START_BYTE2] = ZmqPacketValue.START_BYTE;
        txBuf[ZmqPacketIndex.IND2_LENGTH] = 2; // 2 bytes data
        txBuf[ZmqPacketIndex.IND3_PRODUCT_ID] = ProductID.SMART_DESK;
        txBuf[ZmqPacketIndex.IND4_COMPONENT_ID] = ComponentID.UP_DOWN_MOTOR;
        txBuf[ZmqPacketIndex.IND5_INSTRUCTION] = Instruction.INS_RETURN;
        txBuf[ZmqPacketIndex.IND6_ADDRESS] = temAddr;       
        temData = mDesk.data[temAddr];
        if (temAddr == Address.ADR_HEIGHT){
            if (USE_INCH == true) temData = mDesk.in2mm(temData); 
            #ifdef EN_DESK_LOG
                printf("Height: %d  \r\n",temData);      
            #endif
        }
        txBuf[ZmqPacketIndex.IND6_ADDRESS + 1] = (uint8_t)(temData >> 8);
        txBuf[ZmqPacketIndex.IND6_ADDRESS + 2] = (uint8_t)temData;
        txLength = ZmqPacketIndex.IND6_ADDRESS + 4 + txBuf[ZmqPacketIndex.IND2_LENGTH];
        #ifdef CONSOLE
            printf("TX Length = %d\n",txLength);
        #endif
        txBuf[txLength - 3] = getTxChecksum();
        txBuf[txLength - 2] = ZmqPacketValue.STOP_BYTE;
        txBuf[txLength - 1] = ZmqPacketValue.STOP_BYTE;
        
        //temState = State.STATE_GET_DATA;
                
    }
    
}
char DeskComm::getTxChecksum(){
    int sum = 0;
    for(int i = ZmqPacketIndex.IND2_LENGTH; i < txLength - 3; i++){
        sum += txBuf[i];
    }
    if(sum > 255) sum = sum%255;
    return sum;
}