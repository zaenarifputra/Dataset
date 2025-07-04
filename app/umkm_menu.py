from app.storage import load_json, save_json
from app.recommender import recommend

INVESTOR_PATH = "data/data_investor.json"
HISTORY_PATH = "data/history_umkm.json"

def dashboard(user):
    print(f"\n=== DASHBOARD UMKM: {user['nama']} ===")
    all_history = load_json(HISTORY_PATH, {})
    history = all_history.get(user["nama"], [])

    if history:
        for idx, record in enumerate(history, start=1):
            print(f"\n📌 Pencarian ke-{idx}: \"{record['keyword']}\"")
            if record["results"]:
                for item in record["results"]:
                    print(f"- {item['nama']} dari {item['perusahaan']} (minat: {item['minat']})")
            else:
                print("❌ Tidak ditemukan.")
    else:
        print("📭 Belum ada riwayat pencarian.")

def search_investor(user):
    data = load_json(INVESTOR_PATH)
    keyword = input("🔍 Kata kunci pencarian Investor: ")
    results = recommend(keyword, data, keys=["nama", "perusahaan", "deskripsi", "minat"])

    if results:
        print("\n📋 Hasil Investor yang relevan:")
        for item in results:
            print(f"- {item['nama']} dari {item['perusahaan']} (minat: {item['minat']})")
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
        print(f"\n=== MENU UMKM: {user['nama']} ===")
        print("1. Dashboard")
        print("2. Cari Investor")
        print("3. Logout")
        choice = input("Pilih: ")
        if choice == "1":
            dashboard(user)
        elif choice == "2":
            search_investor(user)
        elif choice == "3":
            print("👋 Logout berhasil.")
            break
        else:
            print("❌ Pilihan tidak valid.")
