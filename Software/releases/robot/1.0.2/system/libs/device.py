from aos.system.libs.api import post_request, call_request
from aos.system.libs.user import User

__add_product__ = "product_id/add"
__gen_product_id__ = "product_id/generate"


class Device(object):

    def __init__(self, verify_code, product_id, product_name, product_type, address_long, address_lat, timezone, source):

        self.product_id = product_id
        self.product_name = product_name
        self.product_type = product_type
        self.address_long = address_long
        self.address_lat = address_lat
        self.timezone = timezone
        self.source = source
        self.verify_code = verify_code

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
                return rs ['product_id']
        return ''

