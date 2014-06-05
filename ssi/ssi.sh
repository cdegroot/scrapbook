#!/bin/bash
#
#  Driver script for ssi.py
#
ssi=$(cd $(dirname $0); /bin/pwd)
export SSI_BASE=$(pwd)
find . -name '*.shtml' | 
    grep -v head |
    grep -v foot |
    while read file
    do 
        dir=$(dirname $file)
        base=$(basename $file)
        (cd $dir; $ssi/ssi.py $base >$(basename $base .shtml).html)
    done
