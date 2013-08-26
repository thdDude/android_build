#!/usr/bin/env python
# Copyright (C) 2012-2013, The CyanogenMod Project
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import print_function

import base64
import json
import netrc
import os
import re
import sys
try:
  # For python3
  import urllib.error
  import urllib.parse
  import urllib.request
except ImportError:
  # For python2
  import imp
  import urllib2
  import urlparse
  urllib = imp.new_module('urllib')
  urllib.error = urllib2
  urllib.parse = urlparse
  urllib.request = urllib2

from xml.etree import ElementTree

product = sys.argv[1];

if len(sys.argv) > 2:
    depsonly = sys.argv[2]
else:
    depsonly = None

try:
    device = product[product.index("_") + 1:]
except:
    device = product

if not depsonly:
    print("Device %s not found. Attempting to retrieve device repository from CyanogenMod Github (http://github.com/CyanogenMod)." % device)

repositories = []

try:
    authtuple = netrc.netrc().authenticators("api.github.com")

    if authtuple:
        githubauth = base64.encodestring('%s:%s' % (authtuple[0], authtuple[2])).replace('\n', '')
    else:
        githubauth = None
except:
    githubauth = None

def add_auth(githubreq):
    if githubauth:
        githubreq.add_header("Authorization","Basic %s" % githubauth)

page = 1
while not depsonly:
    githubreq = urllib.request.Request("https://api.github.com/users/CyanogenMod/repos?per_page=200&page=%d" % page)
    add_auth(githubreq)
    result = json.loads(urllib.request.urlopen(githubreq).read().decode())
    if len(result) == 0:
        break
    for res in result:
        repositories.append(res)
    page = page + 1

def has_branch(branches, revision):
    return revision in [branch['name'] for branch in branches]
