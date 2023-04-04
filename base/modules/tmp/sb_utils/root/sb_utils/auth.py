# Authentication
import base64
import os

from tempfile import TemporaryDirectory
from typing import Dict, Union
from cryptography.fernet import Fernet
from .general import camelCase, toBytes, toStr


class Auth:
    _certsDir: TemporaryDirectory
    username: Union[str, None] = None
    password: Union[str, None] = None
    caCert: Union[str, None] = None
    clientCert: Union[str, None] = None
    clientKey: Union[str, None] = None

    def __init__(self, auth: Dict[str, Union[bytes, str]]):
        auth = {k: toBytes(v) for k, v in (auth or {}).items()}
        if 'TRANSPORT_SECRET' not in os.environ:
            raise ValueError('ENV variable of `TRANSPORT_SECRET` is not set')

        crypto = Fernet(toBytes(os.environ['TRANSPORT_SECRET']))
        self.username = toStr(auth.get('username', ''))
        self.password = toStr(crypto.decrypt(auth['password'])) if 'password' in auth else None
        self._certsDir = TemporaryDirectory()  # pylint: disable=consider-using-with
        for cert in ['ca_cert', 'client_cert', 'client_key']:
            if val := crypto.decrypt(auth[cert]) if cert in auth else None:
                path = os.path.join(self._certsDir.name, cert)
                with open(path, 'w+b') as f:
                    f.write(base64.b64decode(val.split(b'base64,')[1]))
                setattr(self, camelCase(cert), path)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cleanup()

    def cleanup(self):
        self._certsDir.cleanup()
