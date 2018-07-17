/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

/* 
 * File:   DeskCmd.hpp
 * Author: thanh
 *
 * Created on February 17, 2016, 11:18 PM
 */

#ifndef DESKCMD_HPP
#define DESKCMD_HPP
#include"Device/AutonomousCommFrame.h"
#include <iostream>
#include <cstdlib>
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <unistd.h>
#include <string.h>
#include <stdio.h>
#include <pthread.h>
#include <iostream>
#include <iostream>
#include <string.h>
#include "MyZMQ.hpp"
//static struct mAddress{
//    static const uint8_t ADR_VERSION = 0x01; //1
//    static const uint8_t ADR_HEIGHT = 0x02;  //2
//    static const uint8_t ADR_UP = 0x03;         //3
//    static const uint8_t ADR_DOWN = 0x04;
//    static const uint8_t ADR_STOP = 0x05;
//    static const uint8_t ADR_SAVE2POS1 = 0x06;
//    static const uint8_t ADR_MOVE2POS1 = 0x07;
//    static const uint8_t ADR_SAVE2POS2 = 0x08;
//    static const uint8_t ADR_MOVE2POS2 = 0x09;
//    static const uint8_t ADR_USER5 = 0x0A;
//    static const uint8_t ADR_USER6 = 0x0B;
//    static const uint8_t ADR_USER7 = 0x0C;
//    static const uint8_t ADR_USER8 = 0x0D;
//    static const uint8_t ADR_USER9 = 0x0E;
//    static const uint8_t ADR_USER10 = 0x0F;
//    static const uint8_t ADR_MIN_HEIGHT = 0x10;
//    static const uint8_t ADR_MAX_HEIGHT = 0x11;
//    static const uint8_t ADR_HEIGHT_SP = 0x12;
//    static const uint8_t ADR_OPERATE_MODE = 0x13;
//    static const uint8_t ADR_UID = 0x14;
//    static const uint8_t ADR_BOX_STATUS = 0x15;
//    static const uint8_t ADR_STATE = 0x16;
//    static const uint8_t ADR_DIR = 0x17;
//    /*
//     add address to control table
//     
//     */
//    
//    
//    static const uint8_t ADR_RAM_LENGTH = 0x18;
//    
//} Address;
class DeskCmd{
public:
  int moveUp();
  int moveDown();
  int stopMove();
  int saveToSit();
  int moveToSit();
  int saveToStand();
  int moveToStand();
  int getStatus();
  int getHeight();
  int getUID();
  int getVersion();
  int getMinHeight();
  int getMaxHeight();
  int getDir();
  int getState();
  int getHeigthSP();
  int getMode();
  int setHeight(uint16_t height);
  uint8_t rxData[30];
  uint8_t txData[30];
  uint8_t rxLen;
  uint8_t txLen;
  int init();
private:


};


#endif /* DESKCMD_HPP */

