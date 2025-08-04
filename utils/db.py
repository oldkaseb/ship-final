import os
import json
from config import DATA_FOLDER

def ensure_data_folder():
    """ساخت پوشه دیتای گروه‌ها اگر وجود نداشت"""
    if not os.path.exists(DATA_FOLDER):
        os.makedirs(DATA_FOLDER)

def get_group_file(group_id: int) -> str:
    """مسیر فایل JSON ایزوله برای هر گروه"""
    return os.path.join(DATA_FOLDER, f"{group_id}.json")

def load_group_data(group_id: int) -> dict:
    """لود اطلاعات گروه از فایل"""
    path = get_group_file(group_id)
    if not os.path.exists(path):
        data = create_default_data(group_id)
        save_group_data(group_id, data)
        return data
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_group_data(group_id: int, data: dict):
    """ذخیره اطلاعات گروه در فایل"""
    path = get_group_file(group_id)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def create_default_data(group_id: int) -> dict:
    """دیتای اولیه هر گروه"""
    return {
        "group_id": group_id,
        "users": {},  # key: user_id
        "relations": [],  # لیست رل‌ها
        "crushes": {},  # key: user_id → [user_ids]
        "birthdays": {},  # key: user_id → "YYYY-MM-DD"
        "trial_start": None,
        "subscription_until": None,
        "warned_expiry": False,
        "blacklist": [],  # کاربرانی که بلاک شدن
        "logs": [],
        "admins": [],
        "ship_history": [],
    }

def get_user_profile(data: dict, user_id: int) -> dict:
    """اطلاعات پروفایل کاربر خاص در دیتا"""
    if str(user_id) not in data["users"]:
        data["users"][str(user_id)] = {
            "name": None,
            "age": None,
            "city": None,
            "gender": None,  # male/female
            "status": "single",  # single/relationship/ex
            "partner_id": None,
            "relationship_start": None,
            "crash_count": 0,
            "last_updated": None
        }
    return data["users"][str(user_id)]
