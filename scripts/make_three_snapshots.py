import pandas as pd, os, datetime as dt

os.makedirs("data", exist_ok=True)
src = "outputs/mca_master.csv"
if not os.path.exists(src):
    raise SystemExit("Run `python scripts/merge_data.py` first")

df = pd.read_csv(src, dtype=str, low_memory=False)

d1 = (dt.date.today() - dt.timedelta(days=2)).isoformat()
d2 = (dt.date.today() - dt.timedelta(days=1)).isoformat()
d3 = dt.date.today().isoformat()

s1 = f"data/snapshot_{d1}.csv"
s2 = f"data/snapshot_{d2}.csv"
s3 = f"data/snapshot_{d3}.csv"

df.to_csv(s1, index=False)

df2 = df.copy()
if "AuthorizedCapital" in df2.columns:
    ac = pd.to_numeric(df2["AuthorizedCapital"], errors="coerce").fillna(0).astype(int)
    df2["AuthorizedCapital"] = (ac + 100000).astype(str)
df2.to_csv(s2, index=False)

df3 = df2.copy()
if "Status" in df3.columns:
    mask = df3.index.to_series().mod(50).eq(0)
    df3.loc[mask, "Status"] = "Strike Off"
df3.to_csv(s3, index=False)

print(f"Created:\n  {s1}\n  {s2}\n  {s3}")
