# Profil Data Sumber — insightera-andina (2026-09-14)

> Artefak Supervisor 2. Profil read-only; **tidak ada nilai PII yang disalin** ke dokumen ini.
> Reproduksi: `python audit/scripts/profil_sumber_data.py` (butuh `pandas`, `openpyxl`, `scipy`).

## 1. Baseline berkas (SHA-256)

| Berkas | SHA-256 |
|---|---|
| `Data akademik 2012 - 2016.xlsx` | `82d973422ba4e1493b7215999cbaa110cb0a13f391192fb250d2d566632077af` |
| `MK SD.xlsx` | `7a08d54fdf2cef6d920065bc36c9f112496bd31feffe1a2e3f62faf3580487d4` |
| `PENDAFTARAN PESERTA YUDISIUM FAKULTAS SAINS (Jawaban).xlsx` | `c689956b4cccb957b2c0e4cfaf9b5225cb6a0fe8a92f0c7e88fff4e35264b77c` |
| `data sintetis krs khs.xlsx` | `8788343b1e9afa1da3e3de58b940f7455c089d8ddd703810a6668442c7fd3a0d` |
| `Syalaisha Andina .pdf` | `fff20b6cee1acaff9a25491ea47a4571f38045a0fd7b12fb1c5e08c88d82daf0` |

Audit berikutnya membandingkan checksum ini untuk mendeteksi perubahan berkas sumber.

---

## 2. `MK SD.xlsx` — kurikulum Sains Data 2025 (riil)

| Properti | Nilai |
|---|---|
| Baris × kolom | 63 × 7 (`Kode Mata Kuliah Baru`, `Mata Kuliah`, `SKS`, `PRAKT`, `SM`, `KATEGORI`, `METODE`) |
| Null / duplikat kode | 0 / 0 |
| Prefiks kode | SD25 48 · WU25 6 · WT25 5 · WI25 3 · KU25 1 |
| KATEGORI | MK WAJIB 35 · PILIHAN KK 2 7 · PILIHAN KK 1 6 · TPB 6 · MKWK 6 · MKU 3 |
| METODE | PBM 27 · NO 22 · CBM 14 |
| SKS | 2 SKS: 31 · 3 SKS: 31 · 4 SKS: 1; PRAKT 1: 30 MK |
| Σ SKS / Σ (SKS+PRAKT) | 159 / 189 (termasuk seluruh MK pilihan) |
| SM (semester kurikulum) | 1:8 · 2:8 · 3:7 · 4:7 · 5:12 · 6:11 · 7:9 · 8:1 |

Kualitas: bersih. Arti `METODE` (PBM/CBM/NO) belum didefinisikan → wajib di data dictionary.

---

## 3. `data sintetis krs khs.xlsx`

### 3.1 `fact_krs`
| Properti | Nilai |
|---|---|
| Baris | 6.495; null 0; duplikat `id_krs` 0 |
| Mahasiswa / prodi | 135 / SD saja |
| Kode MK | 61 unik; **100 % ada di `MK SD`** |
| `sks` | 2: 2.882 · 3: 589 · 4: 3.024; **`sks` = SKS + PRAKT pada 100 %** |
| Semester diambil = semester kurikulum (`SM`) | 99,8 % |
| MK diambil > 1 kali (mengulang) | 0 |
| Angkatan (semester pertama) | 2020 Ganjil 69 · 2021 Ganjil 58 · 2022 Ganjil 8 |
| Semester terakhir | 7 → 128 mhs; 8 → 7 mhs |
| `id_waktu` | W2020GJ … W2025GJ (11), seluruhnya ada di `dim_waktu` |

### 3.2 `fact_khs`
| Properti | Nilai |
|---|---|
| Baris | 952; null 0; duplikat (mhs, semester) 0 |
| `ip_semester` / `ipk` | 2,38–4,00 / 2,49–4,00 |
| `total_sks_diambil` | 2–24, median 22 |
| = Σ `sks` KRS per (mhs, semester) | **100 %** |
| `ipk` = rerata IP berbobot SKS kumulatif | **100 %** (selisih maks 0,01 — pembulatan) |

### 3.3 `dim_waktu`
11 baris; tanggal buatan: Ganjil = `YYYY-08-01`, Genap = `YYYY+1-01-15`.

### 3.4 `ref_yudis_bersih`
| Properti | Nilai |
|---|---|
| Baris | 135 (`id_mahasiswa`, `sks_final`, `ipk_clean`, `predikat`) |
| Predikat | Sangat Memuaskan 106 · Memuaskan 21 · Pujian 8 |
| `sks_final` = Σ SKS KRS sintetis mhs yang sama | **100 %** |
| `ipk_clean` = IPK akhir `fact_khs` mhs yang sama | **6,7 % (9/135)**; selisih −0,20 … +0,20, SD 0,076 |

### 3.5 Pembandingan dengan yudisium riil Sains Data (135 baris)
| Uji | Hasil |
|---|---|
| Multiset `sks_final` vs `Jumlah SKS`/`SKS FINAL` riil | **identik** |
| Jumlah per predikat | **identik** (106 / 21 / 8) |
| Multiset IPK (2 desimal) | **125/135 sama**; 2 IPK riil tersimpan sebagai tanggal Excel |
| KS SKS (sintetis vs riil) | D = 0,000; p = 1,000 (sirkular) |
| KS IPK (sintetis vs riil) | D = 0,022; p ≈ 1,000 (sirkular) |
| Masa studi riil (tahun) | mean 4,38 · median 4,42 · min 3,50 · maks 5,75; ≤ 3,6 tahun: 2 mhs |
| Masa studi sintetis | 7 semester (≈ 3,5 tahun) untuk 128/135 mhs |

**Kesimpulan:** `ref_yudis_bersih` = yudisium riil Sains Data yang dipseudonimkan & dibersihkan. KRS/KHS dibangkitkan agar Σ SKS cocok dengan data itu, tetapi IPK akhirnya tidak.

---

## 4. `Data akademik 2012 - 2016.xlsx` (riil, dipseudonimkan)

### 4.1 `Data Referensi Mahasiswaa`
| Properti | Nilai |
|---|---|
| Baris | 1.377; null 0; duplikat Id 0; format Id `M-<PRODI>-NNN` |
| Prodi | 10: PWK 228 · TG 202 · GT 188 · SI 187 · IF 166 · EL 141 · AR 130 · FI 98 · TL 24 · GL 13 (tanpa SD) |
| Tanggal Masuk | 2012-08-15 … 2016-08-15 (2012: 47 · 2013: 32 · 2014: 41 · 2015: 281 · 2016: 976) |
| Tanggal Keluar | 2016-09-26 … 2024-01-22; keluar < masuk: 0 |
| Status Mahasiswa | **"Lulus" 1.377 (100 %)** |
| IPK | 1,43–3,94, median 2,91 |
| Total SKS / Jumlah MK | 143–166 (median 146) / 49–65 (median 56) |
| Jenis Kelamin | L 812 · P 565 *(atribut sensitif — pertimbangkan untuk tidak dipakai di dashboard)* |

### 4.2 `Data Program Studi`
44 baris (`Kode`, `Nama Program Studi`, `Jumlah Dosen`, `Fakultas`); **`Fakultas` null 44/44**; SD ada (`S1 SAINS DATA`); seluruh kode prodi di Referensi ada di tabel ini.

### 4.3 `Data Kelas`
3.540 baris (`nama_kelas`, `nama_mk`, `kuota`); **45 baris duplikat**; `nama_mk` 1.204 unik; kuota 0–600 (**0: 13**, ≥ 200: 48); **tanpa tahun/semester/prodi/kode MK**; 33 dari 63 nama MK SD ditemukan secara persis.

### 4.4 `Data Kurikulum`
147 baris (`Nama Kurikulum`, `Jumlah SKS Total`); median 144; **0 SKS: 6 kurikulum** (EL-03, FI-03, MA-02, SI-03, TB-01, TF-01); 36–38 SKS: 3 (AR-01, GL-1, TL-1).

### 4.5 `Data KHS`
| Properti | Nilai |
|---|---|
| Baris × kolom | 22.029 × **2 (`IP`, `SKS`)** — tanpa id mahasiswa, tanpa semester |
| Duplikat baris | **15.790 (71,7 %)** |
| IP | 0–4,00; IP = 0: 92 |
| SKS | 12–178; 143 nilai unik; modus 18 (5.019 baris) |
| Pasangan (IPK, Total SKS) Referensi yang muncul sebagai (IP, SKS) | 916/1.377 |

*Inferensi (NOT VERIFIED):* riwayat IPK/SKS kumulatif per semester dari mahasiswa Referensi, dengan kolom kunci terhapus. Tidak dapat digabung ke mahasiswa atau semester.

---

## 5. `PENDAFTARAN PESERTA YUDISIUM FAKULTAS SAINS (Jawaban).xlsx` (riil, **memuat PII**)

| Properti | Nilai |
|---|---|
| Sheet | 20 sheet periode (10 Juni 2024 … 5 Juni 2026) + `NVScriptsProperties` + `DO NOT DELETE - AutoCrat Job Se…` (konfigurasi Google Apps Script) |
| Baris non-kosong | 151: S1 SAINS DATA 108 · Sains Data 27 · S1 MATEMATIKA 2 · S1 KIMIA 1 · tanpa prodi 13 |
| Tanggal Yudisium | 2024-06-10 … 2026-08-14 |
| Skema | **berubah antar-sheet**: 23–49 kolom; sheet 2024 (Jun–Okt) memuat kolom administrasi (No. SKL, BA, berkas, Kaprodi, NIP/NRK, Merged Doc); header berganti nama (`SKS FINAL` ↔ `Jumlah SKS`, `Indeks Prestasi Kumulatif Final` ↔ `IPK`, `No SK Pbb` ↔ `No SK Pembimbing`, kolom tambahan `Teofl`, 4 varian `Tanggal Lahir`) |
| IPK SD | 2,70–3,89; **2 sel tersimpan sebagai tanggal** |
| SKS SD | 144–155 |
| Predikat SD | SM 106 · M 21 · Pujian 8; **11 "Sangat Memuaskan" dengan IPK > 3,50** |
| `MASA STUDI` | teks "X Tahun Y Bulan Z Hari" (perlu parsing) |

**Kolom PII / kuasi-identifier (nama header, nilai tidak dibuka):** Tempat Lahir; Tanggal Lahir (+ varian); Alamat; Judul TA / Judul Tugas Akhir; Dosen Pembimbing 1–3; Penguji Seminar Proposal/Hasil/Sidang; Dosen Wali; Kaprodi; NIP/NRK; jenis NIP/NRK; No SK Pembimbing; Berkas Transkrip Final; Berkas Berita Acara Sidang; Berkas Surat Bebas UKT; Merged Doc ID/URL (BA Yudisium, SKL). Header **tidak** memuat Nama/NIM/Email.

---

## 6. Ringkasan anomali (masukan aturan DQ / katalog cacat E3)

| # | Anomali | Lokasi | Jumlah | Kode cacat |
|---|---|---|---|---|
| 1 | Tabel tanpa kunci bisnis | Data KHS | 22.029 baris | D12 |
| 2 | Baris duplikat | Data KHS / Data Kelas | 15.790 / 45 | D02 |
| 3 | Schema drift antar-periode | Yudisium | 23–49 kolom, ≥ 4 header berganti nama | D08 |
| 4 | Angka tersimpan sebagai tanggal | Yudisium (IPK) | 2 | D09 |
| 5 | Label kategori tidak seragam | Yudisium (prodi) | 2 varian SD | D10 |
| 6 | Nilai referensi tidak masuk akal | Kurikulum SKS 0 / Kelas kuota 0 | 6 / 13 | D11 |
| 7 | Atribut wajib kosong | Program Studi.Fakultas | 44/44 | D01 (kolom) |
| 8 | Baris kosong/tanpa prodi | Yudisium | 13 | D01 |
| 9 | Predikat vs IPK tidak monoton | Yudisium | 11 | pengecualian aturan bisnis (verifikasi) |
| 10 | Inkonsistensi antar-fakta | IPK akhir KHS sintetis vs yudisium | 126/135 | D05 |

---

## 7. Matriks kecocokan sumber ↔ rancangan draf

| Tabel draf | S1 MK SD | Sintetis | Referensi 2012–16 | Prodi | KHS 2012–16 | Yudisium | Status |
|---|---|---|---|---|---|---|---|
| Dim_Mahasiswa | — | id saja | ✔ (masuk, keluar, angkatan) | — | ✖ | pseudonim diperlukan | SEBAGIAN |
| Dim_Program_Studi | — | kode | kode | ✔ (fakultas kosong) | — | label | SEBAGIAN |
| Dim_Waktu | — | ✔ semester (tanggal buatan) | tanggal | — | ✖ | tanggal | SEBAGIAN |
| Dim_Dosen | — | — | — | jumlah saja | — | nama (PII) | ✖ |
| Dim_Mata_Kuliah | ✔ | kode | — | — | — | — | ✔ (SD saja) |
| Dim_Status_Mahasiswa | — | — | 1 nilai | — | — | — | ✖ |
| Fact_KRS | — | ✔ | — | — | — | — | SINTETIS saja |
| Fact_KHS | — | ✔ | — | — | ✖ tanpa kunci | — | SINTETIS saja |
| Fact_Yudisium | — | ref (riil) | ✔ (setara kelulusan) | — | — | ✔ | ✔ (butuh anonimisasi) |
| Fact_Status | — | — | 1 snapshot "Lulus" | — | — | — | ✖ |

**Volume total ± 35 ribu baris.**
