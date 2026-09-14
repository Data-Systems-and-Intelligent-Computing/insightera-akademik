# INSIGHTERA-ANDINA — Data Lakehouse Medallion untuk Data Akademik Perguruan Tinggi

Repositori penelitian tugas akhir untuk topik **Insightera (domain akademik)**.

| | |
|---|---|
| **Mahasiswa** | Syalaisha Andina Putriansyah (122450121) |
| **Program Studi** | Sains Data, Fakultas Sains, ITERA |
| **Pembimbing (menurut draf)** | Luluk Muthoharoh, M.Si · Ardika Satria, M.Si |
| **Judul draf** | *Perancangan dan Implementasi Data Lakehouse Berbasis Arsitektur Medallion untuk Pengelolaan Data Akademik Perguruan Tinggi* |
| **Audit awal** | 2026-09-14 (Supervisor 2) |
| **Target selesai** | ± 1 bulan → **14 Oktober 2026** (4 minggu kerja + 3 hari buffer) |
| **Status penelitian** | **AT RISK** — desain ada, implementasi & bukti eksperimen **belum ada** |

> Dokumen ini berisi **hasil audit** dan **rancangan penelitian yang direkomendasikan**.
> Seluruh perubahan RQ, cakupan data, dan model dimensional di bawah adalah **usulan** dan
> memerlukan **keputusan Supervisor** (lihat §19) sebelum dibekukan.
>
> Rincian audit: [audit/2026-09-14-audit-awal.md](audit/2026-09-14-audit-awal.md) ·
> Register isu: [audit/issue-register.md](audit/issue-register.md) ·
> Profil data: [audit/data-profiling-2026-09-14.md](audit/data-profiling-2026-09-14.md) ·
> Rencana mingguan: [Rencana-eksperimen-bimbingan/](Rencana-eksperimen-bimbingan/README.md)

---

## 1. Ringkasan audit (untuk Supervisor)

**Posisi sekarang.** Andina sudah punya draf skripsi LaTeX 51 halaman. Bab I–III sudah berisi
latar belakang, 3 rumusan masalah, tinjauan pustaka, arsitektur Medallion (Iceberg, Spark,
MinIO, Airflow, Superset, pola AWAP), serta rancangan 6 dimensi dan 4 fakta. **Bab IV–V,
abstrak, kata pengantar, dan lampiran masih templat** (lorem ipsum, tabel provinsi contoh,
kode contoh `incmatrix`). **Belum ada kode, konfigurasi, log, atau hasil apa pun.** Data yang
dilampirkan terdiri atas 4 berkas XLSX.

**Hambatan utama.** Model dimensional pada draf **tidak bisa dibangun dari data yang ada**, dan
rencana evaluasinya **tidak menguji apa pun secara bermakna**. Ada tiga penyebab:

1. `Data KHS` riil (22.029 baris) **hanya berisi kolom `IP` dan `SKS`**. Tidak ada id mahasiswa
   maupun semester, dan 71,7 % barisnya duplikat. Akibatnya Fact_KHS riil tidak mungkin dibentuk.
2. Sheet `ref_yudis_bersih` di berkas **"data sintetis"** ternyata adalah **data yudisium riil
   Sains Data** yang sudah dipseudonimkan (distribusi SKS dan predikat identik, IPK sama pada
   125/135 baris). Uji KS "fidelitas data sintetis vs data asli" (Tabel 3.4) karena itu
   **sirkular**: data sintetis dibangkitkan dari data riil yang sama.
3. Berkas yudisium memuat **tempat/tanggal lahir, alamat, judul TA, nama dosen, NIP/NRK, dan URL
   dokumen**. Ini bertentangan dengan klaim di §3.2 draf bahwa data "tidak memuat informasi
   identitas individu".

**Kabar baik.** Data yang ada **cukup** untuk penelitian yang lebih sempit dan lebih kuat. Dua
sumber kelulusan riil dengan skema berbeda (Referensi Mahasiswa 2012–2016 dan Yudisium Sains
Data 2024–2026) bisa diintegrasikan ke **satu fakta kelulusan**. Selain itu, cacat data riil yang
ditemukan audit (skema berubah antar-sheet, IPK tersimpan sebagai tanggal, label prodi tidak
seragam, SKS kurikulum = 0, baris duplikat, KHS tanpa kunci) adalah **bahan uji alami** untuk
mekanisme *quality gate* AWAP.

**Rekomendasi inti.** Ubah skripsi dari "membangun lakehouse + dashboard" menjadi
**"merancang, mengimplementasikan, dan mengevaluasi lakehouse Medallion dengan quality gate
Write-Audit-Publish"**. Evaluasinya terukur pada tiga aspek: **kebenaran Gold** (rekonsiliasi
dengan oracle independen), **efektivitas gate** (fault injection), dan **overhead kinerja**
(scale factor × WAP on/off). Dashboard tetap dibuat sebagai luaran artefak, tetapi bukan klaim
ilmiah utama.

| Kesiapan | Status |
|---|---|
| Skripsi | **NOT READY** (gate T1, T3, T4, T5, T7, T8, T9 gagal karena belum ada bukti) |
| Publikasi | **RESEARCH-STAGE** (kontribusi potensial ada; verifikasi literatur eksternal belum dilakukan) |
| Kelayakan 1 bulan | **Layak hanya jika** cakupan dipersempit sesuai D-01…D-05 pada Minggu 1 |

Jumlah temuan: **4 KRITIS · 9 MAYOR · 5 MINOR · 3 SARAN**. Rincian ada di
[audit/issue-register.md](audit/issue-register.md).

---

## 2. Apa yang sudah dikerjakan Andina (breakdown draf)

Sumber: `Syalaisha Andina .pdf` (LaTeX, 51 hlm., dibuat 2026-09-11).

| Bagian | Isi saat ini | Status | Catatan audit |
|---|---|---|---|
| Halaman awal | Pengesahan, orisinalitas, persetujuan publikasi | Templat sebagian | Persetujuan publikasi menyebut *"Proposal Tugas Akhir"*, sedangkan pengesahan menyebut *"Naskah Skripsi untuk Sidang Akhir"* |
| Abstrak / Abstract | Lorem ipsum, kata kunci "ini, itu" | **Kosong** | — |
| Motto, persembahan, kata pengantar | Teks templat ("Prof. Xxxx") | **Kosong** | — |
| 1.1 Latar belakang | Volume data → DW terbatas → lakehouse → Medallion | Draf ada | Belum ada masalah **spesifik ITERA** yang terukur (sistem sumber apa, masalah apa) |
| 1.2 Rumusan masalah | 3 RQ "Bagaimana merancang / menyajikan / mengukur" | Draf ada | Berupa tugas implementasi, bukan pertanyaan yang bisa dijawab dengan bukti (M-01) |
| 1.3 Tujuan | Cermin RQ | Draf ada | — |
| 1.4 Batasan | Data 2012–2025; mahasiswa, dosen, MK | Draf ada | Tidak sesuai data aktual (M-06) |
| 2.1 Penelitian terdahulu | 3 studi | Tipis | Belum memposisikan kontribusi (M-07) |
| 2.2–2.13 Teori | DW, data lake, lakehouse, Medallion, Kimball, storage, table format, metadata, Spark, Iceberg, Superset, data quality | Draf ada | §2.7–2.13 hampir tanpa sitasi |
| 3.1 Deskripsi | Design Science Research | Draf ada | Siklus evaluasi DSR belum didefinisikan |
| 3.2 Data | Tabel 3.1: KHS, MK, Yudisium; klaim "tanpa identitas" | Draf ada | Klaim privasi **BERTENTANGAN** dengan data (C-03) |
| 3.3 Alur | Gambar 3.1: analisis → perancangan → implementasi → pengujian | Draf ada | Keputusan "sesuai kebutuhan analitik" tanpa kriteria |
| 3.4 Perancangan | Gambar 3.2 arsitektur; Kimball 4 langkah; Tabel 3.2 (6 dimensi), 3.3 (4 fakta); Gambar 3.3 ERD | Draf ada | Inkonsistensi grain/kolom antar-artefak (M-04); dimensi/fakta tanpa sumber (C-04) |
| 3.5 Pipeline | AWAP + branch Iceberg + quarantine + Airflow | Draf ada | Tanpa query engine untuk Superset, katalog belum ditentukan (M-03) |
| 3.6 Evaluasi | Tabel 3.4: 11 indikator | Draf ada | Uji KS sirkular (C-02); kinerja tanpa protokol/pembanding (M-02) |
| Bab IV | Templat | **Kosong** | — |
| Bab V | Lorem ipsum | **Kosong** | — |
| Daftar pustaka | 35 entri | Ada | [26] urutan penulis tidak konsisten dengan teks §2.4 |
| Lampiran A–D | Templat pengamatan citra & kode contoh | **Kosong / salah konteks** | — |

**Artefak implementasi:** tidak ada (tidak ada repo Git, kode, DAG, SQL, konfigurasi, log, hasil,
atau dashboard).

---

## 3. Data yang dilampirkan

Profil lengkap: [audit/data-profiling-2026-09-14.md](audit/data-profiling-2026-09-14.md).
Skrip reproduksi: [audit/scripts/profil_sumber_data.py](audit/scripts/profil_sumber_data.py).

| Berkas | Sheet → baris | Isi | Sifat | Temuan utama |
|---|---|---|---|---|
| `MK SD.xlsx` | Sheet1 → 63 | Kurikulum 2025 Sains Data: kode, nama, SKS, PRAKT, SM, kategori, metode | Riil, referensi | Bersih (0 null, 0 duplikat). SKS teori 159, **SKS+praktikum 189** |
| `data sintetis krs khs.xlsx` | fact_krs 6.495 · fact_khs 952 · dim_waktu 11 · ref_yudis_bersih 135 | KRS/KHS 135 mahasiswa SD 2020–2025 | **Campuran**: KRS/KHS sintetis; `ref_yudis_bersih` = **yudisium riil** | Konsisten secara internal (Σsks KRS = SKS KHS 100 %; IPK kumulatif benar). Tidak ada skrip generator. Kurikulum 2025 dipakai untuk angkatan 2020. 128/135 lulus dalam 7 semester |
| `Data akademik 2012 - 2016.xlsx` | Referensi Mahasiswa 1.377 · Program Studi 44 · Kelas 3.540 · Kurikulum 147 · KHS 22.029 | Lulusan 10 prodi angkatan 2012–2016 | Riil, sudah dipseudonimkan (`M-AR-001`) | Status 100 % "Lulus". Fakultas kosong 44/44. **KHS tanpa kunci**, duplikat 71,7 %. Kurikulum: 6 bernilai 0 SKS. Kelas: 45 duplikat, 13 kuota 0 |
| `PENDAFTARAN PESERTA YUDISIUM FAKULTAS SAINS (Jawaban).xlsx` | 20 sheet periode (Jun 2024 – Jun 2026) + 2 sheet konfigurasi AutoCrat → 151 baris | Formulir yudisium Fakultas Sains | Riil, **memuat PII** | 135 baris Sains Data (label "S1 SAINS DATA" 108 / "Sains Data" 27). Jumlah kolom 23–49 berubah antar-sheet. 2 IPK terbaca sebagai tanggal |

**Total volume ± 35 ribu baris.** Artinya:

- Spark/Iceberg/MinIO **tidak dibutuhkan karena volume**. Pembenarannya harus berupa
  **tata kelola** (ACID, time travel, branch/WAP, keterlacakan, skala masa depan), bukan performa.
- Klaim "*scalable*" hanya bisa diuji lewat **scale factor sintetis** yang terdokumentasi (§13).

**Populasi antar-sumber tidak saling beririsan.** Sumber 2012–2016 mencakup 10 prodi tanpa Sains
Data. Data sintetis hanya SD angkatan 2020–2022. Yudisium mencakup SD lulus 2024–2026. **Tidak ada
id mahasiswa bersama** antar-sumber. Integrasi hanya mungkin melalui **dimensi yang diseragamkan**
(prodi, waktu, mata kuliah) dan **fakta berproses bisnis sama** (kelulusan), bukan dengan
menggabungkan riwayat per mahasiswa.

---

## 4. Temuan audit (ringkas)

Detail, bukti, opsi, dan Definition of Done ada di [audit/issue-register.md](audit/issue-register.md).

### KRITIS

| ID | Temuan | Dampak |
|---|---|---|
| **C-01** | Belum ada implementasi, eksperimen, atau hasil. Bab IV–V masih templat, sisa waktu ± 1 bulan | Skripsi belum punya bukti. Jadwal jadi risiko utama |
| **C-02** | Uji "akurasi data sintetis" (KS, p > 0,05) sirkular, dan secara konsep p > 0,05 ≠ fidelitas. IPK akhir sintetis ≠ `ipk_clean` untuk 126/135 mahasiswa (selisih s.d. ±0,20) | Indikator kualitas data sintetis tidak valid. Fakta KHS dan yudisium saling bertentangan |
| **C-03** | Berkas yudisium memuat PII/kuasi-identifier. Klaim "tanpa identitas" di §3.2 bertentangan dengan data. Izin penggunaan data belum terdokumentasi | Risiko etika dan hukum (UU PDP). Data tidak boleh masuk Bronze/Git dalam bentuk ini |
| **C-04** | Model dimensional tidak didukung data: Fact_KHS riil tanpa kunci, Fact_Status tanpa variasi status atau periode, Dim_Dosen tanpa sumber non-PII, Fakultas kosong, tidak ada kunci mahasiswa lintas sumber | Klaim "mengintegrasikan berbagai sumber data akademik" (RQ1) tidak dapat dibuktikan sesuai rancangan saat ini |

### MAYOR

| ID | Temuan |
|---|---|
| M-01 | RQ berupa tugas implementasi ("bagaimana merancang/menyajikan/mengukur") tanpa kriteria jawaban |
| M-02 | Evaluasi kinerja tanpa pembanding, scale factor tak terdefinisi, tanpa repetisi/warm-up/spesifikasi perangkat. Target "hitungan detik yang wajar" tidak terukur |
| M-03 | Arsitektur tidak lengkap: tidak ada query engine Superset ↔ Iceberg, katalog Iceberg belum ditentukan. Quality check sebelum Bronze bertentangan dengan definisi Bronze = data mentah. Diagram menyebut data *unstructured* padahal seluruh sumber XLSX |
| M-04 | Inkonsistensi antar Tabel 3.2/3.3, Gambar 3.3, dan data sintetis (grain fact_krs, nama kolom, `id_dosen` tunggal untuk banyak pembimbing/penguji, `jumlah_mahasiswa` pada grain per-mahasiswa) |
| M-05 | Data sintetis tanpa provenance (skrip, seed, aturan). Realisme temporal buruk (7 semester vs masa studi riil median 4,42 tahun). Survivorship (tidak ada mengulang/gagal/tidak lulus). Berkas "sintetis" berisi data riil |
| M-06 | Periode dan cakupan data tidak konsisten (1.4: 2012–2025; 3.2: 2012–2026; data aktual terputus: 2012–2016, 2020–2025, 2024–2026). "Data dosen" disebut tetapi tidak ada |
| M-07 | Tinjauan pustaka belum memposisikan kontribusi (3 studi, tanpa pembanding evaluasi quality gate). Beberapa rujukan inti lemah atau tidak relevan |
| M-08 | Analisis kebutuhan tanpa bukti (stakeholder, instrumen, daftar KPI). "Dashboard informatif" tidak punya kriteria |
| M-09 | Naskah: abstrak, Bab IV–V, lampiran masih templat. Jenis karya tidak konsisten |

---

## 5. Pertanyaan penelitian

### 5.1 RQ pada draf (dicatat apa adanya)

1. Bagaimana merancang data lakehouse berbasis medallion yang mampu mengintegrasikan berbagai
   sumber data akademik ke dalam sistem pengelolaan data yang terpadu, terstruktur, dan scalable?
2. Bagaimana menyajikan data yang telah diproses dalam bentuk dashboard yang informatif untuk
   mendukung monitoring dan pelaporan data akademik?
3. Bagaimana mengukur performa sistem data lakehouse yang dibangun dalam proses ingestion,
   transformation, dan penyediaan data akademik untuk kebutuhan analitik dan pelaporan?

### 5.2 RQ usulan — **SUPERVISOR DECISION REQUIRED (D-01)**

**RQ utama.**
**Sejauh mana lakehouse berbasis Medallion dengan *quality gate* Write-Audit-Publish (WAP) pada
branch Apache Iceberg mampu (a) menghasilkan Gold layer akademik yang benar terhadap sumbernya,
(b) mencegah data cacat terpublikasi, dan (c) berapa biaya waktu yang ditimbulkannya, ketika
diterapkan pada data akademik ITERA yang heterogen?**

**Sub-RQ**

1. **Kebenaran.** Apakah ukuran pada fakta dan KPI Gold identik dengan hasil perhitungan oracle
   independen dari data sumber (setelah anonimisasi)?
2. **Efektivitas gate.** Berapa proporsi cacat yang terdeteksi dan dikarantina oleh audit pada
   transisi Bronze→Silver dan Silver→Gold, per jenis cacat dan per tingkat injeksi? Berapa tingkat
   positif palsu pada data bersih?
3. **Overhead.** Berapa tambahan waktu eksekusi dan penurunan throughput pipeline dengan WAP
   dibanding tanpa WAP pada beberapa scale factor?
4. **Luaran aplikatif (sekunder).** Apakah KPI akademik yang disepakati dapat disajikan di
   Superset dengan nilai yang 100 % sama dengan Gold?

Hubungan dengan RQ draf: RQ1 draf → sub-RQ 1 dan 2 (desain dibuktikan lewat kebenaran dan
integritas). RQ2 draf → sub-RQ 4. RQ3 draf → sub-RQ 3. **Arah topik tidak berubah**; yang
berubah adalah **kriteria jawabannya**.

---

## 6. Hipotesis / kriteria evaluasi (usulan)

- **H1 — Kebenaran.** Pada data bersih, count dan SUM di Gold identik dengan oracle
  (toleransi 0), dan rerata IPK/masa studi berselisih ≤ 0,005.
- **H2 — Deteksi.** Untuk jenis cacat yang tercakup aturan, recall deteksi ≥ 0,95 dan
  **kontaminasi Gold = 0**. Cacat yang tidak tercakup aturan (mis. nilai salah tetapi masih dalam
  rentang valid) diperkirakan lolos, dan ini dilaporkan sebagai batas metode.
- **H3 — Positif palsu.** Pada data bersih, FPR aturan ≤ 1 %. Setiap positif palsu ditelusuri ke
  aturan bisnis yang belum dimodelkan (contoh nyata: 11 lulusan "Sangat Memuaskan" dengan
  IPK > 3,50).
- **H4 — Overhead.** Overhead relatif WAP menurun ketika scale factor naik, karena sebagian biaya
  (branch, commit metadata) bersifat tetap.
- **H5 — Kontrol positif.** Pipeline **tanpa** gate (B0) yang diberi data cacat **harus**
  mencemari Gold. Jika tidak, injeksi cacat atau oracle-nya salah dan harus diaudit dulu.

Semua hipotesis boleh ditolak. Hasil negatif yang terukur tetap merupakan hasil penelitian.

---

## 7. Batas kontribusi

**Kontribusi yang dituju**

- rancangan dan implementasi referensi lakehouse Medallion + WAP untuk data akademik berbasis
  spreadsheet yang heterogen;
- **katalog cacat data riil** dari sumber akademik ITERA dan pemetaannya ke aturan audit;
- evaluasi kuantitatif **efektivitas quality gate** (fault injection) dan **overhead** WAP;
- integrasi dua sumber kelulusan berskema berbeda ke satu fakta dengan dimensi yang diseragamkan.

**Bukan kontribusi**

- memakai Spark/Iceberg/Airflow/Superset itu sendiri (implementasi ≠ kebaruan);
- membandingkan lakehouse vs data warehouse vs data lake;
- dashboard sebagai temuan ilmiah;
- analitik prediktif atau machine learning;
- klaim tentang performa akademik mahasiswa ITERA dari data sintetis.

> Kebaruan **belum dapat dinyatakan**. Potensi kontribusi sudah teridentifikasi, tetapi
> verifikasi literatur eksternal (terutama studi evaluasi WAP/data quality gate pada lakehouse)
> masih diperlukan.

---

## 8. Sumber data dan perannya (usulan D-02)

| Kode | Sumber | Peran di lakehouse | Masuk fakta/dimensi |
|---|---|---|---|
| S1 | `MK SD.xlsx` | Referensi kurikulum SD 2025 | `dim_mata_kuliah` |
| S2 | Yudisium Fakultas Sains (riil, **dianonimkan sebelum Bronze**) | Kelulusan SD 2024–2026 | `fact_kelulusan` (source = YUD) |
| S3 | Referensi Mahasiswa 2012–2016 (riil) | Kelulusan 10 prodi historis | `fact_kelulusan` (source = HIST), `dim_mahasiswa` |
| S4 | Program Studi 2012–2016 | Referensi prodi | `dim_prodi` (fakultas dan jenjang dari pemetaan terdokumentasi) |
| S5 | KRS/KHS sintetis **v2** (dibangkitkan ulang dengan skrip + seed) | Proses studi per semester SD | `fact_krs`, `fact_khs` — **diberi label SINTETIS** |
| S6 | Data KHS 2012–2016 (tanpa kunci) | **Kasus cacat nyata**: masuk Bronze, ditolak di gate Silver | Quarantine (tidak masuk Gold) |
| S7 | Kelas & Kurikulum 2012–2016 | Referensi opsional + kasus cacat (0 SKS, duplikat, kuota 0) | Silver saja (opsional) |

Aturan wajib:

- **PII dihapus sebelum Bronze** di zona terbatas (`data/raw` → `data/anonymized`). Bronze hanya
  menerima data teranonimkan. Log anonimisasi disimpan sebagai hash kolom dan jumlah baris,
  **bukan nilai**.
- Setiap baris sintetis membawa `is_synthetic = true`. Dashboard menandai KPI sintetis.
- Tidak ada klaim tentang kondisi akademik ITERA yang bersumber dari data sintetis.

---

## 9. Arsitektur target (perbaikan dari Gambar 3.2)

```text
                    ZONA TERBATAS (lokal, tidak di Git)
XLSX sumber ──► de-identifikasi (hapus PII, pseudonim) ──► data/anonymized
                                                               │  checksum + manifest
                                                               ▼
┌──────────────────────── MinIO (object storage) + Iceberg catalog ────────────────────────┐
│ BRONZE (append-only, apa adanya + metadata ingest: source_file, sheet, sha256, ingest_ts)│
│   │  cek STRUKTURAL saja (berkas terbaca, sheet ada)  → gagal: tetap disimpan + flag     │
│   ▼                                                                                      │
│ [WAP] create branch → WRITE silver@branch → AUDIT (aturan DQ) ─ lolos → PUBLISH (main)   │
│                                                         └ gagal → QUARANTINE + laporan   │
│ SILVER (bersih, skema seragam, tipe benar, dedup, label prodi seragam)                   │
│   ▼                                                                                      │
│ [WAP] create branch → WRITE gold@branch → AUDIT (RI, grain, rekonsiliasi) → PUBLISH      │
│ GOLD (dim_* + fact_kelulusan, fact_krs, fact_khs)                                        │
└──────────────────────────────────────────────────────────────────────────────────────────┘
        ▲ Spark (compute)          ▲ Airflow (orkestrasi)            │
                                                                     ▼
                                    Trino (atau Spark Thrift) ──► Superset (dashboard)
```

Perbaikan dibanding draf:

1. **Tidak ada penolakan sebelum Bronze.** Bronze harus menyimpan data mentah (§2.5 draf sendiri).
   Gate semantik dimulai di Bronze→Silver.
2. **Query engine** ditambahkan, karena Superset tidak membaca tabel Iceberg langsung.
3. **Katalog Iceberg** harus dipilih dan diuji pada E0 (REST / JDBC / Nessie). Branch Iceberg
   berlaku per tabel. Jika publish multi-tabel harus atomik (fakta + dimensi sekaligus),
   verifikasi apakah katalog yang dipilih mendukungnya, atau dokumentasikan urutan publish dan
   risikonya. **NOT VERIFIED — diuji di pilot E0.**
4. **Data mentah hanya XLSX (terstruktur).** Hapus klaim *semi-structured/unstructured* dari
   diagram, kecuali memang ada sumber tersebut.
5. **Rencana cadangan:** jika Airflow + Superset menghabiskan > 2 hari pada Minggu 1, orkestrasi
   memakai `Makefile` dan hal ini didokumentasikan sebagai batasan. (Keputusan S1.)

---

## 10. Model dimensional usulan (D-03)

| Tabel | Grain | Ukuran / atribut | Sumber |
|---|---|---|---|
| `fact_kelulusan` | 1 mahasiswa × 1 kelulusan | `ipk_final`, `sks_final`, `masa_studi_bulan`, `predikat`, `source_system` | S2 + S3 (riil) |
| `fact_krs` | 1 mahasiswa × 1 MK × 1 semester | `sks` (= SKS + praktikum, definisi eksplisit), `bobot_nilai` (v2) | S5 (sintetis) |
| `fact_khs` | 1 mahasiswa × 1 semester | `sks_semester`, `ip_semester`, `sks_kumulatif`, `ipk_kumulatif` — **diturunkan dari fact_krs**, bukan dibangkitkan terpisah | S5 (sintetis) |
| `dim_mahasiswa` | 1 pseudonim | `angkatan`, `tanggal_masuk` (jika ada), `is_synthetic` | S3, S2, S5 |
| `dim_prodi` | 1 prodi | `kode`, `nama`, `jenjang`, `fakultas` (pemetaan terdokumentasi) | S4 |
| `dim_mata_kuliah` | 1 MK kurikulum | `sks`, `sks_praktikum`, `semester_kurikulum`, `kategori`, `metode`, `kurikulum` | S1 |
| `dim_semester` | 1 semester akademik | `tahun_akademik`, `ganjil_genap` (tanpa tanggal fiktif) | turunan |
| `dim_tanggal` | 1 hari | untuk tanggal yudisium/lulus | turunan |

Keluar dari cakupan utama (usulan): **`fact_status`** (tidak ada variasi status maupun data
periode) dan **`dim_dosen`** (satu-satunya sumber adalah nama dosen = PII; relasinya
banyak-ke-banyak).

Bus matrix, data dictionary, dan source-to-target mapping ditulis mahasiswa di
[docs/modeling/](docs/modeling/).

---

## 11. Rencana eksperimen

| ID | Nama | Menjawab | Keluaran utama |
|---|---|---|---|
| **E0** | Environment & source readiness | prasyarat | versi komponen terkunci, stack hidup, anonimisasi terverifikasi (0 kolom PII di Bronze), profil sumber |
| **E1** | Functional pipeline end-to-end | prasyarat sub-RQ 1 | DAG sukses, row count per layer, lineage `source_file → gold` |
| **E2** | Reconciliation correctness | sub-RQ 1, H1 | tabel selisih Gold vs oracle per ukuran |
| **E3** | Quality-gate fault injection | sub-RQ 2, H2, H3, H5 | recall/FPR per jenis cacat × tingkat injeksi, kontaminasi Gold B0 vs B1 |
| **E4** | Performance & WAP overhead | sub-RQ 3, H4 | waktu per tahap, throughput, overhead %, CI 95 % |
| **E5** | Dashboard KPI correctness | sub-RQ 4 | kecocokan KPI Superset vs Gold (100 % pada set uji), waktu muat median |
| E6 | Fitur Iceberg (opsional) | pendukung | demo time travel, rollback, schema evolution sebagai uji fungsional |

**Pembanding (baseline) yang bermakna**

- **B0 — pipeline tanpa gate** (tulis langsung ke main): ablasi dan kontrol positif untuk
  kontaminasi.
- **B1 — pipeline dengan WAP**: sistem yang diusulkan.
- **Oracle** — perhitungan independen (pandas/DuckDB) langsung dari berkas teranonimkan, **bukan**
  query ulang ke Gold.

Pembanding lakehouse vs PostgreSQL/DW **tidak direkomendasikan** untuk 1 bulan: biaya tinggi dan
tidak menjawab RQ.

---

## 12. Aturan kualitas data dan katalog cacat

### 12.1 Katalog cacat untuk E3

| Kode | Jenis cacat | Dimensi DQ | Asal |
|---|---|---|---|
| D01 | Primary key null | completeness | injeksi |
| D02 | Primary key duplikat | uniqueness | **nyata** (Kelas 45, KHS 15.790 baris duplikat) + injeksi |
| D03 | Foreign key yatim (MK/prodi tidak ada di dimensi) | consistency | injeksi |
| D04 | IP/IPK di luar [0, 4] | validity | injeksi |
| D05 | IPK kumulatif ≠ turunan IP×SKS | consistency | injeksi |
| D06 | SKS final ≠ Σ SKS KRS | consistency | injeksi |
| D07 | Tanggal keluar < tanggal masuk | validity | injeksi |
| D08 | **Schema drift** (kolom berganti nama/bertambah) | consistency | **nyata** (23–49 kolom antar-sheet yudisium) |
| D09 | **Tipe salah** (angka terbaca tanggal) | validity | **nyata** (2 IPK tersimpan sebagai tanggal) |
| D10 | **Label kategori tidak seragam** | consistency | **nyata** ("S1 SAINS DATA" vs "Sains Data") |
| D11 | Nilai referensi tidak masuk akal (SKS kurikulum 0, kuota 0) | validity | **nyata** (6 kurikulum, 13 kelas) |
| D12 | Tabel tanpa kunci bisnis | completeness | **nyata** (Data KHS 2012–2016) |

Tingkat injeksi: **1 % dan 5 %**. Seed: **5** per kombinasi. Dijalankan pada SF1.

### 12.2 Metrik E3

- recall deteksi per jenis cacat = baris cacat terdeteksi / baris cacat disuntikkan;
- FPR = baris bersih yang dikarantina / baris bersih;
- kontaminasi Gold = baris cacat yang sampai di Gold (B0 vs B1);
- dilaporkan per jenis cacat, bukan hanya rata-rata.

---

## 13. Protokol pengukuran kinerja (E4)

| Faktor | Level |
|---|---|
| Scale factor | **SF1** (135 mhs SD sintetis + sumber riil), **SF10**, **SF100** — replikasi sintetis ber-seed dengan pseudonim unik |
| Mode | B0 (tanpa WAP), B1 (WAP) |
| Tahap | ingest Bronze, Bronze→Silver, Silver→Gold, end-to-end |
| Repetisi | 1 warm-up (dibuang) + **≥ 5 terukur**, urutan run diacak/diselang |

Wajib dicatat per run: `run_id`, `git_commit`, `sf`, `mode`, `stage`, `seed`, `rows_in`,
`rows_out`, `rows_quarantined`, `wall_time_s`, `spark_conf_hash`, `n_data_files`,
`n_snapshots`, `timestamp`. Spesifikasi perangkat (CPU, RAM, disk, OS) dan batas resource
Docker dicatat sekali di `artifacts/reproducibility/`.

Analisis: median dan IQR per sel. Overhead = median(B1)/median(B0) − 1 dengan **bootstrap CI
95 %**. Tanpa klaim "signifikan" jika tidak diuji. Waktu muat dashboard: median 10 kali muat
ulang per dashboard.

Target yang **dihapus** dari Tabel 3.4: "hitungan detik yang wajar", "100 % job sesuai jadwal",
dan "p-value KS > 0,05".

---

## 14. Struktur repository

```text
andina/
├── README.md                      ← audit + desain (dokumen ini)
├── .gitignore                     ← melindungi XLSX/PII dari commit
├── .env.example · Makefile · pyproject.toml · requirements.txt · docker-compose.yml
│
├── audit/                         ← Supervisor 2 (bukan bukti mahasiswa)
│   ├── 2026-09-14-audit-awal.md
│   ├── issue-register.md
│   ├── data-profiling-2026-09-14.md
│   └── scripts/profil_sumber_data.py
│
├── Rencana-eksperimen-bimbingan/
│   ├── README.md · CATATAN_PROGRES_BIMBINGAN.md
│   └── minggu-1/ … minggu-4/README.md
│
├── docs/
│   ├── research/        research-charter, rq, hypotheses, novelty-boundary, scope-freeze, decision-log, penelitian-terkait
│   ├── requirements/    stakeholder, kebutuhan-analitik, kpi-catalog
│   ├── data-governance/ data-inventory, pii-dan-anonimisasi, izin-penggunaan-data, data-sintetis-protokol
│   ├── architecture/    architecture, component-versions, awap-design, catalog-and-branching
│   └── modeling/        bus-matrix, dimensional-model, data-dictionary, source-to-target-mapping, erd.dbml
│
├── data/                          ← isi TIDAK di-commit, kecuali manifests/
│   ├── README.md
│   ├── raw/ · anonymized/ · synthetic/ · fault_injection/
│   └── manifests/  source_manifest.csv · anonymization_log.csv · synthetic_generation_log.csv
│
├── configs/   sources · layers · dq_rules · fault_injection · scale_factors · benchmark · kpi (.yaml)
├── contracts/ bronze/ · silver/ · gold/            ← skema per tabel
├── infra/     minio/ · iceberg-catalog/ · spark/ · trino/catalog/ · airflow/ · superset/
├── dags/      insightera_akademik_medallion_dag.py
├── src/insightera_akademik/
│   ├── anonymize/ · ingest/ · silver/ · gold/ · quality/ · wap/
│   ├── synthetic/ · fault_injection/ · reconciliation/ · benchmark/ · utils/
├── sql/       bronze/ · silver/ · gold/ · kpi/
├── dashboards/ superset/ · screenshots/
├── tests/     unit/ · integration/ · data_quality/ · reproducibility/
├── experiments/
│   ├── E0_environment_source_readiness/     E4_performance_wap_overhead/
│   ├── E1_functional_pipeline/              E5_dashboard_kpi_correctness/
│   ├── E2_reconciliation_correctness/       E6_iceberg_features_optional/
│   └── E3_quality_gate_fault_injection/
├── notebooks/exploratory/
├── results/   raw/ · processed/ · tables/ · figures/ · quarantine_reports/ · benchmark/ · reconciliation/
├── thesis/    main.tex · references.bib · bab/bab1…bab5 · figures/ · tables/
├── paper/     manuscript.md · figures/ · tables/ · bibliography/
├── artifacts/reproducibility/  environment_lock.txt · reproducibility_report.md
└── scripts/
```

Berkas sumber asli yang dilampirkan Andina **dibiarkan di root** sebagai bukti audit (checksum di
profil data). Mahasiswa **memindahkannya** ke `data/raw/` saat memulai Minggu 1, lalu mencatat
checksum di `data/manifests/source_manifest.csv`.

---

## 15. Tools

Stack sesuai draf, ditambah komponen yang hilang:

| Fungsi | Komponen | Catatan |
|---|---|---|
| Object storage | MinIO | — |
| Table format | Apache Iceberg | versi dikunci di `docs/architecture/component-versions.md` |
| Katalog | REST / JDBC / Nessie | **dipilih di E0** berdasarkan dukungan branch/WAP |
| Compute | Apache Spark (PySpark) | mode lokal/standalone, konfigurasi dibekukan |
| Query engine | **Trino** (atau Spark Thrift Server) | **baru**, jembatan ke Superset |
| Orkestrasi | Apache Airflow | cadangan: Makefile |
| BI | Apache Superset | — |
| Oracle & analisis | pandas / DuckDB, NumPy, SciPy, matplotlib | independen dari Spark |
| DQ | aturan eksplisit di `configs/dq_rules.yaml` (boleh dibantu library DQ, tetapi aturan tetap tertulis) | — |
| Reproducibility | Docker Compose, Git, lock file, seed, manifest checksum | — |

**Semua versi harus ditulis dari hasil instalasi nyata, bukan dari asumsi.**

---

## 16. Aturan reproducibility, data, dan Git

- XLSX, `data/raw`, `data/anonymized`, `data/synthetic` **tidak di-commit** (sudah diatur di
  `.gitignore`).
- Yang di-commit: kode, konfigurasi, kontrak skema, manifest checksum, log anonimisasi (tanpa
  nilai), ringkasan hasil, tabel/figur yang dihasilkan skrip.
- Generator sintetis v2 **deterministik** (seed tercatat) dan **dibatasi** agregat riil:
  `sks_final` dan `ipk_final` per mahasiswa = yudisium teranonimkan, distribusi masa studi
  mengikuti yudisium riil. Pelanggaran batasan ini adalah bug, bukan variasi.
- Setiap tabel dan figur di Bab IV harus bisa ditelusuri:

```text
sub-RQ → eksperimen → config → run_id → results/raw → results/processed → tabel/figur → klaim
```

- Sebelum sidang: **fresh run** dari clone bersih menghasilkan ulang minimal 1 tabel E2, 1 tabel
  E3, dan 1 figur E4.

---

## 17. Rencana satu bulan (14 Sep – 14 Okt 2026)

| Minggu | Tanggal | Gate | Fokus | Keluaran wajib |
|---|---|---|---|---|
| **1** | Sen 14 – Min 20 Sep | **G1 — Scope & Foundation Freeze** | Keputusan D-01…D-06, izin data, anonimisasi, KPI ≤ 8, model dimensional v2, stack hidup, Bronze untuk semua sumber, generator sintetis v2 | `scope-freeze.md`, `data/anonymized` + log, Bronze terisi, `erd.dbml` v2, `component-versions.md` |
| **2** | Sen 21 – Min 27 Sep | **G2 — Pipeline Benar** | Silver + Gold + WAP + quarantine, katalog aturan DQ ≥ 15, oracle rekonsiliasi | E1 & E2 selesai, tabel rekonsiliasi |
| **3** | Sen 28 Sep – Min 4 Okt | **G3 — Bukti Utama** | E3 fault injection, E4 benchmark SF × mode, E5 dashboard | `results/` lengkap, figur dan tabel dari skrip |
| **4** | Sen 5 – Min 11 Okt | **G4 — Naskah & Reproducibility** | Bab IV–V, revisi Bab I–III, abstrak, limitasi, fresh run | draf skripsi lengkap, `reproducibility_report.md` |
| Buffer | Sen 12 – Rab 14 Okt | — | perbaikan hasil review pembimbing | — |

Detail harian: [Rencana-eksperimen-bimbingan/](Rencana-eksperimen-bimbingan/README.md).

**Aturan jadwal:** jika G1 belum lolos pada **Rabu 23 Sep**, E4 dipersempit menjadi SF1 + SF10
saja dan E6 dibatalkan, tanpa menunggu keputusan baru.

---

## 18. Definition of Done

Penelitian utama dianggap selesai bila:

- [ ] RQ, hipotesis, cakupan data, dan model dimensional dibekukan dan tercatat di `decision-log.md`;
- [ ] izin penggunaan data terdokumentasi, dan tidak ada kolom PII di Bronze/Silver/Gold (diuji otomatis);
- [ ] klaim §3.2 draf direvisi agar sesuai kondisi data;
- [ ] generator sintetis v2 deterministik, dan batasan agregat riil terpenuhi 100 %;
- [ ] Bronze, Silver, Gold terbentuk untuk seluruh sumber S1–S5, dan S6 tercatat di quarantine;
- [ ] WAP berjalan: tidak ada publish ke main tanpa audit lolos (dibuktikan log);
- [ ] E2: seluruh ukuran Gold cocok dengan oracle, atau setiap selisih dijelaskan;
- [ ] E3: recall/FPR per jenis cacat D01–D12 × 2 tingkat × 5 seed, B0 vs B1;
- [ ] E4: 3 SF × 2 mode × ≥ 5 repetisi, median + IQR + bootstrap CI overhead;
- [ ] E5: ≤ 8 KPI dengan kecocokan 100 % terhadap Gold, KPI sintetis diberi label;
- [ ] Tabel 3.4 diganti dengan indikator yang terukur;
- [ ] seluruh tabel/figur Bab IV dihasilkan skrip dari `results/`;
- [ ] Bab IV–V, abstrak, lampiran terisi; seluruh templat dihapus;
- [ ] fresh run dari clone bersih berhasil dan terdokumentasi.

---

## 19. Keputusan Supervisor yang diperlukan

| ID | Pertanyaan | Opsi | Rekomendasi S2 |
|---|---|---|---|
| **D-01** | Bingkai RQ | A: pertahankan 3 RQ desain + tambah kriteria · **B: RQ evaluasi WAP (§5.2)** · C: desain + uji fungsional saja, tanpa kinerja | **B**, karena memberi bukti terukur dengan biaya setara A |
| **D-02** | Cakupan data | A: semua sumber apa adanya · **B: S1–S5 + S6/S7 sebagai kasus cacat (§8)** · C: menunggu KRS/KHS riil dari BAAK | **B**. C terlalu berisiko untuk 1 bulan |
| **D-03** | Fakta & dimensi | A: 4 fakta sesuai draf · **B: fact_kelulusan + fact_krs + fact_khs, tanpa fact_status/dim_dosen** · C: hanya fact_kelulusan | **B** |
| **D-04** | Data sintetis | A: pakai berkas sekarang + limitasi · **B: generator v2 ber-seed dengan batasan agregat riil** · C: tanpa sintetis | **B**. A mempertahankan C-02 |
| **D-05** | Evaluasi kinerja | A: deskriptif SF1 · **B: SF1/10/100 × WAP on/off** · C: + banding PostgreSQL | **B** |
| **D-06** | Izin & PII data yudisium | A: gunakan setelah izin tertulis + anonimisasi · B: tidak memakai yudisium (hanya S3 riil) · — | **A**. Tanpa izin, pakai B |
| D-07 | Batas dengan Insightera-Andini (non-akademik) dan target publikasi | platform bersama vs terpisah; jurnal nasional terakreditasi vs skripsi saja | platform infra boleh dipakai bersama, **kontribusi & evaluasi terpisah**; target publikasi diputuskan setelah G3 |

---

## 20. Kesiapan

### Skripsi — **NOT READY**

| Gate | Status | Pemblokir |
|---|---|---|
| T0 Masalah & RQ | CONDITIONAL | M-01, M-08 |
| T1 Cakupan & kontribusi | FAIL | C-04, M-07 |
| T2 Metodologi | CONDITIONAL | M-02, M-03 |
| T3 Data | FAIL | C-02, C-03, C-04, M-05, M-06 |
| T4 Implementasi/eksperimen | FAIL | C-01 |
| T5 Hasil & analisis | FAIL | C-01 |
| T6 Klaim–bukti | FAIL | klaim privasi bertentangan; klaim lain belum diuji |
| T7 Reproducibility | FAIL | tidak ada kode/konfigurasi |
| T8 Koherensi naskah | FAIL | M-09 |
| T9 Limitasi & integritas | FAIL | C-03, provenance `ref_yudis_bersih` |

### Publikasi — **RESEARCH-STAGE**

Potensi artikel ada pada **evaluasi kuantitatif quality gate WAP + katalog cacat data akademik
nyata**. Pemblokirnya: belum ada bukti, dan posisi terhadap literatur belum diverifikasi.

---

## Catatan Pembimbing

Alur besarnya kira-kira seperti ini:

```text
4 berkas Excel (ada PII)
   ↓
hapus PII + pseudonim  (di laptop, tidak ke Git)
   ↓
BRONZE  = simpan apa adanya + catat asal berkas
   ↓
[branch] → tulis SILVER di branch → AUDIT → lolos? publish : karantina
   ↓
SILVER  = bersih, tipe benar, label seragam, tanpa duplikat
   ↓
[branch] → tulis GOLD di branch → AUDIT → lolos? publish : karantina
   ↓
GOLD    = dim_* + fact_kelulusan + fact_krs + fact_khs
   ↓
Trino → Superset (≤ 8 KPI)
```

1. **Masalah terbesar sekarang bukan teknologi, tetapi datanya.** Rancangan di draf butuh KHS per
   mahasiswa per semester, status mahasiswa per periode, dan data dosen. Data yang ada tidak
   menyediakan itu: KHS riil kehilangan kolom kunci, status seluruhnya "Lulus", dan data dosen
   hanya berupa nama. Maka model harus **mengikuti data yang benar-benar ada**. Jangan mengarang
   data agar sesuai model.

2. **Integrasi yang jujur.** Data 2012–2016 (10 prodi) dan yudisium Sains Data (2024–2026) sama-sama
   mencatat **kelulusan**, tetapi dengan kolom dan format berbeda. Menyatukan keduanya ke satu
   `fact_kelulusan` dengan `dim_prodi` dan `dim_tanggal` yang sama adalah contoh nyata "integrasi
   sumber heterogen". Itu yang bisa diklaim.

3. **Data sintetis harus diakui sebagai sintetis dan dibuat ulang dengan skrip.** Dalam berkas
   sekarang, `ref_yudis_bersih` adalah data riil, dan IPK terakhir di KHS sintetis tidak sama dengan
   IPK yudisium "mahasiswa yang sama". Versi 2 dibangkitkan **dari KRS** (setiap MK diberi nilai),
   lalu KHS **dihitung**, dan hasil akhirnya **dipaksa sama** dengan SKS/IPK yudisium teranonimkan.
   Dengan begitu tiga fakta konsisten, dan uji rekonsiliasi punya arti.

4. **Inti eksperimennya: apakah AWAP benar-benar menahan data jelek?** Contoh:

```text
Data bersih ──► pipeline B0 (tanpa gate) ──► Gold benar
Data + 5% cacat ──► B0 ──► Gold TERCEMAR     (kontrol positif, harus terjadi)
Data + 5% cacat ──► B1 (WAP) ──► Gold bersih + baris cacat di quarantine
```

   Lalu dihitung, per jenis cacat: berapa yang tertangkap (recall), berapa data bersih yang ikut
   dikarantina (positif palsu), dan berapa yang lolos ke Gold. Separuh jenis cacat **diambil dari
   masalah nyata** yang ditemukan di berkas Andina sendiri: IPK terbaca tanggal, "S1 SAINS DATA"
   vs "Sains Data", kolom yudisium yang berubah tiap periode, SKS kurikulum 0, dan KHS tanpa kunci.

5. **Kinerja diukur dengan jujur.** Data aslinya kecil (± 35 ribu baris), jadi pertanyaannya bukan
   "Spark cepat atau tidak", melainkan **"berapa harga tambahan yang dibayar untuk gate WAP, dan
   apakah harga itu mengecil saat data membesar?"**. Karena itu ada SF1/SF10/SF100 × WAP on/off,
   dengan warm-up, ≥ 5 repetisi, median, dan CI.

6. **Dashboard itu luaran, bukan temuan.** Cukup ≤ 8 KPI (jumlah lulusan per periode & predikat,
   rerata IPK lulusan, median masa studi, % lulus ≤ 4 tahun, beban SKS per semester, sebaran IP per
   angkatan [SINTETIS], komposisi MK wajib/pilihan). Yang diuji: angkanya **sama persis** dengan
   Gold.

7. **Hasil akhir yang kuat bukan** "Lakehouse berhasil dibangun dan dashboard informatif",
   **tetapi** "Gold 100 % cocok dengan oracle; gate WAP menahan X dari 12 jenis cacat dengan recall
   ≥ Y dan tanpa kontaminasi Gold, dengan overhead Z % pada SF100".

Jadi **tidak perlu** menambah sumber data baru, membandingkan dengan data warehouse, atau membuat
model ML. Yang perlu: **mempersempit, membuktikan, dan menulis.**
