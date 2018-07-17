#!/bin/bash

zmq_current_file="/usr/local/lib/pkgconfig/libzmq.pc"
zmq_new_file="./config.json"
zmq_path="~/aos/system/tmp/libzmq4.2.3"

function install_libzmq {

    echo "installing new libzmq ..."
    cd ~/aos/tmp/libzmq4.2.3
    ./autogen.sh -j 8
    ./configure -j 8
    make clean
    make -j 8
    sudo make install -j 8
    sudo ldconfig
}

function uninstall_libzmq{

    cd $zmq_path
    echo "uninstalling ..."
    sudo make uninstall
    make clean
}

function get_zmq_current_version{
    zmq_current_version=`cat $zmq_current_file | grep '^Version:' | grep -o '[0-9.]\+'`
    echo "zmq_current_version -> $zmq_current_version"
    return $zmq_current_version

}

function get_zmq_install_version{
    zmq_new_version=`cat $zmq_new_file | grep '^libzmq:' | grep -o '[0-9.]\+'`
    echo "zmq_new_version -> $zmq_new_version"
    return $zmq_new_version
}


function main{

    if [ -f "$zmq_current_file" ]
    then
        echo "$zmq_current_file found."
        $zmq_current_version=get_zmq_current_version
        $zmq_new_version=get_zmq_install_version

        if [ $zmq_new_version!=$zmq_current_version ]
        then
            uninstall_libzmq
            install_libzmq
        else
            echo "libzmq: current version === new version"
        fi

    else
        echo "$zmq_current_file not found."
        uninstall_libzmq
        install_libzmq
    fi

    #kiem tra da cai dat thanh cong hay ko?
    $zmq_current_version=get_zmq_current_version
    $zmq_new_version=get_zmq_install_version
    if [ $zmq_new_version==$zmq_current_version ]
    then
        echo "install successful"
    fi
}

