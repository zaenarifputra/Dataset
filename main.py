import json
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# File paths
UMKM_FILE = 'data_umkm.json'
USER_FILE = 'users.json'
HISTORY_FILE = 'user_history.json'

# ---------- JSON Utility Functions ----------
def load_json(path, default):
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return default

def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

# ---------- Load Data ----------
umkm_data = load_json(UMKM_FILE, [])
users = load_json(USER_FILE, [])
user_history = load_json(HISTORY_FILE, {})

# ---------- Registrasi ----------
def register():
    print("\n=== REGISTRASI ===")

    nama = input("Nama: ").strip().title()
    perusahaan = input("Perusahaan: ").strip().title()

    # Validasi pilihan sektor
    sektor_valid = ['makanan', 'fashion', 'minuman']
    while True:
        minat = input("Minat sektor (makanan/fashion/minuman): ").strip().lower()
        if minat in sektor_valid:
            break
        print("❌ Minat tidak valid. Silakan pilih: makanan / fashion / minuman.")

    # Cek duplikasi nama dan perusahaan
    for user in users:
        if user['nama'].lower() == nama.lower() and user['perusahaan'].lower() == perusahaan.lower():
            print("❗ Kombinasi nama dan perusahaan sudah terdaftar.")
            return None
        if user['nama'].lower() == nama.lower():
            print("❗ Nama sudah digunakan. Gunakan nama lain.")
            return None
        if user['perusahaan'].lower() == perusahaan.lower():
            print("❗ Nama perusahaan sudah digunakan. Gunakan nama lain.")

    new_user = {
        "nama": nama,
        "perusahaan": perusahaan,
        "minat": minat
    }
    users.append(new_user)
    save_json(USER_FILE, users)

    user_history[nama] = []
    save_json(HISTORY_FILE, user_history)

    print(f"✅ Registrasi berhasil. Selamat datang, {nama}!")
    return new_user

# ---------- Login ----------
def login():
    print("\n=== LOGIN ===")
    nama = input("Masukkan nama Anda: ").strip()
    for user in users:
        if user["nama"].lower() == nama.lower():
            print("✅ Login berhasil.")
            return user
    print("❌ User tidak ditemukan.")
    return None

# ---------- Dashboard ----------
def dashboard(user):
    print(f"\n=== DASHBOARD {user['nama']} ===")
    history = user_history.get(user["nama"], [])
    if history:
        last_keyword = history[-1]
        print(f"📌 Rekomendasi terakhir berdasarkan keyword: '{last_keyword}'")
        search_umkm(user, keyword=last_keyword, show_input=False)
    else:
        print("ℹ️ Belum ada riwayat pencarian.")

# ---------- Cari UMKM ----------
def search_umkm(user, keyword=None, show_input=True):
    if show_input:
        keyword = input("🔍 Masukkan keyword pencarian UMKM: ").strip()

    documents = [umkm["deskripsi"] for umkm in umkm_data]
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(documents + [keyword])
    similarity_scores = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1])[0]
    rekomendasi = sorted(zip(similarity_scores, umkm_data), key=lambda x: x[0], reverse=True)

    print("\n📄 Hasil Rekomendasi:")
    ada_hasil = False
    for score, umkm in rekomendasi:
        if score > 0.1:
            ada_hasil = True
            print(f"- {umkm['nama']} ({umkm['kategori']}) [{umkm['wilayah']}]")
    if not ada_hasil:
        print("❌ Tidak ada hasil yang cocok.")

    # Simpan ke history
    if keyword not in user_history.get(user["nama"], []):
        user_history[user["nama"]].append(keyword)
        save_json(HISTORY_FILE, user_history)

# ---------- Menu Setelah Login ----------
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

# ---------- Main Menu ----------
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

# ---------- Entry Point ----------
if __name__ == "__main__":
    main()
