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

IS_ERROR()	{
    echo ${PIPESTATUS[@]}	|
	xargs -n1	|
	grep -qv '^0$'	||
	return 0

    [ 0 -lt $# ] && msg "ERROR $@"
    return 1
}

trap 'rm -rf $tmpd' EXIT

########################################################
testd=$based/test
srcd=$based/src

tname=002.image

########################################################

cd $testd

rm -rf $testd/test.$tname.html $testd/img

pandoc --standalone $testd/test.$tname.md	\
       --filter $srcd/pandocfilter-shell-exec.py	\
       --to=html5	\
       --output=$testd/test.$tname.html

IS_ERROR pandoc invocation || exit 1

diff -u $testd/test.$tname.expect.html $testd/test.$tname.html

IS_ERROR unexpected output || exit 1

[ -s $testd/img/simple.png ]

IS_ERROR no image file in expected place || exit 1

msg INFO $tname succsess with

rm -f $testd/test.$tname.html
rm -rf $testd/img
