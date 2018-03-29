#!/bin/bash

set -Cu

based=$(readlink -f $(dirname $0)/..)
pname=$(basename $0)
stime=$(date +%Y-%m-%dT%H%M%S%Z)

msg(){
    echo "$pname $stime $(date +%Y%m%d%H%M%S%Z) $@"	>&2
}

tmpd=/tmp/$pname.$stime.$$
if ! mkdir $tmpd ; then
    msg ERROR can not make temporally directory.
    exit 1
fi
trap 'rm -rf $tmpd' EXIT

########################################################
testd=$based/test
srcd=$based/src

tname=001.simple

########################################################

rm -f $testd/test.$tname.html
pandoc --standalone $testd/test.$tname.md	\
       --filter $srcd/pandocfilter-shell-exec.py	\
       --output=$testd/test.$tname.html	&&
diff -u $testd/test.$tname.expect.html $testd/test.$tname.html
