"""
Test Extended Dicts
"""
import copy
import unittest
import uuid

from datetime import datetime
from sb_utils import FrozenDict, ObjectDict, MessageType, QueryDict


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

    def test_FrozenDict(self):
        d = FrozenDict(cmd_args)
        with self.subTest():
            with self.assertRaises(TypeError):
                d.origin = "ORIGIN"

        with self.subTest():
            self.assertEqual(d.content.action, "deny")

    def test_QueryDict(self):
        d = QueryDict(cmd_args)
        with self.subTest():
            self.assertEqual(d.content.action, "deny")

        with self.subTest():
            d.content.action = "allow"
            self.assertEqual(d.content.action, "allow")

        with self.subTest():
            self.assertEqual(d["content.target.uri"], "http://www.example.com")

        with self.subTest():
            self.assertEqual(d.compositeKeys(), ["recipients.0", "recipients.1", "recipients.2", "origin", "created", "msg_type", "request_id", "content.action", "content.target.uri"])


if __name__ == "__main__":
    unittest.main()
