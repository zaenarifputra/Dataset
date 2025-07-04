# Registrasi dan Login
# Digunakan untuk mengelola pengguna, termasuk registrasi dan login
from .storage import load_json, save_json
from os.path import join

USER_PATH = "data/users.json"

def load_users():
    return load_json(USER_PATH)

def save_users(users):
    save_json(USER_PATH, users)

def register():
    users = load_users()
    name = input("Nama: ").strip().title()
    company = input("Perusahaan: ").strip().title()

    while True:
        role = input("Daftar sebagai (investor/umkm): ").strip().lower()
        if role in ["investor", "umkm"]:
            break
        print("❌ Hanya 'investor' atau 'umkm' yang diizinkan.")

    sektor_tersedia = ["makanan", "lingkungan", "teknologi"]
    print("Sektor tersedia:", ", ".join(sektor_tersedia))
    
    while True:
        minat = input("Minat sektor (pilih dari atas): ").strip().lower()
        if minat in sektor_tersedia:
            break
        print("❌ Pilihan sektor tidak valid. Pilih salah satu dari:", ", ".join(sektor_tersedia))

    for user in users:
        if user["nama"].lower() == name.lower():
            print("❌ Nama sudah terdaftar.")
            return None
        if user["perusahaan"].lower() == company.lower():
            print("❌ Perusahaan sudah terdaftar.")
            return None

    user = {"nama": name, "perusahaan": company, "role": role, "minat": minat}
    users.append(user)
    save_users(users)
    print(f"✅ Registrasi berhasil sebagai {role.upper()}")
    return user

def login():
    users = load_users()
    name = input("Nama: ").strip()
    for user in users:
        if user["nama"].lower() == name.lower():
            print("✅ Login berhasil.")
            return user
    print("❌ User tidak ditemukan.")
    return None