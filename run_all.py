import os, glob

def newest_two(pattern):
    files = sorted(glob.glob(pattern), key=os.path.getmtime)
    if len(files) < 2:
        raise SystemExit("Need at least two snapshot files in data/")
    return files[-2], files[-1]

print("1) Merging state files...")
os.system("python scripts/merge_data.py")

old, new = newest_two("data/snapshot_*.csv")
print(f"2) Detecting changes between {old} and {new} ...")
os.system(f"python scripts/detect_changes.py --old {old} --new {new}")

print("3) Enriching changed companies ...")
os.system("python scripts/enrich_data.py")

print("4) Generating AI summary ...")
os.system("python scripts/ai_summary.py")

print("Done. Launch Streamlit with:\n    python -m streamlit run scripts/app_streamlit.py")
