/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

/*
 * File:   testMyserialclass.cpp
 * Author: thanh
 *
 * Created on Jan 8, 2017, 11:43:06 PM
 */

#include "testMyserialclass.hpp"
#include "MySerial.hpp"


CPPUNIT_TEST_SUITE_REGISTRATION(testMyserialclass);

testMyserialclass::testMyserialclass() {
}

testMyserialclass::~testMyserialclass() {
}

void testMyserialclass::setUp() {
}

void testMyserialclass::tearDown() {
}

void testMyserialclass::testInit() {
    MySeial mySeial;
    int result = mySeial.init();
    if (true /*check result*/) {
        CPPUNIT_ASSERT(false);
    }
}

void testMyserialclass::testWriteApi() {
    void* buf;
    uint8_t n;
    MySeial mySeial;
    int result = mySeial.writeApi(buf, n);
    if (true /*check result*/) {
        CPPUNIT_ASSERT(false);
    }
}

void testMyserialclass::testOpenApi() {
    const char* device;
    int baud;
    MySeial mySeial;
    int result = mySeial.openApi(device, baud);
    if (true /*check result*/) {
        CPPUNIT_ASSERT(false);
    }
}

void testMyserialclass::testCloseApi() {
    MySeial mySeial;
    int result = mySeial.closeApi();
    if (true /*check result*/) {
        CPPUNIT_ASSERT(false);
    }
}

void testMyserialclass::testReadApi() {
    void* data;
    MySeial mySeial;
    int result = mySeial.readApi(data);
    if (true /*check result*/) {
        CPPUNIT_ASSERT(false);
    }
}

