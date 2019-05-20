"""
Message Conversion functions
"""
import base64
import cbor2
import collections
import json
import xmltodict
import yaml

from dicttoxml import dicttoxml

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper


def _xml_root(msg):
    if 'message' in msg:
        return msg.get('message', {})

    elif 'response' in msg:
        return msg.get('response', {})

    elif 'action' in msg:
        return 'message'

    elif 'status' in msg:
        return 'response'


def _xml_to_dict(xml):
    tmp = {}
    for k, v in xml.items():
        a = k[1:] if k.startswith("@") else k
        tmp[a] = _xml_to_dict(v) if isinstance(v, collections.OrderedDict) else v
    return tmp


serializations = dict(
    encode=dict(
        cbor=lambda v: base64.b64encode(cbor2.dumps(v)).decode('utf-8'),
        json=lambda v: json.loads(v),
        xml=lambda v: dicttoxml(v, custom_root=_xml_root(v), attr_type=False).decode('utf-8'),
        yaml=lambda v: yaml.dump(v, Dumper=Dumper),
    ),
    decode=dict(
        cbor=lambda v: cbor2.loads(base64.b64decode(v if type(v) is bytes else v.encode())),
        json=lambda v: json.dumps(v),
        xml=lambda v: _xml_root(_xml_to_dict(xmltodict.parse(v))),
        yaml=lambda v: yaml.load(v, Loader=Loader),
    )
)


def encode_msg(msg, enc):
    enc = enc.lower()

    if enc not in serializations['encode']:
        raise ReferenceError('Invalid Encoding')
    elif type(msg) is not dict:
        raise TypeError('Message is not type dict')

    return serializations['encode'].get(enc, serializations['encode']['json'])(msg)


def decode_msg(msg, enc):
    enc = enc.lower()

    if type(msg) is dict:
        return msg
    elif enc not in serializations['decode']:
        raise ReferenceError('Invalid Encoding')
    elif type(msg) not in [str, bytes]:
        raise TypeError('Message is not type string or bytestring')

    return serializations['decode'].get(enc, serializations['decode']['json'])(msg)
