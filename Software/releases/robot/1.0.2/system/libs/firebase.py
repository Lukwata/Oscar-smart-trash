import json

from requests import HTTPError
from aos.system.configs.channel import __FIREBASE_CONFIG__
import pyrebase

class Firebase(object):

  def __init__(self):
    self.firebase = pyrebase.initialize_app(__FIREBASE_CONFIG__)
    self.toke = None
    self.localId = None

  def get_firebase_uid(self, email, password):
    print "get firebase id with %s:%s" % (email, password)
    auth_data = None
    try:
      auth = self.firebase.auth()
      auth_data = auth.create_user_with_email_and_password(email, password)
    except HTTPError as (e, text):
      try:
        error = json.loads(str(text))
        if 'error' in error and error['error']['code'] == 400 and error['error']['message'] == 'EMAIL_EXISTS':
          auth_data = auth.sign_in_with_email_and_password(email, password)
      except Exception as e2:
          print str(e2)
    print auth_data

    if auth_data and 'localId' in auth_data:
        self.localId = auth_data['localId']
        self.idToken = auth_data['idToken']
        return True

    return False









