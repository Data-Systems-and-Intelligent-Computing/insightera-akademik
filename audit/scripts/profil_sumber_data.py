"""SUPERVISOR-2 AUDIT TOOL — BUKAN BUKTI MAHASISWA.
Profil read-only atas berkas sumber yang dilampirkan Andina (audit 2026-09-14).
Jalankan dari root folder andina:  python audit/scripts/profil_sumber_data.py
Butuh: pandas, openpyxl, scipy. Tidak mencetak nilai PII; hanya struktur & statistik agregat.
"""
import pandas as pd, numpy as np, warnings, re
warnings.filterwarnings("ignore")
pd.set_option("display.width", 200); pd.set_option("display.max_columns", 30); pd.set_option("display.max_rows", 80)
from pathlib import Path
D = str(Path(__file__).resolve().parents[2]) + "/"

def h(t): print("\n" + "=" * 8, t)

# ---------- MK SD
mk = pd.read_excel(D + "MK SD.xlsx")
h("MK SD"); print(mk.shape); print(mk.dtypes.to_dict())
print("dup kode:", mk["Kode Mata Kuliah Baru"].duplicated().sum(), "null:", mk.isna().sum().to_dict())
print("prefix:", mk["Kode Mata Kuliah Baru"].str[:4].value_counts().to_dict())
print("KATEGORI:", mk["KATEGORI"].value_counts(dropna=False).to_dict())
print("METODE:", mk["METODE"].value_counts(dropna=False).to_dict())
print("SM:", mk["SM"].value_counts(dropna=False).sort_index().to_dict())
print("SKS:", mk["SKS"].value_counts().to_dict(), "PRAKT:", mk["PRAKT"].value_counts().to_dict(), "sum SKS:", mk["SKS"].sum(), "sum SKS+PRAKT:", (mk["SKS"] + mk["PRAKT"]).sum())
print(mk[mk.isna().any(axis=1)])

# ---------- synthetic
syn = pd.read_excel(D + "data sintetis krs khs.xlsx", sheet_name=None)
krs, khs, dw, ry = syn["fact_krs"], syn["fact_khs"], syn["dim_waktu"], syn["ref_yudis_bersih"]
h("SYN fact_krs"); print(krs.shape, "null:", krs.isna().sum().sum(), "dup id_krs:", krs["id_krs"].duplicated().sum(), "dup full rows:", krs.duplicated().sum())
print("n mhs:", krs["id_mahasiswa"].nunique(), "prodi:", krs["kode_prodi"].value_counts().to_dict())
print("semester:", krs["semester"].value_counts().sort_index().to_dict())
print("sks:", krs["sks"].value_counts().sort_index().to_dict())
print("id_waktu:", sorted(krs["id_waktu"].unique()))
m = krs.merge(mk, left_on="kode_matakuliah", right_on="Kode Mata Kuliah Baru", how="left")
print("MK not in MK SD:", m["Mata Kuliah"].isna().sum(), "distinct codes:", krs["kode_matakuliah"].nunique())
mm = m.dropna(subset=["Mata Kuliah"])
print("sks==SKS:", (mm["sks"] == mm["SKS"]).mean().round(3), " sks==SKS+PRAKT:", (mm["sks"] == mm["SKS"] + mm["PRAKT"]).mean().round(3))
print("sks mismatch examples:\n", mm.loc[(mm["sks"] != mm["SKS"]) & (mm["sks"] != mm["SKS"] + mm["PRAKT"]), ["kode_matakuliah", "Mata Kuliah", "sks", "SKS", "PRAKT"]].drop_duplicates().head(10))
print("semester taken == SM (curriculum):", (mm["semester"] == mm["SM"]).mean().round(3))
rt = krs.groupby(["id_mahasiswa", "kode_matakuliah"]).size()
print("student-MK taken >1:", (rt > 1).sum())
sem_per = krs.groupby("id_mahasiswa")["semester"].max().value_counts().sort_index().to_dict()
print("max semester per student:", sem_per)
# waktu vs semester consistency
first = krs.groupby("id_mahasiswa")["id_waktu"].min()
print("cohort (first id_waktu):", first.value_counts().sort_index().to_dict())

h("SYN fact_khs"); print(khs.shape, "null:", khs.isna().sum().to_dict(), "dup (mhs,sem):", khs.duplicated(["id_mahasiswa", "semester"]).sum())
print("n mhs:", khs["id_mahasiswa"].nunique(), "ip range:", khs["ip_semester"].min(), khs["ip_semester"].max(), "ipk range:", khs["ipk"].min(), khs["ipk"].max())
print("total_sks_diambil:", khs["total_sks_diambil"].describe().round(2).to_dict())
agg = krs.groupby(["id_mahasiswa", "semester"])["sks"].sum().rename("krs_sks").reset_index()
j = khs.merge(agg, on=["id_mahasiswa", "semester"], how="outer", indicator=True)
print("KHS vs KRS join:", j["_merge"].value_counts().to_dict())
jb = j[j["_merge"] == "both"]
print("total_sks_diambil == sum KRS sks:", (jb["total_sks_diambil"] == jb["krs_sks"]).mean().round(3), " mean abs diff:", (jb["total_sks_diambil"] - jb["krs_sks"]).abs().mean().round(2))
# ipk recompute
def recompute(g):
    g = g.sort_values("semester")
    w = (g["ip_semester"] * g["total_sks_diambil"]).cumsum() / g["total_sks_diambil"].cumsum()
    return pd.Series((w.round(2) - g["ipk"]).abs().values, index=g.index)
d = khs.groupby("id_mahasiswa", group_keys=False).apply(recompute)
print("IPK recompute |diff|<=0.01:", (d <= 0.011).mean().round(3), " max diff:", round(d.max(), 3))
print("waktu in khs not in dim_waktu:", set(khs["id_waktu"]) - set(dw["id_waktu"]), " krs:", set(krs["id_waktu"]) - set(dw["id_waktu"]))

h("SYN dim_waktu"); print(dw)
h("SYN ref_yudis_bersih"); print(ry.shape, ry.dtypes.to_dict(), "null:", ry.isna().sum().to_dict())
print(ry.head(3)); print("predikat:", ry["predikat"].value_counts().to_dict())
print("ipk_clean:", ry["ipk_clean"].describe().round(3).to_dict()); print("sks_final:", ry["sks_final"].describe().round(1).to_dict())
print("predikat vs ipk:\n", ry.groupby("predikat")["ipk_clean"].agg(["min", "max", "count"]))
ids_y = set(ry["id_mahasiswa"].astype(str)); ids_k = set(khs["id_mahasiswa"])
last = khs.sort_values("semester").groupby("id_mahasiswa").tail(1).set_index("id_mahasiswa")
cum = khs.groupby("id_mahasiswa")["total_sks_diambil"].sum()
ov = ry.set_index(ry["id_mahasiswa"].astype(str)).join(last[["ipk", "semester"]], how="inner").join(cum)
if len(ov):
    print("ipk_clean == last khs ipk:", (ov["ipk_clean"].round(2) == ov["ipk"].round(2)).mean().round(3), " sks_final == cum sks:", (ov["sks_final"] == ov["total_sks_diambil"]).mean().round(3))
    print("last semester of yudisium students:", ov["semester"].value_counts().to_dict())
print("khs students without yudisium ref:", len(ids_k - ids_y))

# ---------- real 2012-2016
ak = pd.read_excel(D + "Data akademik 2012 - 2016.xlsx", sheet_name=None)
ref = ak["Data Referensi Mahasiswaa"]
h("REAL Referensi Mahasiswa"); print(ref.shape, ref.dtypes.to_dict()); print("null:", ref.isna().sum().to_dict())
print("dup Id:", ref["Id_mahasiswa"].duplicated().sum(), " Id sample:", ref["Id_mahasiswa"].astype(str).head(3).tolist(), " Id len:", ref["Id_mahasiswa"].astype(str).str.len().value_counts().to_dict())
print("JK:", ref["Jenis Kelamin"].value_counts(dropna=False).to_dict())
print("Status:", ref["Status Mahasiswa"].value_counts(dropna=False).to_dict())
for c in ["Tanggal Masuk", "Tanggal Keluar"]:
    s = pd.to_datetime(ref[c], errors="coerce"); print(c, "min/max:", s.min(), s.max(), "unparseable non-null:", (s.isna() & ref[c].notna()).sum(), " year counts:", s.dt.year.value_counts().sort_index().to_dict())
print("IPK:", ref["IPK"].describe().round(3).to_dict()); print("IPK >4 or <0:", ((ref["IPK"] > 4) | (ref["IPK"] < 0)).sum(), " IPK==0:", (ref["IPK"] == 0).sum())
print("Total SKS:", ref["Total SKS"].describe().round(1).to_dict()); print("Jumlah MK:", ref["Jumlah MK"].describe().round(1).to_dict())
print("kode prodi:", ref["kode prodi"].nunique(), ref["kode prodi"].value_counts().head(12).to_dict())
masuk = pd.to_datetime(ref["Tanggal Masuk"], errors="coerce"); keluar = pd.to_datetime(ref["Tanggal Keluar"], errors="coerce")
print("keluar < masuk:", (keluar < masuk).sum())
print("status x keluar null:\n", pd.crosstab(ref["Status Mahasiswa"], keluar.isna()))

ps = ak["Data Program Studi"]; h("REAL Program Studi"); print(ps.shape, ps.head(5).to_string()); print("Fakultas:", ps["Fakultas"].value_counts(dropna=False).to_dict()); print("dup kode:", ps["Kode"].duplicated().sum())
print("ref prodi not in prodi table:", set(ref["kode prodi"].dropna().astype(str)) - set(ps["Kode"].astype(str)))
print("SD in prodi:", ps[ps["Nama Program Studi"].astype(str).str.contains("Data", case=False)].to_string())
kl = ak["Data Kelas"]; h("REAL Kelas"); print(kl.shape, kl.head(5).to_string()); print("null:", kl.isna().sum().to_dict(), "nunique nama_mk:", kl["nama_mk"].nunique(), "dup rows:", kl.duplicated().sum()); print("kuota:", kl["kuota"].describe().round(1).to_dict())
print("nama_mk overlapping MK SD names:", len(set(kl["nama_mk"].astype(str).str.lower().str.strip()) & set(mk["Mata Kuliah"].astype(str).str.lower().str.strip())))
ku = ak["Data Kurikulum"]; h("REAL Kurikulum"); print(ku.shape, ku.head(8).to_string()); print(ku["Jumlah SKS Total"].describe().round(1).to_dict())
kh = ak["Data KHS"]; h("REAL KHS"); print(kh.shape, kh.dtypes.to_dict(), "null:", kh.isna().sum().to_dict()); print("IP:", kh["IP"].describe().round(3).to_dict(), " IP>4:", (kh["IP"] > 4).sum(), " IP==0:", (kh["IP"] == 0).sum()); print("SKS:", kh["SKS"].describe().round(1).to_dict(), " SKS==0:", (kh["SKS"] == 0).sum(), " dup rows:", kh.duplicated().sum())
print("columns: ", list(kh.columns))

# ---------- yudisium
yd = pd.read_excel(D + "PENDAFTARAN PESERTA YUDISIUM FAKULTAS SAINS (Jawaban).xlsx", sheet_name=None)
h("YUDISIUM")
frames = []
allcols = set()
for s, df in yd.items():
    if s in ("NVScriptsProperties",) or s.startswith("DO NOT DELETE"):
        txt = df.astype(str).apply(lambda c: c.str.contains("@")).sum().sum()
        print(f"sheet {s!r}: shape {df.shape}, cells containing '@': {txt}")
        continue
    df = df.dropna(how="all")
    allcols |= set(df.columns.astype(str))
    ipk_c = [c for c in df.columns if str(c).startswith("IPK") or str(c).startswith("Indeks Prestasi")]
    sks_c = [c for c in df.columns if str(c).startswith("Jumlah SKS") or str(c).startswith("SKS FINAL")]
    tgl_c = [c for c in df.columns if str(c).strip() == "Tanggal Yudisium"]
    out = pd.DataFrame({"sheet": s, "prodi": df["Program Studi"].astype(str).str.strip(),
                        "ipk": pd.to_numeric(df[ipk_c[0]].astype(str).str.replace(",", "."), errors="coerce") if ipk_c else np.nan,
                        "sks": pd.to_numeric(df[sks_c[0]], errors="coerce") if sks_c else np.nan,
                        "predikat": df["PREDIKAT"] if "PREDIKAT" in df else np.nan,
                        "masa": df["MASA STUDI"].astype(str) if "MASA STUDI" in df else np.nan,
                        "tgl": df[tgl_c[0]].astype(str) if tgl_c else np.nan})
    frames.append(out)
Y = pd.concat(frames, ignore_index=True)
print("total rows:", len(Y), " per sheet:", Y["sheet"].value_counts(sort=False).to_dict())
print("prodi:", Y["prodi"].value_counts().to_dict())
print("ipk:", Y["ipk"].describe().round(3).to_dict(), " ipk unparsed:", Y["ipk"].isna().sum())
print("sks:", Y["sks"].describe().round(1).to_dict(), " unparsed:", Y["sks"].isna().sum())
print("predikat:", Y["predikat"].value_counts(dropna=False).to_dict())
print("masa studi samples:", Y["masa"].drop_duplicates().head(12).tolist())
print("tgl yudisium samples:", Y["tgl"].drop_duplicates().head(8).tolist())
pii = [c for c in allcols if re.search(r"nama|nim|email|alamat|lahir|hp|telp|wa|judul|pembimbing|penguji|wali|kaprodi|nip|nrk|url|doc id|berkas", c, re.I)]
print("PII / quasi-identifier columns across sheets:", sorted(pii))
sd = Y[Y["prodi"].str.contains("Data", case=False)]
print("Sains Data rows:", len(sd), "ipk:", sd["ipk"].describe().round(3).to_dict(), "sks:", sd["sks"].describe().round(1).to_dict())
from scipy import stats
if len(sd) > 3:
    print("KS syn ipk_clean vs real SD yudisium ipk:", stats.ks_2samp(ry["ipk_clean"].dropna(), sd["ipk"].dropna()))
    print("KS syn ipk_clean vs real ALL yudisium ipk:", stats.ks_2samp(ry["ipk_clean"].dropna(), Y["ipk"].dropna()))
    print("KS syn sks_final vs real SD sks:", stats.ks_2samp(ry["sks_final"].dropna(), sd["sks"].dropna()))
print("ref_yudis ipk multiset == SD yudisium ipk multiset?", sorted(ry["ipk_clean"].round(2).tolist())[:10], sorted(sd["ipk"].round(2).dropna().tolist())[:10])

# ---------- verifikasi tambahan: ref_yudis_bersih vs yudisium riil, realisme temporal sintetis
from collections import Counter
h("VERIFIKASI ref_yudis_bersih vs yudisium riil Sains Data")
real_ipk = Counter(pd.to_numeric(sd["ipk"], errors="coerce").dropna().round(2))
syn_ipk = Counter(ry["ipk_clean"].round(2))
print("IPK sama (multiset overlap):", sum((real_ipk & syn_ipk).values()), "dari", len(ry))
print("sks_final multiset identik:", sorted(ry["sks_final"]) == sorted(pd.to_numeric(sd["sks"], errors="coerce").dropna().astype(int)))
print("predikat riil SD:", sd["predikat"].value_counts().to_dict(), " ref_yudis:", ry["predikat"].value_counts().to_dict())
def _yrs(x):
    m_ = re.match(r"\s*(\d+)\s*Tahun\s*(\d+)\s*Bulan", str(x))
    return int(m_.group(1)) + int(m_.group(2)) / 12 if m_ else np.nan
yrs = sd["masa"].map(_yrs)
print("masa studi riil SD (tahun):", yrs.describe().round(2).to_dict())
lastk = khs.sort_values("semester").groupby("id_mahasiswa").tail(1).set_index("id_mahasiswa")
dd = ry.set_index("id_mahasiswa").join(lastk)
print("IPK akhir sintetis - ipk_clean:", (dd["ipk"] - dd["ipk_clean"]).describe().round(3).to_dict())
print("Sangat Memuaskan dengan IPK > 3.50:", int(((ry["predikat"] == "Sangat Memuaskan") & (ry["ipk_clean"] > 3.5)).sum()))
