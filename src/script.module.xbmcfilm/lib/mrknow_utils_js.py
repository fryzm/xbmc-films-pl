# -*- coding: utf-8 -*-
"""
App name
~~~~~~

:copyright: (c) 2014 by mrknow
:license: GNU GPL Version 3, see LICENSE for more details.
"""

import urllib

"""
def tb24457fc(s):
    r = ""
    tmp = s.split("12326949")
    s = unescape(tmp[0])
    k = unescape(tmp[1] + "624330")
    i = 0
    while i < s.length
       # r += String.fromCharCode((parseInt(k.charAt(i % k.length)) ^ s.charCodeAt(i)) + -6)
        i=1
    return r
"""

def n98c4d2c(s):
    txtArr = s.split('12326949')
    s = urllib.unquote(txtArr[0])
    t = urllib.unquote(txtArr[1] + '624330')
    tmp=''
    for i in range(0,len(s)-1):
        tmp += chr((int(t[i%len(t)])^ord(s[i]))+-6)
    return urllib.unquote(tmp)