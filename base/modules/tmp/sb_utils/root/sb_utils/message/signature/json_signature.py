import base64
import canonicaljson
import json

from functools import partial
from pathlib import Path
from authlib.jose import JsonWebSignature, errors
from typing import Dict, Union


def json_sign(msg: Union[dict, str], privKey: str) -> dict:
    msg: dict = json.loads(msg) if isinstance(msg, str) else msg
    if not privKey:
        raise ValueError("privKey was not passed as a param")

    header = {
        "alg": "ES256",
        "kid": msg.get("headers", {}).get("from", "ORIGIN")
    }
    sig_payload = b".".join([
        base64.b64encode(canonicaljson.encode_canonical_json(header)),
        base64.b64encode(canonicaljson.encode_canonical_json(msg))
    ])
    jws = JsonWebSignature()
    key = Path(privKey).read_bytes()
    sig = jws.serialize_compact(header, sig_payload, key).decode("utf-8").split('.')
    msg["signature"] = f"{sig[0]}..{sig[2]}"
    return msg


def load_key(header: dict, payload: dict, keys: Dict[str, str]) -> bytes:
    if kid := header.get("kid"):
        print(f"Get key for {kid}")
        if k := keys.get(kid):
            return Path(k).read_bytes()
        return b""
    return b""


def json_verify(msg: Union[bytes, dict, str], pubKey: Union[str, Dict[str, str]] = None) -> bool:
    msg: dict = msg if isinstance(msg, dict) else json.loads(msg)
    if signature := msg.pop("signature", None):
        sig = signature.split(".")
        header = json.loads(base64.b64decode(sig[0]))
        sig[1] = base64.b64encode(b'.'.join([
            base64.b64encode(canonicaljson.encode_canonical_json(header)),
            base64.b64encode(canonicaljson.encode_canonical_json(msg))
        ])).decode("utf-8").rstrip("=")

        jws = JsonWebSignature()
        key = Path(pubKey).read_bytes() if isinstance(pubKey, str) else partial(load_key, keys=pubKey)
        try:
            jws.deserialize_compact(".".join(sig), key)
            return True
        except errors.BadSignatureError:
            return False
    raise ValueError("Message is not signed with JWS")
