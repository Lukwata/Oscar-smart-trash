
#include"MyZMQ.hpp"
/*Context Class Implement*/
int Context::setup(){
    this->context = zmq_ctx_new();
    if (this -> context != NULL)
        return 0;
    else return -1;
    #ifdef DEBUG
        assert(this->context != NULL);
    #endif
}
int Context::shutdown(){
    int ctx_shutdown = zmq_ctx_shutdown(this->context);
    return ctx_shutdown;
    #ifdef DEBUG
        assert(ctx_shutdown == 0);
    #endif
}
int Context::terminate(){
    int ctx_term = zmq_ctx_term(this->context);
    #ifdef DEBUG
        assert(ctx_term == 0);
    #endif
    return ctx_term;
}
int Context::destroy(){
    int ctx_destroy = zmq_ctx_destroy(this->context);
    #ifdef  DEBUG   
        assert(ctx_destroy == 0);
    #endif
    return ctx_destroy;
}




/*Requester Class Implement*/
int Requester::setup(void* ctx){
    this->requester = zmq_socket(ctx,ZMQ_REQ);
    this->tTimeOut = TIME_OUT_VAL;
    return zmq_setsockopt(this->requester,ZMQ_RCVTIMEO,&this->tTimeOut,4);
}
int Requester::setEnpoint(const char* ep){
    this->endPoint = ep;
    return 0;
}
int Requester::connect(){
    return  zmq_connect(this->requester,this->endPoint);
}
int Requester::disconnect(){
    return zmq_disconnect(this->requester,this->endPoint);
}
int Requester::start() {
    return this->connect();
}
int Requester::stop(){
    this->disconnect();
    return zmq_close(this->requester);
}
int Requester::receiveOne(){
    try {
        int nlen = zmq_recv(this->requester,this->rxData,this->maxLen,0);
        if ((nlen > 0)&&(nlen <= this->maxLen )){
                this->rxLength = nlen;
            } 
            else {
                this->rxLength = 0;
            }
            return this->rxLength;
    }
    catch (const std::exception& e){
        std::cout << " a standard exception was caught, with message '"
                  << e.what() << "'\n";
    }
    
}
int Requester::receiveMore() {
    return zmq_recv(this->requester,this->rxData,this->maxLen,ZMQ_RCVMORE);
}
int Requester::sendOne() {
    return zmq_send(this->requester,this->txData,(size_t)this->txLength,0);
}
int Requester::sendMore(){
    return zmq_send(this->requester,this->txData,(size_t)this->txLength,ZMQ_SNDMORE);
}
int Requester::sendNull(){
    return zmq_send(this->requester,NULL,0,0);
}
int Requester::addTxData(unsigned char* p, unsigned char len){
    memcpy(this->txData,p,len);
    this->txLength = len;
    return len;
}
/*Replier Class Implement*/
int Replier::setup(void* ctx){
    this->replier = zmq_socket(ctx,ZMQ_REP);
    this->tTimeOut = TIME_OUT_VAL;
    return  zmq_setsockopt(this->replier,ZMQ_RCVTIMEO,&this->tTimeOut,4);
}
int Replier::setEnpoint(const char* ep){
    this->endPoint = ep;
    return 0;
}
int Replier::bind(){
    return zmq_bind(this->replier,this->endPoint);
}
int Replier::unBind(){
    return zmq_unbind(this->replier,this->endPoint);
}
int Replier::start() {
    return this->bind();
}
int Replier::stop() {
    int res = this->unBind();
    if (res == 0){
        return zmq_close(this->replier);
    }
    
}
int Replier::receiveOne(){
    try{
        int nlen = zmq_recv(this->replier,this->rxData,this->maxLen,0);
        #ifdef DEBUG
            assert(nlen >= 0);
        #endif  
            if ((nlen > 0)&&(nlen <= this->maxLen )){
                this->rxLength = nlen;
            } 
            else {
                this->rxLength = 0;
            }
            return this->rxLength;
    }
    catch (const std::exception& e){
        std::cout << " a standard exception was caught, with message '"
                  << e.what() << "'\n";
    }
    
}
int Replier::receiveMore(){
    int len = zmq_recv(this->replier,this->rxData,this->maxLen,ZMQ_RCVMORE);
    this->rxLength = len;
    return len;
}
int Replier::sendOne() {
    int nlen = zmq_send(this->replier,this->txData,(size_t)this->txLength,0);
    #ifdef DEBUG
        assert(nlen == this->txLength);
    #endif
    return nlen;
}
int Replier::sendMore(){
    int len = zmq_send(this->replier,this->txData,(size_t)this->txLength,ZMQ_SNDMORE);
    #ifdef DEBUG
        assert(len == this->txLength);
    #endif
        return len;
}
int Replier::sendNull() {
    int nlen = zmq_send(this->replier,NULL,0,0);
    #ifdef DEBUG
        assert(nlen == 0);
    #endif
        return nlen;
}
int Replier::addTxData(unsigned char* p, unsigned char len){
    memcpy(this->txData,p,len);
    this->txLength = len;
    return len;
}


/* MyZMQ Class Implement*/
int MyZmq::initZmq(){
    return mContext.setup();
}
int MyZmq::initReplier(const char *endpoint){
    this->mReplier.maxLen = MAX_RX_LENGTH;
    this->mReplier.setup(this->mContext.context);
    this->mReplier.setEnpoint(endpoint);
    return this->mReplier.start();
    
}
int MyZmq::initRequester(const char *endpoint){
    this->mRequester.maxLen = MAX_RX_LENGTH;
    this->mRequester.setup(this->mContext.context);
    this->mRequester.setEnpoint(endpoint);
    return this->mRequester.start();

}
int MyZmq::initDealer() {
    this->mDealer.maxLen = MAX_RX_LENGTH;
    return this->mDealer.setup(this->mContext.context);
}
int MyZmq::initRouter(){
    this->mRouter.maxLen = MAX_RX_LENGTH;
    return this->mRouter.setup(this->mContext.context);
}

int Dealer::setup(void* ctx){
    this->dealer = zmq_socket(ctx,ZMQ_DEALER);
    this->tTimeOut = TIME_OUT_VAL;
    #ifdef ENABLE_ZMQ_TIMEOUT 
        zmq_setsockopt(this->dealer,ZMQ_RCVTIMEO,&this->tTimeOut,4);
    #endif
}
int Dealer::connect(){
    int connect_fail = zmq_connect(this->dealer,this->endPoint);
    #ifdef DEBUG
        assert(connect_fail == 0);
    #endif
}
int Dealer::disconnect(){
    int disconnect_fail = zmq_disconnect(this->dealer,this->endPoint);
    #ifdef DEBUG
        assert(disconnect_fail == 0);
    #endif

}


int Router::setup(void* ctx){
   // this->router = zmq_socket(ctx,ZMQ_ROUTER);
    this->tTimeOut = TIME_OUT_VAL;
    #ifdef ENABLE_ZMQ_TIMEOUT 
        zmq_setsockopt(this->router,ZMQ_RCVTIMEO,&this->tTimeOut,4);
    #endif
        return 0;
}