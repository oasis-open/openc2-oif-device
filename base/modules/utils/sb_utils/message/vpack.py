import json
import os
import tempfile

from subprocess import Popen, PIPE


def encode(msg: dict) -> bytes:
    rtn = b""
    msg_tmp = tempfile.NamedTemporaryFile(delete=True)
    enc_tmp = tempfile.NamedTemporaryFile(delete=True)
    with open(msg_tmp.name, "w") as f:
        f.write(json.dumps(msg))

    os.chmod(msg_tmp.name, 0o0777)
    msg_tmp.file.close()

    process = Popen(["json-to-vpack", msg_tmp.name, enc_tmp.name], stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()

    with open(enc_tmp.name, "rb") as f:
        rtn = f.read()

    msg_tmp.close()
    enc_tmp.close()
    return rtn


def decode(msg: bytes) -> dict:
    rtn = {}
    msg_tmp = tempfile.NamedTemporaryFile(delete=True)
    dec_tmp = tempfile.NamedTemporaryFile(delete=True)
    with open(msg_tmp.name, "wb") as f:
        f.write(msg)

    os.chmod(msg_tmp.name, 0o0777)
    msg_tmp.file.close()

    process = Popen(["vpack-to-json", msg_tmp.name, dec_tmp.name], stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()

    with open(dec_tmp.name, "rb") as f:
        rtn = json.load(f)

    print("")
    msg_tmp.close()
    dec_tmp.close()
    return rtn
