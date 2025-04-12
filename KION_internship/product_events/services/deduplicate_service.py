import os
import hashlib
from redis import Redis
from config.settings import DEDUP_FIELDS, REDIS_EVENT_TTL_SECONDS


redis_client = Redis(
    host=os.environ.get("REDIS_HOST"),
    port=int(os.environ.get("REDIS_PORT")),
    db=int(os.environ.get("REDIS_DB")),
    decode_responses=True
)


def extract_deduplication_key(product_event: dict) -> str:
    """
    Creates a unique key string based on key fields from the event.
    """
    return '|'.join(str(product_event.get(field)) for field in DEDUP_FIELDS)


def generate_hash(key_data: str) -> str:
    """
    Generates a SHA256 hash for deduplication comparison.
    """
    return hashlib.sha256(key_data.encode('utf-8')).hexdigest()


def is_duplicate_event(product_event: dict) -> bool:
    """
    Checks for duplicates using Redis hash set only.
    """
    key_data = extract_deduplication_key(product_event)
    event_hash = generate_hash(key_data)

    if redis_client.exists(event_hash):
        return True

    redis_client.setex(event_hash, REDIS_EVENT_TTL_SECONDS, 1)
    return False
