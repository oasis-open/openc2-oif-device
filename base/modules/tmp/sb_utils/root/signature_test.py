import uuid
from datetime import datetime
from sb_utils import Message, MessageType, SerialFormats

cmd = Message(
  recipients=["consumer1@example.com", "consumer2@example.com", "consumer3@example.com"],
  origin="Producer1@example.com",
  created=datetime.now(),  # 1595268027000
  msg_type=MessageType.Request,
  request_id=uuid.UUID("95ad511c-3339-4111-9c47-9156c47d37d3"),
  serialization=SerialFormats.JSON,
  content={
    "request": {
      "action": "deny",
      "target": {
        "uri": "http://www.example.com" 
      }
    }
  }
)

sig = cmd.sign('private.pem')
valid = Message.verify(sig, SerialFormats.JSON, "public.pem")
print(valid)

