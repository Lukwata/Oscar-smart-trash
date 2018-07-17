#! /bin/bash
a="$1"
b="$2"
 sed -i -e "s/\($a:\).*/\1$b/" data.dat
