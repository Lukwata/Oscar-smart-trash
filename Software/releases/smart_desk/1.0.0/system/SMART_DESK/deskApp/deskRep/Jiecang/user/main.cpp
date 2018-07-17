/* 
 * File:   main.cpp
 * Author: thanh
 *
 * Created on September 8, 2015, 11:45 PM
 */
#include"main.hpp"
using namespace std;
DeskManager mDesk;
MySeial mSerial;
MyZmq mZmq;
int count_int;
volatile char USE_INCH = false;
const char *endPoint = "ipc:///tmp/desk_control:9999";
static unsigned int count,check, error_check;
static int e = 0;
pthread_t zmqThread,serialThread,deskThread;
int main(int argc, char *argv[]) {
    
    
    signal(SIGSEGV,signalHandler);
    signal(SIGKILL,signalHandler);
    signal(SIGTERM,signalHandler);
    signal(SIGINT,signalHandler);
    check = false;
    mZmq.initZmq();
    mZmq.initReplier(endPoint);
    pthread_create(&zmqThread,NULL,do_zmq_thread,NULL);
    mSerial.init();
    pthread_create(&serialThread,NULL,do_serial_thread,&mSerial); 
    mDesk.init();
    pthread_create(&deskThread, NULL, do_desk_thread,NULL);
    struct timespec tim,tim2;
    tim.tv_sec = 0;
    tim.tv_nsec = 1000000L;// 1ms
    printf("Process ID : %d\n", getpid());
    mDesk.data[Address.ADR_UID] = getpid();
   while(1){
#if 1 // Desk Controller
       nanosleep(&tim , &tim2);
        //if (currentMode == autoMode) -> auto move up or move down to get setpointHeight = currentHeight
       mDesk.data[Address.ADR_STATE] = mDesk.currentState;
       
        if(mDesk.data[Address.ADR_OPERATE_MODE] == Mode.MODE_AUTO){
            switch(mDesk.currentState){
                //Because of delaying of data returned from desk, error was calculated:
                case State.STATE_UP:
                    
                    e = mDesk.data[Address.ADR_HEIGHT_SP] - 
                            mDesk.data[Address.ADR_HEIGHT] - 4;
                    #ifdef CONSOLE
                        printf("xd = %d,x = %d,e = %d\n",mDesk.data[Address.ADR_HEIGHT_SP],mDesk.data[Address.ADR_HEIGHT],e);
                    #endif                 
                    break;
                case State.STATE_DOWN:
                    e = mDesk.data[Address.ADR_HEIGHT_SP] -
                            mDesk.data[Address.ADR_HEIGHT] + 4;
                    #ifdef CONSOLE
                        printf("xd = %d,x = %d,e = %d\n",mDesk.data[Address.ADR_HEIGHT_SP],mDesk.data[Address.ADR_HEIGHT],e);
                    #endif
                    break;
                    
                default:
                    
                    e = mDesk.data[Address.ADR_HEIGHT_SP] -
                            mDesk.data[Address.ADR_HEIGHT];
                    #ifdef CONSOLE
                        printf("xd = %d,x = %d,e = %d\n",mDesk.data[Address.ADR_HEIGHT_SP],mDesk.data[Address.ADR_HEIGHT],e);
                    #endif
                    break;     
                     
                    
                          
            }
            // error < 0 -> Xd < x ->  need to move down
            if(e <= -5){
                check = false;
                mDesk.setState(State.STATE_DOWN);
                mDesk.resetState(State.STATE_DOWN);
            
            }
            // error > 0 -> x < xd -> need to move up
            else if(e >= 5){
                check = false;
                mDesk.setState(State.STATE_UP);
                mDesk.resetState(State.STATE_UP);
            }
            /* when xd ~ x -> set check = true, set state to free state, mode = Manual mode
            then user can control by keypad, if not set to manuakMode, desk alway move desk up/down
            automatically*/
            else if(check == false){
                check = true; 
                mDesk.setState(State.STATE_STOP);
                mDesk.data[Address.ADR_OPERATE_MODE] = Mode.MODE_MANUAL;              
            }   
        }
#endif
       mDesk.data[Address.ADR_DIR] = (unsigned short)mDesk.data_changed;
   } 
    return 0;
}