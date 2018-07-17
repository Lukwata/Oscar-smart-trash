#!/usr/bin/env python
#
# Copyright (C) 2017 Autonomous Inc. All rights reserved.
#

from aos.system.libs.api import post_request, call_request
from aos.system.libs.util import Util

__add_product__ = "product_id/add"
__gen_product_id__ = "product_id/generate"


class Device(object):

    def __init__(self, **kwargs):

        self.product_id = kwargs.get("product_id", "")
        self.product_name = kwargs.get("product_name", "")
        self.product_type = kwargs.get("product_type", "")
        self.address_long = kwargs.get("address_long", "")
        self.address_lat = kwargs.get("address_lat", "")
        self.timezone = kwargs.get("timezone", "")
        self.source = kwargs.get("source", "")
        self.verify_code = kwargs.get("verify_code", "")
        self.address = Util.decode_text(kwargs.get("address", ""))

        super(Device, self).__init__()

    def add_product(self, token):
            rs = post_request(__add_product__, self.__dict__, token)
            print rs
            return rs is not None and 'status' in rs and rs['status'] == 1

    @staticmethod
    def gen_product_id(token):
        rs = call_request(__gen_product_id__, token=token)
        print "get id=>", rs
        print rs
        if rs:
            if 'status' in rs and rs ['status'] == 1:
                return rs['product_id']
        return ''

