#!/usr/bin/env python
#
# Copyright (C) 2017 Autonomous Inc. All rights reserved.
#

from aos.system.libs.request_api import RequestApi
from aos.system.libs.user import User
from aos.system.libs.util import Util

__add_product__ = "product/add"
__gen_product_id__ = "product_id/generate"
__get_qr_image__ = "product_id/generate-qr"
__check_out__ = "product/checkout"
__check_in__ = "product/checkin"
__get_info__ = "product"
__check_product__ = "product_id/check"


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
            rs = RequestApi(token).get_json(__add_product__, "POST", data=self.__dict__)
            return rs is not None and 'status' in rs and rs['status'] == 1

    @staticmethod
    def gen_product_id(token):
        response_data = RequestApi(token).get_json(__gen_product_id__)

        if response_data and 'status' in response_data and response_data['status'] == 1:
                return response_data['product_id']
        return ''

    @staticmethod
    def check_product(product_id, product_type):
        data = {'product_id': product_id, 'product_type': product_type}
        try:
            return RequestApi().get_json(__check_product__, "POST", data=data)
        except Exception as ex:
            print str(ex)
        return None

    @staticmethod
    def get_info(product_id=None, token=None):
        if not token and not product_id:
            user = User.get_user_info()
            if user:
                token = user.token
                product_id = Util.get_product_id()

        if token and product_id:
            data = {"product_id": product_id}
            return RequestApi(token=token).get_json(__get_info__, data=data, query_parameters=data)
        return None

    @staticmethod
    def get_qr_image():
        return RequestApi().get_json(__get_qr_image__)

    @staticmethod
    def check_out(token=None, product_id=None):
        if not token and not product_id:
            user = User.get_user_info()
            if user:
                token = user.token
                product_id = Util.get_product_id()

        if token and product_id:
            return RequestApi(token).get_json(__check_out__, "POST", data={"product_id": product_id})
        return None

    @staticmethod
    def check_in(name, email, password):
        product_id = Util.get_product_id()
        product_key = Util.get_product_key()
        data_address = Util.get_product_address_config()
        if product_id:
            data = {"email": email, "password": password,
                    "product_id": product_id, "product_key": product_key}
            if name:
                data["fullname"] = name
            if data_address:
                for key, value in data_address.iteritems():
                    if isinstance(data_address[key], (str, unicode)):
                        data_address[key]= data_address[key].encode('utf-8', 'replace').strip()
                data.update(data_address)

            return RequestApi().get_json(__check_in__, "POST", data=data)
        return None

    @staticmethod
    def update_address(product_id=None, token=None, address_data=None):
        if not token and not product_id:
            user = User.get_user_info()
            if user:
                token = user.token
                product_id = Util.get_product_id()

        if token and product_id:
            if address_data is None:
                address_data = Util.get_product_address_config()

            if address_data is not None:
                for key, value in address_data.iteritems():
                    if isinstance(address_data[key], (str, unicode)):
                        address_data[key]= address_data[key].encode('utf-8', 'replace').strip()

            data = {"product_id": product_id}
            data.update(address_data)
            return RequestApi(token=token).get_json(__get_info__, "PUT", data=data, query_parameters=data)
        return None


