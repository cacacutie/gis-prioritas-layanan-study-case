# Studi Kasus GIS: Analisis Kedekatan Laporan terhadap Aset Layanan

Proyek pembelajaran ini berdasarkan webinar **“Career and Competition in the Industrial Era with GIS”**, yang membahas penggunaan GIS di industri, pengelolaan aset, Python, pengolahan data, dan web mapping.

## Studi kasus
Simulasi untuk menemukan aset layanan terdekat dari laporan warga. Program menghitung jarak garis lurus dengan rumus Haversine, mengelompokkan kedekatan, menyimpan tabel CSV, dan membuat visualisasi HTML mandiri yang tidak membutuhkan API key atau tile peta eksternal.

## Teknologi
- Python
- Pandas
- Rumus Haversine
- HTML/CSS/JavaScript untuk visualisasi titik interaktif

## Menjalankan di Windows / VS Code
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python main.py
```
Jika PowerShell menolak aktivasi environment:
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.venv\Scripts\Activate.ps1
```

Sesudah program selesai, buka `output/peta_gis_interaktif.html` di browser. Hasil tabel tersimpan di `output/hasil_analisis_gis.csv`.

## Struktur
```text
gis-prioritas-layanan-study-case/
├── main.py
├── requirements.txt
├── README.md
├── .gitignore
└── output/  # dibuat otomatis saat program dijalankan
```

## Upload ke GitHub
1. Buka https://github.com/new.
2. Nama repository: `gis-prioritas-layanan-study-case`.
3. Pilih Public bila ingin menjadikannya portofolio.
4. Jangan centang opsi untuk membuat README baru.
5. Klik **Create repository**.
6. Pilih **Add file → Upload files**.
7. Upload `main.py`, `requirements.txt`, `README.md`, dan `.gitignore`.
8. Jangan upload `.venv`; folder `output` tidak wajib diunggah.
9. Klik **Commit changes**.

## Batasan
Data dan koordinat merupakan data sintetis, bukan data resmi atau hasil survei. Jarak adalah jarak garis lurus, bukan jarak jalan atau waktu tempuh. Visualisasi HTML menampilkan posisi relatif, bukan peta geografis berskala. Jangan gunakan untuk keputusan layanan publik nyata.
