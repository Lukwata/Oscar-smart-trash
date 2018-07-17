/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

/*
 * File:   testMyserialclass.hpp
 * Author: thanh
 *
 * Created on Jan 8, 2017, 11:43:05 PM
 */

#ifndef TESTMYSERIALCLASS_HPP
#define TESTMYSERIALCLASS_HPP

#include <cppunit/extensions/HelperMacros.h>

class testMyserialclass : public CPPUNIT_NS::TestFixture {
    CPPUNIT_TEST_SUITE(testMyserialclass);

    CPPUNIT_TEST(testInit);
    CPPUNIT_TEST(testWriteApi);
    CPPUNIT_TEST(testOpenApi);
    CPPUNIT_TEST(testCloseApi);
    CPPUNIT_TEST(testReadApi);

    CPPUNIT_TEST_SUITE_END();

public:
    testMyserialclass();
    virtual ~testMyserialclass();
    void setUp();
    void tearDown();

private:
    void testInit();
    void testWriteApi();
    void testOpenApi();
    void testCloseApi();
    void testReadApi();

};

#endif /* TESTMYSERIALCLASS_HPP */

