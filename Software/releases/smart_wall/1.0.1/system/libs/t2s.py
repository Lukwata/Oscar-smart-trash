#phuong macbook
import json
import unicodedata

from aos.sdk.python.send import send_json
from aos.system.libs.util import Util


class T2S:
    @staticmethod
    def run(text):
            if type(text) == type(u''):
                text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore')
            elif type(text) == type(''):
                text = unicodedata.normalize('NFKD', text.decode('utf8')).encode('ascii', 'ignore')

            data = {"text": text}
            source = Util.get_product_id()
            s = {"source": source, "type": "t2s", "data": json.dumps(data), "protocol": "firebase"}

            send_json(json.dumps(s))