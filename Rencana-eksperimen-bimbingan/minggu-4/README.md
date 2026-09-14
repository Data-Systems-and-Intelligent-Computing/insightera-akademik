# Rencana Eksperimen — Minggu 4 (GATE G4: Naskah & Reproducibility)
**Tanggal:** Senin 5 – Minggu 11 Oktober 2026 (buffer: Senin 12 – Rabu 14 Oktober)
**Status eksekusi:** **TERJADWAL**
**Eksperimen:** analisis akhir, E6 (opsional), fresh run
**Isu yang ditutup:** C-01, M-07, M-09, m-01…m-04

---

## H1 (Sen 5 Okt) — Finalisasi hasil

- Bangkitkan ulang seluruh tabel & figur dari `results/` dengan satu perintah (`make figures tables`).
- Periksa rantai jejak untuk setiap tabel/figur: sub-RQ → eksperimen → config → run_id → raw → processed → tabel/figur.
- E6 (opsional, **hanya** jika G3 lolos tepat waktu): time travel, rollback, schema evolution sebagai uji fungsional lulus/gagal.

## H2–H3 (Sel 6 – Rab 7 Okt) — Bab IV Hasil & Pembahasan

Struktur usulan:

1. **Implementasi artefak** — arsitektur v2, stack & versi, model dimensional v2, statistik layer (E1).
2. **Kebenaran Gold** — rekonsiliasi (E2) → sub-RQ 1 / H1.
3. **Efektivitas quality gate** — recall/FPR per jenis cacat, B0 vs B1, cacat nyata vs buatan (E3) → sub-RQ 2 / H2, H3, H5.
4. **Overhead WAP** — waktu & throughput per SF, overhead + CI (E4) → sub-RQ 3 / H4.
5. **Dashboard** — KPI & kecocokan (E5) → sub-RQ 4.
6. **Pembahasan** — hasil vs hipotesis (diterima/ditolak), temuan data nyata (katalog cacat), perbandingan dengan penelitian terdahulu, implikasi bagi pengelola data akademik.
7. **Ancaman terhadap validitas** — satu institusi, data proses studi sintetis, survivorship data historis, scale factor sebagai replikasi, aturan DQ ditulis penulis.

**Aturan:** setiap angka mengutip tabel/figur; tidak ada kata "signifikan" tanpa uji; hasil sintetis selalu dilabeli.

## H4 (Kam 8 Okt) — Bab V + revisi Bab I–III

| Bagian | Revisi |
|---|---|
| §1.2–1.3 | RQ & tujuan sesuai `docs/research/rq.md` |
| §1.4 | batasan sesuai `data-inventory.md` (periode, populasi, sintetis) |
| §2.1 | tabel penelitian terdahulu ≥ 10 studi + paragraf gap + strategi penelusuran (M-07) |
| §2.4 | metadata rujukan [26] diperbaiki dari sumber primer |
| §2.7–2.13 | sitasi (m-04) |
| §3.2 | Tabel 3.1 v2; **hapus klaim "tidak memuat identitas"**, ganti dengan prosedur anonimisasi (C-03) |
| §3.4 | Gambar 3.2 v2, Tabel 3.2/3.3 & Gambar 3.3 dari `erd.dbml` v2 (M-03, M-04) |
| §3.6 | Tabel 3.4 v2: indikator E1–E5 dengan target terukur (M-02) |
| Bab V | satu kesimpulan per sub-RQ, berbasis bukti; saran berbasis batasan |

## H5 (Jum 9 Okt) — Abstrak, lampiran, kebersihan naskah

- Abstrak ID/EN (tujuan, metode, hasil kuantitatif utama, kesimpulan), kata kunci.
- Lampiran: aturan DQ, kontrak skema Gold, konfigurasi benchmark, potongan DAG, katalog KPI.
- Hapus seluruh templat (`grep -ri "lorem\|hello, here\|xxxx\|incmatrix"` kosong).
- Konsistensi "Jenis karya" di halaman persetujuan publikasi.
- Salah ketik m-01; atribusi gambar m-03.

## H6–H7 (Sab 10 – Min 11 Okt) — Fresh run & reproducibility

1. Clone bersih ke direktori baru; letakkan hanya `data/raw/` (di luar Git) sesuai `source_manifest.csv` (checksum cocok).
2. `make all`: anonimisasi → sintetis → Bronze → Silver → Gold → E2 → 1 konfigurasi E3 → E4 SF1 (≥ 3 repetisi) → figur.
3. Bandingkan dengan hasil utama: E2 identik; E3 identik (seed sama); E4 dalam rentang IQR yang dilaporkan.
4. Tulis `artifacts/reproducibility/reproducibility_report.md` (langkah, durasi, perbedaan, penjelasan).

---

## Kriteria kelulusan Gate G4

- [ ] Bab IV–V lengkap; setiap sub-RQ terjawab dengan bukti yang dirujuk
- [ ] Bab I–III direvisi sesuai tabel di atas; klaim privasi diperbaiki
- [ ] Tidak ada templat tersisa di naskah
- [ ] Seluruh tabel/figur dihasilkan ulang dengan satu perintah
- [ ] Fresh run berhasil dan terdokumentasi
- [ ] Register isu: seluruh KRITIS berstatus SELESAI atau RISIKO DITERIMA (dengan keputusan S1)

## Buffer (Sen 12 – Rab 14 Okt)

Hanya untuk revisi dari review pembimbing. **Tidak** untuk eksperimen baru.
