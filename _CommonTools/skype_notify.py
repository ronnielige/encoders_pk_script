__author__ = 'HD-User'

from Skype4Py import Skype
import sys

# client = Skype()
# client.Attach()
# user = sys.argv[1]
# message = ' '.join(sys.argv[2:])
# client.SendMessage(user, message)
# #client.PlaceCall(user)

def skype_message(user_name, message_text):
  client = Skype()
  client.Attach()
  client.SendMessage(user_name, message_text)


def skype_call(user_name, message_text):
  client = Skype()
  client.Attach()
  client.PlaceCall(user_name)