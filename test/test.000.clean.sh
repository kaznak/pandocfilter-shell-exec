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

########################################################

grep -Ev '^[[:space:]]*#' $testd/test.000.test.lst	|
awk '{	tname = $1
    	print "'$testd'/test."tname".html"	}'	|
xargs rm -f
