import os
import subprocess
import shutil
import sys
import platform
import traceback

# --- Cek Ketersediaan Cython ---
try:
    import Cython
    CYTHON_AVAILABLE = True
except ImportError:
    CYTHON_AVAILABLE = False
    print("Error: Cython tidak terinstal.")
    print("Silakan jalankan 'pip install cython' terlebih dahulu.")
    if "ANDROID_ROOT" in os.environ and platform.system() == "Linux":
        print("Untuk Cython di Termux, Anda juga perlu 'pkg install clang' dan 'pkg install python-dev'.")
    sys.exit(1) # Keluar jika Cython tidak tersedia

# --- Fungsi Utama Obfuskasi Cython ---
def get_user_file_input():
    """Meminta nama file Python yang ingin diobfuskasi dari pengguna."""
    # Menampilkan logo dan informasi author sebelum input file
    print("""
 ▗▄▄▖▄   ▄    ■  ▐▌    ▄▄▄  ▄▄▄▄   ▗▄▖ ▗▄▄▖ ▗▄▄▄▖
▐▌   █   █ ▗▄▟▙▄▖▐▌   █   █ █   █ ▐▌ ▐▌▐▌ ▐▌▐▌   
▐▌    ▀▀▀█   ▐▌  ▐▛▀▚▖▀▄▄▄▀ █   █ ▐▌ ▐▌▐▛▀▚▖▐▛▀▀▘
▝▚▄▄▖▄   █   ▐▌  ▐▌ ▐▌            ▝▚▄▞▘▐▙▄▞▘▐▌   
      ▀▀▀    ▐▌                                  
                                                 
                                                 
""")
    print("Author   : n1k4xryougaaa'")
    print("Developer: NyctophileSkyzo")
    print("Credit   : https://github.com/n1k4xryougaaa/CythonOBF")
    print("-" * 50) # Garis pemisah untuk estetika

    while True:
        file_name = input("Masukkan nama file Python (misal: script.py): ").strip()
        if not file_name:
            print("Nama file tidak boleh kosong. Silakan coba lagi.")
        elif not os.path.exists(file_name):
            print(f"Error: File '{file_name}' tidak ditemukan di direktori saat ini.")
            print("Pastikan file berada di direktori yang sama dengan skrip ini.")
        else:
            return file_name

def clean_up_cython_build(module_name, pyx_file_name, setup_file_name, original_input_is_py):
    """Membersihkan file sementara yang dihasilkan Cython."""
    print("\n--- Membersihkan file sementara Cython ---")

    # Hapus file .c yang dihasilkan Cython
    generated_c_file = pyx_file_name.replace('.pyx', '.c')
    if os.path.exists(generated_c_file):
        os.remove(generated_c_file)
        print(f"Menghapus file C sementara: {generated_c_file}")

    # Hapus file setup.py
    if os.path.exists(setup_file_name):
        os.remove(setup_file_name)
        print(f"Menghapus file setup: {setup_file_name}")

    # Hapus file .pyx sementara jika itu hasil konversi dari .py
    if original_input_is_py and os.path.exists(pyx_file_name):
        os.remove(pyx_file_name)
        print(f"Menghapus file .pyx sementara: {pyx_file_name}")
    
    # Hapus direktori build/
    build_dir = "build"
    if os.path.exists(build_dir) and os.path.isdir(build_dir):
        try:
            shutil.rmtree(build_dir)
            print(f"Menghapus direktori sementara: {build_dir}/")
        except Exception as e:
            print(f"Peringatan: Gagal menghapus direktori '{build_dir}/': {e}")


def obfuscate_with_cython_process(input_file_path):
    """
    Mengelola seluruh proses obfuskasi dengan Cython untuk file input yang diberikan.
    """
    base_name = os.path.splitext(input_file_path)[0] # Nama file tanpa ekstensi
    pyx_file_name = base_name + ".pyx"
    module_name = base_name.replace(".", "_") + "_module" # Nama modul Python yang unik
    setup_file_name = "setup_cython_build.py"
    main_app_file_name = "main_" + base_name + "_app.py"
    original_input_is_py = False # Flag untuk pembersihan .pyx

    print(f"\n--- Memulai Obfuskasi dengan Cython untuk '{input_file_path}' ---")

    # 1. Salin konten .py ke .pyx jika inputnya .py
    if input_file_path.lower().endswith(".py"):
        original_input_is_py = True
        try:
            shutil.copyfile(input_file_path, pyx_file_name)
            print(f"Konten '{input_file_path}' disalin ke '{pyx_file_name}'.")
        except Exception as e:
            print(f"Error saat menyalin file: {e}")
            sys.exit(1)
    elif input_file_path.lower().endswith(".pyx"):
        pyx_file_name = input_file_path # Jika user sudah kasih .pyx, pakai itu langsung
    else:
        print("Error: File input harus berupa file Python (.py) atau Cython (.pyx).")
        sys.exit(1)

    # 2. Buat file setup.py untuk kompilasi
    setup_content = f"""
from setuptools import setup, Extension
from Cython.Build import cythonize
import os

ext_modules = [
    Extension(
        "{module_name}",
        ["{pyx_file_name}"],
    )
]

setup(
    name='CythonObfuscatedApp',
    ext_modules=cythonize(ext_modules, compiler_directives={{'language_level': "3"}}),
)
"""
    with open(setup_file_name, 'w') as f:
        f.write(setup_content)
    print(f"'{setup_file_name}' (script kompilasi) dibuat.")

    # 3. Jalankan perintah kompilasi
    print(f"Memulai kompilasi '{pyx_file_name}' ke modul C/C++... (Ini mungkin membutuhkan waktu)")
    try:
        # Bersihkan file .so/.pyd lama sebelum kompilasi baru
        for f in os.listdir('.'):
            if f.startswith(module_name) and (f.endswith('.so') or f.endswith('.pyd')):
                os.remove(f)
                print(f"Menghapus file lama: {f}")

        # Jalankan subprocess dengan output yang ditangkap
        process = subprocess.Popen(
            [sys.executable, setup_file_name, "build_ext", "--inplace"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        # Tampilkan output secara real-time
        for line in iter(process.stdout.readline, ''):
            sys.stdout.write(line)
            sys.stdout.flush()
        for line in iter(process.stderr.readline, ''):
            sys.stderr.write(line)
            sys.stderr.flush()

        process.wait() # Tunggu hingga proses selesai

        if process.returncode != 0:
            raise subprocess.CalledProcessError(process.returncode, process.args, output=process.stdout.read(), stderr=process.stderr.read())

        print("Kompilasi Cython berhasil!")

    except subprocess.CalledProcessError as e:
        print(f"\nError saat kompilasi Cython: Kode keluar {e.returncode}")
        print("Pastikan Anda memiliki kompilator C/C++ (seperti GCC/Clang untuk Linux/Termux/macOS atau MSVC untuk Windows) dan Python development headers terinstal dengan benar.")
        print("\n--- Detail Output Kompilasi (stderr) ---")
        print(e.stderr)
        print("--- Detail Output Kompilasi (stdout) ---")
        print(e.output)
        clean_up_cython_build(module_name, pyx_file_name, setup_file_name, original_input_is_py)
        sys.exit(1)
    except FileNotFoundError:
        print("\nError: Perintah 'python' tidak ditemukan atau Cython tidak dapat diakses.")
        print("Pastikan Python ada di PATH Anda dan Cython terinstal dengan benar.")
        clean_up_cython_build(module_name, pyx_file_name, setup_file_name, original_input_is_py)
        sys.exit(1)
    except Exception as e:
        print(f"\nError tak terduga selama kompilasi: {e}")
        traceback.print_exc() # Tampilkan full traceback
        clean_up_cython_build(module_name, pyx_file_name, setup_file_name, original_input_is_py)
        sys.exit(1)

    # 4. Buat script utama yang menggunakan modul yang dikompilasi
    main_app_content = f"""
# {main_app_file_name}
import {module_name}
import os
import sys

if __name__ == "__main__":
    # Membersihkan layar saat aplikasi diobfuskasi dijalankan
    os.system('cls' if sys.platform.startswith('win') else 'clear')

    print("Memanggil fungsi dari modul Cython yang diobfuskasi...")
    print("-----------------------------------------------------")
    print(f"Modul '{module_name}' berhasil diimpor.")
    print("Anggota yang tersedia di modul ini (fungsi, kelas, dll.):")
    print(dir({module_name}))
    print("-----------------------------------------------------")

    # --- Contoh Pemanggilan Berdasarkan script.py yang Anda Berikan ---
    # Jika file asli Anda memiliki kelas 'hello' dengan metode 'print_hello':
    if hasattr({module_name}, 'hello'):
        try:
            obj = {module_name}.hello()
            if hasattr(obj, 'print_hello'):
                obj.print_hello()
            else:
                print(f"Peringatan: Metode 'print_hello' tidak ditemukan di kelas 'hello' dari modul yang diobfuskasi.")
        except Exception as e:
            print(f"Error saat mencoba memanggil hello.print_hello(): {{e}}")
            # import traceback; traceback.print_exc() # Bisa di-uncomment untuk debugging lebih lanjut
    else:
        print(f"Peringatan: Kelas 'hello' tidak ditemukan di modul yang diobfuskasi.")

    # --- Contoh Pemanggilan Fungsi Umum (jika ada di file asli Anda) ---
    # Uncomment dan sesuaikan baris di bawah ini jika file asli Anda memiliki fungsi-fungsi ini.
    # if hasattr({module_name}, 'my_custom_function'):
    #     {module_name}.my_custom_function()
    # if hasattr({module_name}, 'add_two_numbers'):
    #     result = {module_name}.add_two_numbers(50, 75)
    #     print(f"Hasil penjumlahan dari fungsi kustom: {{result}}")

    print("\\nUntuk menjalankan aplikasi ini, Anda memerlukan '{main_app_file_name}' dan file")
    print("'{module_name}.*.so' (atau '.pyd' di Windows) yang dibuat oleh Cython.")
    print("Jika Anda di Termux dan ada error 'dlopen failed', pindahkan kedua file")
    print("ini ke direktori HOME Termux Anda (~), lalu jalankan dari sana.")
"""
    with open(main_app_file_name, 'w') as f:
        f.write(main_app_content)
    print(f"'{main_app_file_name}' (aplikasi utama) dibuat.")

    print("\nProses Obfuskasi Cython Selesai!")
    print(f"Untuk menjalankan aplikasi ini: 'python {main_app_file_name}'")
    
    compiled_so_file = ""
    for f in os.listdir('.'):
        if f.startswith(module_name) and (f.endswith('.so') or f.endswith('.pyd')):
            compiled_so_file = f
            break
    
    if compiled_so_file:
        print(f"Anda akan menemukan file '{compiled_so_file}' yang dikompilasi di direktori ini.")
    else:
        print("Peringatan: Tidak dapat menemukan file modul yang dikompilasi (.so/.pyd). Mungkin ada masalah dalam kompilasi.")

    if "ANDROID_ROOT" in os.environ and platform.system() == "Linux":
        print("\nCatatan Penting untuk Termux:")
        if compiled_so_file:
            print(f"Jika Anda mendapat error 'dlopen failed', pindahkan '{main_app_file_name}' dan")
            print(f"'{compiled_so_file}' (file hasil kompilasi) ke direktori HOME Termux Anda (`~`).")
            print(f"Misal: 'mv {main_app_file_name} ~ && mv {compiled_so_file} ~'")
            print(f"Kemudian jalankan dari direktori HOME: 'cd ~ && python {main_app_file_name}'")
        else:
            print("Peringatan Termux: Modul kompilasi tidak ditemukan, tidak bisa memberikan instruksi pemindahan.")
        
    clean_up_cython_build(module_name, pyx_file_name, setup_file_name, original_input_is_py)


if __name__ == "__main__":
    # Membersihkan layar konsol saat skrip obf.py dimulai
    # 'cls' untuk Windows, 'clear' untuk Linux/macOS/Termux
    os.system('cls' if sys.platform.startswith('win') else 'clear')

    user_input_file_name = get_user_file_input()
    obfuscate_with_cython_process(user_input_file_name)
    sys.exit(0) # Keluar setelah proses selesai