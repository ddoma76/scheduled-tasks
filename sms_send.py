from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient
import certifi

import urllib3
urllib3.disable_warnings()

import os
account_sid = os.environ.get("ACCOUNT_SID")
auth_token = os.environ.get("AUTH_TOKEN")
phone_no = os.environ.get("PHONE_NO")

def easy_client():
  client = Client(account_sid, auth_token)
  return client

def get_proxy_client():
  # 1. Create a custom HTTP client that points to the certifi bundle
  proxy_client = TwilioHttpClient()
  proxy_client.session.verify = certifi.where()

  # 2. Pass that custom client when initializing the Twilio Client
  client = Client(account_sid, auth_token, http_client=proxy_client)
  return client

def get_client_without_verify():
  # Create a client that explicitly tells the underlying session NOT to verify
  proxy_client = TwilioHttpClient()
  proxy_client.session.verify = False  # <--- This disables the SSL check

  client = Client(account_sid, auth_token, http_client=proxy_client)
  return client

def send_message(client, message_txt, phone_to):
  message = client.messages.create(
    messaging_service_sid='MGc554ead5c44ad1e2418e97408aa263e9',
    body=message_txt,
    to=phone_to
  )
  print(message.sid)

#client = get_client_without_verify()
#send_message(client, 'Ahoy', phone_no)


#https://console.twilio.com/
    #get auth token!
#https://www.twilio.com/docs/messaging#sms-and-mms