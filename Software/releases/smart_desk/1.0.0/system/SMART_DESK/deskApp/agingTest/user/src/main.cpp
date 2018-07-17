#include"MyZMQ.hpp"
#include "Device/AutonomousCommFrame.h"
#include <iostream>
#include <stddef.h>
#include <cstdlib>
#include <zmq.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <stdio.h>
#include <pthread.h>

#include <termios.h>
#include <fcntl.h>   /* File control definitions */
#include <errno.h>   /* Error number definitions */
#include <signal.h>
#include <unistd.h>    /* UNIX standard function definitions */
#include <assert.h>
#include<time.h>
#include <stdio.h>
#include <string.h>
//#define TEST
#define DEMO_1

/*
 * 
 */
MyZmq mZmq;
unsigned char tx[20],rx[20];
unsigned char len = 0;
int a;
unsigned short h,sum;
char s[20],str[20];
unsigned char b,c,addr;
void moveUp(); //
void moveDown(); //
void stopMove(); //
void saveToSit(); //
void moveToSit(); //
void saveToStand();//
void moveToStand();//
void getStatus(); //
void getHeight(); //
void getUID(); //
void getVersion(); //
void getMinHeight(); //
void getMaxHeight(); //
void getDir(); //
void getState(); //
void getHeigthSP(); //
void getMode();
void setHeight(uint16_t height);
void Reset();
void SpeakerOn();
void SpeakerOff();
void MicOn();
void MicOff();
int check = 0;
    time_t t;
int sleep_time = 45;
int main(int argc, char** argv) {
    
    printf("agrument = %d\n",argc);
    if (argc == 2){
        printf("param = %d\n",atoi(argv[1]));
        sleep_time = atoi(argv[1]);
    }
    mZmq.initZmq();
    mZmq.initRequester("ipc:///tmp/desk_control:9999");


    while(1){        
        // main function
#ifdef TEST
    int a = rand()%31;
    switch(a){
        case 0:
            moveUp();
            sleep(20);            
            break;
        case 1:
            getStatus();
            break;
        case 2:
            getMinHeight();
            break;
        case 3:
            getHeight();
            break;
        case 4:
            getDir();
            break;
        case 5:
            moveToStand();
            sleep(20);
            break;
        case 6:
            moveUp();
            sleep(20);
            break;
        case 7:
            break;
        case 8:
            moveDown();
            sleep(20);            
            break;
        case 9:
            setHeight(rand()%650);
            sleep(20);
            break;
        case 10:
            setHeight(rand()%650);
            sleep(20);
            break;
        case 11:
            moveUp();
            sleep(20);
            break;
        case 12:
            getUID();
            break;
        case 13:
            saveToSit();
            sleep(10);
            break;
        case 14:
            getVersion();
            break;
        case 15:
            moveDown();
            sleep(20);
            break;
        case 16:
            stopMove();
            break;
            
        case 17:
            setHeight(rand()%650);
            sleep(20); 
            break;
        case 18:
            moveToSit();
            sleep(20);
            break;
        case 19:
            moveToStand();
            sleep(20);
            break;
        case 20:
            getMaxHeight();
            break;
        case 21:
            moveDown();
            sleep(20);
            break;
        case 22:
            moveToSit();
            sleep(20);
            break;
            
        case 23:
            getState();
            break;
        case 24:
            saveToStand();
            sleep(20);;
            break;
        case 25:
            moveUp();
            sleep(10);
            break;
        case 26:
            stopMove();
            break;  
        case 27:
            Reset();
            sleep(60);
            break;
        case 28:
            SpeakerOn();
            break;
        case 29:
            SpeakerOff();
            break;
        case 30:
            MicOn();
            break;
        case 31:
            MicOff();
            break;
    }
    if(mZmq.mRequester.receiveOne() > 0){
            int x = mZmq.mRequester.rxData[mZmq.mRequester.rxLength-5]*256 + mZmq.mRequester.rxData[mZmq.mRequester.rxLength - 4];
            printf("%d\n",x);
    }
    sleep(5);
#endif
#ifdef DEMO_1
    check++;
    if(mZmq.mRequester.receiveOne() > 0){
        int x = mZmq.mRequester.rxData[mZmq.mRequester.rxLength-5]*256 + mZmq.mRequester.rxData[mZmq.mRequester.rxLength - 4];
        printf("%d\n",x);
}
    if (check == 1){
        moveDown();
    }
    else if (check == 2){
        moveUp();
        check = 0;
    }
    sleep(sleep_time);
    
#endif    
    
    }
    return 0;
}



void moveUp(){
    tx[0] = 0xFF; // Start Byte 1
    tx[1] = 0xFF; // Start Byte 2
    tx[2] = 0x02; // length
    tx[3] = ProductId.SmartDesk; //product id
    tx[4] = ComponentId.UpDownMotor; // component id
    tx[5] = Instructions.Write; // instruction
    tx[6] = ControlTableAddress.Up; // address
    tx[7] = 0x01; // param 1
    tx[8] = 0x01; // param 2
    tx[9] = 0x0F; // check sum
    tx[10] = 0xFA;// stop byte 1
    tx[11] = 0xFA;// stop byte 2
    len = 12;
    sum = tx[2]+tx[3]+tx[4]+tx[5]+tx[6]+tx[7]+tx[8];
    if(sum > 255) sum = sum%255;
    tx[9] = (unsigned char)sum;         
    mZmq.mRequester.addTxData(tx,len);
    mZmq.mRequester.sendOne();
    printf("Up-");
    time(&t);
    printf("%s\n",ctime(&t));

}
void moveDown(){
    tx[0] = 0xFF; // Start Byte 1
    tx[1] = 0xFF; // Start Byte 2
    tx[2] = 0x02; // length
    tx[3] = ProductId.SmartDesk; //product id
    tx[4] = ComponentId.UpDownMotor; // component id
    tx[5] = Instructions.Write; // instruction
    tx[6] = ControlTableAddress.Down; // address
    tx[7] = 0x01; // param 1
    tx[8] = 0x01; // param 2
    tx[9] = 0x0F; // check sum
    tx[10] = 0xFA;// stop byte 1
    tx[11] = 0xFA;// stop byte 2
    len = 12;
    sum = tx[2]+tx[3]+tx[4]+tx[5]+tx[6]+tx[7]+tx[8];
    if(sum > 255) sum = sum%255;
    tx[9] = (unsigned char)sum;         
    mZmq.mRequester.addTxData(tx,len);
    mZmq.mRequester.sendOne();
    printf("Down-");
    time(&t);
    printf("%s\n",ctime(&t));
}
void stopMove(){
    tx[0] = 0xFF; // Start Byte 1
    tx[1] = 0xFF; // Start Byte 2
    tx[2] = 0x02; // length
    tx[3] = ProductId.SmartDesk; //product id
    tx[4] = ComponentId.UpDownMotor; // component id
    tx[5] = Instructions.Write; // instruction
    tx[6] = ControlTableAddress.Stop; // address
    tx[7] = 0x01; // param 1
    tx[8] = 0x01; // param 2
    tx[9] = 0x0F; // check sum
    tx[10] = 0xFA;// stop byte 1
    tx[11] = 0xFA;// stop byte 2
    len = 12;
    sum = tx[2]+tx[3]+tx[4]+tx[5]+tx[6]+tx[7]+tx[8];
    if(sum > 255) sum = sum%255;
    tx[9] = (unsigned char)sum;
    mZmq.mRequester.addTxData(tx,len);
    printf("Set Desk Stop\n");  
    mZmq.mRequester.sendOne();
}
void getHeight(){
    tx[0] = 0xFF; // Start Byte 1
    tx[1] = 0xFF; // Start Byte 2
    tx[2] = 0x02; // length
    tx[3] = ProductId.SmartDesk; //product id
    tx[4] = ComponentId.UpDownMotor; // component id
    tx[5] = Instructions.Read; // instruction
    tx[6] = ControlTableAddress.Height; // address
    tx[7] = 0x01; // param 1
    tx[8] = 0x01; // param 2
    tx[9] = 0x0F; // check sum
    tx[10] = 0xFA;// stop byte 1
    tx[11] = 0xFA;// stop byte 2
    len = 12;
    sum = tx[2]+tx[3]+tx[4]+tx[5]+tx[6]+tx[7]+tx[8];
    if(sum > 255) sum = sum%255;
    tx[9] = (unsigned char)sum;
    mZmq.mRequester.addTxData(tx,len);
    printf("Get Height of Desk?-> ");
    mZmq.mRequester.sendOne();
}
void getUID(){
    tx[0] = 0xFF; // Start Byte 1
    tx[1] = 0xFF; // Start Byte 2
    tx[2] = 0x02; // length
    tx[3] = ProductId.SmartDesk; //product id
    tx[4] = ComponentId.UpDownMotor; // component id
    tx[5] = Instructions.Read; // instruction
    tx[6] = ControlTableAddress.UserID; // address
    tx[7] = 0x01; // param 1
    tx[8] = 0x01; // param 2
    tx[9] = 0x0F; // check sum
    tx[10] = 0xFA;// stop byte 1
    tx[11] = 0xFA;// stop byte 2
    len = 12;
    sum = tx[2]+tx[3]+tx[4]+tx[5]+tx[6]+tx[7]+tx[8];
    if(sum > 255) sum = sum%255;
    tx[9] = (unsigned char)sum;
    mZmq.mRequester.addTxData(tx,len);
    printf("Get UUID of Desk? -> ");
    mZmq.mRequester.sendOne();
}
void saveToSit(){
    tx[0] = 0xFF; // Start Byte 1
    tx[1] = 0xFF; // Start Byte 2
    tx[2] = 0x02; // length
    tx[3] = ProductId.SmartDesk; //product id
    tx[4] = ComponentId.UpDownMotor; // component id
    tx[5] = Instructions.Write; // instruction
    tx[6] = ControlTableAddress.SaveToPos1; // address
    tx[7] = 0x01; // param 1
    tx[8] = 0x01; // param 2
    tx[9] = 0x0F; // check sum
    tx[10] = 0xFA;// stop byte 1
    tx[11] = 0xFA;// stop byte 2
    len = 12;
    sum = tx[2]+tx[3]+tx[4]+tx[5]+tx[6]+tx[7]+tx[8];
    if(sum > 255) sum = sum%255;
    tx[9] = (unsigned char)sum;
    mZmq.mRequester.addTxData(tx,len);
    printf("Save Current Height To POS1\n");
    mZmq.mRequester.sendOne();
}
void moveToSit(){
    tx[0] = 0xFF; // Start Byte 1
    tx[1] = 0xFF; // Start Byte 2
    tx[2] = 0x02; // length
    tx[3] = ProductId.SmartDesk; //product id
    tx[4] = ComponentId.UpDownMotor; // component id
    tx[5] = Instructions.Write; // instruction
    tx[6] = ControlTableAddress.MoveToPos1; // address
    tx[7] = 0x01; // param 1
    tx[8] = 0x01; // param 2
    tx[9] = 0x0F; // check sum
    tx[10] = 0xFA;// stop byte 1
    tx[11] = 0xFA;// stop byte 2
    len = 12;
    sum = tx[2]+tx[3]+tx[4]+tx[5]+tx[6]+tx[7]+tx[8];
    if(sum > 255) sum = sum%255;
    tx[9] = (unsigned char)sum;
    mZmq.mRequester.addTxData(tx,len);
    printf("Move To POS1\n");
    mZmq.mRequester.sendOne();
}
void saveToStand(){
    tx[0] = 0xFF; // Start Byte 1
    tx[1] = 0xFF; // Start Byte 2
    tx[2] = 0x02; // length
    tx[3] = ProductId.SmartDesk; //product id
    tx[4] = ComponentId.UpDownMotor; // component id
    tx[5] = Instructions.Write; // instruction
    tx[6] = ControlTableAddress.SaveToPos2; // address
    tx[7] = 0x01; // param 1
    tx[8] = 0x01; // param 2
    tx[9] = 0x0F; // check sum
    tx[10] = 0xFA;// stop byte 1
    tx[11] = 0xFA;// stop byte 2
    len = 12;
    sum = tx[2]+tx[3]+tx[4]+tx[5]+tx[6]+tx[7]+tx[8];
    if(sum > 255) sum = sum%255;
    tx[9] = (unsigned char)sum;
    mZmq.mRequester.addTxData(tx,len);
    printf("Save Current Height To POS2\n");
    mZmq.mRequester.sendOne();
}
void moveToStand(){
    tx[0] = 0xFF; // Start Byte 1
    tx[1] = 0xFF; // Start Byte 2
    tx[2] = 0x02; // length
    tx[3] = ProductId.SmartDesk; //product id
    tx[4] = ComponentId.UpDownMotor; // component id
    tx[5] = Instructions.Write; // instruction
    tx[6] = ControlTableAddress.MoveToPos2; // address
    tx[7] = 0x01; // param 1
    tx[8] = 0x01; // param 2
    tx[9] = 0x0F; // check sum
    tx[10] = 0xFA;// stop byte 1
    tx[11] = 0xFA;// stop byte 2
    len = 12;
    sum = tx[2]+tx[3]+tx[4]+tx[5]+tx[6]+tx[7]+tx[8];
    if(sum > 255) sum = sum%255;
    tx[9] = (unsigned char)sum;
    mZmq.mRequester.addTxData(tx,len);
    printf("Move To POS2\n");
    mZmq.mRequester.sendOne();
}
void getStatus(){
    tx[0] = 0xFF; // Start Byte 1
    tx[1] = 0xFF; // Start Byte 2
    tx[2] = 0x02; // length
    tx[3] = ProductId.SmartDesk; //product id
    tx[4] = ComponentId.UpDownMotor; // component id
    tx[5] = Instructions.Read; // instruction
    tx[6] = ControlTableAddress.BoxStatus; // address
    tx[7] = 0x01; // param 1
    tx[8] = 0x01; // param 2
    tx[9] = 0x0F; // check sum
    tx[10] = 0xFA;// stop byte 1
    tx[11] = 0xFA;// stop byte 2
    len = 12;
    sum = tx[2]+tx[3]+tx[4]+tx[5]+tx[6]+tx[7]+tx[8];
    if(sum > 255) sum = sum%255;
    tx[9] = (unsigned char)sum;
    mZmq.mRequester.addTxData(tx,len);
    printf("Get Desk Status? -> ");
    mZmq.mRequester.sendOne();
}
void getVersion(){
    tx[0] = 0xFF; // Start Byte 1
    tx[1] = 0xFF; // Start Byte 2
    tx[2] = 0x02; // length
    tx[3] = ProductId.SmartDesk; //product id
    tx[4] = ComponentId.UpDownMotor; // component id
    tx[5] = Instructions.Read; // instruction
    tx[6] = ControlTableAddress.Version; // address
    tx[7] = 0x01; // param 1
    tx[8] = 0x01; // param 2
    tx[9] = 0x0F; // check sum
    tx[10] = 0xFA;// stop byte 1
    tx[11] = 0xFA;// stop byte 2
    len = 12;
    sum = tx[2]+tx[3]+tx[4]+tx[5]+tx[6]+tx[7]+tx[8];
    if(sum > 255) sum = sum%255;
    tx[9] = (unsigned char)sum;
    mZmq.mRequester.addTxData(tx,len);
    printf("Get Desk Version? -> ");
    mZmq.mRequester.sendOne();
}
void getMinHeight(){
    tx[0] = 0xFF; // Start Byte 1
    tx[1] = 0xFF; // Start Byte 2
    tx[2] = 0x02; // length
    tx[3] = ProductId.SmartDesk; //product id
    tx[4] = ComponentId.UpDownMotor; // component id
    tx[5] = Instructions.Read; // instruction
    tx[6] = ControlTableAddress.MinHeight; // address
    tx[7] = 0x01; // param 1
    tx[8] = 0x01; // param 2
    tx[9] = 0x0F; // check sum
    tx[10] = 0xFA;// stop byte 1
    tx[11] = 0xFA;// stop byte 2
    len = 12;
    sum = tx[2]+tx[3]+tx[4]+tx[5]+tx[6]+tx[7]+tx[8];
    if(sum > 255) sum = sum%255;
    tx[9] = (unsigned char)sum;
    mZmq.mRequester.addTxData(tx,len);
    printf("Get Min Height? -> ");
    mZmq.mRequester.sendOne();

}
void getMaxHeight(){
    tx[0] = 0xFF; // Start Byte 1
    tx[1] = 0xFF; // Start Byte 2
    tx[2] = 0x02; // length
    tx[3] = ProductId.SmartDesk; //product id
    tx[4] = ComponentId.UpDownMotor; // component id
    tx[5] = Instructions.Read; // instruction
    tx[6] = ControlTableAddress.MaxHeight; // address
    tx[7] = 0x01; // param 1
    tx[8] = 0x01; // param 2
    tx[9] = 0x0F; // check sum
    tx[10] = 0xFA;// stop byte 1
    tx[11] = 0xFA;// stop byte 2
    len = 12;
    sum = tx[2]+tx[3]+tx[4]+tx[5]+tx[6]+tx[7]+tx[8];
    if(sum > 255) sum = sum%255;
    tx[9] = (unsigned char)sum;
    mZmq.mRequester.addTxData(tx,len);
    printf("Get Max Height? -> ");
    mZmq.mRequester.sendOne();
}
void getDir(){
    tx[0] = 0xFF; // Start Byte 1
    tx[1] = 0xFF; // Start Byte 2
    tx[2] = 0x02; // length
    tx[3] = ProductId.SmartDesk; //product id
    tx[4] = ComponentId.UpDownMotor; // component id
    tx[5] = Instructions.Read; // instruction
    tx[6] = ControlTableAddress.MoveDirection; // address
    tx[7] = 0x01; // param 1
    tx[8] = 0x01; // param 2
    tx[9] = 0x0F; // check sum
    tx[10] = 0xFA;// stop byte 1
    tx[11] = 0xFA;// stop byte 2
    len = 12;
    sum = tx[2]+tx[3]+tx[4]+tx[5]+tx[6]+tx[7]+tx[8];
    if(sum > 255) sum = sum%255;
    tx[9] = (unsigned char)sum;
    mZmq.mRequester.addTxData(tx,len);
    printf("Get Direction? -> ");
    mZmq.mRequester.sendOne();
}
void getState(){
    tx[0] = 0xFF; // Start Byte 1
    tx[1] = 0xFF; // Start Byte 2
    tx[2] = 0x02; // length
    tx[3] = ProductId.SmartDesk; //product id
    tx[4] = ComponentId.UpDownMotor; // component id
    tx[5] = Instructions.Read; // instruction
    tx[6] = ControlTableAddress.ControllerState; // address
    tx[7] = 0x01; // param 1
    tx[8] = 0x01; // param 2
    tx[9] = 0x0F; // check sum
    tx[10] = 0xFA;// stop byte 1
    tx[11] = 0xFA;// stop byte 2
    len = 12;
    sum = tx[2]+tx[3]+tx[4]+tx[5]+tx[6]+tx[7]+tx[8];
    if(sum > 255) sum = sum%255;
    tx[9] = (unsigned char)sum;
    mZmq.mRequester.addTxData(tx,len);
    printf("Get State? -> ");
    mZmq.mRequester.sendOne();
}
void setHeight(uint16_t height){
    int a = rand()%650;
    uint8_t b,c;
    a += 600;
    b = (uint8_t)((a >> 8)&0x00ff);
    c = (uint8_t)(a&0x00ff);
    tx[0] = 0xFF;
    tx[1] = 0xFF;
    tx[2] = 0x02; //length
    tx[3] = 0x03; // Product
    tx[4] = 0x03; // Coponent
    tx[5] = 0x02; // Instruction
    tx[6] = ControlTableAddress.SetPointHeight; // Addr
    tx[7] = b; // data1
    tx[8] = c; // data2
    sum = 10;
    sum += tx[6];
    sum += (short)c+(short)b;
    if(sum > 255) sum =sum%255;
    tx[9] = (char)sum;
    tx[10] = 0xFA; 
    tx[11]= 0xFA;
    len = 12;
    printf("set Height: %d\n",a);
    mZmq.mRequester.addTxData(tx,len);
    mZmq.mRequester.sendOne();


}
void Reset(){
    tx[0] = 0xFF; // Start Byte 1
    tx[1] = 0xFF; // Start Byte 2
    tx[2] = 0x02; // length
    tx[3] = ProductId.SmartDesk; //product id
    tx[4] = ComponentId.UpDownMotor; // component id
    tx[5] = Instructions.Write; // instruction
    tx[6] = ControlTableAddress.Reset; // address
    tx[7] = 0x01; // param 1
    tx[8] = 0x01; // param 2
    tx[9] = 0x0F; // check sum
    tx[10] = 0xFA;// stop byte 1
    tx[11] = 0xFA;// stop byte 2
    len = 12;
    sum = tx[2]+tx[3]+tx[4]+tx[5]+tx[6]+tx[7]+tx[8];
    if(sum > 255) sum = sum%255;
    tx[9] = (unsigned char)sum;
    mZmq.mRequester.addTxData(tx,len);
    printf("Reset\n");
    mZmq.mRequester.sendOne();    

}

void SpeakerOn(){
    tx[0] = 0xFF; // Start Byte 1
    tx[1] = 0xFF; // Start Byte 2
    tx[2] = 0x02; // length
    tx[3] = ProductId.SmartDesk; //product id
    tx[4] = ComponentId.UpDownMotor; // component id
    tx[5] = Instructions.Write; // instruction
    tx[6] = ControlTableAddress.Speaker; // address
    tx[7] = 0x00; // param 1
    tx[8] = 0x01; // param 2
    tx[9] = 0x0F; // check sum
    tx[10] = 0xFA;// stop byte 1
    tx[11] = 0xFA;// stop byte 2
    len = 12;
    sum = tx[2]+tx[3]+tx[4]+tx[5]+tx[6]+tx[7]+tx[8];
    if(sum > 255) sum = sum%255;
    tx[9] = (unsigned char)sum;
    mZmq.mRequester.addTxData(tx,len);
    printf("Set Speaker on\n");
    mZmq.mRequester.sendOne();
}

void SpeakerOff(){
    tx[0] = 0xFF; // Start Byte 1
    tx[1] = 0xFF; // Start Byte 2
    tx[2] = 0x02; // length
    tx[3] = ProductId.SmartDesk; //product id
    tx[4] = ComponentId.UpDownMotor; // component id
    tx[5] = Instructions.Write; // instruction
    tx[6] = ControlTableAddress.Speaker; // address
    tx[7] = 0x00; // param 1
    tx[8] = 0x00; // param 2
    tx[9] = 0x0F; // check sum
    tx[10] = 0xFA;// stop byte 1
    tx[11] = 0xFA;// stop byte 2
    len = 12;
    sum = tx[2]+tx[3]+tx[4]+tx[5]+tx[6]+tx[7]+tx[8];
    if(sum > 255) sum = sum%255;
    tx[9] = (unsigned char)sum;
    mZmq.mRequester.addTxData(tx,len);
    printf("Set Speaker off\n");
    mZmq.mRequester.sendOne();
}

void MicOn(){
    tx[0] = 0xFF; // Start Byte 1
    tx[1] = 0xFF; // Start Byte 2
    tx[2] = 0x02; // length
    tx[3] = ProductId.SmartDesk; //product id
    tx[4] = ComponentId.UpDownMotor; // component id
    tx[5] = Instructions.Write; // instruction
    tx[6] = ControlTableAddress.Mic; // address
    tx[7] = 0x00; // param 1
    tx[8] = 0x01; // param 2
    tx[9] = 0x0F; // check sum
    tx[10] = 0xFA;// stop byte 1
    tx[11] = 0xFA;// stop byte 2
    len = 12;
    sum = tx[2]+tx[3]+tx[4]+tx[5]+tx[6]+tx[7]+tx[8];
    if(sum > 255) sum = sum%255;
    tx[9] = (unsigned char)sum;
    mZmq.mRequester.addTxData(tx,len);
    printf("Set Led Mic On\n ");
    mZmq.mRequester.sendOne();
}

void MicOff(){
        tx[0] = 0xFF; // Start Byte 1
    tx[1] = 0xFF; // Start Byte 2
    tx[2] = 0x02; // length
    tx[3] = ProductId.SmartDesk; //product id
    tx[4] = ComponentId.UpDownMotor; // component id
    tx[5] = Instructions.Write; // instruction
    tx[6] = ControlTableAddress.Mic; // address
    tx[7] = 0x00; // param 1
    tx[8] = 0x00; // param 2
    tx[9] = 0x0F; // check sum
    tx[10] = 0xFA;// stop byte 1
    tx[11] = 0xFA;// stop byte 2
    len = 12;
    sum = tx[2]+tx[3]+tx[4]+tx[5]+tx[6]+tx[7]+tx[8];
    if(sum > 255) sum = sum%255;
    tx[9] = (unsigned char)sum;
    mZmq.mRequester.addTxData(tx,len);
    printf("Set Led Mic Offn\n ");
    mZmq.mRequester.sendOne();
}