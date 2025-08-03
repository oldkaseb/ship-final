import os
import json

DATA_DIR = "data"

# اطمینان از وجود دایرکتوری data
os.makedirs(DATA_DIR, exist_ok=True)

def get_group_file(group_id: int) -> str:
    return os.path.join(DATA_DIR, f"{group_id}.json")


def load_group_data(group_id: int) -> dict:
    file_path = get_group_file(group_id)
    if not os.path.exists(file_path):
        return {}
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_group_data(group_id: int, data: dict):
    file_path = get_group_file(group_id)
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# تابعی برای ادمین‌های مرکزی در فایل admin.py و ... 
def load_data(filename: str) -> dict:
    path = os.path.join(DATA_DIR, filename)
    if not os.path.exists(path):
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_data(filename: str, data: dict):
    path = os.path.join(DATA_DIR, filename)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
