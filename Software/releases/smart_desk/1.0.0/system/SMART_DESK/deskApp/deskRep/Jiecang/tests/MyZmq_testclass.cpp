/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

/*
 * File:   MyZmq_testclass.cpp
 * Author: thanh
 *
 * Created on Feb 17, 2016, 7:40:40 AM
 */

#include "MyZmq_testclass.hpp"
#include "../MyZMQ.hpp"
#include<time.h>
#include <stdlib.h>

CPPUNIT_TEST_SUITE_REGISTRATION(MyZmq_testclass);

MyZmq_testclass::MyZmq_testclass() {
}

MyZmq_testclass::~MyZmq_testclass() {
}

void MyZmq_testclass::setUp() {
}

void MyZmq_testclass::tearDown() {
}

void MyZmq_testclass::testSetupContext() {
    Context context;
    int result = context.setup();
    if (result != 0) {
        CPPUNIT_ASSERT(false);
    }
}

void MyZmq_testclass::testShutdown() {
    Context context;
    int result = context.setup();
    if (result != 0) {
        CPPUNIT_ASSERT(false);
    }
    result = context.shutdown();
    if (result != 0) {
        CPPUNIT_ASSERT(false);
    }
}

void MyZmq_testclass::testTerminate() {
    Context context;
    int result = context.setup();
    if (result != 0) {
        CPPUNIT_ASSERT(false);
    }
    result = context.terminate();
    if (result != 0) {
        CPPUNIT_ASSERT(false);
    }
}

void MyZmq_testclass::testDestroy() {
    Context context;
    int result = context.setup();
    if (result != 0) {
        CPPUNIT_ASSERT(false);
    }
    result = context.destroy();
    if (result != 0) {
        CPPUNIT_ASSERT(false);
    }
}

void MyZmq_testclass::testSetupReplier() {
    Context context;
    if (context.setup() != 0) {
        CPPUNIT_ASSERT(false);
    }
    Replier replier;
    if (replier.setup(context.context) != 0) {
        CPPUNIT_ASSERT(false);
    }
}

void MyZmq_testclass::testSetEnpoint() {
    Context context;
    if (context.setup() != 0) {
        CPPUNIT_ASSERT(false);
    }
    Replier replier;
    if (replier.setup(context.context) != 0) {
        CPPUNIT_ASSERT(false);
    }
    const char* ep = "ipc:///tmp/desk_control:9999";
    if (replier.setEnpoint(ep) != 0) {
        CPPUNIT_ASSERT(false);
    }
}

void MyZmq_testclass::testStart() {
    Context context;
    if (context.setup() != 0) {
        CPPUNIT_ASSERT(false);
    }
    Replier replier;
    if (replier.setup(context.context) != 0) {
        CPPUNIT_ASSERT(false);
    }
    const char* ep = "ipc:///tmp/desk_control:9999";
    if (replier.setEnpoint(ep) != 0) {
        CPPUNIT_ASSERT(false);
    }
    if (replier.start() != 0) {
        CPPUNIT_ASSERT(false);
    }
}

void MyZmq_testclass::testStop() {
    Context context;
    if (context.setup() != 0) {
        CPPUNIT_ASSERT(false);
    }
    Replier replier;
    if (replier.setup(context.context) != 0) {
        CPPUNIT_ASSERT(false);
    }
    const char* ep = "ipc:///tmp/desk_control:9999";
    if (replier.setEnpoint(ep) != 0) {
        CPPUNIT_ASSERT(false);
    }
    if (replier.start() != 0) {
        CPPUNIT_ASSERT(false);
    }
    if (replier.stop() != 0) {
        CPPUNIT_ASSERT(false);
    }
}

void MyZmq_testclass::testReceiveOne() {
    Context context;
    if (context.setup() != 0) {
        CPPUNIT_ASSERT(false);
    }
    Replier replier;
    if (replier.setup(context.context) != 0) {
        CPPUNIT_ASSERT(false);
    }
    const char* ep = "ipc:///tmp/desk_control:9999";
    if (replier.setEnpoint(ep) != 0) {
        CPPUNIT_ASSERT(false);
    }
    if (replier.start() != 0) {
        CPPUNIT_ASSERT(false);
    }
    
}

void MyZmq_testclass::testReceiveMore() {
    Replier replier;
    int result = replier.receiveMore();
    if (true /*check result*/) {
        CPPUNIT_ASSERT(false);
    }
}

void MyZmq_testclass::testSendOne() {
    Replier replier;
    int result = replier.sendOne();
    if (true /*check result*/) {
        CPPUNIT_ASSERT(false);
    }
}

void MyZmq_testclass::testSendMore() {
    Replier replier;
    int result = replier.sendMore();
    if (true /*check result*/) {
        CPPUNIT_ASSERT(false);
    }
}

void MyZmq_testclass::testSendNull() {
    Replier replier;
    int result = replier.sendNull();
    if (true /*check result*/) {
        CPPUNIT_ASSERT(false);
    }
}

void MyZmq_testclass::testAddTxData() {
    unsigned char* p;
    unsigned char len;
    Replier replier;
    int result = replier.addTxData(p, len);
    if (true /*check result*/) {
        CPPUNIT_ASSERT(false);
    }
}

void MyZmq_testclass::testInitZmq() {
    MyZmq myZmq;
    if (myZmq.initZmq() != 0) {
        CPPUNIT_ASSERT(false);
    }
}

void MyZmq_testclass::testInitReplier() {
    MyZmq myZmq;
    if (myZmq.initZmq() != 0) {
        CPPUNIT_ASSERT(false);
    }
    if (myZmq.initReplier("ipc:///tmp/desk_control:9999") != 0) {
        CPPUNIT_ASSERT(false);
    }
}

void MyZmq_testclass::testInitRequester() {
    MyZmq myZmq;
    int result = myZmq.initRequester("ipc:///tmp/desk_control:9999");
    if (true /*check result*/) {
        CPPUNIT_ASSERT(false);
    }
}

void MyZmq_testclass::testInitDealer() {
    MyZmq myZmq;
    int result = myZmq.initDealer();
    if (true /*check result*/) {
        CPPUNIT_ASSERT(false);
    }
}

void MyZmq_testclass::testInitRouter() {
    MyZmq myZmq;
    int result = myZmq.initRouter();
    if (true /*check result*/) {
        CPPUNIT_ASSERT(false);
    }
}
void MyZmq_testclass::testZmqComm(){
    MyZmq mZmq;
    mZmq.initZmq();
    mZmq.initReplier("ipc:///tmp/desk_control:9999");
    struct timespec tim,tim2;
    tim.tv_sec = 0;
    tim.tv_nsec = 10000000L;
    printf("Please Send any data to ipc:///tmp/desk_control:9999 to finish Zmq test\n ");
    while(1){
        nanosleep(&tim , &tim2);
        //Reading data from ZMQ
        mZmq.mReplier.receiveOne(); // Lien tuc nhan data tu zmq
        
        if(mZmq.mReplier.rxLength > 0){ // Pre check packet
            for(int i = 0; i < mZmq.mReplier.rxLength;i++){
                    printf("%x ",(unsigned char)mZmq.mReplier.rxData[i]);
            }
            
            break;
            
        }
        
    }
}
