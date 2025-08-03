# 🛡️ CythonOBF: Otomatisasi Obfuskasi Kode Python dengan Cython

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/n1k4xryougaaa/CythonOBF/blob/main/LICENSE)
[![Python Version](https://img.shields.io/badge/python-3.x-blue.svg)](https://www.python.org/)

**CythonOBF** adalah utilitas Python yang dirancang untuk secara otomatis **mengobfusasi dan mengkompilasi file kode sumber Python Anda menjadi modul biner** (seperti `.so` di Linux/macOS/Android atau `.pyd` di Windows) menggunakan **Cython**. Proyek ini bertujuan untuk **melindungi logika inti** aplikasi Python Anda dari *reverse engineering*, sekaligus menyediakan skrip peluncur yang informatif untuk modul yang sudah diobfuskasi.

---

## 🔍 Bagaimana Kode `obf.py` Ini Bekerja?

Skrip `obf.py` adalah inti dari proyek ini. Ini mengotomatiskan seluruh alur kerja Cython, mulai dari mengambil file Python Anda hingga menghasilkan modul biner yang dapat didistribusikan. Berikut adalah penjelasan langkah-demi-langkah dari prosesnya:

### 1. Pengecekan Prasyarat Cython (`CYTHON_AVAILABLE` Check)

* Memeriksa apakah pustaka **Cython** sudah terinstal.
* Jika tidak ditemukan, mencetak pesan *error* dan memberikan instruksi instalasi (`pip install cython`), termasuk saran khusus untuk Termux (`pkg install clang` dan `python-dev`).

### 2. Input Pengguna (`get_user_file_input()` Function)

* Berinteraksi dengan pengguna untuk mendapatkan nama file Python (`.py`) yang ingin diobfuskasi.
* Memiliki *loop* validasi untuk memastikan file benar-benar ada di direktori saat ini.

### 3. Proses Obfuskasi Utama (`obfuscate_with_cython_process()` Function)

#### a. Penentuan Nama File Dinamis

* Mengambil nama dasar file (tanpa ekstensi), misalnya `script` dari `script.py`.
* Menentukan nama: `pyx_file_name`, `module_name`, `setup_file_name`, dan `main_app_file_name`.

#### b. Konversi `.py` ke `.pyx`

* Jika input `.py`, menggunakan `shutil.copyfile()` untuk menyalin kontennya ke `.pyx`.
* Catatan: `shutil.copyfile()` bersifat *encoding-agnostik*, aman untuk semua format teks.

#### c. Pembuatan `setup_cython_build.py`

* Membuat skrip `setup.py` untuk mengatur proses kompilasi Cython.

#### d. Kompilasi dengan Cython (`subprocess.run()`)

* Menjalankan perintah: `python setup_cython_build.py build_ext --inplace`.
* Menghapus file modul biner lama jika ada.
* Menangkap dan mencetak kesalahan jika kompilasi gagal.

#### e. Pembuatan `main_aplikasi_app.py`

* Membuat file peluncur Python baru.
* Mengimpor dan menjalankan modul biner (`script_module`).
* Mencetak semua anggota modul (`dir(...)`) dan mencoba memanggil kelas `hello` dan metode `print_hello()`.

#### f. Pembersihan File Sementara (`clean_up_cython_build()` Function)

* Menghapus file perantara: `.c`, `.pyx`, `setup_*.py`, direktori `build/`.

---

## ✨ Fitur Utama

* **Kompilasi ke Kode Mesin**: Mengubah Python menjadi `.so` atau `.pyd` yang sulit dibaca.
* **Otomatisasi Penuh**: Dari `.py` ke modul biner siap pakai.
* **Skrip Peluncur Otomatis**: `main_namafileanda_app.py`.
* **Inspeksi Modul**: Tampilkan anggota modul dengan `dir(...)`.
* **Pembersihan Otomatis**: Menghapus file Cython yang tidak diperlukan.
* **Dukungan Lintas Platform**: Linux, Termux, Windows, dan macOS.

---

## 💻 Persyaratan Sistem

* **Python 3.x** (disarankan 3.8+)
* **pip**
* **Cython**
* **Kompilator C/C++**: GCC/Clang/MSVC
* **Python Development Headers**

### Instalasi Dependensi

```bash
# Linux (Debian/Ubuntu)
sudo apt update
sudo apt install python3-dev build-essential
pip install cython

# Termux (Android)
pkg update && pkg upgrade
pkg install python python-dev clang make
pip install cython

# Windows
# 1. Instal Python dari python.org (centang "Add to PATH")
# 2. Instal "Build Tools for Visual Studio" dari visualstudio.microsoft.com/downloads
#    Pilih workload: "Desktop development with C++"
# 3. Jalankan:
pip install cython

# macOS
xcode-select --install
pip install cython
```

---

## 🚀 Penggunaan

### Klon Repositori

```bash
git clone https://github.com/n1k4xryougaaa/CythonOBF.git
cd CythonOBF
```

### Siapkan File Python Anda

Letakkan file `.py` Anda di direktori yang sama.

Contoh: `script.py`

```python
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
    os.system('clear' if 'linux' in sys.platform.lower() else 'cls')
    obj = hello()
    obj.print_hello()
```

### Jalankan Skrip Obfuskasi

```bash
python obf.py
```

Masukkan nama file saat diminta, misalnya: `script.py`.

### Contoh Output Terminal

```
--- Memulai Obfuskasi dengan Cython untuk 'script.py' ---
Konten 'script.py' disalin ke 'script.pyx'.
'setup_cython_build.py' (script kompilasi) dibuat.
Memulai kompilasi 'script.pyx' ke modul C/C++...
Kompilasi Cython berhasil!
'main_script_app.py' (aplikasi utama) dibuat.

Proses Obfuskasi Cython Selesai!
Untuk menjalankan aplikasi ini: 'python main_script_app.py'
```

Jika sukses, file berikut akan muncul:

* `main_script_app.py`
* `script_module.cpython-312.so` (atau `.pyd` di Windows)

---

## ⚠️ Catatan Penting untuk Termux

Jika muncul error `dlopen failed`:

```bash
mv main_script_app.py ~
mv script_module.cpython-312.so ~
cd ~
python main_script_app.py
```

---

## ▶️ Jalankan Aplikasi yang Diobfuskasi

```bash
python main_script_app.py
```

Contoh Output:

```
Memanggil fungsi dari modul Cython yang diobfuskasi...
-----------------------------------------------------
Modul 'script_module' berhasil diimpor.
Anggota yang tersedia di modul ini:
['__builtins__', '__doc__', '__file__', '__loader__', '__name__', '__package__', '__spec__', '__test__', 'hello']
-----------------------------------------------------

  Source Obfuscated with Chimera
       The lost Source - KEY
```

---

## 📂 Struktur Repositori

```
CythonOBF/
├── obf.py                      # Skrip utama
├── main_namafileanda_app.py    # (Dihasilkan) Skrip peluncur
├── namafileanda_module.cpython-312.so # (Dihasilkan) Modul biner
├── .gitignore                  # File ignore
├── README.md                   # Keterangan proyek
└── LICENSE                     # Lisensi MIT
```

**Catatan:** File sumber asli (`.py`), serta file perantara seperti `.pyx`, `.c`, `setup_cython_build.py`, dan `build/` **tidak diunggah** ke repositori ini demi menjaga kerahasiaan kode Anda.

---

## 📜 Lisensi

Proyek ini dilisensikan di bawah **MIT License**. Lihat file LICENSE untuk detail.

---

## 🤝 Kontribusi

Kontribusi dan saran sangat dihargai!
Silakan buka issue atau kirim pull request jika Anda memiliki ide atau menemukan masalah.

---

Jika Anda ingin saya jadikan ini file `.md` yang siap diunduh, tinggal beri tahu saja.
