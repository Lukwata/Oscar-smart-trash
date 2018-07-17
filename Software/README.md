#Build the aos system
1. Use aos/ for all autonomous device
2. Build brain: `go build -tags netgo`
3. Copy "brain" execute to `aos/system/<device_type>/`


#How to config OS
go to [.bashrc](https://github.com/duyhtq/maya/blob/develop/aos/bashrc) file (on local device):

add 2 rows:
`export DEVICE_TYPE=SMART_DESK`

with list [`DEVICE_TYPE`](https://github.com/duyhtq/maya/blob/develop/aos/system/configs/device.py) :

`SMART_DESK`
`SMART_WALL`
`PERSONAL_ROBOT`
`TELE_PORT`
`DRONE`
