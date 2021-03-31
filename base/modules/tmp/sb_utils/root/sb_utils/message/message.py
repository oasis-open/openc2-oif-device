import struct
import uuid

from datetime import datetime
from io import BytesIO
from typing import Any, Dict, List, Union

from . import signature
from .enums import MessageType, SerialTypes
from ..general import toBytes, unixTimeMillis
from ..serialize import decode_msg, encode_msg, SerialFormats


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
    # A unique identifier created by the Producer and copied by Consumer into all Responses, in order to support
    # reference to a particular Command, transaction, or event chain
    request_id: uuid.UUID
    # Media Type that identifies the format of the content, including major version
    # Incompatible content formats must have different serializations
    # Content_type application/openc2 identifies content defined by OpenC2 language specification versions 1.x, i.e.,
    # all versions that are compatible with version 1.0
    content_type: SerialFormats
    # Message body as specified by serialization and msg_type
    content: dict

    __slots__ = ("recipients", "origin", "created", "msg_type", "request_id", "content_type", "content")

    def __init__(self, recipients: Union[str, List[str]] = "", origin: str = "", created: datetime = None, msg_type: MessageType = None, request_id: uuid.UUID = None, serialization: SerialFormats = None, content: dict = None):
        self.recipients = (recipients if isinstance(recipients, list) else [
                           recipients]) if recipients else []
        self.origin = origin
        self.created = created or datetime.utcnow()
        self.msg_type = msg_type or MessageType.Request
        self.request_id = request_id or uuid.uuid4()
        self.content_type = serialization or SerialFormats.JSON
        self.content = content or {}

    def __setattr__(self, key: str, val):
        val = self._validate_content(val) if key == "content" else val
        if key in self.__slots__:
            object.__setattr__(self, key, val)
            return
        raise AttributeError(f"Cannot set an unknown attribute of {key}")

    def __str__(self):
        msg = self.content.copy()
        if self.msg_type == MessageType.Request:
            target = list(msg.pop("target", {"TARGET": ""}).keys())[0]
            m_type = f"{msg.pop('action', 'ACTION').capitalize()}:{target.capitalize()}"
        elif self.msg_type == MessageType.Response:
            m_type = f"Status:{msg.pop('status', 'STATUS')}"
        else:
            m_type = "Notif"
        return f"Message: <{self.msg_type.name}({m_type}) - {msg}>"

    @property
    def mimetype(self) -> str:
        msg_type: Dict[MessageType, str] = {
            MessageType.Request: "cmd",
            MessageType.Response: "rsp",
            MessageType.Notification: "notif"
        }.get(self.msg_type, "notif")
        # Media Type that identifies the format of the content, including major version
        return f"application/openc2-{msg_type}+{self.content_type};version=1.0"

    @property
    def serialization(self) -> str:
        # message encoding
        return self.content_type.name

    def serialize(self) -> Union[bytes, str]:
        return self.oc2_message(serialize=True)

    # OpenC2 Specifics
    @property
    def oc2_headers(self) -> dict:
        return {
            # A unique identifier created by Producer and copied by Consumer into responses
            "request_id": str(self.request_id),
            # Creation date/time of the content
            "created": int(unixTimeMillis(self.created)),
            # Authenticated identifier of the creator of/authority for a request
            "from": self.origin or None,
            # Authenticated identifier(s) of the authorized recipient(s) of a message
            "to": self.recipients or []
        }

    @property
    def oc2_body(self) -> dict:
        return {
            "openc2": {
                # Message body as specified by msg_type (the ID/Name of Content)
                self.msg_type.name.lower(): self.content
            }
        }

    def oc2_message(self, serialize: bool = False) -> Union[bytes, dict, str]:
        msg = {
            "headers": self.oc2_headers,
            "body": self.oc2_body
            # signature??
        }
        return encode_msg(msg, self.content_type, raw=True) if serialize else msg

    @classmethod
    def oc2_loads(cls, m: Union[bytes, str], serial: SerialFormats = SerialFormats.JSON) -> "Message":
        msg = decode_msg(m, serial)
        headers = msg.get("headers", None)
        body = msg.get("body", None)
        if None in [headers, body]:
            raise KeyError("Message is not properly formatted with keys of `headers` and `body`")

        if created := headers.get("created", None):
            created = datetime.fromtimestamp(created / 1000.0)

        if request_id := headers.get("request_id", None):
            request_id = uuid.UUID(request_id)

        msg_type = list(body["openc2"].keys())[0]
        return cls(
            recipients=headers.get("to", None),
            origin=headers.get("from", None),
            created=created,
            msg_type=MessageType.from_name(msg_type),
            request_id=request_id,
            serialization=serial,
            content=body["openc2"][msg_type]
        )

    # Struct like options
    def pack(self) -> bytes:
        return bytes([
            self.msg_type,
            SerialTypes.from_name(self.content_type)
        ]) + toBytes(self.oc2_message(serialize=True))

    @classmethod
    def unpack(cls, m: bytes) -> "Message":
        serial = SerialFormats.from_value(SerialTypes.from_value(m[1]).name)
        msg = decode_msg(m[2:], serial, raw=True)
        headers = msg.get("headers", None)
        body = msg.get("body", None)
        if None in [headers, body]:
            raise KeyError("Message is not properly formatted with keys of `headers` and `body`")

        if created := headers.get("created", None):
            created = datetime.fromtimestamp(created / 1000.0)

        if request_id := headers.get("request_id", None):
            request_id = uuid.UUID(request_id)

        msg_type = list(body["openc2"].keys())[0]
        return cls(
            recipients=headers.get("to", None),
            origin=headers.get("from", None),
            created=created,
            msg_type=MessageType.from_name(msg_type),
            request_id=request_id,
            serialization=serial,
            content=body["openc2"][msg_type]
        )

    # Dumper/Loader
    def dump(self, file: Union[str, BytesIO]) -> None:
        if isinstance(file, str):
            with open(file, "wb") as f:
                f.write(self.dumps())
        elif isinstance(file, BytesIO):
            file.write(self.dumps())
        raise TypeError(f"File is not expected string/BytesIO object, given {type(file)}")

    def dumps(self) -> bytes:
        fmt = SerialTypes.from_name(self.content_type)
        return b"\xF5\xBE".join([  # §¥
            b"\xF5\xBD".join(map(str.encode, self.recipients)),  # §¢
            self.origin.encode(),
            struct.pack("LI", *map(int, str(self.created.timestamp()).split("."))),
            struct.pack("B", self.msg_type),
            self.request_id.bytes,
            struct.pack("B", fmt),
            encode_msg(self.content, SerialFormats.CBOR, raw=True)
        ])

    @classmethod
    def load(cls, file: Union[str, BytesIO]) -> "Message":
        if isinstance(file, str):
            with open(file, "rb") as f:
                return cls.loads(f.read())
        elif isinstance(file, BytesIO):
            return cls.loads(file.read())
        raise TypeError(f"File is not expected string/BytesIO object, given {type(file)}")

    @classmethod
    def loads(cls, m: bytes) -> "Message":
        msg = m.split(b"\xF5\xBE")
        if len(msg) != 7:
            raise ValueError("The OpenC2 message was not properly loaded")
        [recipients, origin, created, msg_type, request_id, serialization, content] = msg

        return cls(
            recipients=list(filter(None, map(bytes.decode, recipients.split(b"\xF5\xBD")))),
            origin=origin.decode(),
            created=datetime.fromtimestamp(float(".".join(map(str, struct.unpack("LI", created))))),
            msg_type=MessageType(struct.unpack("B", msg_type)[0]),
            request_id=uuid.UUID(bytes=request_id),
            serialization=SerialFormats.from_value(SerialTypes.from_value(struct.unpack("B", serialization)[0]).name),
            content=decode_msg(content, SerialFormats.CBOR, raw=True)
        )

    # Signature options
    def sign(self, privKey: str) -> Any:
        if sign := getattr(signature, f"{self.content_type.name.lower()}_sign", None):
            return sign(self.serialize(), privKey)
        raise AttributeError(f"{self.content_type.name} does not have a valid signature function")

    @classmethod
    def verify(cls, msg: Union[bytes, str], fmt: SerialFormats, pubKey: str = None) -> Any:
        if verify := getattr(signature, f"{fmt.name.lower()}_verify", None):
            return verify(msg, pubKey)
        raise AttributeError(f"{fmt.name} does not have a valid verify function")

    # Utility Functions
    def _validate_content(self, val: dict) -> dict:
        msg_keys = {*val.keys()}
        if self.msg_type == MessageType.Request:
            if req_keys := ({"action", "target"} - msg_keys):
                raise KeyError(f"Message is missing a required key(s) of {', '.join(req_keys)}")
        elif self.msg_type == MessageType.Response:
            if req_keys := ({"status", } - msg_keys):
                raise KeyError(f"Message is missing a required key(s) of {', '.join(req_keys)}")
        elif self.msg_type == MessageType.Notification:
            pass
        else:
            print("Message property `msg_type` not set, cannot validate message")
        return val
