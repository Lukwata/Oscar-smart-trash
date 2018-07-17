/* 
 * File:   Thread.hpp
 * Author: thanh
 *
 * Created on September 17, 2015, 1:32 AM
 */

#ifndef THREAD_HPP
#define	THREAD_HPP
#include<zmq.h>
void *do_zmq_thread(void *data);
void *do_serial_thread(void *data);
void *do_desk_thread(void *data);
void serialHandler(int signum);
void signalHandler(int signum);
void catch_tstp(int signum);
#endif	/* THREAD_HPP */

