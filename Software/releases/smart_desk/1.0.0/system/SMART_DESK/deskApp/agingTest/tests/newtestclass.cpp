/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

/*
 * File:   newtestclass.cpp
 * Author: thanh
 *
 * Created on Mar 10, 2016, 11:59:42 PM
 */

#include "newtestclass.hpp"


CPPUNIT_TEST_SUITE_REGISTRATION(newtestclass);

newtestclass::newtestclass() {
}

newtestclass::~newtestclass() {
}

void newtestclass::setUp() {
}

void newtestclass::tearDown() {
}

int Replier::setup(void* ctx);

void newtestclass::testSetup() {
    void* ctx;
    Replier replier;
    int result = replier.setup(ctx);
    if (true /*check result*/) {
        CPPUNIT_ASSERT(false);
    }
}

int Replier::setEnpoint(const char* ep);

void newtestclass::testSetEnpoint() {
    const char* ep;
    Replier replier;
    int result = replier.setEnpoint(ep);
    if (true /*check result*/) {
        CPPUNIT_ASSERT(false);
    }
}

int Replier::start();

void newtestclass::testStart() {
    Replier replier;
    int result = replier.start();
    if (true /*check result*/) {
        CPPUNIT_ASSERT(false);
    }
}

int Replier::stop();

void newtestclass::testStop() {
    Replier replier;
    int result = replier.stop();
    if (true /*check result*/) {
        CPPUNIT_ASSERT(false);
    }
}

int Replier::receiveOne();

void newtestclass::testReceiveOne() {
    Replier replier;
    int result = replier.receiveOne();
    if (true /*check result*/) {
        CPPUNIT_ASSERT(false);
    }
}

int Replier::receiveMore();

void newtestclass::testReceiveMore() {
    Replier replier;
    int result = replier.receiveMore();
    if (true /*check result*/) {
        CPPUNIT_ASSERT(false);
    }
}

int Replier::sendOne();

void newtestclass::testSendOne() {
    Replier replier;
    int result = replier.sendOne();
    if (true /*check result*/) {
        CPPUNIT_ASSERT(false);
    }
}

int Replier::sendMore();

void newtestclass::testSendMore() {
    Replier replier;
    int result = replier.sendMore();
    if (true /*check result*/) {
        CPPUNIT_ASSERT(false);
    }
}

int Replier::sendNull();

void newtestclass::testSendNull() {
    Replier replier;
    int result = replier.sendNull();
    if (true /*check result*/) {
        CPPUNIT_ASSERT(false);
    }
}

int Replier::addTxData(unsigned char* p, unsigned char len);

void newtestclass::testAddTxData() {
    unsigned char* p;
    unsigned char len;
    Replier replier;
    int result = replier.addTxData(p, len);
    if (true /*check result*/) {
        CPPUNIT_ASSERT(false);
    }
}

