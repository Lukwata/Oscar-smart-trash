#!/usr/bin/env python
#
# Copyright (C) 2017 Autonomous Inc. All rights reserved.
#

import json
import os
from requests import HTTPError
import pyrebase

class Firebase(object):
  firebase = None

  def __init__(self):
    firebase_config_path = os.environ['__FIREBASE_CONFIG__']
    __FIREBASE_CONFIG__ = None
    if firebase_config_path is not None:
      try:
        with open(firebase_config_path) as data_file:
           __FIREBASE_CONFIG__ = json.load(data_file)
      except Exception as ex:
        print(str(ex))

    if __FIREBASE_CONFIG__ is not None:
      self.firebase = pyrebase.initialize_app(__FIREBASE_CONFIG__)
    self.idToken = None
    self.localId = None
  
  def get_firebase_uid(self, email, password):
    print "get firebase id with %s:%s" % (email, password)
    if self.firebase is None:
      print "cannot alloc firebase instance"
      return False
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









