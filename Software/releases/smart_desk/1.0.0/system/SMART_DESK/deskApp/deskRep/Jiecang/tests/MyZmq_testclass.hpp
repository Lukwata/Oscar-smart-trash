/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

/*
 * File:   MyZmq_testclass.hpp
 * Author: thanh
 *
 * Created on Feb 17, 2016, 7:40:40 AM
 */

#ifndef MYZMQ_TESTCLASS_HPP
#define MYZMQ_TESTCLASS_HPP

#include <cppunit/extensions/HelperMacros.h>
#include <iostream>
#include <cstdlib>
#include <zmq.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <stdio.h>
#include <pthread.h>

class MyZmq_testclass : public CPPUNIT_NS::TestFixture {
    CPPUNIT_TEST_SUITE(MyZmq_testclass);

    CPPUNIT_TEST(testSetupContext);
    CPPUNIT_TEST(testShutdown);
    CPPUNIT_TEST(testTerminate);
    CPPUNIT_TEST(testDestroy);
    CPPUNIT_TEST(testSetupReplier);
    CPPUNIT_TEST(testSetEnpoint);
    CPPUNIT_TEST(testStart);
    CPPUNIT_TEST(testStop);
    CPPUNIT_TEST(testReceiveOne);
//    CPPUNIT_TEST(testReceiveMore);
//    CPPUNIT_TEST(testSendOne);
//    CPPUNIT_TEST(testSendMore);
//    CPPUNIT_TEST(testSendNull);
//    CPPUNIT_TEST(testAddTxData);
    CPPUNIT_TEST(testInitZmq);
    CPPUNIT_TEST(testInitReplier);
//    CPPUNIT_TEST(testInitRequester);
//    CPPUNIT_TEST(testInitDealer);
//    CPPUNIT_TEST(testInitRouter);
    CPPUNIT_TEST(testZmqComm);

    CPPUNIT_TEST_SUITE_END();

public:
    MyZmq_testclass();
    virtual ~MyZmq_testclass();
    void setUp();
    void tearDown();

private:
    void testSetupContext();
    void testShutdown();
    void testTerminate();
    void testDestroy();
    void testSetupReplier();
    void testSetEnpoint();
    void testStart();
    void testStop();
    void testReceiveOne();
    void testReceiveMore();
    void testSendOne();
    void testSendMore();
    void testSendNull();
    void testAddTxData();
    void testInitZmq();
    void testInitReplier();
    void testInitRequester();
    void testInitDealer();
    void testInitRouter();
    void testZmqComm();

};

#endif /* MYZMQ_TESTCLASS_HPP */

