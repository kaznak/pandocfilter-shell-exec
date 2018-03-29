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
    if type(elm) == pf.CodeBlock and 'shell-exec' in elm.classes:
        attr = elm.attributes
        prog = attr.get('prog',u'sh')
        if 'prog' in attr:
            del attr['prog']

        code = elm.text + '\n'

        sys.stderr.write(
            'shell-exec #' + elm.identifier + ' prog=' + prog + '\n'
        )
    
        p = Popen(
            # !!TODO!! handle tab delimter
            [ s for s in prog.split(' ') if s != '' ],
            stdin=PIPE, stdout=PIPE )
        p.stdin.write(code.encode('utf-8'))
        elm.text = p.communicate()[0].decode('utf-8')
        p.stdin.close

        elm.attributes = attr

        return elm

def proc_image(elm,doc):
    if type(elm) == pf.CodeBlock and 'image' in elm.classes:
        attr = elm.attributes

        altstr = attr.get('alt','an image')
        if 'alt' in attr:
            del attr['alt']
        title = attr.get('title','an image')
        if 'title' in attr:
            del attr['title']

        url = elm.text.strip()
        sys.stderr.write(
            'image #' + elm.identifier + 'url=' + url + '\n'
        )
        return pf.Para(pf.Image(
            pf.Str(altstr),
            url = url,
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
if __name__ == "__main__":
    pf.run_filters(
        [
            proc_shell_exec,
            # below filters must listed after shell_exec.
            proc_image,
            proc_csv_table,
        ],
        doc = None)
