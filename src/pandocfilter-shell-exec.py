#!/usr/bin/env python

import os
import sys
import json
import panflute as pf
from subprocess import Popen, PIPE
import collections as c
import io
import csv

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

def proc_csv_table(elm,doc):
    if type(elm) == pf.CodeBlock and 'csv-table' in elm.classes:
        sys.stderr.write(
            'csv-table #' + elm.identifier + '\n'
        )
        attr = elm.attributes

        caption = attr.get('caption',None)
        if 'caption' in attr:
            del attr['caption']

        alignment = attr.get('alignment',None)
        if 'alignment' in attr:
            del attr['alignment']
            
        width = attr.get('width',None)
        if 'width' in attr:
            del attr['width']
        
        with io.StringIO(elm.text) as dat:
            reader = csv.reader(
                dat,
                dialect = csv.excel,
                strict = True
            )
            body = []
            for row in reader:
                cells = [pf.TableCell(pf.Plain(pf.Str(x))) for x in row]
                body.append(pf.TableRow(*cells))

        if 'header' in attr:
            header = body.pop(0)
            del attr['header']
        else:
            header = None

        return pf.Div(
            # content
            pf.Table(
                *body,
                header = header,
                caption = caption,
                alignment = alignment,
                width = width
            ),
            identifier = elm.identifier,
            classes = elm.classes,
            attributes = attr
        )

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
            proc_csv_table,
        ],
        doc = None)
