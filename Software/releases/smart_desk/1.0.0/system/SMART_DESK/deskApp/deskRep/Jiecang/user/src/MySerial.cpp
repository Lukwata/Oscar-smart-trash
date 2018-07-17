#include"main.hpp"
//#include "MySerial_testclass.hpp"
#include<string.h>
#ifdef USE_RK3288
    #define SERIAL_DEVICE "/dev/ttyS1"
#endif
#define DEV1 "/dev/ttyAMA0"
#define DEV2 "/dev/ttyS1"
#define DEV3 "/dev/ttyUSB0"
int config (int fd);
int MySeial::init(){
    if(this->openApi(DEV1,B9600) >   -1){
        printf("-I- open %s ok\n",this->dev);
    }
    else  if(this->openApi(DEV2,B9600) >  -1){
    
        printf("-I- open %s ok\n",this->dev);
        
    } else if(this->openApi(DEV3,B9600) >  -1){
        
        printf("-I- open %s ok\n",this->dev);
    }
    assert(this->fd >= 0);
    return this->fd;
}
int MySeial::writeApi( void* buf,uint8_t n){
    try{
        return write(this->fd, buf,n);
    }
    catch (int e){
        return e;
    
    }   
}
int MySeial::openApi(const char *device,int baud){
    int res = open(device,O_RDWR | O_NOCTTY | O_NDELAY);
    int res1 = -1;
    if(res > 0){
        res1 = this->config(res, baud);
    } 
    if((res > -1)&&(res1 > -1)){
        this->fd = res;
        this->dev = device;
        return 0;
    }
    else {
        this -> fd = -1;
        this->dev = device;
        return -1;
    }
    
}
int MySeial::closeApi(){
    return  close(this->fd);  
}
int MySeial::readApi(void *data){
    return read(this ->fd,(char*)data,1);
}


// 
int MySeial::config(int fd, int baud){
    struct termios  config;
    // check the devices is a tty device?
    if (!isatty (fd))
       {
//            printf ("-E- %s not is a tty devices \r\n",this->dev);
            return -1;
       }
    // get the current port config
    if (tcgetattr (fd, &config) < 0)
       {
//            printf ("-E- cannot get current config \r\n");
            return -1;
       }
    config.c_iflag &= ~(IGNBRK | BRKINT | ICRNL | INLCR |PARMRK | INPCK | ISTRIP | IXON);
    config.c_oflag = 0;
    config.c_lflag &= ~(ECHO | ECHONL | ICANON | IEXTEN | ISIG);
    config.c_cflag &= ~(CSIZE | PARENB);
    config.c_cflag |= CS8;
    config.c_cc[VMIN]  = 1;
    config.c_cc[VTIME] = 0;
    // Set baud rate
    if (cfsetispeed (&config, baud) < 0 || cfsetospeed (&config, baud) < 0){
//        printf ("-E- %s cannot set baudrate \r\n",this->dev);
	return -1;
    } else {
//        printf("-I- %s baudrate set to 9600 \n",this->dev);
    }
    if (tcsetattr (fd, TCSAFLUSH, &config) < 0){
//	printf ("-E- %s config failed \r\n", this->dev);
        return -1;
    }
  
   // 
    return 0;
}
