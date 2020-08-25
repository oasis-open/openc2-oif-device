import base64
import canonicaljson
import json
import jws
import struct
import uuid

from Crypto.Hash import SHA
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from datetime import datetime
from enum import Enum
from typing import (
    List,
    Union
)

from .general import unixTimeMillis
from .message import decode_msg, encode_msg, SerialFormats


class MessageType(Enum):
    """
    The type of an OpenC2 Message
    """
    Command = 'cmd'         # The initiator of a two-way message exchange.
    Response = 'rsp'        # A response linked to a request in a two-way message exchange.
    Notification = 'notif'  # A (one-way) message that is not a request or response.  (Placeholder)


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
    content_type: SerialFormats
    # Message body as specified by content_type and msg_type
    content: dict

    __slots__ = ("recipients", "origin", "created", "msg_type", "status", "request_id", "content_type", "content")

    def __init__(self, recipients: Union[str, List[str]] = "", origin: str = "", created: datetime = None, msg_type: MessageType = None, status: int = None, request_id: uuid.UUID = None, content_type: SerialFormats = None, content: dict = None):
        self.recipients = (recipients if isinstance(recipients, list) else [recipients]) if recipients else []
        self.origin = origin
        self.created = created or datetime.utcnow()
        self.msg_type = msg_type or MessageType.Command
        self.status = status or 404
        self.request_id = request_id or uuid.uuid4()
        self.content_type = content_type or SerialFormats.JSON
        self.content = content or {}

    def __setattr__(self, key, val):
        if key in self.__slots__:
            object.__setattr__(self, key, val)
            return
        raise AttributeError("Cannot set an unknown attribute")

    def __str__(self):
        return f"OpenC2 Message: <{self.msg_type.name}; {self.content}>"

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
            content_type=SerialFormats(struct.unpack("B", content_type)[0]),
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

    # OpenC2 Specifics
    @property
    def oc2Dict(self) -> dict:
        msg = dict(
            # Media Type that identifies the format of the content, including major version
            content_type=f"application/openc2-{self.msg_type.value}+{self.content_type.value};version=1.0",
            # Message body as specified by msg_type (the ID/Name of Content)
            content=self.content if self.content_type == SerialFormats.JSON else encode_msg(self.content, self.content_type),
            # A unique identifier created by Producer and copied by Consumer into responses
            request_id=str(self.request_id),
            # Creation date/time of the content
            created=int(unixTimeMillis(self.created))
        )

        if self.origin:
            # Authenticated identifier of the creator of/authority for a request
            msg['from'] = self.origin

        if self.recipients:
            # Authenticated identifier(s) of the authorized recipient(s) of a message
            msg['to'] = self.recipients

        return msg

    @property
    def oc2List(self) -> list:
        return [
            # Message body as specified by msg_type (the ID/Name of Content)
            encode_msg(self.content, self.content_type),
            # A unique identifier created by Producer and copied by Consumer into responses
            str(self.request_id),
            # Creation date/time of the content
            int(unixTimeMillis(self.created)),
            # Authenticated identifier of the creator of/authority for a request
            self.origin or None,
            # Authenticated identifier(s) of the authorized recipient(s) of a message
            self.recipients or []
        ]

    def oc2Signed(self, privKey: str) -> dict:
        if not privKey:
            raise ValueError("privKey was not passed as a param")

        msg = self.oc2Dict
        header = {
            "alg": "RS256",
            "kid": msg.get("from", 'ORIGIN')
        }
        header_b = base64.b64encode(canonicaljson.encode_canonical_json(header)).decode()
        payload_b = base64.b64encode(canonicaljson.encode_canonical_json(msg)).decode()
        sig_payload = f'{header_b}.{payload_b}'
        with open(privKey, 'rb') as f:
            key = RSA.importKey(f.read())

        sig = jws.sign(header, sig_payload, key).decode()
        print(sig_payload)
        print('--'*100)
        print(sig)
        print('--'*100)
        msg['signature'] = f'{header_b}..{sig}'
        return msg

    @staticmethod
    def oc2Verify(msg: dict, pubKey: str) -> bool:
        signature = msg.pop('signature', None)
        if not signature:
            raise ValueError("Message is not signed with JWS")
        if not pubKey:
            raise ValueError("pubKey was not passed as a param")

        header_b, payload, sig = signature.split('.')
        print(f'{header_b}\n{"--"*100}\n{sig}\n{"--"*100}')
        header = json.loads(base64.b64decode(header_b))
        header.pop('kid', None)
        payload_b = base64.b64encode(canonicaljson.encode_canonical_json(msg)).decode()
        sig_payload = f'{header_b}.{payload_b}'
        combo = f'{header_b}\n{"--"*100}\n{payload_b}\n{"--"*100}\n{sig}'
        print(combo)
        print('--'*100)

        with open(pubKey, 'rb') as f:
            key = RSA.importKey(f.read())

        h = SHA.new(sig_payload.encode('utf-8'))
        verifier = PKCS1_v1_5.new(key)
        if verifier.verify(h, sig):
            print("The signature is authentic.")
        else:
            print("The signature is not authentic.")

        try:
            jws.verify(header, sig_payload, sig, key)
            return True
        except jws.exceptions.SignatureError:
            return False
