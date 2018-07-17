os="none"
#Detect which board to run
if uname -m |grep x86_64 ; then
        os="x64"
 #       echo "Detected $os "
fi

if uname -m |grep arm ; then
        os="RPI"
#        echo "Detected Arm Board"
fi
if uname -m |grep i686 ; then
        os="x86"
fi
chmod +x  user/$os/deskreq
./user/$os/deskreq

