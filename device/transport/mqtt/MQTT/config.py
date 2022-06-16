import os
from sb_utils import FrozenDict, safe_cast

Config = FrozenDict(
    TLS_ENABLED=os.environ.get('MQTT_TLS_ENABLED', False),
    TLS_SELF_SIGNED=safe_cast(os.environ.get('MQTT_TLS_SELF_SIGNED', 0), int, 0),
    CAFILE=os.environ.get('MQTT_CAFILE', None),
    CLIENT_CERT=os.environ.get('MQTT_CLIENT_CERT', None),
    CLIENT_KEY=os.environ.get('MQTT_CLIENT_KEY', None),
    USERNAME=os.environ.get('MQTT_DEFAULT_USERNAME', None),
    PASSWORD=os.environ.get('MQTT_DEFAULT_PASSWORD', None),
    MQTT_PREFIX=os.environ.get('MQTT_PREFIX', ''),
    MQTT_HOST=os.environ.get('MQTT_HOST', 'queue'),
    MQTT_PORT=safe_cast(os.environ.get('MQTT_PORT', 1883), int, 1883),
    # TODO: find alternatives??
    TRANSPORT_TOPICS=[t.lower().strip() for t in os.environ.get("MQTT_TRANSPORT_TOPICS", "").split(",")],
    TOPICS=[t.lower().strip() for t in os.environ.get("MQTT_TOPICS", "").split(",")],
    # ETCD Options
    ETCD_HOST=os.environ.get('ETCD_HOST', 'etcd'),
    ETCD_PORT=safe_cast(os.environ.get('ETCD_PORT', 2379), int, 2379),
    RSP_SPECIFIC=safe_cast(os.environ.get('RSP_SPECIFIC', False), bool, False)
)
