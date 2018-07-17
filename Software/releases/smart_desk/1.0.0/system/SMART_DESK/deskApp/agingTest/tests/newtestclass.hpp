/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

/*
 * File:   newtestclass.hpp
 * Author: thanh
 *
 * Created on Mar 10, 2016, 11:59:40 PM
 */

#ifndef NEWTESTCLASS_HPP
#define NEWTESTCLASS_HPP

#include <cppunit/extensions/HelperMacros.h>

class newtestclass : public CPPUNIT_NS::TestFixture {
    CPPUNIT_TEST_SUITE(newtestclass);

    CPPUNIT_TEST(testSetup);
    CPPUNIT_TEST(testSetEnpoint);
    CPPUNIT_TEST(testStart);
    CPPUNIT_TEST(testStop);
    CPPUNIT_TEST(testReceiveOne);
    CPPUNIT_TEST(testReceiveMore);
    CPPUNIT_TEST(testSendOne);
    CPPUNIT_TEST(testSendMore);
    CPPUNIT_TEST(testSendNull);
    CPPUNIT_TEST(testAddTxData);

    CPPUNIT_TEST_SUITE_END();

public:
    newtestclass();
    virtual ~newtestclass();
    void setUp();
    void tearDown();

private:
    void testSetup();
    void testSetEnpoint();
    void testStart();
    void testStop();
    void testReceiveOne();
    void testReceiveMore();
    void testSendOne();
    void testSendMore();
    void testSendNull();
    void testAddTxData();

};

#endif /* NEWTESTCLASS_HPP */

