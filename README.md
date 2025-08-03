# CythonOBF
Secure your Python logic! This repo showcases Cython-based obfuscation to compile Python into highly protected binary modules.

# 🛡️ CythonOBF: Otomatisasi Obfuskasi Kode Python dengan Cython

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/n1k4xryougaaa/CythonOBF/blob/main/LICENSE)
[![Python Version](https://img.shields.io/badge/python-3.x-blue.svg)](https://www.python.org/)

CythonOBF adalah utilitas Python yang dirancang untuk secara otomatis **mengobfusasi dan mengkompilasi file kode sumber Python Anda menjadi modul biner** (seperti `.so` di Linux/macOS/Android atau `.pyd` di Windows) menggunakan **Cython**. Proyek ini bertujuan untuk **melindungi logika inti** aplikasi Python Anda dari *reverse engineering*, sekaligus menyediakan skrip peluncur yang informatif untuk modul yang sudah diobfuskasi.

---

## Bagaimana Kode `obf.py` Ini Bekerja?

Skrip `obf.py` adalah inti dari proyek ini. Ini mengotomatiskan seluruh alur kerja Cython, mulai dari mengambil file Python Anda hingga menghasilkan modul biner yang dapat didistribusikan. Berikut adalah penjelasan langkah-demi-langkah dari prosesnya:

### 1. Pengecekan Prasyarat Cython (`CYTHON_AVAILABLE` Check)

* Skrip pertama-tama memeriksa apakah pustaka **Cython** sudah terinstal di sistem Anda.
* Jika tidak ditemukan, skrip akan mencetak pesan *error* dan memberikan instruksi instalasi (`pip install cython`), termasuk saran khusus untuk lingkungan Termux (`pkg install clang` dan `python-dev`). Ini memastikan Anda memiliki lingkungan yang tepat sebelum melanjutkan.

### 2. Input Pengguna (`get_user_file_input()` Function)

* Fungsi ini bertanggung jawab untuk berinteraksi dengan pengguna dan mendapatkan nama file Python (`.py`) yang ingin diobfuskasi.
* Ini memiliki *loop* validasi untuk memastikan input tidak kosong dan file yang dimasukkan benar-benar ada di direktori saat ini. Ini mencegah *error* pada tahap awal.

### 3. Proses Obfuskasi Utama (`obfuscate_with_cython_process()` Function)

Ini adalah fungsi orkestrator yang mengelola seluruh alur kerja:

* **Penentuan Nama File Dinamis**:
    * Mengambil nama dasar file input (tanpa ekstensi, misal `script` dari `script.py`).
    * Mendefinisikan `pyx_file_name` (misal `script.pyx`), `module_name` (misal `script_module`), `setup_file_name` (`setup_cython_build.py`), dan `main_app_file_name` (misal `main_script_app.py`) secara dinamis berdasarkan input pengguna. Ini memastikan setiap *output* konsisten dengan nama file asli Anda.
* **Konversi `.py` ke `.pyx`**:
    * Jika file input adalah `.py`, skrip akan menggunakan `shutil.copyfile()` untuk menyalin konten file Python asli Anda ke file baru dengan ekstensi `.pyx`. Ini penting karena Cython bekerja dengan file `.pyx` sebagai input utamanya.
    * **Catatan tentang *Encoding***: `shutil.copyfile()` menyalin file byte-per-byte, membuatnya *agnostik* terhadap *encoding* (UTF-8, Latin-1, dll.). Ini adalah metode paling aman untuk memastikan integritas konten file Anda saat disalin untuk kompilasi Cython.
* **Pembuatan `setup_cython_build.py`**:
    * Sebuah *script* `setup.py` temporer dibuat. File ini adalah konfigurasi standar yang digunakan oleh `setuptools` (yang bekerja sama dengan Cython) untuk memberi tahu bagaimana cara mengkompilasi file `.pyx` Anda menjadi modul ekstensi.
* **Kompilasi Cython (`subprocess.run()`):**
    * Menggunakan `subprocess.run()` untuk menjalankan perintah kompilasi Cython. Perintah ini pada dasarnya adalah `python setup_cython_build.py build_ext --inplace`.
    * Sebelum kompilasi, skrip akan mencari dan menghapus file modul biner (`.so`/`.pyd`) lama yang mungkin ada dengan nama yang sama, mencegah konflik.
    * Jika kompilasi berhasil, pesan "Kompilasi Cython berhasil!" akan dicetak. Jika ada *error* (misalnya, kompilator C/C++ tidak ditemukan, atau ada *error* sintaksis dalam kode Cython), *error* tersebut akan ditangkap dan pesan *debug* akan ditampilkan.
* **Pembuatan `main_aplikasi_app.py`**:
    * Setelah kompilasi berhasil, skrip ini membuat file peluncur Python baru.
    * File peluncur ini akan mengimpor modul biner yang baru dibuat (misal, `script_module`).
    * **Penting**: File peluncur ini secara spesifik mencoba untuk:
        * Mencetak semua anggota (fungsi, kelas, variabel) yang tersedia di dalam modul biner menggunakan `dir({module_name})`. Ini membantu Anda mengetahui apa yang bisa Anda panggil dari kode asli Anda.
        * Secara eksplisit mencoba menginisialisasi **kelas `hello` dan memanggil metode `print_hello()`** dari modul yang diobfuskasi, berdasarkan struktur `script.py` yang Anda berikan. Ini memastikan *output* yang Anda inginkan akan ditampilkan.
        * Menyertakan bagian komentar untuk memanggil fungsi-fungsi umum lainnya (seperti `my_custom_function`), yang bisa diaktifkan pengguna jika sesuai dengan file aslinya.
    * Memberikan instruksi yang jelas kepada pengguna tentang cara menjalankan aplikasi yang diobfuskasi, termasuk catatan khusus untuk pengguna Termux mengenai masalah `dlopen` dan pemindahan file.
* **Pembersihan File Sementara (`clean_up_cython_build()` Function)**:
    * Setelah semua proses kompilasi dan pembuatan file selesai (berhasil atau gagal), fungsi ini dipanggil untuk menghapus file-file perantara seperti `script.c`, `setup_cython_build.py`, dan `script.pyx` (jika itu adalah salinan sementara dari file `.py` asli). Ini menjaga direktori proyek Anda tetap bersih dan hanya menyisakan `obf.py`, `main_namafileanda_app.py`, dan modul biner yang diobfuskasi.

---

## ✨ Fitur Utama

* **Kompilasi ke Kode Mesin**: Mengubah kode Python menjadi modul biner (`.so` atau `.pyd`), yang jauh lebih sulit dibaca daripada *bytecode* Python.
* **Otomatisasi Penuh**: Mengelola seluruh alur kerja Cython dari input `.py` hingga *output* modul biner yang siap dijalankan.
* **Skrip Peluncur Otomatis**: Menghasilkan file Python (`main_namafileanda_app.py`) yang secara dinamis mengimpor dan mengeksekusi modul yang diobfuskasi.
* **Inspeksi Modul**: Skrip peluncur menampilkan anggota (fungsi, kelas) yang tersedia di modul yang diobfuskasi, membantu Anda berinteraksi dengannya.
* **Pembersihan Otomatis**: Menghapus semua file perantara (`.pyx`, `.c`, `setup_*.py`, `build/`) setelah kompilasi berhasil.
* **Dukungan Lintas Platform**: Proses obfuskasi dan kompilasi didukung di Linux, Termux (Android), Windows, dan macOS.

---

## 💪 Persyaratan Sistem

Pastikan Anda memiliki prasyarat berikut sebelum menjalankan `obf.py`:

* **Python 3.x** (disarankan 3.8 atau lebih baru)
* **pip**
* **Cython**
* **Kompilator C/C++**: GCC/Clang (Linux/macOS/Termux) atau Microsoft Visual C++ Build Tools (Windows).
* **Python Development Headers**: `python3-dev` (Linux), `python-dev` (Termux).

### Instalasi Dependensi

Instal dependensi via `pip` dan *package manager* OS Anda:

```bash
# Untuk Linux (Debian/Ubuntu)
sudo apt update
sudo apt install python3-dev build-essential  # build-essential menyediakan GCC
pip install cython

# Untuk Termux (Android)
pkg update && pkg upgrade
pkg install python python-dev clang make
pip install cython

# Untuk Windows
# 1. Unduh & instal Python 3.x dari python.org (centang "Add Python to PATH")
# 2. Unduh "Build Tools for Visual Studio" dari [visualstudio.microsoft.com/downloads](https://visualstudio.microsoft.com/downloads)
#    Saat instalasi, pilih "Desktop development with C++" workload.
# 3. Buka Command Prompt (atau Developer Command Prompt for VS)
pip install cython

# Untuk macOS
xcode-select --install # Instal Xcode Command Line Tools
pip install cython

🚀 Penggunaan
Klon Repositori:

Bash

git clone [https://github.com/n1k4xryougaaa/CythonOBF.git](https://github.com/n1k4xryougaaa/CythonOBF.git)
cd CythonOBF
Siapkan File Python Anda:
Tempatkan file Python (.py) yang ingin Anda obfusasi (misalnya, my_app_logic.py) di direktori yang sama dengan obf.py.

Contoh script.py:

Python

# script.py
class hello:
    def print_hello(self):
        print("""
Source Obfuscated with Chimera
The lost Source - KEY

""")

if __name__ == '__main__':
    import os
    import sys
    # Clear screen based on OS (hanya efektif saat dijalankan langsung, tidak saat diimpor sebagai modul)
    os.system('clear' if 'linux' in sys.platform.lower() else 'cls')
    obj = hello()
    obj.print_hello()
```
Jalankan Skrip Obfuskasi obf.py:

Bash

python obf.py
Anda akan diminta untuk memasukkan nama file Python Anda:
Masukkan nama file Python yang ingin diobfuskasi (misal: my_app.py): 
Ketik nama file Anda (misal, script.py) dan tekan Enter.

Skrip akan menampilkan log proses kompilasi Cython secara real-time:

--- Memulai Obfuskasi dengan Cython untuk 'script.py' ---
Konten 'script.py' disalin ke 'script.pyx'.
'setup_cython_build.py' (script kompilasi) dibuat.
Memulai kompilasi 'script.pyx' ke modul C/C++...
Kompilasi Cython berhasil!
'main_script_app.py' (aplikasi utama) dibuat.

Proses Obfuskasi Cython Selesai!
Untuk menjalankan aplikasi ini: 'python main_script_app.py'
Anda akan menemukan file 'script_module.cpython-312.so' (atau '.pyd') yang dikompilasi di direktori ini.

Catatan Penting untuk Termux:
Jika Anda mendapat error 'dlopen failed', pindahkan 'main_script_app.py' dan
'script_module.cpython-312.so' (file hasil kompilasi) ke direktori HOME Termux Anda (`~`).
Misal: 'mv main_script_app.py ~ && mv script_module.cpython-312.so ~'
Kemudian jalankan dari direktori HOME: 'cd ~ && python main_script_app.py'

--- Membersihkan file sementara Cython ---
Menghapus file C sementara: script.c
Menghapus file setup: setup_cython_build.py
Menghapus file .pyx sementara: script.pyx
Jalankan Aplikasi yang Diobfuskasi:

Setelah proses obfuskasi selesai, Anda akan menemukan:

main_NAMAFILENDA_app.py: Skrip peluncur.

NAMAFILENDA_module.cpython-VERSI.so (atau .pyd di Windows): Modul biner yang diobfuskasi.

Jalankan aplikasi diobfuskasi Anda:

Bash

python main_NAMAFILENDA_app.py
(Ganti NAMAFILENDA dan VERSI sesuai dengan nama file yang dihasilkan dari kompilasi Anda, misalnya main_script_app.py dan script_module.cpython-312.so)

Contoh Output:

Memanggil fungsi dari modul Cython yang diobfuskasi...
-----------------------------------------------------
Modul 'script_module' berhasil diimpor.
Anggota yang tersedia di modul ini (fungsi, kelas, dll.):
['__builtins__', '__doc__', '__file__', '__loader__', '__name__', '__package__', '__spec__', '__test__', 'hello']
-----------------------------------------------------

  Source Obfuscated with Chimera
       The lost Source - KEY

Untuk menjalankan aplikasi ini, Anda memerlukan 'main_script_app.py' dan file
'script_module.*.so' (atau '.pyd' di Windows) yang dibuat oleh Cython.
Jika Anda di Termux dan ada error 'dlopen failed', pindahkan kedua file
ini ke direktori HOME Termux Anda (~), lalu jalankan dari sana.
Selamat! Jika Anda melihat output yang mirip, kode Anda berhasil diobfuskasi dan dijalankan dari modul biner.

📂 Struktur Repositori Ini
CythonOBF/
├── obf.py                      # Skrip utama untuk melakukan obfuskasi
├── main_namafileanda_app.py    # (Dihasilkan oleh obf.py) Skrip peluncur untuk aplikasi yang diobfuskasi
├── namafileanda_module.cpython-312.so # (Dihasilkan oleh obf.py) Modul inti yang diobfuskasi dan dikompilasi
├── .gitignore                  # Mengabaikan file sumber asli dan file perantara Cython
├── README.md                   # File keterangan ini
└── LICENSE                     # File lisensi proyek
Catatan Penting: Kode sumber asli Anda (misalnya script.py), serta semua file perantara yang dihasilkan Cython (.pyx, .c, setup_cython_build.py, dan direktori build/), TIDAK DIUNGGAH ke repositori ini. Ini adalah tujuan utama obfuskasi, menjaga kerahasiaan logika inti Anda.

📜 Lisensi
Proyek ini dilisensikan di bawah Lisensi MIT. Lihat file LICENSE untuk detail lebih lanjut.

🤝 Kontribusi
Kontribusi dan saran sangat dihargai! Jika Anda memiliki ide untuk perbaikan atau menemukan masalah, silakan buka issue atau kirim pull request.
