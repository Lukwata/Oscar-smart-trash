
#include "main.hpp"
void DeskManager::init(){
    // TX Buffer Init
    memset(this->txBuf, 0 , sizeof(this->txBuf));
    this->txDataLength = 0;
    // RX Buffer Init
    memset(this->rxBuf, 0 , sizeof(this->rxBuf));
    this->rxDataLength = 0;
    // 
    this->max_state_count = 60;
    this->currentState = State.STATE_STOP;
    this->setState(State.STATE_FREE);
    this->rxDataLength = 0;
    this->rx_data_updated = 0;
    this->rx_begin = 0;
    this->rx_end = 0;
    
    this->Comm.init();
    this->memFlag = false;
    this -> en_checksum = true;
    this ->num_checksum_fail = 0;
    this -> direction = 0;
    this -> data_changed = false;
    this -> currentHeigh = 0;
    this->initControlTable();
    
}
void DeskManager::moveUp(){
    this->txBuf[0] = 0xF1;
    this->txBuf[1] = 0xF1;
    this->txBuf[2] = 0x01;
    this->txBuf[3] = 0x00;
    this->txBuf[4] = 0x01;
    this->txBuf[5] = 0x7E;
    this->txDataLength = 6;
}
void DeskManager::moveDown(){
    this->txBuf[0] = 0xF1;
    this->txBuf[1] = 0xF1;
    this->txBuf[2] = 0x02;
    this->txBuf[3] = 0x00;
    this->txBuf[4] = 0x02;
    this->txBuf[5] = 0x7E;
    this->txDataLength = 6;
}
void DeskManager::stopMove(){
    this->txBuf[0] = 0xF1;
    this->txBuf[1] = 0xF1;
    this->txBuf[2] = 0x0A;
    this->txBuf[3] = 0x00;
    this->txBuf[4] = 0x0A;
    this->txBuf[5] = 0x7E;
    this->txDataLength = 6;
}
void DeskManager::getDeskStatus(){
    this->txBuf[0] = 0xF1;
    this->txBuf[1] = 0xF1;
    this->txBuf[2] = 0x07;
    this->txBuf[3] = 0x00;
    this->txBuf[4] = 0x07;
    this->txBuf[5] = 0x7E;
    this->txDataLength = 6;
}
void DeskManager::getDeskMinMax(){
    this->txBuf[0] = 0xF1;
    this->txBuf[1] = 0xF1;
    this->txBuf[2] = 0x0C;
    this->txBuf[3] = 0x00;
    this->txBuf[4] = 0x0C;
    this->txBuf[5] = 0x7E;
    this->txDataLength = 6;
}
void DeskManager::setState(unsigned char state){
    this->preState = this->currentState;
    this->currentState = state;
}
void DeskManager::resetState(unsigned char state){
    switch (state){
        case State.STATE_UP:
            this -> up_state_count = 0;
            break;
        case State.STATE_DOWN:
            this -> down_state_count = 0;
            break;
        case State.STATE_STOP:
            this -> stop_state_count = 0;
            break;
        case State.STATE_FREE:
            this -> free_state_count = 0;
            break;
        case State.STATE_ERROR:
            this -> error_state_count = 0;
            break;
        case State.STATE_MOVE2POS1:
            this -> move2pos1_state_count = 0;
            break;
        case State.STATE_MOVE2POS2:
            this -> move2pos2_state_count = 0;
            break;
        case State.STATE_ALL:
            this -> up_state_count = 0;
            this -> down_state_count = 0;
            this -> stop_state_count = 0;
            this -> free_state_count = 0;
            this -> error_state_count = 0;
            this -> reset_state_count = 0;
            this -> move2pos1_state_count = 0;
            this -> move2pos2_state_count = 0;
            break;
    }
}
void DeskManager::addDataRxBuf(char c){
    if(this->rxDataLength <  MAX_RX_LENGTH -1  ){
        // add data to buffer
        this->rxBuf[this->rxDataLength++] = c;
        // Check Stop byte received?
        if(c == CtrBoxFcn.RX_STOP_BYTE){
            
//            printf("rx length = %d\n",this->rxDataLength);
            for(int i = this->rxDataLength - 1; i > 0; i--){
                // Get position of stop Bytes
                if(rxBuf[i] == CtrBoxFcn.RX_STOP_BYTE){
                    rx_end = i;
                }
                // Get position of start bytes 1
                
                if((this->rxBuf[i] == CtrBoxFcn.RX_START_BYTE1)&&
                        (this->rxBuf[i-1] == CtrBoxFcn.RX_START_BYTE2)){
                    this->rx_begin = i -1;
                    this->rx_data_updated = true;
                    break;
                }   
            } 
        }
    }
    else this->rxDataLength = 0;
}
char DeskManager::isCheckSumOK(){
    if(this->rxBuf[this->rx_begin + DeskPacket.IND_FUNCTION] == 
            CtrBoxFcn.ERROR_CODE) return true;
    else{
        unsigned int sum = this->rxBuf[rx_begin + DeskPacket.IND_FUNCTION]+
        rxBuf[rx_begin + DeskPacket.IND_DATA_LENGTH ];
        if(rxBuf[rx_begin + DeskPacket.IND_DATA_LENGTH] > 0){
            unsigned int tem = rx_begin + DeskPacket.IND_DATA_LENGTH + 1;
            for (int i = tem; i< tem +rxBuf[rx_begin + DeskPacket.IND_DATA_LENGTH];i++ )
                sum += rxBuf[i];
        }
        if(sum >= 256){
            sum = sum%256;
        }
        #ifdef CONSOLE
            printf("[Serial]sum =%d, [Box]sum=%d\n",sum,rxBuf[rx_end-1]);
        #endif
        if (sum == rxBuf[rx_end - 1])
        {
            return true;
        }
        else return false;
    }
}
void DeskManager::getDeskAction(){
    // Checking Function Byte returned frome Desk
    extern volatile char USE_INCH;
    switch(rxBuf[rx_begin + DeskPacket.IND_FUNCTION]){
        //incase desk return current Heigh;
        case CtrBoxFcn.CURENT_HEIGHT:
            // real value from control box
            this ->currentHeigh = rxBuf[rx_end -4]*256 + rxBuf[rx_end -3 ]; 
            // Check the height value to determine which  unit of height and set flag to remember.          
            if((USE_INCH == false)&&( this ->currentHeigh < data[Address.ADR_MIN_HEIGHT] - 5)&&(this ->currentHeigh > 40)){
                USE_INCH = true;  
            #ifdef EN_DESK_LOG
                printf("Inch Control Box Detected,Height = %d\n",this ->currentHeigh);
            #endif  
                }
            // only update height value to control table if new value came.
//            if(this ->currentHeigh != this->data[Address.ADR_HEIGHT]){
//                this -> direction = this ->currentHeigh - this->data[Address.ADR_HEIGHT];
//                this->data[Address.ADR_HEIGHT] = this ->currentHeigh;
//                #ifdef CONSOLE
//                    printf("-I- Current Height = %d\n",this->data[Address.ADR_HEIGHT]);
//                #endif
//            }  
            this -> direction = this ->currentHeigh - this->data[Address.ADR_HEIGHT];
            //printf("h = %d, dir = %d\n",this ->currentHeigh, this-> direction);
            this->data[Address.ADR_HEIGHT] = this ->currentHeigh;
            
            // Checking Memory pad Flag and update only having change            
            if (this->memFlag != rxBuf[rx_end -2]){
                this->memFlag = rxBuf[rx_end -2];
                if (this->memFlag == 1) this->data[Address.ADR_SAVE2POS1] = 2;
                else if (this->memFlag == 2) this->data[Address.ADR_SAVE2POS2] = 2;
                else if(this->memFlag == 3){
                    this->data[Address.ADR_SAVE2POS1] = 2;
                    this->data[Address.ADR_SAVE2POS2] = 2;
                }           
            }
            /*
             Neu state hien tai dang la state error hoac reset ma co data chieu cao
             * tra ve thi qua trinh tu dong reset da xong, -> set to free state.
             */ 
          
            if ((this -> currentState == State.STATE_RESET) ||(this -> currentState == State.STATE_ERROR)){
                this -> setState(State.STATE_FREE);         
            }
            break;
        case CtrBoxFcn.ERROR_CODE:
            this->data[Address.ADR_OPERATE_MODE] = Mode.MODE_MANUAL;
            this->setState(State.STATE_ERROR);
            #ifdef CONSOLE
                printf("-E- Desk in Error Mode\n");
            #endif
            break;
        case CtrBoxFcn.RESET_MODE:
            this->data[Address.ADR_OPERATE_MODE] = Mode.MODE_MANUAL;
            this->setState(State.STATE_RESET);
            #ifdef CONSOLE
                printf("-E- Desk in Reset Mode\n");
            #endif
            break;
        case CtrBoxFcn.MAX_MIN_HEIGHT:            
            this->data[Address.ADR_MIN_HEIGHT] = rxBuf[rx_end - 2] + rxBuf[rx_end -3]*256;
            this->data[Address.ADR_MAX_HEIGHT] = rxBuf[rx_end - 4] + rxBuf[rx_end -5]*256;
            
            
#ifdef CONSOLE
            printf("Min Height = %d, Max Height = %d\n",this->data[Address.ADR_MIN_HEIGHT],this->data[Address.ADR_MAX_HEIGHT]);
#endif
            break;
    }
}
void DeskManager::initControlTable(){
    data[Address.ADR_VERSION] = 0x03;
    data[Address.ADR_HEIGHT] = DEFAULT_HEIGHT;
    data[Address.ADR_UP] = 1;
    data[Address.ADR_DOWN] = 1;
    data[Address.ADR_STOP] = 1;
    data[Address.ADR_SAVE2POS1] = 1;
    data[Address.ADR_MOVE2POS1] = 1;
    data[Address.ADR_SAVE2POS2] = 1;
    data[Address.ADR_MOVE2POS2] = 1;
    data[Address.ADR_USER5] = DEFAULT_HEIGHT;
    data[Address.ADR_USER6] = DEFAULT_HEIGHT;
    data[Address.ADR_USER7] = DEFAULT_HEIGHT;
    data[Address.ADR_USER8] = DEFAULT_HEIGHT;
    data[Address.ADR_USER9] = DEFAULT_HEIGHT;
    data[Address.ADR_USER10] = DEFAULT_HEIGHT;
    data[Address.ADR_MIN_HEIGHT] = DESK_MIN_HEIGHT;
    data[Address.ADR_MAX_HEIGHT] = DESK_MAX_HEIGHT;
    data[Address.ADR_HEIGHT_SP] = DEFAULT_HEIGHT;
    data[Address.ADR_OPERATE_MODE] = Mode.MODE_MANUAL;
    data[Address.ADR_UID] = (unsigned short)UID;
    data[Address.ADR_BOX_STATUS] = 1;
    data[Address.ADR_DIR] = 0;

}
void DeskManager::addToLog(const char* p){
#if 0
    FILE* pFile = fopen("logFile.txt", "a");
    fprintf(pFile, "%s %s\n",__TIMESTAMP__,p);
    fclose(pFile);
#endif

}
void DeskManager::saveToPos1(){
    this->txBuf[0] = 0xF1;
    this->txBuf[1] = 0xF1;
    this->txBuf[2] = 0x03;
    this->txBuf[3] = 0x00;
    this->txBuf[4] = 0x03;
    this->txBuf[5] = 0x7E;
    this->txDataLength = 6;
}
void DeskManager::saveToPos2(){
    this->txBuf[0] = 0xF1;
    this->txBuf[1] = 0xF1;
    this->txBuf[2] = 0x04;
    this->txBuf[3] = 0x00;
    this->txBuf[4] = 0x04;
    this->txBuf[5] = 0x7E;
    this->txDataLength = 6;
}
void DeskManager::moveToPos1(){
    this->txBuf[0] = 0xF1;
    this->txBuf[1] = 0xF1;
    this->txBuf[2] = 0x05;
    this->txBuf[3] = 0x00;
    this->txBuf[4] = 0x05;
    this->txBuf[5] = 0x7E;
    this->txDataLength = 6;
}
void DeskManager::moveToPos2(){
    this->txBuf[0] = 0xF1;
    this->txBuf[1] = 0xF1;
    this->txBuf[2] = 0x06;
    this->txBuf[3] = 0x00;
    this->txBuf[4] = 0x06;
    this->txBuf[5] = 0x7E;
    this->txDataLength = 6;
}
unsigned short DeskManager::mm2in(unsigned short mm){
    return (unsigned short) (mm*0.3937);

}
unsigned short DeskManager::in2mm(unsigned short in){
    return (unsigned short) (in/0.3937);

}