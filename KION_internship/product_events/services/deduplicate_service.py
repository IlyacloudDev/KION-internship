import os
import hashlib
from redis import Redis
from config.settings import DEDUP_FIELDS, REDIS_EVENT_TTL_SECONDS
from pybloom_live import ScalableBloomFilter


bloom_filter = ScalableBloomFilter(initial_capacity=100000, error_rate=0.001)


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
    Checks for duplicates using a two-layer check:
    1. Bloom filter (in-memory, fast) to reduce число запросов к Redis.
    2. Redis for precise, persistent check.

    If the event hash is not found in the Bloom filter, it is immediately
    added and saved into Redis. If it is found in the Bloom filter, we double-check
    using Redis for confirmation.
    """
    key_data = extract_deduplication_key(product_event)
    event_hash = generate_hash(key_data)

    if event_hash in bloom_filter:
        if redis_client.exists(event_hash):
            return True
        else:
            redis_client.setex(event_hash, REDIS_EVENT_TTL_SECONDS, 1)
            return False
    else:
        bloom_filter.add(event_hash)
        redis_client.setex(event_hash, REDIS_EVENT_TTL_SECONDS, 1)
        return False
