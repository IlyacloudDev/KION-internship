import os
import hashlib
from redis import Redis
from config.settings import DEDUP_FIELDS, REDIS_EVENT_TTL_SECONDS, BLOOM_KEY, ERROR_RATE, INIT_CAP, EXPANSION


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

    if not redis_client.exists(BLOOM_KEY):
        redis_client.execute_command(
            "BF.RESERVE",
            BLOOM_KEY,
            ERROR_RATE,
            INIT_CAP,
            "EXPANSION",
            EXPANSION
        )

    in_bloom = redis_client.execute_command("BF.EXISTS", BLOOM_KEY, event_hash)

    if in_bloom:
        if redis_client.exists(event_hash):
            return True
        else:
            redis_client.setex(event_hash, REDIS_EVENT_TTL_SECONDS, 1)
            return False

    redis_client.execute_command("BF.ADD", BLOOM_KEY, event_hash)
    redis_client.setex(event_hash, REDIS_EVENT_TTL_SECONDS, 1)
    return False
