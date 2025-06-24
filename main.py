import json
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# File paths
UMKM_FILE = 'data_umkm.json'
USER_FILE = 'users.json'
HISTORY_FILE = 'user_history.json'

# Load JSON
def load_json(path, default):
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return default

# Save JSON
def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

# Load all data
umkm_data = load_json(UMKM_FILE, [])
users = load_json(USER_FILE, [])
user_history = load_json(HISTORY_FILE, {})

# ------------------- REGISTRASI -------------------
def register():
    print("\n=== REGISTRASI ===")
    nama = input("Nama: ").strip()
    asal_perusahaan = input("Perusahaan: ").strip()
    minat = input("Minat sektor (makanan/fashion/minuman): ").strip()

    if any(user['nama'].lower() == nama.lower() for user in users):
        print("❗ User sudah ada.")
        return None

    new_user = {
        "nama": nama,
        "perusahaan": asal_perusahaan,
        "minat": minat
    }

    users.append(new_user)
    save_json(USER_FILE, users)
    user_history[nama] = []
    save_json(HISTORY_FILE, user_history)

    print(f"✅ Registrasi berhasil. Selamat datang, {nama}!")
    return new_user

# ------------------- LOGIN -------------------
def login():
    print("\n=== LOGIN ===")
    nama = input("Masukkan nama Anda: ").strip()
    for user in users:
        if user["nama"].lower() == nama.lower():
            print("✅ Login berhasil.")
            return user
    print("❌ User tidak ditemukan.")
    return None

# ------------------- DASHBOARD -------------------
def dashboard(user):
    print(f"\n=== DASHBOARD {user['nama']} ===")
    history = user_history.get(user["nama"], [])
    if history:
        last_keyword = history[-1]
        print(f"📌 Rekomendasi dari pencarian terakhir: '{last_keyword}'")
        search_umkm(user, keyword=last_keyword, show_input=False)
    else:
        print("ℹ️ Belum ada riwayat pencarian.")

# ------------------- SEARCH UMKM -------------------
def search_umkm(user, keyword=None, show_input=True):
    if show_input:
        keyword = input("🔍 Masukkan keyword pencarian UMKM: ").strip()

    documents = [umkm["deskripsi"] for umkm in umkm_data]
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(documents + [keyword])
    similarity = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1])
    hasil = sorted(zip(similarity[0], umkm_data), key=lambda x: x[0], reverse=True)

    print("\n📄 Hasil Rekomendasi:")
    ada = False
    for score, umkm in hasil:
        if score > 0.1:
            ada = True
            print(f"- {umkm['nama']} ({umkm['kategori']}) [{umkm['wilayah']}]")
    if not ada:
        print("❌ Tidak ada hasil yang cocok.")

    # Simpan keyword ke riwayat
    history = user_history.get(user["nama"], [])
    if keyword not in history:
        history.append(keyword)
        user_history[user["nama"]] = history
        save_json(HISTORY_FILE, user_history)

# ------------------- MENU SETELAH LOGIN -------------------
def menu_login(user):
    while True:
        print("\n📌 Menu:")
        print("1. Cari UMKM")
        print("2. Lihat Dashboard")
        print("3. Logout")
        pilihan = input("Pilih: ")
        if pilihan == "1":
            search_umkm(user)
        elif pilihan == "2":
            dashboard(user)
        elif pilihan == "3":
            print("🔒 Logout berhasil.")
            break
        else:
            print("❌ Pilihan tidak valid.")

# ------------------- MAIN -------------------
def main():
    print("=== CuanIntelligent System ===")
    while True:
        print("\nMenu Utama:")
        print("1. Register")
        print("2. Login")
        print("3. Keluar")
        pilihan = input("Pilih: ")

        if pilihan == "1":
            user = register()
            if user:
                dashboard(user)
                menu_login(user)
        elif pilihan == "2":
            user = login()
            if user:
                dashboard(user)
                menu_login(user)
        elif pilihan == "3":
            print("👋 Keluar dari sistem. Sampai jumpa!")
            break
        else:
            print("❌ Pilihan tidak valid.")

if __name__ == "__main__":
    main()