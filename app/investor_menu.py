from app.storage import load_json, save_json
from app.recommender import recommend

UMKM_PATH = "data/data_umkm.json"
HISTORY_PATH = "data/history_investor.json"

def dashboard(user):
    print(f"\n=== DASHBOARD INVESTOR: {user['nama']} ===")
    all_history = load_json(HISTORY_PATH, {})
    history = all_history.get(user["nama"], [])

    if history:
        for idx, record in enumerate(history, start=1):
            print(f"\n📌 Pencarian ke-{idx}: \"{record['keyword']}\"")
            if record["results"]:
                for item in record["results"]:
                    print(f"- {item['nama']} ({item['kategori']}) [{item['wilayah']}]")
            else:
                print("❌ Tidak ditemukan.")
    else:
        print("📭 Belum ada riwayat pencarian.")

def search_umkm(user):
    data = load_json(UMKM_PATH)
    keyword = input("🔍 Kata kunci pencarian UMKM: ")
    results = recommend(keyword, data, keys=["nama", "kategori", "deskripsi", "wilayah"])

    if results:
        print("\n📋 Hasil UMKM yang relevan:")
        for item in results:
            print(f"- {item['nama']} ({item['kategori']}) [{item['wilayah']}]")
    else:
        print("❌ Tidak ditemukan.")

    all_history = load_json(HISTORY_PATH, {})
    all_history.setdefault(user["nama"], []).append({
        "keyword": keyword,
        "results": results
    })
    save_json(HISTORY_PATH, all_history)

# ✅ Tambahkan fungsi menu agar bisa dipanggil dari main.py
def menu(user):
    while True:
        print(f"\n=== MENU INVESTOR: {user['nama']} ===")
        print("1. Dashboard")
        print("2. Cari UMKM")
        print("3. Logout")
        choice = input("Pilih: ")
        if choice == "1":
            dashboard(user)
        elif choice == "2":
            search_umkm(user)
        elif choice == "3":
            print("👋 Logout berhasil.")
            break
        else:
            print("❌ Pilihan tidak valid.")
