import json
import os

# Digunakan untuk menyimpan dan memuat data JSON, Jika file tidak ada, akan mengembalikan nilai default
def load_json(path, default=[]):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return default

def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)