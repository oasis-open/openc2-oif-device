# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import uuid


def prefixUUID(pre='PREFIX', max=30):
    uid_max = max - (len(pre) + 10)
    uid = str(uuid.uuid4()).replace('-', '')[:uid_max]
    return f'{pre}-{uid}'[:max]


def safe_load(file_obj):
    try:
        return json.load(file_obj)
    except Exception as e:
        print(f'{file_obj.name} - {e}')
        return {}
