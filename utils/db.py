# utils/db.py - مدیریت ذخیره‌سازی ایزوله برای هر گروه
import os
import json
from datetime import datetime, timedelta

DATA_PATH = "data"
os.makedirs(DATA_PATH, exist_ok=True)

def group_file_path(chat_id):
    return os.path.join(DATA_PATH, f"group_{chat_id}.json")

def init_group_data(chat_id, owner_id=None):
    file_path = group_file_path(chat_id)
    if not os.path.exists(file_path):
        data = {
            "installed": False,
            "owner_id": owner_id,
            "expiration": (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d"),
            "users": {},         # کل اطلاعات کاربران
            "crushes": {},       # کراش‌ها
            "couples": [],       # کاپل‌ها
            "settings": {        # تنظیمات پیشرفته گروه
                "admins": [],
                "channel_required": None,
                "ship_time": "22:00",
                "ask_time": "18:00",
                "managers": {
                    "sellers": [],
                    "owners": []
                }
            }
        }
        save_group_data(chat_id, data)
        return data
    else:
        return load_group_data(chat_id)

def load_group_data(chat_id):
    file_path = group_file_path(chat_id)
    if not os.path.exists(file_path):
        return init_group_data(chat_id)
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_group_data(chat_id, data):
    file_path = group_file_path(chat_id)
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def get_user(data, user_id):
    uid = str(user_id)
    if uid not in data["users"]:
        data["users"][uid] = {}
    return data["users"][uid]

def is_test_expired(group_data):
    exp_date = group_data.get("expiration")
    if not exp_date:
        return True
    try:
        return datetime.strptime(exp_date, "%Y-%m-%d") < datetime.now()
    except:
        return True
