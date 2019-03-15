import sys
sys.path.append('../')

from server.test_module.controllers import send_presence

REQUEST = {
        "action": "presence",
        "type": "status",
        "user": {
                "account_name":  "User Name",
                "status":      "Yep, I am here!"
        }
    }

RESPONSE = {
            "response": 200,
            "msg": "Hi User Name"
   }


def presence_msg_request_to_response():
    assert send_presence(REQUEST) == RESPONSE
