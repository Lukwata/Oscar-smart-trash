#!/usr/bin/env python
#
# Copyright (C) 2017 Autonomous Inc. All rights reserved.
#

import os
import urllib2
import urllib
import json
import requests

__BASE_URL__ = "https://autonomousbrain.com/v2/"
if 'API_BASE_URL' in os.environ:
    __BASE_URL__ = os.environ['API_BASE_URL']
print __BASE_URL__

# list of services
__userInfo__ = "info/user_n_product"


def call_request(endpoint, params=None, token=None):
    try:

        headers = {}
        if token:
            headers = {"Authorization": "Autonomous " + token}

        url = __BASE_URL__ + endpoint

        if params:
            url += urllib.urlencode(params)

        print "call server at %s" % (url)

        request = urllib2.Request(url, None, headers)
        response = urllib2.urlopen(request)
        return json.loads(response.read())
    except Exception as ex:
        print str(ex)
    return None


def post_request(endpoint, data, token=None):
    headers = {}
    if token:
        headers = {"Authorization": "Autonomous " + token}
    url = __BASE_URL__ + endpoint
    print "call post server at %s" % (url)
    data = urllib.urlencode(data)
    print "data=>", data
    request = urllib2.Request(url, data=data, headers=headers)
    try:
        return json.loads(urllib2.urlopen(request).read())
    except Exception as e:
        print "post_request => error =>", str(e)

    return None


def user_info(user_id, email, user_hash, product_id):
    params = {'user_id': user_id, 'email': email, 'user_hash': user_hash, 'product_id': product_id}
    try:
        r = requests.post(__BASE_URL__ + __userInfo__, data=params)
        return r.json()
    except Exception as ex:
        print str(ex)
    return None


# if __name__ == '__main__':
#     print user_info(user_id='617', email='NN@autonomousbrain.com', user_hash='499af80859047b8e1a93249765abe6ee')
