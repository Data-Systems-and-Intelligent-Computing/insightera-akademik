# Laporan Audit — insightera-andina

> Artefak Supervisor 2. Ditempatkan di folder mahasiswa atas instruksi eksplisit Supervisor 1
> (2026-09-14). Temuan terperinci beserta opsi dan Definition of Done ada di
> [issue-register.md](issue-register.md); laporan ini tidak mengulanginya kata per kata.

## 1. Metadata Audit

- **Mahasiswa:** Syalaisha Andina Putriansyah (122450121), Sains Data ITERA
- **Jenis audit:** audit repositori penuh (awal) + audit data
- **Tanggal audit:** 2026-09-14
- **Lokasi:** `insightera/andina/`
- **Branch / commit:** — (bukan repositori Git)
- **Commit audit sebelumnya:** tidak ada
- **Kondisi working tree:** tidak berlaku; baseline ditetapkan dengan checksum SHA-256 berkas (lihat [data-profiling-2026-09-14.md](data-profiling-2026-09-14.md) §1)
- **Fase penelitian utama:** perancangan (Bab I–III draf)
- **Fase sekunder:** belum ada implementasi

## 2. Cakupan Audit

Audit penuh atas seluruh bukti yang dilampirkan:

- draf skripsi `Syalaisha Andina .pdf` (51 halaman: seluruh teks, Gambar 3.1–3.3, Tabel 2.1, 3.1–3.4, daftar pustaka, lampiran);
- empat berkas XLSX (seluruh sheet), diprofil read-only dengan `audit/scripts/profil_sumber_data.py`.

Tidak diaudit: literatur eksternal (tidak ditelusuri), perilaku runtime Iceberg/Spark/Trino (belum ada implementasi), folder `insightera/andini` (hanya dilihat daftar berkasnya untuk S-03).

## 3. Bukti yang Diperiksa

| Kategori | Bukti | Lokasi | Relevansi |
|---|---|---|---|
| Naskah | Bab I–V, abstrak, lampiran | `Syalaisha Andina .pdf` | sentral |
| Riset | Rumusan masalah, tujuan, batasan | PDF §1.2–1.4 | sentral |
| Metode | Alur penelitian | PDF Gambar 3.1 | sentral |
| Arsitektur | Arsitektur & pipeline ETL | PDF Gambar 3.2, §3.4.2.1, §3.5 | sentral |
| Model | Dimensi, fakta, ERD | PDF Tabel 3.2, 3.3, Gambar 3.3 | sentral |
| Evaluasi | Ringkasan pengujian | PDF Tabel 3.4 | sentral |
| Literatur | Penelitian terdahulu, pustaka | PDF Tabel 2.1, Daftar Pustaka | pendukung |
| Data | Kurikulum SD | `MK SD.xlsx` | sentral |
| Data | KRS/KHS sintetis, dim_waktu, ref yudisium | `data sintetis krs khs.xlsx` | sentral |
| Data | Referensi mahasiswa, prodi, kelas, kurikulum, KHS 2012–2016 | `Data akademik 2012 - 2016.xlsx` | sentral |
| Data | Formulir yudisium FS (20 periode) | `PENDAFTARAN PESERTA YUDISIUM FAKULTAS SAINS (Jawaban).xlsx` | sentral |

## 4. Kondisi Repositori

- Tidak ada Git, kode, konfigurasi, log, hasil, atau dashboard.
- Pada audit ini S2 membuat **kerangka repositori kosong** (folder + berkas placeholder), `README.md`,
  `.gitignore` pelindung PII, rencana mingguan, dan berkas audit. Berkas asli mahasiswa **tidak diubah
  atau dipindahkan**.
- Berkas yang **wajib diisi mahasiswa** (RQ, hipotesis, model, kode, eksperimen) sengaja dibiarkan kosong
  sesuai batas kepengarangan.

## 5. Status Riset Eksekutif

**Status:** `AT RISK`

**Hambatan utama:** model dimensional dan rencana evaluasi di draf tidak dapat direalisasikan dengan data
yang tersedia (C-04, C-02), sementara belum ada implementasi (C-01) dan sisa waktu ± 1 bulan.

**Mengapa ini hambatannya:** implementasi yang dimulai dari model draf akan tertahan pada Fact_KHS riil
(tanpa kunci), Fact_Status (tanpa variasi), dan Dim_Dosen (PII). Evaluasi di Tabel 3.4 akan "lolos" secara
trivial (uji KS sirkular, target tidak dapat gagal). Artinya kerja satu bulan bisa menghasilkan sistem yang
berjalan tetapi tanpa bukti ilmiah. Karena itu keputusan cakupan harus diambil **sebelum** menulis kode.

## 6. Verifikasi Isu Sebelumnya

Tidak berlaku (audit pertama).

## 7–10. Temuan

Lihat [issue-register.md](issue-register.md):

| Tingkat | ID |
|---|---|
| KRITIS | C-01, C-02, C-03, C-04 |
| MAYOR | M-01 … M-09 |
| MINOR | m-01 … m-05 |
| SARAN | S-01 … S-03 |

## 11. Validitas Riset

**Status:** `NEEDS ATTENTION`

- Masalah umum (pengelolaan data akademik terfragmentasi) relevan, tetapi belum ditunjukkan dengan bukti spesifik ITERA (sistem sumber, frekuensi pelaporan, masalah konkret).
- RQ berupa tugas desain/implementasi (M-01). DSR bisa diterima untuk skripsi, **asalkan** fase evaluasi artefak punya kriteria yang dapat gagal.
- Kontribusi belum dipisahkan dari implementasi (memakai Iceberg/Spark bukan kebaruan). Potensi kontribusi: evaluasi quality gate WAP + katalog cacat data akademik nyata (perlu verifikasi literatur).
- Kecocokan data ↔ rancangan rendah (C-04).

## 12. Validitas Eksperimen

**Status:** `BLOCKED` (belum ada eksperimen; rancangan evaluasi tidak memadai)

- Tidak ada variabel bebas/terikat yang eksplisit. Usulan: mode pipeline (B0/B1), scale factor, jenis & tingkat cacat → waktu, throughput, recall, FPR, kontaminasi Gold.
- Tidak ada baseline (M-02). Usulan: B0 tanpa gate (ablasi + kontrol positif), oracle independen.
- Konfonder potensial pada E4: start-up JVM/Spark, cache OS, ukuran file kecil ("small files") setelah banyak commit Iceberg, sumber daya Docker berbagi dengan Superset/Airflow. Mitigasi: warm-up, urutan diacak, resource limit tetap, catat `n_data_files`/`n_snapshots`, Superset dimatikan saat benchmark.
- Konfonder potensial pada E3: aturan DQ ditulis setelah melihat cacat yang disuntikkan (overfitting aturan). Mitigasi: bekukan `dq_rules.yaml` **sebelum** membangkitkan set injeksi, dan laporkan cacat di luar cakupan aturan.

## 13. Validitas Kode / Implementasi

**Status:** `NOT ASSESSED` (tidak ada kode)

## 14. Validitas Statistik

**Status:** `AT RISK`

- Uji KS dengan p > 0,05 sebagai bukti "akurasi" salah secara konsep dan sirkular pada data ini (C-02).
- Rencana kinerja tidak menyebut repetisi, ukuran pemusatan, atau ketidakpastian (M-02).
- Usulan: median + IQR, bootstrap CI 95 % untuk rasio overhead, recall/FPR dengan interval (mis. Wilson) per jenis cacat, tanpa klaim signifikansi tanpa uji yang sesuai.

## 15. Reproducibility

**Status:** `NOT REPRODUCIBLE`

Belum ada: spesifikasi dependensi, definisi lingkungan, versi perangkat lunak, spesifikasi perangkat keras, seed, skrip generator sintetis, prosedur anonimisasi, konfigurasi pipeline, instruksi eksekusi, keluaran mentah, skrip analisis, proses pembuatan figur.

Positif: sumber data berupa berkas tetap, sehingga checksum baseline dapat ditetapkan (sudah dicatat).

## 16. Konsistensi Klaim–Bukti

| ID | Klaim (draf) | Status | Bukti kunci | Masalah utama |
|---|---|---|---|---|
| CLM-01 | "Data yang diperoleh tidak memuat informasi identitas individu" (§3.2) | **BERTENTANGAN** (CONTRADICTED) | header kolom yudisium | tempat/tanggal lahir, alamat, judul TA, nama & NIP dosen, URL dokumen |
| CLM-02 | Data penelitian periode 2012–2025 (§1.4) / 2012–2026 (§3.2) | SEBAGIAN DIDUKUNG | 3 XLSX | periode terputus; tidak ada data angkatan 2017–2019 |
| CLM-03 | Data meliputi KHS, mata kuliah, yudisium (Tabel 3.1) | SEBAGIAN DIDUKUNG | `Data KHS`, `fact_khs`, `MK SD` | KHS riil tanpa kunci; KHS SD hanya sintetis |
| CLM-04 | Batasan data: mahasiswa, dosen, mata kuliah (§1.4) | SEBAGIAN DIDUKUNG | seluruh XLSX | tidak ada data dosen non-PII |
| CLM-05 | Lakehouse "terpadu, terstruktur, scalable" (RQ1/Tujuan 1) | NOT TESTED | — | belum ada implementasi; "scalable" tanpa definisi |
| CLM-06 | AWAP "menyaring kualitas data secara otomatis" (§3.4.2.1) | NOT TESTED | — | — |
| CLM-07 | Branch Iceberg sebagai isolasi selama transformasi (§3.5) | NOT TESTED | — | katalog belum dipilih; perilaku multi-tabel belum diverifikasi |
| CLM-08 | Fidelitas data sintetis diukur dengan KS (Tabel 3.4) | NOT TESTED; rancangan **tidak valid** | `ref_yudis_bersih` = yudisium riil | sirkular (C-02) |
| CLM-09 | Hasil Begoli et al.: query +50 %, storage 10× vs CSV (Tabel 2.1) | NOT VERIFIED | — | perlu cek sumber primer |

## 17. Ancaman terhadap Validitas

**Validitas konstruk**
- "Akurasi data sintetis" dioperasionalkan sebagai p-value KS, yang tidak mengukur akurasi → diganti batasan deterministik + deskripsi jarak distribusi.
- "Scalable" dan "informatif" tanpa definisi operasional → klaim tidak dapat diuji.

**Validitas internal**
- Waktu benchmark didominasi overhead start-up pada volume ± 35 ribu baris → efek WAP bisa tertutup. Perlu SF10/SF100 dan warm-up.
- Aturan DQ yang disetel setelah melihat cacat injeksi akan menaikkan recall secara semu.

**Validitas eksternal**
- Hanya satu institusi; data proses studi hanya SD dan sintetis; sumber historis hanya lulusan (survivorship). Hasil E3/E4 tidak otomatis berlaku untuk sistem akademik lain atau data berskala produksi.

**Validitas kesimpulan**
- Scale factor sintetis mereplikasi pola yang sama. Throughput pada SF100 bukan bukti performa pada data riil sebesar itu.

## 18. Kesiapan Skripsi

**Status keseluruhan:** `NOT READY`

| Gate | Status | Bukti kunci | Isu pemblokir |
|---|---|---|---|
| T0 Masalah & RQ | CONDITIONAL | PDF §1.1–1.3 | M-01, M-08 |
| T1 Cakupan & kontribusi | FAIL | PDF §1.4, §2.1 | C-04, M-07 |
| T2 Metodologi | CONDITIONAL | PDF Bab III | M-02, M-03 |
| T3 Data | FAIL | 4 XLSX | C-02, C-03, C-04, M-05, M-06 |
| T4 Implementasi | FAIL | — | C-01 |
| T5 Hasil | FAIL | — | C-01 |
| T6 Klaim–bukti | FAIL | §16 | CLM-01 bertentangan |
| T7 Reproducibility | FAIL | — | C-01 |
| T8 Koherensi naskah | FAIL | PDF | M-04, M-09 |
| T9 Limitasi & integritas | FAIL | — | C-03; provenance `ref_yudis_bersih` perlu klarifikasi |

**Catatan integritas (bahasa netral):** berkas berlabel "data sintetis" memuat sheet yang nilainya identik dengan data yudisium riil yang sudah dipseudonimkan. Kemungkinan besar ini dimaksudkan sebagai data acuan untuk membangkitkan data sintetis. Namun penamaan dan pencampurannya **perlu diklarifikasi dan didokumentasikan** agar tidak ada data riil yang dilaporkan sebagai sintetis, atau sebaliknya.

## 19. Kesiapan Publikasi

**Status keseluruhan:** `RESEARCH-STAGE`

Pemblokir: belum ada bukti (C-01); posisi literatur dan kebaruan belum diverifikasi (M-07); klaim privasi (C-03). Potensi artikel: evaluasi kuantitatif efektivitas dan overhead quality gate WAP pada data akademik heterogen berbasis spreadsheet, dengan katalog cacat nyata. **Venue belum dinilai.**

## 20. Jalur Riset yang Direkomendasikan

```text
1. S1 memutuskan D-01…D-06 (≤ Rabu 16 Sep 2026).
2. Izin data + de-identifikasi sebelum menyentuh stack (C-03).
3. Model dimensional v2 + source-to-target mapping dari data nyata (C-04, M-04).
4. Generator sintetis v2 dengan batasan agregat riil (C-02, M-05).
5. Stack minimum hidup + uji perilaku branch/WAP (E0, M-03).
6. Bronze → Silver → Gold + oracle rekonsiliasi (E1, E2).
7. Bekukan dq_rules.yaml → fault injection (E3).
8. Benchmark SF × mode (E4) → dashboard ≤ 8 KPI (E5).
9. Tabel/figur dari skrip → Bab IV–V → revisi Bab I–III → fresh run.
```

## 21. Keputusan Supervisor 1 yang Diperlukan

Rincian opsi dan rekomendasi: [README.md §19](../README.md#19-keputusan-supervisor-1-yang-diperlukan).

`SUPERVISOR-1 DECISION REQUIRED`: **D-01** (bingkai RQ), **D-02** (cakupan data), **D-03** (fakta/dimensi), **D-04** (data sintetis), **D-05** (evaluasi kinerja), **D-06** (izin & PII yudisium), D-07 (batas dengan Andini & target publikasi).

## 22. Definition of Done — Milestone Berikutnya (Gate G1, Minggu 1)

- [ ] D-01…D-06 tercatat di `docs/research/decision-log.md` dengan tanggal dan pemberi keputusan
- [ ] Repositori Git dibuat; tidak ada XLSX/PII dalam riwayat
- [ ] Izin data terdokumentasi **atau** cadangan D-06 B diberlakukan
- [ ] `data/anonymized/` terbentuk + `anonymization_log.csv`; uji "0 kolom PII" lulus
- [ ] `docs/modeling/erd.dbml` v2 + `source-to-target-mapping.md` tanpa kolom Gold tak bersumber
- [ ] `docs/requirements/kpi-catalog.md` ≤ 8 KPI
- [ ] Stack (MinIO, katalog, Spark, Trino) hidup; `component-versions.md` terisi dari instalasi
- [ ] Uji branch → write → audit → publish → rollback berhasil pada 1 tabel (log di `results/raw/E0/`)
- [ ] Bronze berisi seluruh sumber S1–S7 dengan metadata ingest
- [ ] Generator sintetis v2 lulus uji batasan 100 %

## 23. Pembaruan Status Audit

```yaml
student: insightera-andina
audit_type: full-initial
audit_date: 2026-09-14
audited_commit: null            # belum ada Git; baseline = sha256 berkas di data-profiling-2026-09-14.md
previous_audited_commit: null
primary_phase: design (draft Bab I–III)
current_bottleneck: data-model mismatch + invalid evaluation design before any implementation
next_audit: 2026-09-21 (verifikasi Gate G1)
```

## 24. Penilaian Penutup Supervisor 2

Proyek ini sekarang **berisiko** karena rancangan yang ditulis lebih ambisius daripada data yang tersedia,
dan rencana evaluasinya tidak dapat gagal. Risiko terpenting yang belum terselesaikan adalah
**penggunaan data yudisium yang memuat data pribadi tanpa izin/anonimisasi terdokumentasi** (C-03),
disusul **ketidaksesuaian model dimensional dengan data** (C-04). Keduanya dapat diselesaikan dalam
Minggu 1 tanpa data baru, melalui keputusan cakupan yang tegas. Audit berikutnya (≈ 21 Sep 2026)
harus memverifikasi Gate G1, terutama: tidak ada PII di Bronze, mapping sumber→Gold lengkap, dan
generator sintetis v2 memenuhi batasan agregat riil.
