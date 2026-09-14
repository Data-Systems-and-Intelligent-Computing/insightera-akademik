# Rencana Eksperimen — Minggu 3 (GATE G3: Bukti Utama)
**Tanggal:** Senin 28 September – Minggu 4 Oktober 2026
**Status eksekusi:** **TERJADWAL**
**Eksperimen:** E3 (Quality-Gate Fault Injection), E4 (Performance & WAP Overhead), E5 (Dashboard KPI Correctness)
**Isu yang ditutup:** M-02

---

## H1–H3 (Sen 28 – Rab 30 Sep) — E3 Fault injection

**Desain**

| Faktor | Level |
|---|---|
| Jenis cacat | D01–D12 (README §12.1); D08–D12 memakai pola nyata dari data |
| Tingkat injeksi | 1 %, 5 % (per tabel sasaran) |
| Seed | 5 per kombinasi |
| Mode | B0 (tanpa gate), B1 (WAP) |
| Data | SF1 |

**Langkah**

1. Pastikan hash `configs/dq_rules.yaml` = hash yang dibekukan di G2.
2. `src/insightera_akademik/fault_injection/inject.py` membangkitkan salinan data + **ground truth** baris cacat (`row_key`, `defect_code`) di `data/fault_injection/`.
3. Jalankan B0 dan B1 per kombinasi.
4. Hitung per jenis cacat × tingkat × mode:
   - recall = cacat terdeteksi / cacat disuntikkan
   - FPR = baris bersih dikarantina / baris bersih
   - kontaminasi Gold = baris cacat yang sampai di Gold
5. **Kontrol positif (H5):** B0 wajib menunjukkan kontaminasi > 0 untuk cacat yang mengubah Gold. Jika tidak, periksa injektor/oracle **sebelum** menafsirkan B1.
6. Cacat yang tidak tertangkap dilaporkan apa adanya (batas aturan), **tanpa** menambah aturan setelah melihat hasil.

**Keluaran:** `results/raw/E3/*.csv` · `results/processed/e3_detection.csv` · tabel recall/FPR dengan interval Wilson 95 % · figur recall per jenis cacat.

## H4–H5 (Kam 1 – Jum 2 Okt) — E4 Benchmark

**Desain** (dibekukan di `configs/benchmark.yaml` sebelum run pertama)

| Faktor | Level |
|---|---|
| Scale factor | SF1, SF10, SF100 |
| Mode | B0, B1 |
| Tahap | ingest, bronze→silver, silver→gold, end-to-end |
| Repetisi | 1 warm-up (dibuang) + ≥ 5 terukur |
| Urutan | diacak/diselang antar mode & SF |

**Kontrol konfonder**
- Superset & Airflow webserver dimatikan saat benchmark (atau resource terisolasi dan dicatat).
- Konfigurasi Spark & batas resource Docker tetap; hash konfigurasi dicatat per run.
- Catat `n_data_files` & `n_snapshots` per tabel (efek small files / riwayat snapshot); reset tabel antar run **atau** catat sebagai variabel.

**Analisis**
- median + IQR per sel;
- overhead = median(B1)/median(B0) − 1, bootstrap CI 95 % (≥ 2.000 resample);
- throughput = rows_out / wall_time_s;
- **tanpa** klaim "signifikan" jika tidak diuji dengan uji yang sesuai.

**Keluaran:** `results/benchmark/e4_runs.csv` · `results/processed/e4_summary.csv` · figur waktu vs SF (log-scale, B0 vs B1, dengan IQR).

## H6–H7 (Sab 3 – Min 4 Okt) — E5 Dashboard

| # | Tugas | Keluaran |
|---|---|---|
| 6.1 | Hubungkan Superset → Trino → Gold | `infra/superset/`, `infra/trino/catalog/` |
| 6.2 | Bangun ≤ 8 KPI dari `kpi-catalog.md`; KPI sintetis diberi label **SINTETIS** di judul | `dashboards/superset/` (export), `dashboards/screenshots/` |
| 6.3 | Set uji: untuk tiap KPI ≥ 3 kombinasi filter → nilai Superset vs query SQL langsung ke Gold vs oracle | `results/processed/e5_kpi_check.csv` (target 100 % cocok) |
| 6.4 | Waktu muat: 10 kali muat ulang per dashboard, cache dikosongkan secara konsisten; laporkan median | `results/processed/e5_load_time.csv` |

---

## Kriteria kelulusan Gate G3

- [ ] E3: D01–D12 × 2 tingkat × 5 seed × 2 mode selesai; kontrol positif B0 terpenuhi
- [ ] E3: `dq_rules.yaml` tidak berubah sejak G2 (hash sama)
- [ ] E4: 3 SF × 2 mode × ≥ 5 repetisi (atau SF1+SF10 bila pemicu penyempitan aktif)
- [ ] E4: overhead dengan CI 95 %; spesifikasi perangkat terdokumentasi
- [ ] E5: seluruh KPI 100 % cocok pada set uji; waktu muat median tercatat
- [ ] Seluruh tabel & figur dihasilkan skrip dari `results/`, tanpa angka manual
