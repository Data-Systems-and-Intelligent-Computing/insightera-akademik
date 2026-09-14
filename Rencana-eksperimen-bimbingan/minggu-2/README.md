# Rencana Eksperimen — Minggu 2 (GATE G2: Pipeline Benar)
**Tanggal:** Senin 21 – Minggu 27 September 2026
**Status eksekusi:** **TERJADWAL**
**Eksperimen:** E1 (Functional Pipeline), E2 (Reconciliation Correctness)
**Isu yang ditutup:** M-03 · verifikasi desain C-02/C-04 pada data nyata

---

## H1–H2 (Sen 21 – Sel 22 Sep) — Silver

| # | Tugas | Keluaran |
|---|---|---|
| 1.1 | Kontrak skema Silver per tabel (nama, tipe, nullable, kunci) | `contracts/silver/*.yaml` |
| 1.2 | Transformasi: parsing tipe (termasuk IPK-tanggal), seragamkan label prodi, parsing `MASA STUDI` → bulan, dedup, satukan skema yudisium antar-periode | `src/insightera_akademik/silver/transform.py`, `sql/silver/` |
| 1.3 | **Katalog aturan DQ ≥ 15** (completeness, uniqueness, validity, referential, consistency) dengan id aturan, tabel, ekspresi, ambang, aksi (karantina/gagal) | `configs/dq_rules.yaml` |
| 1.4 | Quarantine: baris gagal + `rule_id` + `run_id` disimpan terpisah | `src/insightera_akademik/quality/quarantine.py`, `results/quarantine_reports/` |

## H3–H4 (Rab 23 – Kam 24 Sep) — Gold + WAP

| # | Tugas | Keluaran |
|---|---|---|
| 3.1 | Dimensi: `dim_mahasiswa`, `dim_prodi`, `dim_mata_kuliah`, `dim_semester`, `dim_tanggal` | `src/insightera_akademik/gold/build_dimensions.py` |
| 3.2 | Fakta: `fact_kelulusan` (HIST + YUD), `fact_krs`, `fact_khs` (diturunkan dari KRS) | `src/insightera_akademik/gold/build_facts.py` |
| 3.3 | WAP: branch → write → audit (aturan Silver + integritas referensial + grain unik + rekonsiliasi hitungan) → publish / quarantine | `src/insightera_akademik/wap/branch_publish.py` |
| 3.4 | Mode **B0** (tanpa gate, tulis langsung ke main) dengan kode transformasi yang **sama** | flag `--mode B0|B1` |
| 3.5 | DAG Airflow (atau Makefile cadangan): ingest → silver → gold, satu `run_id` | `dags/insightera_akademik_medallion_dag.py` |

## H5 (Jum 25 Sep) — E1 Functional pipeline

- Jalankan end-to-end mode B1 pada SF1.
- Catat per tahap: `rows_in`, `rows_out`, `rows_quarantined`, status task.
- Lineage: sampel 10 baris Gold ditelusuri balik ke `source_file` + `sheet` Bronze.
- **Harapan nyata:** `Data KHS` 2012–2016 dikarantina (D12); anomali m-05 muncul sesuai keputusan Minggu 1.

**Keluaran:** `experiments/E1_functional_pipeline/` + `results/processed/e1_layer_counts.csv`

## H6–H7 (Sab 26 – Min 27 Sep) — E2 Reconciliation

| # | Tugas | Keluaran |
|---|---|---|
| 6.1 | **Oracle independen** (pandas/DuckDB) dari `data/anonymized` + `data/synthetic`; **tidak** membaca Gold dan tidak memakai kode transformasi Spark | `src/insightera_akademik/reconciliation/oracle.py` |
| 6.2 | Bandingkan ukuran: jumlah lulusan per prodi × periode × predikat; rerata & median IPK lulusan; median masa studi; Σ SKS KRS per semester; rerata IP per angkatan × semester; jumlah baris per fakta | `results/reconciliation/e2_diff.csv` |
| 6.3 | Toleransi: count/sum = 0; rerata ≤ 0,005 | tabel lolos/gagal |
| 6.4 | Setiap selisih ≠ 0 → akar masalah tercatat (bug diperbaiki, **bukan** toleransi dilonggarkan) | `experiments/E2_reconciliation_correctness/README.md` |

---

## Kriteria kelulusan Gate G2

- [ ] Silver & Gold terbentuk untuk seluruh sumber dalam cakupan; kontrak skema lulus
- [ ] `dq_rules.yaml` ≥ 15 aturan, **dibekukan** (hash dicatat) sebelum Minggu 3
- [ ] E1: seluruh task sukses; row count & quarantine per tahap terdokumentasi; lineage 10 sampel valid
- [ ] E2: 100 % ukuran dalam toleransi, atau setiap selisih dijelaskan dan diperbaiki
- [ ] Publish ke main **tidak pernah** terjadi tanpa audit lolos (bukti log WAP)
- [ ] Mode B0 dan B1 menghasilkan Gold identik pada data bersih
