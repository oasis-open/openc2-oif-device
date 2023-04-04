"""
OSQuery prometheus_metrics ORM
"""
from ....orm import BaseModel
from peewee import BigIntegerField, DoubleField, TextField


class PrometheusMetrics(BaseModel):
    """
    Retrieve metrics from a Prometheus server.
    """
    target_name = TextField(help_text="Address of prometheus target")
    metric_name = TextField(help_text="Name of collected Prometheus metric")
    metric_value = DoubleField(help_text="Value of collected Prometheus metric")
    timestamp_ms = BigIntegerField(help_text="Unix timestamp of collected data in MS")

    class Meta:
        table_name = "prometheus_metrics"
