from app.user import register, login
from app.investor_menu import menu as investor_menu
from app.umkm_menu import menu as umkm_menu

def main():
    print("=== CUANtelligence System ===")
    while True:
        print("\n1. Register\n2. Login\n3. Exit")
        choice = input("Pilih: ")
        if choice == "1":
            user = register()
            if user:
                if user["role"] == "investor":
                    investor_menu(user)
                else:
                    umkm_menu(user)
        elif choice == "2":
            user = login()
            if user:
                if user["role"] == "investor":
                    investor_menu(user)
                else:
                    umkm_menu(user)
        elif choice == "3":
            print("👋 Keluar dari sistem.")
            break
        else:
            print("❌ Pilihan tidak valid.")

if __name__ == "__main__":
    main()
