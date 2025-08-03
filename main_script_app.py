
# main_script_app.py
import script_module
import os
import sys

if __name__ == "__main__":
    # Membersihkan layar saat aplikasi diobfuskasi dijalankan
    os.system('cls' if sys.platform.startswith('win') else 'clear')

    print("Memanggil fungsi dari modul Cython yang diobfuskasi...")
    print("-----------------------------------------------------")
    print(f"Modul 'script_module' berhasil diimpor.")
    print("Anggota yang tersedia di modul ini (fungsi, kelas, dll.):")
    print(dir(script_module))
    print("-----------------------------------------------------")

    # --- Contoh Pemanggilan Berdasarkan script.py yang Anda Berikan ---
    # Jika file asli Anda memiliki kelas 'hello' dengan metode 'print_hello':
    if hasattr(script_module, 'hello'):
        try:
            obj = script_module.hello()
            if hasattr(obj, 'print_hello'):
                obj.print_hello()
            else:
                print(f"Peringatan: Metode 'print_hello' tidak ditemukan di kelas 'hello' dari modul yang diobfuskasi.")
        except Exception as e:
            print(f"Error saat mencoba memanggil hello.print_hello(): {e}")
            # import traceback; traceback.print_exc() # Bisa di-uncomment untuk debugging lebih lanjut
    else:
        print(f"Peringatan: Kelas 'hello' tidak ditemukan di modul yang diobfuskasi.")

    # --- Contoh Pemanggilan Fungsi Umum (jika ada di file asli Anda) ---
    # Uncomment dan sesuaikan baris di bawah ini jika file asli Anda memiliki fungsi-fungsi ini.
    # if hasattr(script_module, 'my_custom_function'):
    #     script_module.my_custom_function()
    # if hasattr(script_module, 'add_two_numbers'):
    #     result = script_module.add_two_numbers(50, 75)
    #     print(f"Hasil penjumlahan dari fungsi kustom: {result}")

    print("\nUntuk menjalankan aplikasi ini, Anda memerlukan 'main_script_app.py' dan file")
    print("'script_module.*.so' (atau '.pyd' di Windows) yang dibuat oleh Cython.")
    print("Jika Anda di Termux dan ada error 'dlopen failed', pindahkan kedua file")
    print("ini ke direktori HOME Termux Anda (~), lalu jalankan dari sana.")
