/* 
 * File:   MySerial.hpp
 * Author: thanh
 *
 * Created on September 15, 2015, 9:45 AM
 */

#ifndef MYSERIAL_HPP
#define	MYSERIAL_HPP
#include "Config.hpp"
#include<pthread.h>
#include<string.h>
#define TERMINATOR  1
#define BYTES 2

class MySeial{  
private:
    int config(int fd, int baud);
public:
    int fd;
    int init();
    int writeApi( void *buf, uint8_t n);
    int readApi(void *data);
    int openApi(const char *device, int baud);
    int closeApi();
    const char *dev;
    int (*callbackFcn)(void *);
    int setCallbackFcn(int (*fcn)(void *));
    const char * Port;
    uint16_t BaudRate;
    int8_t Terminator ;
    uint8_t Status;
    uint16_t ByteAvailable ;
    int (*BytesAvailableFcn)(void);
    uint16_t BytesAvailableFcnCount;
    uint8_t BytesAvailableFcnMode;
    uint16_t InputBufferSize;
    uint16_t OutputBufferSize;
    int (*OutputEmptyFc)(void);
    
};
#endif	/* MYSERIAL_HPP */

