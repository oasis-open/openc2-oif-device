# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import cbor2
import collections
from dicttoxml import dicttoxml
import json
import xmltodict

xml_root = dict(
    command='command',
    response='response'
)


def load_xml(m):
    """
    :parammg: XML Encoded message
    :type m: str
    """
    def _xml_to_dict(xml):
        tmp = {}

        for t in xml:
            if type(xml[t]) == collections.OrderedDict:
                tmp[t] = _xml_to_dict(xml[t])
            else:
                tmp[t[1:] if t.startswith("@") else t] = xml[t]

        return tmp

    if type(m) == str:
        return _xml_to_dict(xmltodict.parse(m))[xml_root['command']]

    else:
        raise Exception('Cannot load xml, improperly formatted')


encodings = dict(
    encode=dict(
        cbor=cbor2.dumps,
        json=json.dumps,
        protobuf=json.dumps,
        xml=lambda x: dicttoxml(x, custom_root=xml_root['response'], attr_type=False)
    ),
    decode=dict(
        cbor=cbor2.loads,
        json=json.loads,
        protobuf=json.loads,
        xml=load_xml
    )
)


def encode_msg(msg, enc):
    if enc not in encodings['encode']:
        raise ReferenceError('Invalid Encoding')
    elif type(msg) is not dict:
        raise TypeError('Message is not type dict')

    return encodings['encode'].get(enc, encodings['encode']['json'])(msg)


def decode_msg(msg, enc):
    if enc not in encodings['decode']:
        raise ReferenceError('Invalid Encoding')
    elif type(msg) not in [str, bytes]:
        raise TypeError('Message is not type string or bytestring')

    return encodings['decode'].get(enc, encodings['decode']['json'])(msg)
