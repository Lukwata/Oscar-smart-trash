/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

/*
 * File:   MySerial_testclass.cpp
 * Author: thanh
 *
 * Created on Feb 16, 2016, 7:20:27 PM
 */

#include "MySerial_testclass.hpp"
#include "MySerial.hpp"
#include <string.h>
#include <stdio.h>


CPPUNIT_TEST_SUITE_REGISTRATION(MySerial_testclass);

MySerial_testclass::MySerial_testclass() {
}

MySerial_testclass::~MySerial_testclass() {
}

void MySerial_testclass::setUp() {
}

void MySerial_testclass::tearDown() {
}

void MySerial_testclass::testInit() {
    /*
     int MySerial::init();
     
     * Requirement: file /dev/ttyAMA0 has permission read/write for pi user
     * Input: Null
     * Output: zeros if successful, otherwise it returns -1
     */
    MySeial mySeial;
    int result = mySeial.init();
    if (result < 0) {
        CPPUNIT_ASSERT(false);
    }
}

void MySerial_testclass::testWriteApi() {
    /*
     * int writeApi( void *buf, uint8_t n);
     */
    const  char* buf = "TestSerial";
    uint8_t n = strlen(buf);
    MySeial mySeial;
    mySeial.init();
    int result;
    printf("Send: TestSerial\n");
    result = mySeial.writeApi((char*)buf, n);
    
    if (result != strlen(buf)) {
        CPPUNIT_ASSERT(false);
    }
}

void MySerial_testclass::testOpenApi() {
    MySeial mySeial;
    mySeial.init();
    int result = mySeial.openApi();
    if (result == -1) {
        CPPUNIT_ASSERT(false);
    }
}

void MySerial_testclass::testCloseApi() {
    MySeial mySeial;
    mySeial.init();
    int result = mySeial.closeApi();
    if (result == -1) {
        CPPUNIT_ASSERT(false);
    }
}
void MySerial_testclass::testComm(){
    const  char* buf = "TestSerial";
    uint8_t n = strlen(buf);
    struct timespec tim,tim2;
    int nn;
    tim.tv_sec = 0;
    tim.tv_nsec = 3000000L;
    char c;
     MySeial mySeial;
    mySeial.init();
    int result;
    printf("Please press Up/Down button on keypad to finish Serial Test\n");
    result = mySeial.writeApi((char*)buf, n);
    
    if (result != strlen(buf)) {
        CPPUNIT_ASSERT(false);
    }
    result = 0;
    printf("Receive: ");
    uint32_t count,count1;
    while(1){
        //nanosleep(&tim , &tim2);
        nn = mySeial.readApi(&c);
        if(nn > 0){
            printf("%d",c);
            count++;
            if (count >= 10)
            break;
        }
    }

}