#! /usr/bin/env monkeyrunner
'''
Copyright (C) 2012  Diego Torres Milano
Created on Oct 12, 2012

@author: diego
'''


import re
import sys
import os

# This must be imported before MonkeyRunner and MonkeyDevice,
# otherwise the import fails.
# PyDev sets PYTHONPATH, use it
try:
    for p in os.environ['PYTHONPATH'].split(':'):
        if not p in sys.path:
            sys.path.append(p)
except:
    pass
    
try:
    sys.path.append(os.path.join(os.environ['ANDROID_VIEW_CLIENT_HOME'], 'src'))
except:
    pass

from com.dtmilano.android.viewclient import ViewClient

from com.android.monkeyrunner import MonkeyRunner, MonkeyDevice

VPS = "javascript:alert(document.getElementsByTagName('html')[0].innerHTML);"
PACKAGE = 'com.android.browser'                                          
ACTIVITY = '.BrowserActivity'                           
COMPONENT = PACKAGE + "/" + ACTIVITY
URI = 'http://dtmilano.blogspot.com'
                   

device, serialno = ViewClient.connectToDeviceOrExit()

device.startActivity(component=COMPONENT, uri=URI)
MonkeyRunner.sleep(3)

vc = ViewClient(device=device, serialno=serialno)

device.drag((240, 180), (240, 420), 10, 10)

url = vc.findViewByIdOrRaise('id/url')
url.touch()
MonkeyRunner.sleep(1)

device.press('KEYCODE_DEL', MonkeyDevice.DOWN_AND_UP)
for c in VPS:
    device.type(c)   
device.press('KEYCODE_ENTER', MonkeyDevice.DOWN_AND_UP)
MonkeyRunner.sleep(3)

vc.dump()
print vc.findViewByIdOrRaise('id/message').getText().replace('\\n', "\n")

device.press('KEYCODE_BACK', MonkeyDevice.DOWN_AND_UP)
