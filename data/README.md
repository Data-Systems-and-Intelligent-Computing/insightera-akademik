# data/

> **Tidak ada isi folder ini yang di-commit**, kecuali `manifests/*.csv` dan `.gitkeep`.
> Sumber asli memuat data pribadi (audit C-03).

| Folder | Isi | Siapa yang mengisi | Masuk Git |
|---|---|---|---|
| `raw/` | XLSX asli dari pemberi data, **tanpa diubah** | mahasiswa (pindahkan dari root) | ✖ |
| `anonymized/` | hasil de-identifikasi; **satu-satunya input Bronze** | `src/insightera_akademik/anonymize/` | ✖ |
| `synthetic/` | KRS/KHS sintetis v2 + scale factor (SF1/10/100) | `src/insightera_akademik/synthetic/` | ✖ |
| `fault_injection/` | salinan data bercacat + ground truth | `src/insightera_akademik/fault_injection/` | ✖ |
| `manifests/` | `source_manifest.csv` (file, sheet, baris, sha256) · `anonymization_log.csv` (kolom dihapus/digeneralisasi, jumlah baris — **tanpa nilai**) · `synthetic_generation_log.csv` (seed, parameter, versi generator) | skrip terkait | ✔ |

## Berkas sumber saat audit (2026-09-14)

| Berkas | Sifat | Peran usulan |
|---|---|---|
| `MK SD.xlsx` | riil | S1 → `dim_mata_kuliah` |
| `PENDAFTARAN PESERTA YUDISIUM FAKULTAS SAINS (Jawaban).xlsx` | riil, **PII** | S2 → `fact_kelulusan` (setelah izin + anonimisasi) |
| `Data akademik 2012 - 2016.xlsx` | riil, pseudonim | S3 Referensi → `fact_kelulusan`, `dim_mahasiswa`; S4 Prodi → `dim_prodi`; S6 KHS → quarantine; S7 Kelas/Kurikulum → Silver opsional |
| `data sintetis krs khs.xlsx` | **campuran** (sheet `ref_yudis_bersih` = riil) | digantikan generator v2 (S5); disimpan sebagai arsip pembanding |

Checksum baseline: [../audit/data-profiling-2026-09-14.md](../audit/data-profiling-2026-09-14.md) §1.
