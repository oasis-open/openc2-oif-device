"""
Test Message Signature
"""
import os
import unittest
import uuid

from datetime import datetime
from sb_utils import Message, MessageType, SerialFormats


test_dir = os.path.dirname(os.path.realpath(__file__))
request_id = uuid.UUID("95ad511c-3339-4111-9c47-9156c47d37d3")
cmd_args = {
    "recipients": ["consumer1@example.com", "consumer2@example.com", "consumer3@example.com"],
    "origin": "Producer1@example.com",
    "created": datetime.utcfromtimestamp(1595268027),
    "msg_type": MessageType.Request,
    "request_id": request_id,
    "content": {
        "action": "deny",
        "target": {
          "uri": "http://www.example.com"
        }
    }
}
rsp_args = {
    "recipients": [],
    "origin": "",
    "created": datetime.now(),
    "msg_type": MessageType.Response,
    "request_id": request_id,
    "content": {}
}


class SignatureTests(unittest.TestCase):
    def test_json_signature(self):
        msg = Message(**cmd_args, serialization=SerialFormats.JSON)
        with self.subTest('Sign JSON message'):
            signed = msg.sign(os.path.join(test_dir, 'keys/private.pem'))
        with self.subTest('Verify Signed JSON message'):
            self.assertTrue(Message.verify(signed, SerialFormats.JSON, os.path.join(test_dir, 'keys/public.pem')))


if __name__ == "__main__":
    unittest.main()
