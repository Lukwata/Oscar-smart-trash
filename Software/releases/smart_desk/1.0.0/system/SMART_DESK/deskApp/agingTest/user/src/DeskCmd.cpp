/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */


#include"DeskCmd.hpp"

int DeskCmd::init(){
    memset(this->rxData,0,sizeof(this->rxData));
    this->rxLen = 0;
    memset(this->txData,0,sizeof(this->txData));
    this->txLen = 0;
    return 0;
}
int DeskCmd::moveUp(){
    extern MyZmq mZmq;
    this->txData[0] = 0xFF; // Start Byte 1
    this->txData[1] = 0xFF; // Start Byte 2
    this->txData[2] = 0x02; // length
    this->txData[3] = 0x03; //product id
    this->txData[4] = 0x03; // component id
    this->txData[5] = 0x02; // instruction
    this->txData[6] = ControlTableAddress.Up; // address
    this->txData[7] = 0x01; // param 1
    this->txData[8] = 0x01; // param 2
    this->txData[9] = 0x0F; // check sum
    this->txData[10] = 0xFA;// stop byte 1
    this->txData[11] = 0xFA;// stop byte 2
    this->txLen = 12;
    mZmq.mRequester.addTxData(this->txData,this->txLen);
    printf("Set Desk Move Up\n");
    printf("Sending Data to Desk...\n");
    return mZmq.mRequester.sendOne();
}
int DeskCmd::moveDown(){
    extern MyZmq mZmq;
    this->txData[0] = 0xFF; // Start Byte 1
    this->txData[1] = 0xFF; // Start Byte 2
    this->txData[2] = 0x02; // length
    this->txData[3] = 0x03; //product id
    this->txData[4] = 0x03; // component id
    this->txData[5] = 0x02; // instruction
    this->txData[6] = ControlTableAddress.Down; // address
    this->txData[7] = 0x01; // param 1
    this->txData[8] = 0x01; // param 2
    this->txData[9] = 0x10; // check sum
    this->txData[10] = 0xFA;// stop byte 1
    this->txData[11] = 0xFA;// stop byte 2
    this->txLen = 12;
    mZmq.mRequester.addTxData(txData,txLen);
    printf("Set Desk Move Down\n");
    
    printf("Sending Data to Desk...\n");
    return mZmq.mRequester.sendOne();

}
int DeskCmd::stopMove(){
     extern MyZmq mZmq;
    txData[0] = 0xFF; // Start Byte 1
    txData[1] = 0xFF; // Start Byte 2
    txData[2] = 0x02; // length
    txData[3] = 0x03; //product id
    txData[4] = 0x03; // component id
    txData[5] = 0x02; // instruction
    txData[6] = ControlTableAddress.Stop; // address
    txData[7] = 0x01; // param 1
    txData[8] = 0x01; // param 2
    txData[9] = 0x11; // check sum
    txData[10] = 0xFA;// stop byte 1
    txData[11] = 0xFA;// stop byte 2
    txLen = 12;
    mZmq.mRequester.addTxData(txData,txLen);
    printf("Set Desk Stop\n");  
    
    printf("Sending Data to Desk...\n");
    return mZmq.mRequester.sendOne();
}