"""Periodic reporting of log message statistics to SQS and MongoDB."""

from collections import Counter
from datetime import datetime, timedelta, timezone
import json
import os
from threading import Lock

import boto3

from ztm_tools.mongo_tools.mongo_connect import create_mongo_connection


_lock = Lock()
_message_counts = Counter()
_total_messages = 0
_last_report_at = None


def record_logger_call(message_type):
    """Record a call to ``main_logger`` (called internally by logger.py)."""
    global _total_messages
    normalized_type = str(message_type).lower()
    if normalized_type not in {"info", "warning", "error", "crit"}:
        normalized_type = "info"  # main_logger emits unknown types as INFO
    with _lock:
        _message_counts[normalized_type] += 1
        _total_messages += 1


def reporter():
    """Publish log type ratios every ten minutes when called periodically.

    Configuration uses ``MICROSERVICE_NAME``, ``MONGO_URI`` and the same
    SQS settings as :func:`ztm_tools.sqs.sender.send_message`.
    """
    global _last_report_at, _total_messages
    now = datetime.now(timezone.utc)
    with _lock:
        if _last_report_at is None:
            _last_report_at = now
            return None
        if now - _last_report_at < timedelta(minutes=10):
            return None

        total = _total_messages
        counts = dict(_message_counts)
        statistics = {
            message_type: count / total if total else 0
            for message_type, count in sorted(counts.items())
        }
        report = {
            "microservice_name": os.getenv("MICROSERVICE_NAME", "unknown"),
            "reported_at": now,
            "statistics": statistics,
            "message_counts": counts,
            "total_messages": total,
        }
        _last_report_at = now
        _message_counts.clear()
        _total_messages = 0

    # Isolate delivery failures so one destination does not prevent the other.
    try:
        sqs = boto3.client(
            "sqs",
            endpoint_url=os.getenv("S3_ENDPOINT"),
            region_name=os.getenv("SQS_REGION_NAME"),
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        )
        queue_url = sqs.get_queue_url(QueueName="status")["QueueUrl"]
        sqs.send_message(QueueUrl=queue_url, MessageBody=json.dumps(report, default=str))
    except Exception:
        # Reporting must not raise into the periodic service loop.
        pass

    try:
        mongo = create_mongo_connection(os.getenv("MONGO_URI"))
        if mongo is not None:
            database = os.getenv("MONGO_DB", "Poznan")
            mongo[database]["Logs"].insert_one(report)
            mongo.close()
    except Exception:
        pass

    return report
