"""
Test Extended Dicts
"""
import copy
import os
import unittest
import uuid

from datetime import datetime
from sb_utils import ObjectDict, MessageType


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


class SignatureTests(unittest.TestCase):
    def test_ObjectDict(self):
        d = ObjectDict(cmd_args)

        with self.subTest():
            d1 = copy.copy(d)
            self.assertDictEqual(d, d1)

        with self.subTest():
            d1 = copy.deepcopy(d)
            self.assertDictEqual(d, d1)


if __name__ == "__main__":
    unittest.main()
