# Authentication
import base64
import os

from cryptography.fernet import Fernet
from tempfile import TemporaryDirectory
from typing import (
    Dict,
    Union
)
from .general import (
    toBytes,
    toStr
)


class Auth:
    _certsDir: TemporaryDirectory
    username: Union[str, None] = None
    password: Union[str, None] = None
    caCert: Union[str, None] = None
    clientCert: Union[str, None] = None
    clientKey: Union[str, None] = None

    def __init__(self, auth: Dict[str, Union[bytes, str]]):
        auth = {k: toBytes(v) for k, v in (auth or {}).items()}
        crypto = Fernet(os.environ['TRANSPORT_SECRET']) if 'TRANSPORT_SECRET' in os.environ else None
        if crypto is None:
            raise ValueError('ENV variable of `TRANSPORT_SECRET` is not set')
        self.username = toStr(auth.get('username', ''))
        self.password = toStr(crypto.decrypt(auth['password'])) if 'password' in auth else None
        self._certsDir = TemporaryDirectory()
        for cert in ['ca_cert', 'client_cert', 'client_key']:
            val = crypto.decrypt(auth[cert]) if cert in auth else None
            if val:
                path = os.path.join(self._certsDir.name, cert)
                with open(path, 'w+b') as f:
                    f.write(base64.b64decode(val.split(b'base64,')[1]))
                setattr(self, cert, path)

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.cleanup()

    def cleanup(self):
        self._certsDir.cleanup()
