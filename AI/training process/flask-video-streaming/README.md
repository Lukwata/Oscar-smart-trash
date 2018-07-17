flask-video-streaming
=====================

Supporting code for my article [video streaming with Flask](http://blog.miguelgrinberg.com/post/video-streaming-with-flask) and its follow-up [Flask Video Streaming Revisited](http://blog.miguelgrinberg.com/post/flask-video-streaming-revisited).

#install more libs to work
https://www.hackster.io/ruchir1674/video-streaming-on-flask-server-using-rpi-ef3d75

To install Uv4l on Raspbian Wheezy add the following line to the file /etc/apt/sources.list :
deb http://www.linux-projects.org/listing/uv4l_repo/raspbian/ jessie main

##=======

sudo apt-get update 
sudo apt-get install uv4l uv4l-raspicam 
sudo apt-get install uv4l-server uv4l-uvc uv4l-xscreen uv4l-mjpegstream uv4l-dummy uv4l-raspidisp 
