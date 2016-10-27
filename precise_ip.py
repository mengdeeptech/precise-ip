#!/usr/bin/env python
# encoding: utf-8
# by masterzh


import sys
import urllib2
import json


site = 'http://api.map.baidu.com/highacciploc/v1'


def precise_ip(ip, ak):
    url = site + '?qcip=' + ip + '&qterm=pc&ak=' + ak + '&coord=bd09ll&extensions=3'

    try:
        r = urllib2.urlopen(url, timeout=10)
    except Exception, e:
        print e
        return ''
    else:
        data = r.read()

    if data is None:
        return 'IP地址定位失败！'

    info = json.loads(data)

    if 'content' in info:
        cnt = info['content']
        pos = ''
        if 'address_component' in info['content']:
            pos += cnt['address_component'].get('country', '') + ' '
            pos += repr(cnt['address_component'].get('admin_area_code', 000)) + ' '

        pos += info['content'].get('formatted_address', '') + ' '

        if 'location' in cnt:
            lat = cnt['location'].get('lat')
            lng = cnt['location'].get('lng')
            pos += '(%d, %d)' % (lat, lng)

        return pos


def output_xml(ip, pos):
    print '''<?xml version="1.0"?>
<items>
  <item uid="%s" arg="argsx" autocomplete="autocompletex">
    <title>%s</title>
    <icon>icon.png</icon>
  </item>
</items>''' % (ip, pos)


def query(ip, ak):
    output_xml(ip, precise_ip(ip, ak))
