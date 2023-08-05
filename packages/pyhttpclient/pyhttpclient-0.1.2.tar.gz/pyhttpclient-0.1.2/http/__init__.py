#!/usr/bin/python
# -*- coding: utf-8 -*-
import urllib2
import urllib
from StringIO import StringIO
import gzip
import json
import logging


def read_and_log(r):
    s = r.read()
    encoding = r.info().get('Content-Encoding')
    if encoding and 'gzip' in encoding:
        buf = StringIO(s)
        f = gzip.GzipFile(fileobj=buf)
        s = f.read()
    logging.debug('receive:%s', s)
    # print r.url,s
    return s


def put(url, data=None, headers=None, timeout=object()):
    logging.debug('request PUT to %s', url)
    opener = urllib2.build_opener(urllib2.HTTPHandler)
    request = urllib2.Request(url,
                              data=(data and urllib.urlencode(data) or ''),
                              headers=headers and headers or {})
    request.get_method = lambda: 'PUT'
    return read_and_log(opener.open(request, timeout=timeout))


def delete(url, data=None, headers=None, timeout=object()):
    logging.debug('request DELETE to %s', url)
    opener = urllib2.build_opener(urllib2.HTTPHandler)
    request = urllib2.Request(url,
                              data=(data and urllib.urlencode(data) or ''),
                              headers=headers and headers or {})
    request.get_method = lambda: 'DELETE'
    return read_and_log(opener.open(request, timeout=timeout))


def post(url, query=None, data=None, headers=None, timeout=object(), dataGzip=False, dataJson=False):
    opener = urllib2.build_opener(urllib2.HTTPHandler)
    query = query and urllib.urlencode(query) or ''
    if isinstance(data, dict):
        if dataJson:
            data = json.dumps(data)
            if not headers: headers = {}
            headers['Content-Type'] = 'application/json'
        else:
            data = urllib.urlencode(data)
    elif isinstance(data, str):
        if not headers: headers = {}
        headers['Content-Type'] = 'application/json'

    if dataGzip:
        if not headers: headers = {}
        headers['Content-Encoding'] = 'gzip'
        out = StringIO()
        with gzip.GzipFile(fileobj=out, mode="w") as f:
            f.write(data)
        data = out.getvalue()
    url = '%s?%s' % (url, query)
    logging.debug('request POST to %s with data=%s headers=%s', url, data, headers)
    request = urllib2.Request(url, data=data,
                              headers=headers and headers or {})
    request.get_method = lambda: 'POST'
    return read_and_log(opener.open(request, timeout=timeout))


def get(url, data=None, headers=None, timeout=object(), dataGzip=False):
    opener = urllib2.build_opener(urllib2.HTTPHandler)
    data = data and urllib.urlencode(data) or ''
    url = '%s?%s' % (url, data)
    if dataGzip:
        if not headers:
            headers = {}
        headers['Accept-Encoding'] = 'gzip'
    logging.debug('request GET to %s with headers=%s', url, headers)
    request = urllib2.Request(url,
                              headers=headers and headers or {})
    return read_and_log(opener.open(request, timeout=timeout))


# def upload(url, filename, fileParam='file', query=None, data=None, headers=None):
#     import MultipartPostHandler
#     import cookielib
#     cookies = cookielib.CookieJar()
#     opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookies),
#                                   MultipartPostHandler.MultipartPostHandler)
#     query = query and urllib.urlencode(query) or ''
#     data = {'x': 'x', fileParam: open(filename, "rb")}
#     return read_and_log(opener.open('%s?%s' % (url, query), data))

if __name__ == '__main__':
    # print get('http://www.notexistised.com')
    logging.basicConfig(level=logging.DEBUG)
    get('http://www.163.com', timeout=1)
