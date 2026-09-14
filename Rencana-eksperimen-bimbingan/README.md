# Rencana Eksperimen & Logbook Pelaksanaan (Insightera-Andina)

Rencana kerja 4 minggu + 3 hari buffer (14 Sep – 14 Okt 2026) untuk:
**"Perancangan dan Implementasi Data Lakehouse Berbasis Arsitektur Medallion untuk Pengelolaan Data Akademik Perguruan Tinggi"**
*(bingkai evaluasi usulan: Medallion + quality gate Write-Audit-Publish — menunggu keputusan D-01)*

* **Mahasiswa:** Syalaisha Andina Putriansyah (NIM 122450121)
* **Pembimbing:** Luluk Muthoharoh, M.Si · Ardika Satria, M.Si
* **Program Studi:** Sains Data, Institut Teknologi Sumatera (ITERA)
* **Status terkini:** Audit awal selesai (2026-09-14). Minggu 1 **BELUM DIMULAI**.

---

### Dokumen rekam jejak

👉 **[CATATAN_PROGRES_BIMBINGAN.md](./CATATAN_PROGRES_BIMBINGAN.md)** — diisi mahasiswa setiap akhir hari kerja/bimbingan.
👉 **[../audit/issue-register.md](../audit/issue-register.md)** — isu yang harus ditutup per gate.

---

## Peta gate

| Minggu | Tanggal | Gate | Fokus | Isu yang ditutup | Status |
|---|---|---|---|---|---|
| **[Minggu 1](./minggu-1/README.md)** | 14–20 Sep | **G1 Scope & Foundation Freeze** | keputusan cakupan, izin & anonimisasi, model v2, KPI, stack, Bronze, generator sintetis v2 | C-03, C-04, C-02 (desain), M-01, M-04, M-05, M-06, M-08 | BELUM DIMULAI |
| **[Minggu 2](./minggu-2/README.md)** | 21–27 Sep | **G2 Pipeline Benar** | Silver, Gold, WAP, quarantine, aturan DQ, oracle — E1, E2 | M-03 | TERJADWAL |
| **[Minggu 3](./minggu-3/README.md)** | 28 Sep–4 Okt | **G3 Bukti Utama** | E3 fault injection, E4 benchmark, E5 dashboard | M-02 | TERJADWAL |
| **[Minggu 4](./minggu-4/README.md)** | 5–11 Okt | **G4 Naskah & Reproducibility** | Bab IV–V, revisi Bab I–III, fresh run | C-01, M-07, M-09, m-01…m-04 | TERJADWAL |
| Buffer | 12–14 Okt | — | revisi hasil review pembimbing | sisa | — |

## Aturan pelaksanaan

1. **Gate tidak dilompati.** Eksperimen minggu berikutnya tidak dimulai sebelum gate minggu ini lolos, kecuali S1 memutuskan lain.
2. **Pemicu penyempitan otomatis:** jika G1 belum lolos pada **Rab 23 Sep**, E4 hanya SF1 + SF10 dan E6 dibatalkan.
3. **Bekukan sebelum melihat hasil:** `dq_rules.yaml` dibekukan sebelum set fault injection dibangkitkan; `benchmark.yaml` dibekukan sebelum run E4.
4. **Setiap angka di naskah** berasal dari `results/` yang dihasilkan skrip, tidak diketik manual.
5. **Tidak ada XLSX/PII di Git**, termasuk pada commit sementara.
6. Bimbingan singkat **Senin & Kamis** (usulan) untuk verifikasi gate; audit progres S2 setiap Senin.
