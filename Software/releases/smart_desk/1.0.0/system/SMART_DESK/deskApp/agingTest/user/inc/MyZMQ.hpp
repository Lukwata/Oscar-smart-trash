#ifndef MYZMQ_HPP
#define	MYZMQ_HPP
#include <zmq.h>
#include <iostream>
#include <string.h>
#define TIME_OUT_VAL 1000
#define     MAX_RX_LENGTH        120
#define     MAX_TX_LENGTH        20
class Context{
public:
    void *context;
    int setup();
    int setNumberOfThread(int value);
    int setMaxSocket(int value);
    int setIPv6(int value);
    int shutdown();
    int terminate();
    int destroy();

};
class Requester{
public:
    void *requester;
    int setup(void * ctx);
    int start();
    int stop();
    int sendMore();
    int sendOne();
    int sendNull();
    int receiveOne();
    int receiveMore();
    int setEnpoint(const char *ep);
    const char *endPoint;
    unsigned char rxData[30];
    unsigned char rxLength;
    unsigned char txData[30];
    unsigned char txLength;
    size_t maxLen;
    int tTimeOut;
    int addTxData(unsigned char *p, unsigned char len);
private:
    int connect();
    int disconnect();
    
};
class Replier{
public:
    void * replier;
    int setup(void * ctx);
    int start();
    int stop();
    int sendMore();
    int sendOne();
    int sendNull();
    int receiveOne();
    int receiveMore();
    int setEnpoint(const char *ep);
    const char *endPoint;
    char rxData[30];
    unsigned char rxLength;
    unsigned char txData[30];
    unsigned char txLength;
    size_t maxLen;
    int tTimeOut;
    int addTxData(unsigned char *p, unsigned char len);
private:
    int bind();
    int unBind();

};
class Dealer{
public:
    void *dealer;
    int setup(void * ctx);
    int startServer();
    int StartClient();
    int stopServer();
    int stopClient();
    int sendMore();
    int sendOne();
    int sendNull();
    int receiveOne();
    int receiveMore();
    int setEnpoint(const char *ep);
    const char *endPoint;
    unsigned char rxData[30];
    unsigned char rxLength;
    unsigned char txData[30];
    unsigned char txLength;
    size_t maxLen;
    int tTimeOut;
    int addTxData(unsigned char *p, unsigned char len);
private:
    int connect();
    int disconnect();
    int bind();
    int unBind();
};
class Router{
    public:
    int *router;
    int setup(void* ctx);
    int start();
    int stop();
    int sendMore();
    int sendOne();
    int sendNull();
    int receiveOne();
    int receiveMore();
    int setEnpoint(const char *ep);
    const char *endPoint;
    unsigned char rxData[30];
    unsigned char rxLength;
    unsigned char txData[30];
    unsigned char txLength;
    size_t maxLen;
    int tTimeOut;
    int addTxData(unsigned char *p, unsigned char len);
private:
    int connect();
    int disconnect();
    int bind();
    int unBind();
};
class MyZmq{
public:
    int initReplier(const char *endpoint);
    int initRequester(const char *endpoint);
    int initDealer();
    int initRouter();
    Requester mRequester;
    Replier mReplier;
    Dealer mDealer;
    Router mRouter;
    Context mContext;
    int initZmq();    
};
#endif
