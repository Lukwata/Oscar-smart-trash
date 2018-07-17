/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

/* 
 * File:   main.cpp
 * Author: thanh
 *
 * Created on January 13, 2017, 11:47 PM
 */

#include <cstdlib>
#include <iostream>
#include "SmartDesk/AddonBoardController.hpp"


using namespace std;

/*
 * 
 */
AddonBoardController mDesk;
string s;

int main(int argc, char** argv) {
    if(argc == 2){
        s = argv[1];
    }
    int major, minor, patch;
    zmq_version (&major, &minor, &patch); 
    printf ("Current ØMQ version is %d.%d.%d\n", major, minor, patch);
    struct timespec tim,tim2;
    tim.tv_sec = 0;
    tim.tv_nsec = 999999999L; // 999ms
    if(argc == 2){
        mDesk.Init("data.dat",s);
    }
    else
    {
        mDesk.Init("data.dat");
    }
    mDesk.Start();
    
    while(1){
      nanosleep(&tim , &tim2);
      
    }
    
    return 0;
}

