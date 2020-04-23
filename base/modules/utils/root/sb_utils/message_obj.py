import struct
import uuid

from datetime import datetime
from enum import Enum
from typing import (
    List,
    Union
)

from .message import decode_msg, encode_msg


class ContentType(Enum):
    """
    The content format of an OpenC2 Message
    """
    Binn = 1
    BSON = 2
    CBOR = 3
    JSON = 4
    MsgPack = 5
    S_Expression = 6
    # smile = 7
    XML = 8
    UBJSON = 9
    YAML = 10
    VPack = 11


class MessageType(Enum):
    """
    The type of an OpenC2 Message
    """
    Command = 1     # The Message content is an OpenC2 Command
    Response = 2    # The Message content is an OpenC2 Response


class Message:
    """
    Message parameter holding class
    """
    # to - Authenticated identifier(s) of the authorized recipient(s) of a message
    recipients: List[str]
    # from - Authenticated identifier of the creator of or authority for execution of a message
    origin: str
    # Creation date/time of the content.
    created: datetime
    # The type of OpenC2 Message
    msg_type: MessageType
    # Populated with a numeric status code in Responses
    status: int
    # A unique identifier created by the Producer and copied by Consumer into all Responses, in order to support reference to a particular Command, transaction, or event chain
    request_id: uuid.UUID
    # Media Type that identifies the format of the content, including major version
    # Incompatible content formats must have different content_types
    # Content_type application/openc2 identifies content defined by OpenC2 language specification versions 1.x, i.e., all versions that are compatible with version 1.0
    content_type: ContentType
    # Message body as specified by content_type and msg_type
    content: dict

    __slots__ = ("recipients", "origin", "created", "msg_type", "status", "request_id", "content_type", "content")

    def __init__(self, recipients: Union[str, List[str]] = "", origin: str = "", created: datetime = None, msg_type: MessageType = None, status: int = None, request_id: uuid.UUID = None, content_type: ContentType = None, content: dict = None):
        self.recipients = (recipients if isinstance(recipients, list) else [recipients]) if recipients else []
        self.origin = origin
        self.created = created or datetime.utcnow()
        self.msg_type = msg_type or MessageType.Command
        self.status = status or 404
        self.request_id = request_id or uuid.uuid4()
        self.content_type = content_type or ContentType.JSON
        self.content = content or {}

    def __setattr__(self, key, val):
        if key in self.__slots__:
            object.__setattr__(self, key, val)
            return
        raise AttributeError("Cannot set an unknown attribute")

    def __str__(self):
        return f"Open Message: <{self.msg_type.name}; {self.content}>"

    @classmethod
    def load(cls, m: bytes) -> 'Message':
        msg = m.split(b"\xF5\xBE")
        print(len(msg))
        if len(msg) != 8:
            raise ValueError("The OpenC2 message was not properly loaded")
        [recipients, origin, created, msg_type, status, request_id, content_type, content] = msg
        return cls(
            recipients=list(filter(None, map(bytes.decode, recipients.split(b"\xF5\xBD")))),
            origin=origin.decode(),
            created=datetime.fromtimestamp(float(".".join(map(str, struct.unpack('LI', created))))),
            msg_type=MessageType(struct.unpack("B", msg_type)[0]),
            status=struct.unpack("I", status)[0],
            request_id=uuid.UUID(bytes=request_id),
            content_type=ContentType(struct.unpack("B", content_type)[0]),
            content=decode_msg(content, 'cbor', raw=True)
        )

    @property
    def serialization(self) -> str:
        return self.content_type.name  # message encoding

    @property
    def dict(self) -> dict:
        return dict(
            recipients=self.recipients,
            origin=self.origin,
            created=self.created,
            msg_type=self.msg_type,
            status=self.status,
            request_id=self.request_id,
            content_type=self.content_type,
            content=self.content
        )

    @property
    def list(self) -> list:
        return [
            self.recipients,
            self.origin,
            self.created,
            self.msg_type,
            self.status,
            self.request_id,
            self.content_type,
            self.content
        ]

    def serialize(self) -> Union[bytes, str]:
        return encode_msg(self.content, self.content_type.name.lower(), raw=True)

    def dump(self) -> bytes:
        return b"\xF5\xBE".join([  # §¥
            b"\xF5\xBD".join(map(str.encode, self.recipients)),  # §¢
            self.origin.encode(),
            struct.pack('LI', *map(int, str(self.created.timestamp()).split("."))),
            struct.pack("B", self.msg_type.value),
            struct.pack("I", self.status),
            self.request_id.bytes,
            struct.pack("B", self.content_type.value),
            encode_msg(self.content, 'cbor', raw=True)
        ])
