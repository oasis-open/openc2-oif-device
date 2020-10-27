import base64
import canonicaljson
import json
import jws

from Crypto.Hash import SHA
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
# TODO: prep for varying serialization signatures


def oc2Signed(msg: dict, privKey: str) -> dict:
    if not privKey:
        raise ValueError("privKey was not passed as a param")

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
