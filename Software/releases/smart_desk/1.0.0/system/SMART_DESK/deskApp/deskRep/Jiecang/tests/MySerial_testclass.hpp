/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

/*
 * File:   MySerial_testclass.hpp
 * Author: thanh
 *
 * Created on Feb 16, 2016, 7:20:24 PM
 */

#ifndef MYSERIAL_TESTCLASS_HPP
#define MYSERIAL_TESTCLASS_HPP

#include <cppunit/extensions/HelperMacros.h>

class MySerial_testclass : public CPPUNIT_NS::TestFixture {
    CPPUNIT_TEST_SUITE(MySerial_testclass);

    //CPPUNIT_TEST(testConfig);
    CPPUNIT_TEST(testInit);
    CPPUNIT_TEST(testOpenApi);
    CPPUNIT_TEST(testWriteApi);
    CPPUNIT_TEST(testComm);
    CPPUNIT_TEST(testCloseApi);

    CPPUNIT_TEST_SUITE_END();

public:
    MySerial_testclass();
    virtual ~MySerial_testclass();
    void setUp();
    void tearDown();

private:
    //void testConfig();
    void testInit();
    void testOpenApi();
    void testWriteApi();   
    void testCloseApi();
    void testComm();

};

#endif /* MYSERIAL_TESTCLASS_HPP */

