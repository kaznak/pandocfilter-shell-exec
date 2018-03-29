#!/usr/bin/env python

import os
import sys
import json
import panflute as pf
from subprocess import Popen, PIPE

#############################################################
def proc_shell_exec(elm, doc):
    prog = u'sh'
    code = elm.text

    sys.stderr.write(
        'shell-exec #' + elm.identifier + ' prog=' + prog + '\n'
    )
    
    p = Popen([prog], stdin=PIPE, stdout=PIPE)
    p.stdin.write(code.encode('utf-8'))
    elm.text = p.communicate()[0].decode('utf-8')
    p.stdin.close

    return elm

#############################################################
def pandoc_filter(elm, doc):
    # print((elm,doc), file=sys.stderr)
    if type(elm) == pf.CodeBlock and 'shell-exec' in elm.classes:
        elm = proc_shell_exec(elm, doc)
        return elm

#############################################################
if __name__ == "__main__":
    pf.run_filters(
        [
            pandoc_filter,
        ],
        doc = None)
