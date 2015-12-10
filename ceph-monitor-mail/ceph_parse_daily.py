#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import subprocess
import traceback
import codecs
from collections import defaultdict
import requests
from pyecho import echo
from jinja2 import Template
from sendmail import smtp_conn,send_mail

_basedir = os.path.dirname(os.path.abspath(__file__))

def get_ceph():
    try:
        args = ['ceph', 'osd', 'tree']
        p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        s = p.stdout.readlines()
        return s
    except:
        print traceback.format_exc()
        return False

def format_info(content):
    results = defaultdict(list)
    for l in content:
        if l[0] == '#':
            continue
        else:
            r = l.strip().split()
            if r[2] not in ['root', 'rack']:
                if r[2] == 'host':
                    results[r[3]]
                    host = r[3]
                else:
                    results[host].append({'osd_id': r[2], 
                                          'status': r[3], 
                                          'usable':r[4]})
    return results

def format_status(content):
    results = defaultdict(lambda: defaultdict(int))
    for host in content:
        for record in content.get(host):
            if record.get('status') == 'down':
                results[host]['down'] += 1
            if record.get('status') == 'up':
                results[host]['up'] += 1
    return results

def format_output(content):
    template = Template(codecs.open(os.path.join(_basedir, 'template.html')).read())
    status = format_status(content)
    msg = template.render(content=content, status=status)
    return msg

def main():
    # mail smtp
    sender = u'zhangdonghongemail@163.com'
    subject = u'鹏博士机房ceph集群每日运行状态报告'
    session = smtp_conn('smtp.163.com', 25,
                        'zhangdonghongemail@163.com',
                        'xxxxxxxxxxx')

    content = get_ceph()
    if content:
        body = format_output(format_info(content))
        send_mail(session, 'html', sender, ['zhangdonghongemail@163.com'], subject, body)
        

if __name__ == '__main__':
    main()
