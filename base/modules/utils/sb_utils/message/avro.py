import fastavro

from io import BytesIO


def encode(msg: dict):
    rtn = BytesIO()
    fastavro.schemaless_writer(rtn, {}, msg)
    rtn.close()
    return rtn.getvalue()


def decode(msg: bytes) -> dict:
    msg = BytesIO(msg)
    return fastavro.schemaless_reader(msg, {})
