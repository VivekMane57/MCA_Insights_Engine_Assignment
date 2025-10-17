import pandas as pd, os, datetime as dt

os.makedirs("data", exist_ok=True)
src = "outputs/mca_master.csv"
if not os.path.exists(src):
    raise SystemExit("Run `python scripts/merge_data.py` first")

df = pd.read_csv(src, dtype=str, low_memory=False)

day1 = (dt.date.today() - dt.timedelta(days=1)).isoformat()
day2 = dt.date.today().isoformat()

snap1 = f"data/snapshot_{day1}.csv"
snap2 = f"data/snapshot_{day2}.csv"

df.to_csv(snap1, index=False)

df2 = df.copy()
if "AuthorizedCapital" in df2.columns:
    ac = pd.to_numeric(df2["AuthorizedCapital"], errors="coerce").fillna(0).astype(int)
    df2["AuthorizedCapital"] = (ac + 100000).astype(str)
df2.to_csv(snap2, index=False)

print(f"Created:\n  {snap1}\n  {snap2}")
