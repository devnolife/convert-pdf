# Konversi Dokumen DOCX ke PDF dan Pengiriman ke Server Penyimpanan

Aplikasi ini adalah layanan API sederhana berbasis Flask yang memungkinkan pengguna untuk mengunggah file `.docx`, mengonversinya menjadi format PDF, dan kemudian mengirimkan file PDF tersebut ke server penyimpanan.

## Fitur

- Mengunggah file `.docx` melalui endpoint API.
- Mengonversi file `.docx` menjadi PDF menggunakan library `docx2pdf`.
- Mengirim file PDF yang telah dikonversi ke server penyimpanan.
- Menghapus file sementara setelah proses selesai untuk menjaga kebersihan penyimpanan.

## Teknologi yang Digunakan

- **Python 3.x**
- **Flask**: Framework web untuk membuat API.
- **docx2pdf**: Library untuk konversi file `.docx` ke PDF.
- **requests**: Library untuk melakukan permintaan HTTP ke server penyimpanan.

## Prasyarat

- **Python 3.x** harus terinstal di sistem Anda.
- **Microsoft Word** (untuk Windows) atau **LibreOffice** (untuk macOS/Linux) diperlukan oleh `docx2pdf` untuk melakukan konversi.
- Koneksi internet untuk mengirim file ke server penyimpanan.

## Instalasi

1. **Kloning repositori atau salin kode sumber** ke direktori pilihan Anda.

2. **Buat virtual environment** (opsional tapi direkomendasikan):

   ```bash
   python -m venv env
   source env/bin/activate  # Untuk Linux/Mac
   env\Scripts\activate     # Untuk Windows
   ```

3. **Instal dependensi** menggunakan `pip`:

   ```bash
   pip install -r requirements.txt
   ```

   Jika Anda tidak memiliki file `requirements.txt`, buat file tersebut dengan isi berikut:

   ```
   Flask
   docx2pdf
   requests
   ```

   Lalu jalankan perintah di atas.

## Konfigurasi

Tidak ada konfigurasi khusus yang diperlukan. Pastikan saja URL server penyimpanan sudah benar dalam kode:

```python
url = "https://storage"
```

Jika diperlukan, ganti URL tersebut dengan URL server penyimpanan Anda.

## Menjalankan Aplikasi

Setelah semua dependensi terinstal, Anda dapat menjalankan aplikasi dengan perintah:

```bash
python app.py
```

Aplikasi akan berjalan dalam mode debug di `http://localhost:5000/`.

## Menggunakan API

### Endpoint: `/convert`

- **Metode HTTP:** `POST`
- **Deskripsi:** Menerima file `.docx`, mengonversinya menjadi PDF, dan mengirimkannya ke server penyimpanan.

#### Parameter

- **file**: File `.docx` yang akan diunggah. Dikirim sebagai `multipart/form-data`.

#### Respons

- **Sukses:** Mengembalikan respons dari server penyimpanan.
- **Gagal:** Mengembalikan pesan kesalahan dalam format JSON.

#### Contoh Permintaan

**Menggunakan `curl`:**

```bash
curl -X POST -F "file=@/path/ke/file_anda.docx" http://localhost:5000/convert
```

**Menggunakan Python `requests`:**

```python
import requests

url = 'http://localhost:5000/convert'
files = {'file': open('/path/ke/file_anda.docx', 'rb')}

response = requests.post(url, files=files)
print(response.text)
```

## Penanganan Kesalahan

- Jika tidak ada file yang dikirim, API akan mengembalikan status **400 Bad Request** dengan pesan:

  ```json
  {"error": "Tidak ada file yang dikirim"}
  ```

- Jika tidak ada file yang dipilih, API akan mengembalikan status **400 Bad Request** dengan pesan:

  ```json
  {"error": "Tidak ada file yang dipilih"}
  ```

- Jika terjadi kesalahan saat konversi, API akan mengembalikan status **500 Internal Server Error** dengan pesan:

  ```json
  {"error": "Konversi gagal", "message": "Detail kesalahan"}
  ```

- Jika gagal mengirim file ke server penyimpanan, API akan mengembalikan status **500 Internal Server Error** dengan pesan:

  ```json
  {"error": "Gagal mengirim file ke server penyimpanan", "message": "Detail kesalahan"}
  ```

## Struktur Proyek

```
├── app.py                # Kode utama aplikasi Flask
├── requirements.txt      # Daftar dependensi Python
├── uploads/              # Direktori untuk menyimpan file yang diunggah sementara
├── outputs/              # Direktori untuk menyimpan file PDF hasil konversi sementara
└── README.md             # Dokumentasi aplikasi (file ini)
```

## Catatan Penting

- **Hak Akses File:**

  Pastikan aplikasi memiliki izin untuk membaca, menulis, dan menghapus file di direktori `uploads/` dan `outputs/`.

- **Keamanan:**

  - Selalu validasi dan sanitasi input dari pengguna untuk mencegah serangan seperti path traversal.
  - Pertimbangkan untuk menambahkan mekanisme autentikasi dan otorisasi jika aplikasi akan digunakan secara publik.
  - Jalankan aplikasi di server produksi menggunakan server WSGI seperti Gunicorn atau uWSGI, bukan dalam mode debug.

- **Dependensi `docx2pdf`:**

  Library `docx2pdf` memerlukan Microsoft Word (untuk Windows) atau LibreOffice (untuk macOS/Linux) terinstal di sistem untuk melakukan konversi. Pastikan aplikasi memiliki akses ke aplikasi tersebut.

- **Penanganan Nama File:**

  Kode menggunakan nama file asli yang dikirim oleh pengguna. Pastikan bahwa nama file tersebut unik untuk menghindari konflik. Jika ada kemungkinan nama file yang sama dikirim oleh beberapa pengguna, pertimbangkan untuk menambahkan mekanisme penamaan ulang file.

## Kontribusi

Kontribusi sangat diterima. Silakan lakukan fork repositori ini dan ajukan pull request untuk perbaikan atau penambahan fitur.

## Lisensi

Aplikasi ini dilisensikan di bawah [MIT License](LICENSE).

## Terima Kasih

Terima kasih telah menggunakan aplikasi ini. Semoga bermanfaat!
