#!/usr/bin/env python

import os
import sys
import json
import panflute as pf
from subprocess import Popen, PIPE
import collections as c

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

def proc_image(elm,doc):
    attr = elm.attributes

    altstr = attr.get('alt','an image')
    if 'alt' in attr:
        del attr['alt']
    title = attr.get('title','an image')
    if 'title' in attr:
        del attr['title']

    return pf.Para(pf.Image(
        pf.Str(altstr),
        url = elm.text.strip(),
        title = title,
        identifier = elm.identifier,
        classes = elm.classes,
        attributes = attr
    ))

#############################################################
def pandoc_filter(elm, doc):
    # print((elm,doc), file=sys.stderr)
    if type(elm) == pf.CodeBlock and 'shell-exec' in elm.classes:
        elm = proc_shell_exec(elm, doc)

        if 'image' in elm.classes:
            sys.stderr.write(
                'shell-exec #' + elm.identifier + ' output as Image\n'
            )
            return proc_image(elm, doc)
        else:
            sys.stderr.write(
                'shell-exec #' + elm.identifier + ' output as CodeBlock \n'
            )
            return elm

#############################################################
if __name__ == "__main__":
    pf.run_filters(
        [
            pandoc_filter,
        ],
        doc = None)
