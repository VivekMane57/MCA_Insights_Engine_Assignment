import os, glob, subprocess, pandas as pd

def newest_three(pattern):
    files = sorted(glob.glob(pattern), key=os.path.getmtime)
    if len(files) < 3:
        raise SystemExit("Need at least three snapshot files in data/")
    return files[-3], files[-2], files[-1]

def safe_read(path):
    if not os.path.exists(path) or os.path.getsize(path) == 0:
        return pd.DataFrame(columns=["CIN","Change_Type","Field_Changed","Old_Value","New_Value","Date"])
    return pd.read_csv(path, dtype=str, low_memory=False)

os.makedirs("outputs", exist_ok=True)

d1, d2, d3 = newest_three("data/snapshot_*.csv")
print(f"Snapshots:\n  {d1}\n  {d2}\n  {d3}")

subprocess.run(["python","scripts/detect_changes.py","--old",d1,"--new",d2,"--out","outputs/change_log_d1_d2.csv"], check=True)
subprocess.run(["python","scripts/detect_changes.py","--old",d2,"--new",d3,"--out","outputs/change_log_d2_d3.csv"], check=True)

df1 = safe_read("outputs/change_log_d1_d2.csv")
df2 = safe_read("outputs/change_log_d2_d3.csv")
allc = pd.concat([df1, df2], ignore_index=True).drop_duplicates()
allc.to_csv("outputs/daily_change_log_all.csv", index=False)
print("Wrote outputs/change_log_d1_d2.csv, outputs/change_log_d2_d3.csv, outputs/daily_change_log_all.csv")
