#include"main.hpp"
#include<string.h>
void serialHandler(int signum,siginfo_t *ioinfo, void * context){
    extern MySeial mSerial;
    extern DeskManager mDesk;
    char c;
    #ifdef ENABLE_SERIAL_EVENT
        if(ioinfo->si_code == 1){
            int n = read(mSerial.fd,&c,1);
            #ifdef DEBUG
                assert(n == 1);
            #endif
                if(n > 0) mDesk.addDataRxBuf(c);
        }
    #endif
}
void *do_zmq_thread(void *data){
    /*
     Nhan packet command Up/Down/Get Height/Set Height tu client
     
     */
    extern MyZmq mZmq;
    extern DeskManager mDesk;
    struct timespec tim,tim2;
    tim.tv_sec = 0;
    tim.tv_nsec = 10000000L;//10ms
#if 1
    while(1){
        nanosleep(&tim , &tim2);
        //Reading data from ZMQ
        mZmq.mReplier.receiveOne(); // Lien tuc nhan data tu zmq
        
        if(mZmq.mReplier.rxLength > 10){ // Pre check packet
            mDesk.Comm.addData(mZmq.mReplier.rxData,mZmq.mReplier.rxLength); // add zmq data vao buffer
            if(mDesk.Comm.isChecksumOk()){ 
                /*Get information*/       
                mDesk.Comm.getAction(); // get command from packet
                mZmq.mReplier.addTxData(mDesk.Comm.txBuf,mDesk.Comm.txLength);
                mZmq.mReplier.sendOne();
            
            }else{
                mZmq.mReplier.sendNull();
            }
        }
        else{
            mZmq.mReplier.sendNull();
        }
            
    }
#endif  
}
void *do_serial_thread(void *data){
    /*
     This thread handles:
        - Receice data from serial port, add to buffer and check if  packet are received?
        - Valid packet : check checksum, get start/stop byte index.
        - Get information from packet and update to control table: get function/data
     *      + function: 0x01: Current Height, 0x02: Error Code, 0x04: Reset Mode,
     *          0x07: Max and min height
            + data[RAM_HEIGHT_IND]: was set when receive height function
     *      + data[RAM_OPERATE_MODE_IND]: 
     *      + DeskManager.state
     5
     * 
     
     */
    
    extern DeskManager mDesk;
    extern MySeial mSerial;
    // Register Serial Handle
    // signal(SIGIO, serialHandler);
    /* allow the process to receive SIGIO */
    //fcntl (mSerial.fd, F_SETOWN, getpid());
    /* Make the file descriptor asynchronous (the manual page says only
        O_APPEND and O_NONBLOCK, will work with F_SETFL...) */
    //fcntl (mSerial.fd, F_SETFL, fcntl(mSerial.fd, F_GETFL) | FASYNC);
    //fcntl(mSerial.fd, F_SETSIG,SIGIO);
    //struct sigaction act;
    //sigemptyset(&act.sa_mask);
    //act.sa_flags = act.sa_flags|SA_SIGINFO;
    //act.sa_sigaction = serialHandler;
    //act.sa_restorer = NULL;
    //sigaction(SIGIO,&act,NULL);
    struct timespec tim,tim2;
    tim.tv_sec = 0;
    tim.tv_nsec = 3000000L;//3ms
    char c;
    while(1){
        nanosleep(&tim , &tim2);
        #ifndef ENABLE_SERIAL_EVENT
            int n = mSerial.readApi(&c);
            if(n > 0){
            #ifdef EN_SER_LOG
                printf("Received data from control box , data = %x\n",(unsigned char)c);
            #endif
                mDesk.addDataRxBuf(c);
                // Neu Co nhan duoc data tu control box thi update wire connected
                if (mDesk.data[Address.ADR_BOX_STATUS] == 1){
                
                    mDesk.data[Address.ADR_BOX_STATUS] = 2;
                }
                
            }
        #endif
        
        if((mDesk.rx_data_updated)&&(mDesk.rx_end - mDesk.rx_begin > 4)){
            // Default enable checksum packet from control box, if the number of 
            // checksum fail > 4 then disable checksum.
            if(mDesk.en_checksum == true){
            
                if (mDesk.isCheckSumOK() == false){
                    mDesk.num_checksum_fail++;
                    printf("-I- Checksum Error detected:%d\n",10 -mDesk.num_checksum_fail );
                    if(mDesk.num_checksum_fail >= 10){
                        printf("-I- Checksum Disabled\n");
                        mDesk.en_checksum = false;
                    }
                
                }
                else{
                    mDesk.getDeskAction();
                }
            }
            else{
                mDesk.getDeskAction();
            }
            
            mDesk.rx_data_updated = false;
        }
    }
    
}
void *do_desk_thread(void *data){
    extern DeskManager mDesk;
    extern MySeial mSerial;
    extern MyZmq mZmq;
    extern volatile char USE_INCH;
    static unsigned char count = 0;
    struct timespec tim,tim2;
    bool stand_sit_flag = false;
    tim.tv_sec = 0;
    tim.tv_nsec = 400000000L;
    while(1){
        nanosleep(&tim , &tim2);
        switch (mDesk.currentState){            
            case State.STATE_UP:
                /*
                 STATE_UP  works  in  manual mode and auto mode
                 * In manual mode, user can send command up, down, stop from phone, can use buttons on keypad.
                 * In auto mode, it was called when user call Set Height command, during set_height process, user can stop desk,
                 * but cannot user button up/down on keypad.                
                 */
                #ifdef EN_DESK_LOG
                    if (mDesk.preState != mDesk.currentState){
                        printf("Mode: Up, Height: %d \r\n",mDesk.data[Address.ADR_HEIGHT]);
                        mDesk.setState(mDesk.currentState);
                    }
                #endif
                // Prepare packet data to send to Control-Box
                mDesk.moveUp();
                // Send Packet data to control box
                mSerial.writeApi(mDesk.txBuf, mDesk.txDataLength);
                //Check if the board has stucked in STATE_UP for a long time, then change state to STATE_STOP
                mDesk.up_state_count++;
                if(mDesk.up_state_count >= mDesk.max_state_count){
                    mDesk.setState(State.STATE_STOP);
                    mDesk.resetState(State.STATE_UP);
                    mDesk.data[Address.ADR_OPERATE_MODE] = Mode.MODE_MANUAL;
                }
                //Check  if Move Up process reach the maximum height of desk then change state to STATE_STOP.
                unsigned short tem1;
                tem1 = mDesk.data[Address.ADR_HEIGHT];
                if (USE_INCH == true){
                    tem1 = mDesk.in2mm(tem1);
                }          
                if(tem1 >= mDesk.data[Address.ADR_MAX_HEIGHT] - 5){
                    mDesk.setState(State.STATE_STOP);
                    mDesk.resetState(State.STATE_UP);
                    mDesk.data[Address.ADR_OPERATE_MODE] = Mode.MODE_MANUAL;  
                }
                // check if desk moves down when in STATE_UP
                if ((mDesk.up_state_count > 5) && (mDesk.direction < 0)){
                    mDesk.setState(State.STATE_STOP);   
                    mDesk.resetState(State.STATE_UP);
                    mDesk.data[Address.ADR_OPERATE_MODE] = Mode.MODE_MANUAL;
                    mDesk.direction = 0;
                }
                break;
            case State.STATE_DOWN:
                /*
                 STATE_DOWN  works  in  manual mode and auto mode
                 * In manual mode, user can send command up, down, stop from phone, can use buttons on keypad.
                 * In auto mode, it was called when user call Set Height command, during set_height process, user can stop desk,
                 * but cannot user button up/down on keypad.                
                 */
                #ifdef EN_DESK_LOG
                    if (mDesk.preState != mDesk.currentState){
                        //system("clear");
                        printf("Mode: Down, Height: %d \r\n",mDesk.data[Address.ADR_HEIGHT]);
                        mDesk.setState(mDesk.currentState);
                    }
                #endif
                // Prepare packet data to send to Control-Box    
                mDesk.moveDown();
                // Send Packet data to control box
                mSerial.writeApi(mDesk.txBuf, mDesk.txDataLength);
                //Check if the board has stucked in STATE_DOWN for a long time, then change state to STATE_STOP
                mDesk.down_state_count++;
                if(mDesk.down_state_count >= mDesk.max_state_count){
                    mDesk.setState(State.STATE_STOP);
                    mDesk.resetState(State.STATE_DOWN);
                    mDesk.data[Address.ADR_OPERATE_MODE] = Mode.MODE_MANUAL;
                }
                //Check  if Move Down process reach the minimum height of desk then change state to STATE_STOP.
                unsigned short tem;
                tem = mDesk.data[Address.ADR_HEIGHT];
                if (USE_INCH == true){
                    tem = mDesk.in2mm(tem);
                }
                if(tem <= mDesk.data[Address.ADR_MIN_HEIGHT] + 5){
                    mDesk.setState(State.STATE_STOP);
                    mDesk.resetState(State.STATE_UP);
                    mDesk.data[Address.ADR_OPERATE_MODE] = Mode.MODE_MANUAL;  
                    printf("dir = %d\n",mDesk.direction);
                }
                // check if desk moves up when in STATE_DOWN
                if ((mDesk.down_state_count > 5) && (mDesk.direction > 0)){
                    mDesk.setState(State.STATE_STOP);   
                    mDesk.resetState(State.STATE_UP);
                    mDesk.data[Address.ADR_OPERATE_MODE] = Mode.MODE_MANUAL;
                    mDesk.direction = 0;
                }
                break;
            case State.STATE_STOP:
                #ifdef EN_DESK_LOG
                    if (mDesk.preState != mDesk.currentState){
                        //system("clear");
                        printf("Mode: Stop, Height: %d\n",mDesk.data[Address.ADR_HEIGHT]);
                    }
                #endif
                //Can only stop desk by this command if previous state is: STATE_MOVE2POS1, STATE_MOVE2POS2
                if (stand_sit_flag == true){
                    printf("-I- Force Stop Desk\n");
                    mDesk.moveUp();
                    mSerial.writeApi(mDesk.txBuf, mDesk.txDataLength);    
                    stand_sit_flag = false;
                }
                //Stop desk if previous state is: STATE_UP or STATE_DOWN
                mDesk.stopMove();
                mSerial.writeApi(mDesk.txBuf, mDesk.txDataLength);  
                mDesk.stopMove();
                mSerial.writeApi(mDesk.txBuf, mDesk.txDataLength);
                // Reset all state count
                mDesk.resetState(State.STATE_ALL);
                // Set to Free Mode                             
                mDesk.setState(State.STATE_FREE);               
                break;
            case State.STATE_FREE:
                /*
                 There are two options for this mode
                 *  1. sending ping packet continously to control-box to update the status. so keypad light is always on.
                 *  2. sending ping packet for n times. then doing nothing.                           
                 */
                mDesk.free_state_count++;
                #ifdef EN_CONT_PING
                if(mDesk.free_state_count >= 5){
                    mDesk.data[Address.ADR_OPERATE_MODE] = Mode.MODE_MANUAL;
                    // Wake up the control box if it is sleeping
                    mDesk.getDeskStatus();
                    mSerial.writeApi(mDesk.txBuf, mDesk.txDataLength);
                    // Get min max height
                    mDesk.getDeskMinMax();
                    mSerial.writeApi(mDesk.txBuf,mDesk.txDataLength);
                    mDesk.resetState(State.STATE_FREE);
                    #ifdef EN_DESK_LOG
                        printf("Mode: Free, Height: %d \r\n",mDesk.data[Address.ADR_HEIGHT]);
                    #endif
                }                                       
                #endif
                #ifndef EN_CONT_PING
                if(mDesk.free_state_count++ < 3){                                        
                    mDesk.data[Address.ADR_OPERATE_MODE] = Mode.MODE_MANUAL;  
                    // Wake up the control box if it is sleeping
                    mDesk.getDeskStatus();
                    mSerial.writeApi(mDesk.txBuf, mDesk.txDataLength);
                    // Get min max height
                    mDesk.getDeskMinMax();
                    mSerial.writeApi(mDesk.txBuf,mDesk.txDataLength);                    
                    #ifdef EN_DESK_LOG
                        printf("Mode: Free, Height: %d \r\n",mDesk.data[Address.ADR_HEIGHT]);
                    #endif  
                    //ff ff 2 3 3 3 16 0 3 24 fa fa         
                }
                else mDesk.free_state_count = 2;                                              
                #endif
                break;
            case State.STATE_ERROR:
                /*
                 This state 
                 
                 */
                #ifdef EN_DESK_LOG
                    if (mDesk.preState != mDesk.currentState){
                        //system("clear");
                        printf("Mode: Error, Height: %d \r\n",mDesk.data[Address.ADR_HEIGHT]);
                        mDesk.setState(mDesk.currentState);
                    }
                #endif
                mDesk.error_state_count++;
                if(mDesk.error_state_count >= 20){
                    mDesk.error_state_count = 0;
                    mDesk.resetState(State.STATE_FREE);
                    mDesk.setState(State.STATE_FREE);
                }
                if(mDesk.error_state_count < 2){
                    mDesk.getDeskStatus();
                    mSerial.writeApi(mDesk.txBuf, mDesk.txDataLength);
                }
                else{
                    mDesk.moveDown();
                    mSerial.writeApi(mDesk.txBuf, mDesk.txDataLength);
                }
                break;
            case State.STATE_RESET:
                
                #ifdef EN_DESK_LOG
                    if (mDesk.preState != mDesk.currentState){
                        //system("clear");
                        printf("-I- Reset State\r\n");
                        mDesk.setState(mDesk.currentState);
                    }
                #endif
                mDesk.reset_state_count++;
                if(mDesk.reset_state_count >= 20){
                    mDesk.reset_state_count = 0;
                    mDesk.resetState(State.STATE_FREE);
                    mDesk.setState(State.STATE_FREE);
                }
                if(mDesk.reset_state_count < 2){
                    mDesk.getDeskStatus();
                    mSerial.writeApi(mDesk.txBuf, mDesk.txDataLength);
                }
                else{
                    mDesk.moveDown();
                    mSerial.writeApi(mDesk.txBuf, mDesk.txDataLength);
                }
                break;
            case State.STATE_SAVE2POS1:
                mDesk.getDeskStatus();
                mSerial.writeApi(mDesk.txBuf, mDesk.txDataLength);
                usleep(100000);
                mDesk.saveToPos1();
                mSerial.writeApi(mDesk.txBuf,mDesk.txDataLength);
                mDesk.setState(State.STATE_FREE);
                #ifdef EN_DESK_LOG
                    //system("clear");
                    printf("Saved current Height to Sit Position\n");
                #endif
                break;
            case State.STATE_MOVE2POS1:       
                mDesk.move2pos1_state_count++;  
                if (mDesk.move2pos1_state_count < 2 ){
                    mDesk.getDeskStatus();
                    mSerial.writeApi(mDesk.txBuf, mDesk.txDataLength);
                    usleep(100000);
                    mDesk.moveToPos1();
                    mSerial.writeApi(mDesk.txBuf,mDesk.txDataLength);
                    usleep(100000);
                    mDesk.moveToPos1();
                    mSerial.writeApi(mDesk.txBuf,mDesk.txDataLength);
                    stand_sit_flag = true;
                    #ifdef EN_DESK_LOG
                        //system("clear");
                        printf("Moving to Sit Position\n");
                    #endif
                
                }    
                if(mDesk.move2pos1_state_count >= 10){
                    //printf("c = %d\n",mDesk.move2pos1_state_count);
                    if(mDesk.direction == 0){
                        stand_sit_flag = false;
                        mDesk.setState(State.STATE_STOP); 
                    
                    }
                }
                if(mDesk.move2pos1_state_count >= mDesk.max_state_count){
                    stand_sit_flag = false;
                    mDesk.setState(State.STATE_STOP);
                }  
                                                    
                break;
            case State.STATE_SAVE2POS2:
                mDesk.getDeskStatus();
                mSerial.writeApi(mDesk.txBuf, mDesk.txDataLength);
                usleep(100000);
                mDesk.saveToPos2();
                mSerial.writeApi(mDesk.txBuf,mDesk.txDataLength);
                mDesk.setState(State.STATE_FREE);
                #ifdef EN_DESK_LOG
                    //system("clear");
                    printf("Saved current Height to Sit Position\n");
                #endif
                break;
                
                
            case State.STATE_MOVE2POS2:
                mDesk.move2pos2_state_count++;  
                if (mDesk.move2pos2_state_count < 2 ){
                    mDesk.getDeskStatus();
                    mSerial.writeApi(mDesk.txBuf, mDesk.txDataLength);
                    usleep(100000);
                    mDesk.moveToPos2();
                    mSerial.writeApi(mDesk.txBuf,mDesk.txDataLength);   
                    usleep(100000);
                    mDesk.moveToPos2();
                    mSerial.writeApi(mDesk.txBuf,mDesk.txDataLength); 
                    stand_sit_flag = true;
                    #ifdef EN_DESK_LOG
                        //system("clear");
                        printf("Moving to Stand Position\n");
                    #endif
                
                }    
                if(mDesk.move2pos2_state_count >= 10){
                    //printf("c = %d\n",mDesk.move2pos1_state_count);
                    if(mDesk.direction == 0){
                        stand_sit_flag = false;
                        mDesk.setState(State.STATE_STOP); 
                    
                    }
                }
                if(mDesk.move2pos2_state_count >= mDesk.max_state_count){
                    stand_sit_flag = false;
                    mDesk.setState(State.STATE_STOP);
                }
                
                break;
            case State.STATE_GET_DATA:
                mDesk.setState(State.STATE_FREE);
                break;
        }  
    }
}
void signalHandler(int signum){
    extern MySeial mSerial;
    extern MyZmq mZmq;
    extern int count_int;
    if(signum == SIGSEGV){
        printf("Segmentation violation detected\n");
        system("sudo reboot");
        exit(0);
    }
    if(signum == SIGTERM){
        mSerial.closeApi();
        printf("%s closed\n",mSerial.dev);
        mZmq.mReplier.stop();
        signal(SIGTERM, SIG_DFL);
    }
    if(signum == SIGINT){
        printf("\nAre you sure to quit? Press Ctrl+C to quit!\n");
        signal(SIGINT,SIG_DFL);
    }
}
void catch_tstp(int signum){
    signal(SIGTSTP,catch_tstp);
    printf("He He, Khong De gi pause duoc tao dau!\n");
}

