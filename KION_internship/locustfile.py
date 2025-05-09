from locust import HttpUser, task, between
import random
from datetime import datetime, timezone


class ProductEventUser(HttpUser):
    wait_time = between(0.1, 0.5)

    @task
    def send_product_event(self):
        now_utc = datetime.now(timezone.utc)
        payload = {
            "platform": "android_tv",
            "event_name": "app_list",
            "profile_age": -1,
            "user_agent": "ru.mts.mtstv/1.1.137.74.6.1(20240214)",
            "screen": "",
            "event_datetime_str": "2025-04-02 12:15:05",
            "event_datetime": "2025-04-02T09:15:05.000Z",
            "event_date": "2025-04-02",
            "auth_method": "",
            "auth_type": "",
            "request_id": str(random.randint(100000, 999999)),
            "referer": "",
            "subscription_name": "",
            "subscription_id": "",
            "deeplink": "",
            "payment_type": "",
            "transaction_id": "",
            "purchase_option": "",
            "content_type": "",
            "content_gid": "",
            "content_name": "",
            "content_id": "",
            "promocode": "",
            "promocode_code": "",
            "quality": "",
            "play_url": "",
            "channel_name": "",
            "channel_id": "",
            "channel_gid": "",
            "cause": "",
            "button_id": "",
            "button_text": "",
            "feedback_text": "",
            "experiments": [
                "original_videoshelf_enabled:true",
                "auth_type:websso",
                "subscriptions_design:new"
            ],
            "season": "",
            "episode": "",
            "discount_items_ids": [],
            "discount_items_names": [],
            "content_provider": "",
            "story_type": "",
            "userId": "",
            "playtime_ms": None,
            "duration": None,
            "client_id": "46cfe3e87e0c097a",
            "discount": [],
            "is_trial": None,
            "price": 0,
            "dt_add": now_utc.isoformat().replace("+00:00", "Z"),
            "url_user_event": "",
            "event_receive_timestamp": int(now_utc.timestamp()),
            "event_receive_dt_str": now_utc.strftime("%Y-%m-%d %H:%M:%S.%f"),
            "shelf_name": "",
            "shelf_index": None,
            "card_index": None,
            "error_message": "",
            "platform_useragent": "",
            "product_id": "328da3b0-7623-443c-a3bd-dbc5a9222e75",
            "r": str(random.randint(10000, 99999)),
            "sc": 1,
            "sid": "8772092941743208318",
            "sr": "1920x1080",
            "ts": now_utc.isoformat().replace("+00:00", "+03:00"),
            "os": "Android",
            "mnf": "SDMC",
            "mdl": "DV9135",
            "os_family": "Other",
            "is_mobile": 0,
            "is_pc": 0,
            "is_tablet": 0,
            "is_touch_capable": 0,
            "client_id_query": "46cfe3e87e0c097a",
            "time": 0,
            "search_films": [],
            "recommended_films": [],
            "user_device_is_tv": 1,
            "waterbase_device_id": "5C7B5C5D47CD",
            "error_severity": 999,
            "error_category": 999,
            "app_version": "1.1.137.74.6.1",
            "downloaded": -25,
            "inserted_dt": now_utc.isoformat().replace("+00:00", "Z"),
            "build_model": "DV9135",
            "build_manufacturer": "SDMC",
            "debug": False
        }

        self.client.post("/product_events/", json=payload)
