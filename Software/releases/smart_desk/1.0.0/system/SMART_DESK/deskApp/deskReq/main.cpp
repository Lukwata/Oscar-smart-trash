/* 
 * File:   main.cpp
 * Author: thanh
 *
 * Created on September 29, 2015, 8:54 AM
 */
#include "SmartDesk/DeskRequester.hpp"
#include <iostream>
#include <stddef.h>
#include <cstdlib>
#include <zmq.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <stdio.h>
#include <pthread.h>

#include <termios.h>
#include <fcntl.h>   /* File control definitions */
#include <errno.h>   /* Error number definitions */
#include <signal.h>
#include <unistd.h>    /* UNIX standard function definitions */
#include <assert.h>
#include<time.h>
//#define TEST

/*
 * 
 */
DeskRequester mDesk;
int main(int argc, char** argv) {
    struct timespec tim,tim2;
    tim.tv_sec = 0;
    tim.tv_nsec = 100000000L; // 100ms
    int major, minor, patch;
    zmq_version (&major, &minor, &patch); 
    printf ("Current ØMQ version is %d.%d.%d\n", major, minor, patch);
    
    while(1){        
        nanosleep(&tim , &tim2);
        mDesk.Run();

    }
    return 0;
}
