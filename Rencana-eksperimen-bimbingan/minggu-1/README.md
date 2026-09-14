# Rencana Eksperimen — Minggu 1 (GATE G1: Scope & Foundation Freeze)
**Tanggal:** Senin 14 – Minggu 20 September 2026
**Status eksekusi:** **BELUM DIMULAI**
**Eksperimen:** E0 (Environment & Source Readiness)
**Isu yang ditutup:** C-03, C-04, M-01, M-04, M-05, M-06, M-08 · desain C-02

> Prinsip Minggu 1: **putuskan dulu, baru membangun.** Model mengikuti data yang ada, bukan sebaliknya.

---

## H1–H2 (Sen 14 – Sel 15 Sep) — Keputusan & izin

| # | Tugas | Keluaran |
|---|---|---|
| 1.1 | Baca `README.md` + `audit/issue-register.md`; siapkan pertanyaan untuk bimbingan | catatan di `CATATAN_PROGRES_BIMBINGAN.md` |
| 1.2 | Bimbingan keputusan D-01…D-06 | `docs/research/decision-log.md` (tanggal, opsi dipilih, alasan, pemberi keputusan) |
| 1.3 | Ajukan/konfirmasi izin tertulis penggunaan data yudisium & data akademik | `docs/data-governance/izin-penggunaan-data.md` (status + rujukan surat) |
| 1.4 | Buat repositori Git dari kerangka ini; pastikan `.gitignore` aktif **sebelum** commit pertama | commit awal; `git log --all -- '*.xlsx'` kosong |
| 1.5 | Pindahkan XLSX asli ke `data/raw/`; catat checksum | `data/manifests/source_manifest.csv` (file, sheet, baris, sha256) |

## H3 (Rab 16 Sep) — Anonimisasi & inventaris

| # | Tugas | Keluaran |
|---|---|---|
| 3.1 | Daftar kolom PII per sheet (lihat `audit/data-profiling-2026-09-14.md` §5) + perlakuan (hapus / generalisasi / pseudonim) | `docs/data-governance/pii-dan-anonimisasi.md` |
| 3.2 | Implementasi de-identifikasi: pseudonim acak ber-seed (bukan hash NIM), tanggal lahir & alamat & judul & nama dosen **dihapus** | `src/insightera_akademik/anonymize/deidentify.py` → `data/anonymized/` |
| 3.3 | Uji otomatis "0 kolom PII" | `tests/data_quality/test_no_pii.py` lulus |
| 3.4 | Inventaris data: periode, populasi, baris, sifat riil/sintetis, peran | `docs/data-governance/data-inventory.md` (menutup M-06) |
| 3.5 | Keputusan untuk setiap anomali m-05 (perbaiki di Silver / karantina / pengecualian aturan bisnis) | tabel di `data-inventory.md` |

**Cadangan D-06:** jika izin yudisium belum ada per **Jumat 18 Sep**, S2 dikeluarkan; `fact_kelulusan` hanya dari Referensi 2012–2016.

## H4 (Kam 17 Sep) — Model dimensional v2 & KPI

| # | Tugas | Keluaran |
|---|---|---|
| 4.1 | Bus matrix: proses bisnis × dimensi seragam | `docs/modeling/bus-matrix.md` |
| 4.2 | ERD v2 sebagai satu sumber kebenaran (grain, PK/FK, tipe) | `docs/modeling/erd.dbml` |
| 4.3 | Source-to-target mapping: **setiap** kolom Gold → sheet/kolom sumber atau rumus turunan | `docs/modeling/source-to-target-mapping.md` (menutup C-04) |
| 4.4 | Data dictionary (termasuk definisi `sks`, `METODE`, `predikat`, `masa_studi_bulan`) | `docs/modeling/data-dictionary.md` |
| 4.5 | ≤ 8 KPI: definisi, rumus, tabel Gold, grain, sumber kebutuhan, label riil/sintetis | `docs/requirements/kpi-catalog.md`, `docs/requirements/stakeholder.md` (menutup M-08) |
| 4.6 | RQ final + definisi operasional + pemetaan sub-RQ → eksperimen → metrik | `docs/research/rq.md`, `docs/research/hypotheses.md` (menutup M-01) |

## H5 (Jum 18 Sep) — Generator sintetis v2

| # | Tugas | Keluaran |
|---|---|---|
| 5.1 | Tulis protokol **sebelum** kode: sumber batasan riil, parameter, seed, apa yang TIDAK dijamin | `docs/data-governance/data-sintetis-protokol.md` |
| 5.2 | Bangkitkan KRS + nilai per MK → **hitung** KHS (IP, IPK kumulatif) | `src/insightera_akademik/synthetic/generate_krs_khs.py` |
| 5.3 | Batasan keras per mahasiswa: `sks_kumulatif` akhir = `sks_final`; `ipk_kumulatif` akhir = `ipk_final` (yudisium teranonimkan); masa studi mengikuti distribusi riil | uji `tests/unit/test_synthetic_constraints.py` lulus 100 % |
| 5.4 | Kolom `is_synthetic = true`; log seed & parameter | `data/manifests/synthetic_generation_log.csv` |
| 5.5 | Scale factor SF10/SF100: replikasi dengan pseudonim unik + seed | `src/insightera_akademik/synthetic/scale_factor.py`, `configs/scale_factors.yaml` |

## H6–H7 (Sab 19 – Min 20 Sep) — Stack & Bronze (E0)

| # | Tugas | Keluaran |
|---|---|---|
| 6.1 | `docker-compose.yml`: MinIO + katalog Iceberg + Spark + Trino (Airflow & Superset boleh menyusul Minggu 2–3) | stack hidup; `docs/architecture/component-versions.md` dari **hasil instalasi nyata** |
| 6.2 | **Uji perilaku branch/WAP** pada 1 tabel: create branch → write → audit → publish → rollback; catat apakah publish multi-tabel atomik | `docs/architecture/catalog-and-branching.md` + log `results/raw/E0/` (M-03) |
| 6.3 | Ingest S1–S7 ke Bronze apa adanya + `source_file`, `sheet`, `sha256`, `ingest_ts`; cek **struktural** saja | `src/insightera_akademik/ingest/to_bronze.py`; row count Bronze = row count sumber |
| 6.4 | Catat spesifikasi perangkat (CPU, RAM, disk, OS) & batas resource Docker | `artifacts/reproducibility/environment_lock.txt` |

---

## Kriteria kelulusan Gate G1

- [ ] D-01…D-06 tercatat di `decision-log.md`
- [ ] Izin data terdokumentasi **atau** cadangan D-06 berlaku
- [ ] `test_no_pii` lulus pada `data/anonymized` **dan** Bronze
- [ ] `source-to-target-mapping.md`: 0 kolom Gold tanpa sumber/rumus
- [ ] `erd.dbml` v2 konsisten dengan bus matrix & data dictionary
- [ ] ≤ 8 KPI terdefinisi lengkap
- [ ] Generator v2: batasan keras terpenuhi 100 % (SF1); SF10/SF100 dapat dibangkitkan ulang identik dengan seed yang sama
- [ ] Uji branch → write → audit → publish → rollback berhasil & terlog
- [ ] Row count Bronze = sumber untuk S1–S7
- [ ] Tidak ada XLSX di riwayat Git

**Jika gagal di Rab 23 Sep:** E4 dipersempit (SF1 + SF10), E6 dibatalkan.
