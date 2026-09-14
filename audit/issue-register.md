# Register Isu — insightera-andina

**Mahasiswa:** Syalaisha Andina Putriansyah (122450121) · **Topik:** Data Lakehouse Medallion untuk Data Akademik (Insightera)
**Dibuka:** 2026-09-14 (audit awal — belum ada repositori Git; baseline = berkas terlampir, checksum di `data-profiling-2026-09-14.md`)
**Terakhir diperbarui:** 2026-09-14

> Artefak Supervisor 2. Ditempatkan di folder mahasiswa atas instruksi Supervisor 1.
> Seluruh angka dapat direproduksi dengan `python audit/scripts/profil_sumber_data.py`.

Kosakata status: `TERBUKA` · `SEDANG DITANGANI` · `SEBAGIAN TERSELESAIKAN` · `SELESAI` · `RISIKO DITERIMA` · `DIGANTIKAN` · `DIBUKA KEMBALI`

## Ringkasan

| Tingkat Keparahan | Jumlah | Terbuka |
|---|---|---|
| KRITIS | 4 | 4 |
| MAYOR | 9 | 9 |
| MINOR | 5 | 5 |
| SARAN | 3 | 3 |

**Isu pemblokir Gate G1 (Minggu 1):** C-03 (izin & PII), C-04 (model tidak didukung data), C-02/M-05 (data sintetis), M-01 (RQ).
**Isu pemblokir skripsi:** seluruh KRITIS + M-02, M-03, M-09.

| ID | Sev. | Area | Temuan singkat | Status | Blok |
|---|---|---|---|---|---|
| C-01 | KRITIS | THS/EXP | Tidak ada implementasi, eksperimen, atau hasil; Bab IV–V templat | TERBUKA | Skripsi |
| C-02 | KRITIS | STAT/DATA | Uji KS fidelitas sintetis sirkular; IPK sintetis ≠ yudisium | TERBUKA | Skripsi |
| C-03 | KRITIS | INT/DATA | PII di data yudisium; klaim "tanpa identitas" bertentangan | TERBUKA | Riset, Skripsi |
| C-04 | KRITIS | DATA/EXP | Model dimensional tidak didukung data sumber | TERBUKA | Riset, Skripsi |
| M-01 | MAYOR | RQ | RQ berupa tugas implementasi tanpa kriteria jawaban | TERBUKA | Skripsi |
| M-02 | MAYOR | EXP | Evaluasi kinerja tanpa pembanding & protokol | TERBUKA | Skripsi |
| M-03 | MAYOR | EXP/CODE | Arsitektur tidak lengkap/inkonsisten | TERBUKA | Skripsi |
| M-04 | MAYOR | FIG | Inkonsistensi Tabel 3.2/3.3 vs Gambar 3.3 vs data | TERBUKA | Skripsi |
| M-05 | MAYOR | DATA/INT | Data sintetis tanpa provenance, tidak realistis, bercampur data riil | TERBUKA | Skripsi |
| M-06 | MAYOR | DATA/THS | Periode & cakupan data tidak konsisten | TERBUKA | Skripsi |
| M-07 | MAYOR | CON/PUB | Tinjauan pustaka belum memposisikan kontribusi | TERBUKA | Skripsi, Publikasi |
| M-08 | MAYOR | RQ | Analisis kebutuhan & KPI tanpa bukti | TERBUKA | Skripsi |
| M-09 | MAYOR | THS | Naskah sebagian besar templat; jenis karya tidak konsisten | TERBUKA | Skripsi |
| m-01 | MINOR | THS | Salah ketik di gambar & teks | TERBUKA | — |
| m-02 | MINOR | DATA | Dim_Mata_Kuliah mengabaikan atribut yang tersedia | TERBUKA | — |
| m-03 | MINOR | FIG | Keterangan gambar tidak informatif; atribusi gambar pinjaman | TERBUKA | — |
| m-04 | MINOR | THS | §2.7–2.13 hampir tanpa sitasi | TERBUKA | — |
| m-05 | MINOR | DATA | Anomali data riil belum terdokumentasi (bukan kesalahan mahasiswa) | TERBUKA | — |
| S-01 | SARAN | EXP | Jadikan anomali nyata sebagai katalog cacat E3 | TERBUKA | — |
| S-02 | SARAN | CON | Integrasi 2 sumber kelulusan ke satu fakta | TERBUKA | — |
| S-03 | SARAN | RQ | Koordinasi batas dengan Insightera-Andini | TERBUKA | — |

---

## KRITIS

### C-01 — Belum ada implementasi, eksperimen, maupun hasil
**Status: TERBUKA** · Gate: T4, T5, T7 · Memblokir: seluruh Bab IV–V
**Bukti:** isi folder `insightera/andina/` pada 2026-09-14 hanya 4 XLSX + 1 PDF; `Syalaisha Andina .pdf` hlm. 22–27 (Bab IV: teks "Hello, here is some text without a meaning", Tabel 4.2 daftar provinsi), hlm. 27–28 (Bab V lorem ipsum), Lampiran C (kode contoh `incmatrix`).

Tidak ada repositori Git, kode, DAG Airflow, SQL, konfigurasi, kontrak skema, log, hasil, maupun
dashboard. Tabel 3.4 mendefinisikan 11 indikator, tetapi belum ada satu pun yang diukur. Sisa waktu
sekitar 1 bulan.

**Mengapa penting:** tanpa bukti, tidak ada klaim yang bisa dipertahankan di sidang. Menginstal stack
(MinIO + katalog Iceberg + Spark + Trino + Airflow + Superset) bisa menghabiskan beberapa hari.

**Opsi**
- **A** — Pertahankan cakupan draf penuh (4 fakta, 6 dimensi, semua indikator). *Risiko jadwal sangat tinggi; sebagian fakta tidak punya data (C-04).*
- **B** — Persempit sesuai D-01…D-05 (3 fakta, E0–E5, stack minimum), dengan gate mingguan. *Layak 1 bulan jika G1 lolos pada 20–23 Sep.*
- **C** — Hanya implementasi fungsional + dashboard, tanpa E3/E4. *Paling cepat, tetapi tidak menjawab RQ kinerja dan lemah untuk sidang/publikasi.*

**Rekomendasi S2:** B.
**Keputusan S1:** YA (D-01, D-03, D-05).

**Definition of Done**
- [ ] Repositori Git dibuat dengan struktur di README §14; commit pertama ≤ 16 Sep 2026
- [ ] E0–E5 memiliki `run_e*.py`, konfigurasi, dan keluaran di `results/`
- [ ] Bab IV berisi hasil dari `results/` (bukan templat); Bab V menjawab setiap sub-RQ

### C-02 — Uji "akurasi data sintetis" sirkular dan salah konsep; fakta sintetis bertentangan dengan yudisium
**Status: TERBUKA** · Gate: T3, T6 · Berdampak: Tabel 3.4 baris "Accuracy – Data Sintesis", Fact_KHS, Fact_Yudisium
**Bukti:** `data sintetis krs khs.xlsx` sheet `ref_yudis_bersih`, `fact_khs`; `PENDAFTARAN PESERTA YUDISIUM ... .xlsx` (20 sheet periode); draf §3.6 Tabel 3.4.

Tiga masalah bertumpuk:

1. **`ref_yudis_bersih` adalah data riil.** Dari 135 barisnya, multiset `sks_final` **identik** dengan
   `Jumlah SKS`/`SKS FINAL` yudisium Sains Data, jumlah predikat **identik** (106 SM / 21 M / 8 Pujian),
   dan nilai IPK sama pada **125/135** baris. 10 sisanya berbeda karena pembulatan/pembersihan
   (2 sel IPK sumber tersimpan sebagai tanggal Excel). ID diganti `M0001…M0135`, urutan diacak.
2. **Uji KS sirkular.** `sks_final` sintetis = Σ SKS KRS sintetis pada 100 % mahasiswa, artinya generator
   dipaksa sama dengan data riil. Uji KS ulang oleh S2: SKS D = 0,000, p = 1,0; IPK D = 0,022,
   p ≈ 1,0. Hasil "lolos" dijamin oleh konstruksi, bukan bukti fidelitas.
3. **Salah konsep statistik.** p > 0,05 berarti *tidak cukup bukti adanya perbedaan*, bukan
   *distribusinya sama*. Nilai p juga bergantung pada n.

Selain itu, **IPK akhir di `fact_khs` ≠ `ipk_clean` pada 126/135 mahasiswa** (selisih −0,20 s.d. +0,20,
SD 0,076). Mahasiswa yang sama punya dua IPK akhir berbeda di dua fakta.

**Mengapa penting:** indikator akurasi di Tabel 3.4 tidak mengukur apa pun. Jika fakta KHS dan
yudisium dibangun dari berkas ini, rekonsiliasi Gold akan gagal atau harus ditutupi.

**Opsi**
- **A** — Pertahankan berkas, hapus uji KS, laporkan inkonsistensi sebagai limitasi. *Murah; inkonsistensi antar-fakta tetap ada.*
- **B** — Generator v2 ber-seed: bangkitkan nilai per MK di KRS → **hitung** KHS → paksa SKS/IPK akhir = yudisium teranonimkan. Validasi dengan **cek batasan deterministik** (100 % terpenuhi) + deskripsi distribusi (median, IQR, D-statistic sebagai ukuran jarak, **tanpa** klaim p-value). *Biaya ± 1–2 hari; fakta konsisten.*
- **C** — Hapus data sintetis; tanpa fact_krs/fact_khs. *Kehilangan proses studi per semester dan scale factor untuk E4.*

**Rekomendasi S2:** B.
**Keputusan S1:** YA (D-04).

**Definition of Done**
- [ ] Baris "Accuracy – Data Sintesis (KS p > 0,05)" dihapus dari Tabel 3.4
- [ ] `src/insightera_akademik/synthetic/generate_krs_khs.py` + seed di `data/manifests/synthetic_generation_log.csv`
- [ ] Uji otomatis: `ipk_kumulatif` akhir = `ipk_final` yudisium dan `sks_kumulatif` = `sks_final` untuk 100 % mahasiswa
- [ ] `docs/data-governance/data-sintetis-protokol.md` menyatakan data riil yang dipakai sebagai batasan

### C-03 — Data pribadi pada sumber yudisium; klaim privasi bertentangan; izin tidak terdokumentasi
**Status: TERBUKA** · Gate: T3, T9 · Memblokir: ingest S2 ke Bronze, commit Git
**Bukti:** `PENDAFTARAN PESERTA YUDISIUM FAKULTAS SAINS (Jawaban).xlsx` (header kolom lintas sheet); draf §3.2 ("Data yang diperoleh tidak memuat informasi identitas individu").

Kolom yang ditemukan pada header sheet: `Tempat Lahir`, `Tanggal Lahir` (4 varian nama), `Alamat`,
`Judul TA`/`Judul Tugas Akhir`, nama `Dosen Pembimbing 1–3`, `Penguji` seminar/sidang, `Dosen Wali`,
`Kaprodi`, `NIP/NRK`, `No SK Pembimbing`, `Merged Doc ID/URL` (BA Yudisium, SKL), dan tautan
`Berkas Transkrip Final`/`Berita Acara Sidang`/`Surat Bebas UKT`. Ada juga 2 sheet konfigurasi
Google Apps Script (AutoCrat). Header tidak memuat kolom Nama/NIM, tetapi kombinasi prodi + tanggal
lahir + judul TA + periode yudisium **cukup untuk mengidentifikasi ulang** individu. *(Audit tidak
membuka atau menyalin nilai kolom tersebut.)*

Klaim §3.2 berstatus **BERTENTANGAN**. Tidak ada surat izin/persetujuan penggunaan data maupun
prosedur anonimisasi dalam bukti.

**Mengapa penting:** data pribadi berada di bawah UU No. 27 Tahun 2022 tentang Pelindungan Data
Pribadi. Memasukkan data ini ke MinIO/Git/dashboard atau mencetaknya di skripsi menimbulkan risiko
etika dan hukum bagi mahasiswa dan institusi.

**Opsi**
- **A** — Minta izin tertulis dari pemilik data (Fakultas Sains/BAAK). De-identifikasi **sebelum** Bronze: hapus semua kolom di atas, pseudonim acak (bukan hash NIM), generalisasi tanggal ke bulan/periode. Uji otomatis "0 kolom PII".
- **B** — Tanpa izin: jangan pakai S2; fact_kelulusan hanya dari S3 (sudah dipseudonimkan).
- **C** — Pakai apa adanya dengan pernyataan limitasi. *Tidak dapat diterima.*

**Rekomendasi S2:** A, dengan B sebagai cadangan otomatis bila izin belum ada per 18 Sep 2026.
**Keputusan S1:** YA (D-06).

**Definition of Done**
- [ ] `docs/data-governance/izin-penggunaan-data.md` merujuk surat/izin (nomor, tanggal, pemberi)
- [ ] `docs/data-governance/pii-dan-anonimisasi.md` berisi daftar kolom dihapus/digeneralisasi
- [ ] `tests/data_quality/` memuat uji yang gagal bila kolom PII ada di Bronze/Silver/Gold
- [ ] XLSX asli tidak pernah masuk riwayat Git (`git log --all -- '*.xlsx'` kosong)
- [ ] Kalimat §3.2 draf direvisi sesuai kondisi data

### C-04 — Model dimensional tidak didukung data sumber
**Status: TERBUKA** · Gate: T1, T3 · Berdampak: RQ1 draf, Tabel 3.2, 3.3, Gambar 3.3
**Bukti:** `Data akademik 2012 - 2016.xlsx` (sheet `Data KHS`, `Data Referensi Mahasiswaa`, `Data Program Studi`); draf §3.4.2.2, Tabel 3.2–3.3.

| Elemen draf | Kebutuhan | Kondisi data | Status |
|---|---|---|---|
| Fact_KHS (riil) | id mahasiswa + semester + IP/IPK | `Data KHS`: 22.029 baris, **hanya kolom `IP` dan `SKS`**; 15.790 baris duplikat (71,7 %) | TIDAK DAPAT DIBANGUN dari data riil |
| Fact_Status | status per mahasiswa per periode | `Status Mahasiswa` = "Lulus" untuk 1.377/1.377; satu snapshot, tanpa periode | TIDAK DIDUKUNG |
| Dim_Dosen | id dosen, prodi | Tidak ada tabel dosen; hanya nama dosen di yudisium (PII) & `Jumlah Dosen` per prodi | TIDAK DIDUKUNG |
| Dim_Program_Studi.Fakultas, Jenjang | nilai terisi | `Fakultas` null 44/44; jenjang hanya tersirat di prefiks "S1" | SEBAGIAN |
| Integrasi lintas sumber | kunci mahasiswa bersama | Populasi tidak beririsan: 10 prodi (masuk 2012–2016), SD sintetis (2020–2022), SD yudisium (lulus 2024–2026) | TIDAK ADA KUNCI BERSAMA |

*Inferensi (NOT VERIFIED):* 916 dari 1.377 pasangan (`IPK`, `Total SKS`) di Referensi Mahasiswa muncul
sebagai pasangan (`IP`, `SKS`) di `Data KHS`, dan `SKS` bernilai 12–178. Ini mengindikasikan `Data KHS`
adalah riwayat kumulatif per semester dari mahasiswa yang sama yang kolom kuncinya terhapus.
Konfirmasi hanya bisa dari pemberi data.

**Mengapa penting:** RQ1 mengklaim integrasi "berbagai sumber data akademik". Dengan model sekarang,
dua dari empat fakta tidak punya sumber, dan tidak ada integrasi tingkat mahasiswa yang bisa
ditunjukkan.

**Opsi**
- **A** — Minta ulang data KHS/status dengan kunci dari pemberi data. *Bergantung pihak luar; risiko jadwal.*
- **B** — Remodel mengikuti data: `fact_kelulusan` (S3 riil + S2 riil, skema berbeda → satu fakta), `fact_krs` + `fact_khs` (sintetis v2, berlabel); keluarkan `fact_status` & `dim_dosen`; `Data KHS` 2012–2016 menjadi kasus quarantine (D12). Klaim integrasi dipersempit ke **dimensi seragam + fakta kelulusan multi-sumber**.
- **C** — Pertahankan model draf, isi fakta yang kosong dengan data sintetis. *Menyamarkan kekurangan data; memperparah C-02.*

**Rekomendasi S2:** B (boleh sambil menjalankan A; jika data baru datang sebelum 25 Sep, dievaluasi ulang).
**Keputusan S1:** YA (D-02, D-03).

**Definition of Done**
- [ ] `docs/modeling/source-to-target-mapping.md`: setiap kolom Gold → sheet & kolom sumber (atau "turunan", dengan rumus)
- [ ] `docs/modeling/bus-matrix.md` dan `erd.dbml` v2 konsisten dengan README §10
- [ ] Tidak ada kolom Gold tanpa sumber pada mapping
- [ ] Klaim integrasi di Bab I/III/V dirumuskan ulang sesuai cakupan

---

## MAYOR

### M-01 — RQ berupa tugas implementasi tanpa kriteria jawaban
**Status: TERBUKA** · Gate: T0
**Bukti:** draf §1.2 (3 RQ), §1.3.

RQ1 "Bagaimana merancang…", RQ2 "Bagaimana menyajikan…", RQ3 "Bagaimana mengukur…". Ketiganya
terjawab cukup dengan *melakukan* pekerjaannya, dan tidak ada kondisi yang membuat jawabannya
"tidak". RQ3 menanyakan *cara* mengukur, bukan *hasil* pengukuran. Istilah "scalable", "terpadu",
dan "informatif" tidak didefinisikan operasional.

**Opsi:** A — pertahankan RQ, tambahkan kriteria keberhasilan terukur per RQ · **B — RQ evaluasi WAP (README §5.2)** · C — satu RQ desain + evaluasi fungsional saja.
**Rekomendasi S2:** B. **Keputusan S1:** YA (D-01). S2 tidak menulis ulang RQ di naskah.

**Definition of Done**
- [ ] `docs/research/rq.md` berisi RQ final + definisi operasional setiap istilah kunci
- [ ] Setiap sub-RQ dipetakan ke ≥ 1 eksperimen dan ≥ 1 metrik
- [ ] Bab I §1.2–1.3 dan Bab V konsisten dengan `rq.md`

### M-02 — Evaluasi kinerja tanpa pembanding, protokol, maupun target terukur
**Status: TERBUKA** · Gate: T2
**Bukti:** draf Tabel 3.4 (baris Timeliness, Waktu eksekusi query, Throughput, Waktu muat), Gambar 3.1 ("Pengujian kinerja ETL").

"Scale factor" disebut tetapi tidak didefinisikan (tidak ada level, generator, atau ukuran). Tidak ada
baseline, jumlah repetisi, warm-up, spesifikasi perangkat, atau metode agregasi. Target "tercatat dan
dibandingkan", "dapat dihitung", dan "dalam hitungan detik yang wajar" tidak dapat gagal. "100 % job
selesai sesuai jadwal" trivial untuk batch lokal. Volume data aktual ± 35 ribu baris, sehingga waktu
akan didominasi start-up Spark, bukan pemrosesan.

**Opsi:** A — deskriptif per tahap pada SF1 · **B — SF1/10/100 × WAP on/off, ≥ 5 repetisi, median/IQR/bootstrap CI (README §13)** · C — B + banding PostgreSQL/DW.
**Rekomendasi S2:** B. C tidak menjawab RQ dan terlalu mahal. **Keputusan S1:** YA (D-05).

**Definition of Done**
- [ ] `configs/scale_factors.yaml` & `configs/benchmark.yaml` membekukan level, repetisi, warm-up, urutan run
- [ ] `results/benchmark/*.csv` memuat kolom per README §13
- [ ] Spesifikasi perangkat & batas resource Docker di `artifacts/reproducibility/`
- [ ] Tabel 3.4 diganti dengan target terukur

### M-03 — Arsitektur tidak lengkap dan tidak konsisten dengan definisinya sendiri
**Status: TERBUKA** · Gate: T2
**Bukti:** draf Gambar 3.2, §2.5 (Bronze "tanpa melalui proses transformasi apapun"), §3.5.

1. **Quality check sebelum Bronze** (jalur *Fail → Quarantine* sebelum *Extract*) bertentangan dengan
   peran Bronze sebagai preservasi data mentah (§2.5).
2. **Tidak ada query engine** antara tabel Iceberg dan Superset. Superset membutuhkan mesin SQL
   (mis. Trino atau Spark Thrift Server).
3. **Katalog Iceberg tidak disebut.** Branch dan WAP bergantung pada katalog dan versi. Branch Iceberg
   bersifat per tabel, sehingga publish Gold (beberapa dimensi + fakta) tidak otomatis atomik
   lintas tabel. *Perilaku pada stack yang dipilih: NOT VERIFIED — harus diuji di E0.*
4. Sumber digambarkan *structured, semi-structured, unstructured*, padahal seluruh sumber XLSX.
5. Label "Extrack", ikon "Data Science/ML" tanpa kebutuhan di RQ.

**Opsi:** **A — perbaiki diagram & teks sesuai README §9 dan uji perilaku branch di E0** · B — tanpa branch (WAP via staging table + swap) jika katalog tidak mendukung · C — tanpa WAP (hanya validasi pasca-tulis). *C menghilangkan inti evaluasi.*
**Rekomendasi S2:** A, dengan B sebagai cadangan terdokumentasi. **Keputusan S1:** TIDAK (teknis), kecuali jika C dipilih.

**Definition of Done**
- [ ] Gambar 3.2 v2 memuat katalog, query engine, dan Bronze tanpa penolakan semantik
- [ ] `docs/architecture/catalog-and-branching.md`: hasil uji E0 (create branch → write → audit → fast-forward/publish → rollback) dengan log
- [ ] `docs/architecture/component-versions.md` terisi dari hasil instalasi nyata

### M-04 — Inkonsistensi rancangan antar Tabel 3.2/3.3, Gambar 3.3, dan data sintetis
**Status: TERBUKA** · Gate: T8
**Bukti:** draf §3.4.2.2 (grain), Tabel 3.2, 3.3, Gambar 3.3; `data sintetis krs khs.xlsx`.

| Elemen | Teks/tabel | Gambar 3.3 (ERD) | Data sintetis |
|---|---|---|---|
| fact_krs grain | 1 mahasiswa × 1 MK × 1 periode; ukuran `SKS_Diambil` | ukuran `total_sks_diambil`, `jumlah_mk_diambil` (agregat) | `sks` per MK ✔ teks |
| fact_khs | `Total_SKS_Diambil` | `id_khs`, `total_sks` | `total_sks_diambil`, tanpa `id_khs` |
| dim_mahasiswa | `Tanggal_Lulus` | `tanggal_keluar` | — (tidak ada sheet) |
| fact_yudisium | dimensi `Dim_Dosen` | satu `id_dosen` | pembimbing 2–3 + penguji 4–6 per mahasiswa di sumber |
| fact_status | ukuran `Jumlah_Mahasiswa` | sama | grain per mahasiswa ⇒ selalu 1 (factless) |
| dim_waktu | `Tanggal`, `Bulan`, `Tahun` | sama | granularitas semester dengan tanggal buatan (01-08 / 15-01); yudisium bertanggal harian |

**Opsi:** **A — satu sumber kebenaran (`erd.dbml`), tabel & gambar dibangkitkan/diselaraskan darinya** · B — koreksi manual per artefak.
**Rekomendasi S2:** A. **Keputusan S1:** TIDAK.

**Definition of Done**
- [ ] `docs/modeling/erd.dbml` v2 = Tabel 3.2/3.3 = Gambar 3.3 = kontrak `contracts/gold/` (dicek di review)
- [ ] Relasi dosen banyak-ke-banyak dimodelkan dengan bridge **atau** dikeluarkan dari cakupan (D-03)
- [ ] `dim_semester` dan `dim_tanggal` dipisah, tanpa tanggal fiktif

### M-05 — Data sintetis tanpa provenance, tidak realistis, dan bercampur data riil
**Status: TERBUKA** · Gate: T3, T9
**Bukti:** `data sintetis krs khs.xlsx`; `MK SD.xlsx`; yudisium kolom `MASA STUDI`.

- Tidak ada skrip, seed, parameter, atau aturan pembangkitan.
- **Kurikulum 2025** (kode `SD25-`, `WT25-`, dll.) diterapkan pada angkatan **2020** (69 mhs), 2021 (58), 2022 (8).
- **128/135** mahasiswa selesai dalam 7 semester (≈ 3,5 tahun), padahal masa studi riil lulusan SD:
  median 4,42 tahun, min 3,5; hanya 2/135 ≤ 3,6 tahun.
- Survivorship: tidak ada MK diulang (0), tidak ada mahasiswa tidak lulus, IP semester minimum 2,38,
  dan 99,8 % MK diambil tepat di semester kurikulumnya.
- `sks` = SKS + PRAKT pada 100 % baris. Ini konsisten, tetapi definisinya tidak dinyatakan.
- Berkas berlabel "sintetis" berisi sheet data riil (lihat C-02).

**Opsi:** **A — generator v2 (lihat C-02 Opsi B) + parameter realisme dari data riil (distribusi masa studi, proporsi mengulang bila ada rujukan) + label `is_synthetic`** · B — gunakan apa adanya + limitasi eksplisit · C — tanpa data sintetis.
**Rekomendasi S2:** A. **Keputusan S1:** YA (D-04, bersama C-02).

**Definition of Done**
- [ ] Protokol sintetis ditulis sebelum pembangkitan (tidak diubah setelah melihat hasil E2–E4)
- [ ] Distribusi masa studi sintetis dilaporkan berdampingan dengan riil (median, IQR)
- [ ] Anakronisme kurikulum diselesaikan (pakai kurikulum yang berlaku per angkatan) **atau** dinyatakan sebagai limitasi

### M-06 — Periode dan cakupan data tidak konsisten di naskah
**Status: TERBUKA** · Gate: T3, T8
**Bukti:** draf §1.4 butir 1 ("2012 hingga 2025") & 3 ("mahasiswa, dosen, mata kuliah"), §3.1 ("data kelulusan, data sintesis"), §3.2 ("2012–2026"; KHS, MK, yudisium).

Data aktual: Referensi Mahasiswa angkatan masuk 2012–2016 (lulus 2016-09 s.d. 2024-01); sintetis
2020/2021 Ganjil – 2025/2026 Ganjil; yudisium Juni 2024 – Juni 2026 (tanggal yudisium hingga
2026-08-14). Tidak ada data 2017–2019 untuk angkatan masuk. Tidak ada data dosen. Batasan hanya
menyebut ITERA, padahal sebagian data (MK, yudisium, sintetis) hanya Sains Data/Fakultas Sains.

**Definition of Done**
- [ ] Tabel 3.1 v2: setiap sumber dengan periode, populasi, jumlah baris, sifat (riil/sintetis), dan peran
- [ ] §1.4 dan §3.2 memakai angka yang sama dengan `docs/data-governance/data-inventory.md`

### M-07 — Tinjauan pustaka belum memposisikan kontribusi
**Status: TERBUKA** · Gate: T1 · Blok publikasi
**Bukti:** draf §2.1 Tabel 2.1 (3 studi), daftar pustaka [10], [12], [13], [26].

- Hanya 3 penelitian terdahulu, tanpa kolom pembanding yang relevan (jenis evaluasi, metrik kualitas data, ada/tidaknya quality gate).
- Definisi lakehouse bersandar pada [10] (jurnal manajemen, domain manufaktur), sedangkan sumber primer [26] dikutip dengan urutan penulis "M. A. Zaharia, A. Ghodsi, R. Xin, M. Armbrust", yang tidak konsisten dengan teks §2.4 ("Armbrust et al."). Metadata perlu dicek pada sumber asli.
- Ringkasan Begoli et al. [13] ("performa query hingga 50 %, penyimpanan 10 kali lipat dibandingkan CSV") tampak sebagai efek format Parquet vs CSV, bukan lakehouse per se. *NOT VERIFIED — cek pada naskah asli.*
- Belum ada studi yang menjadi pembanding langsung untuk evaluasi WAP / data quality gate.

**Catatan:** S2 **tidak** menambahkan rujukan. Penelusuran literatur eksternal belum dilakukan.

**Definition of Done**
- [ ] Tabel penelitian terdahulu ≥ 10 studi dengan kolom: domain, stack, jenis evaluasi, metrik DQ, quality gate (ya/tidak), keterbatasan
- [ ] Paragraf gap menyatakan secara eksplisit apa yang belum dievaluasi di literatur yang ditelusuri, beserta strategi penelusurannya (basis data, kata kunci, rentang tahun)
- [ ] Metadata rujukan [26] diperbaiki dari sumber primer

### M-08 — Analisis kebutuhan dan KPI tanpa bukti
**Status: TERBUKA** · Gate: T0
**Bukti:** draf §3.4.1 butir 1; Tabel 3.4 aspek Dashboard ("Seluruh KPI yang direncanakan tersedia").

Tidak ada daftar stakeholder, instrumen (wawancara/kuesioner/dokumen acuan), maupun daftar KPI.
Target dashboard merujuk ke "KPI yang direncanakan" yang tidak pernah didefinisikan.

**Definition of Done**
- [ ] `docs/requirements/kpi-catalog.md`: ≤ 8 KPI, masing-masing dengan definisi, rumus, sumber Gold, grain, pemilik kebutuhan, dan label riil/sintetis
- [ ] Sumber kebutuhan terdokumentasi (notulen singkat dengan pihak prodi/fakultas **atau** dokumen acuan resmi yang dirujuk)

### M-09 — Naskah sebagian besar masih templat; jenis karya tidak konsisten
**Status: TERBUKA** · Gate: T8
**Bukti:** draf hlm. v–ix (abstrak lorem ipsum, kata kunci "ini, itu", kata pengantar "Prof. Xxxx"), Bab IV–V, Lampiran A–D (templat pengamatan citra, kode `incmatrix`), hlm. iv ("Jenis karya: Proposal Tugas Akhir") vs hlm. ii ("Naskah Skripsi untuk Sidang Akhir").

**Definition of Done**
- [ ] Tidak ada teks templat tersisa (`grep -i "lorem\|hello, here\|xxxx"` kosong pada sumber LaTeX)
- [ ] Lampiran berisi artefak relevan (DAG, aturan DQ, kontrak skema, konfigurasi benchmark)
- [ ] Jenis karya konsisten

---

## MINOR

### m-01 — Salah ketik pada gambar dan teks
**Bukti:** Gambar 3.1 "Anilisis Kebutuhan"; Gambar 3.2 "Extrack", "unstuctured"; §1.1 "mengolahnnya", "perguran"; §2.5 "diperkenalkan dan oleh"; §3.4.1 "medallion arcitecture"; Tabel 3.3 "pegukuran".
**Tindakan:** perbaiki saat revisi Bab I–III (Minggu 4).
**DoD:** tidak ada salah ketik yang tercantum di sini pada naskah revisi.

### m-02 — Dim_Mata_Kuliah mengabaikan atribut yang tersedia
**Bukti:** `MK SD.xlsx` memiliki `PRAKT`, `SM`, `KATEGORI`; Tabel 3.2 hanya `Kode`, `Nama_MK`, `SKS_Total`, `Metode`.
**Tindakan:** tambahkan `sks_praktikum`, `semester_kurikulum`, `kategori`, `kurikulum`; definisikan `sks_total = SKS + PRAKT` bila itu yang dimaksud.
**DoD:** data dictionary memuat definisi dan sumber tiap atribut.

### m-03 — Keterangan gambar tidak informatif; atribusi gambar pinjaman
**Bukti:** Gambar 3.3 berjudul "Schema"; Gambar 2.1–2.3 direproduksi dari rujukan [19], [26], [23].
**Tindakan:** keterangan deskriptif ("Fact constellation schema Gold layer v2"); nyatakan "diadaptasi dari" atau gambar ulang.
**DoD:** setiap gambar pinjaman diberi atribusi yang sesuai.

### m-04 — Subbab teori hampir tanpa sitasi
**Bukti:** §2.7 (1 sitasi), §2.8–2.12 (0 sitasi), §2.13 (0 sitasi untuk dimensi DQ).
**Tindakan:** sitasi dokumentasi resmi/literatur primer untuk Iceberg, Spark, Superset, dan dimensi kualitas data.
**DoD:** setiap klaim faktual tentang perilaku sistem memiliki rujukan.

### m-05 — Anomali data riil belum terdokumentasi *(bukan kesalahan mahasiswa)*
**Bukti:** lihat `data-profiling-2026-09-14.md` §5: Kurikulum 6 entri 0 SKS dan 3 entri 36–38 SKS; Kelas 45 baris duplikat, 13 kuota 0, 48 kuota ≥ 200; yudisium 23–49 kolom antar-sheet, header berganti nama, 2 IPK tersimpan sebagai tanggal, label prodi 2 varian; 11 lulusan "Sangat Memuaskan" dengan IPK > 3,50 (kemungkinan aturan masa studi — **NOT VERIFIED**, cek Peraturan Akademik).
**Tindakan:** catat di `docs/data-governance/data-inventory.md`; jadikan aturan DQ atau pengecualian aturan bisnis yang terdokumentasi.
**DoD:** setiap anomali punya keputusan: diperbaiki di Silver / dikarantina / pengecualian aturan bisnis.

---

## SARAN

### S-01 — Jadikan anomali nyata sebagai katalog cacat E3
**Saran:** D02, D08–D12 pada README §12.1 diambil dari m-05, sehingga evaluasi gate tidak hanya memakai cacat buatan.
**Manfaat:** validitas eksternal E3 meningkat; menjadi bahan diskusi yang kuat untuk sidang dan artikel.

### S-02 — Integrasi dua sumber kelulusan ke satu fakta
**Saran:** `fact_kelulusan` dari Referensi Mahasiswa 2012–2016 (10 prodi) dan Yudisium SD 2024–2026, dengan `source_system` dan dimensi seragam.
**Manfaat:** memberi bukti integrasi heterogen yang nyata tanpa data baru.

### S-03 — Koordinasi batas dengan Insightera-Andini
**Saran:** `insightera/andini` berisi data non-akademik (beasiswa, prestasi, tracer study, ormawa). Jika infrastruktur dipakai bersama, tetapkan sejak Minggu 1 komponen mana yang dibangun bersama dan kontribusi/evaluasi mana yang milik masing-masing.
**Manfaat:** mencegah duplikasi kerja dan tumpang-tindih klaim kontribusi.
