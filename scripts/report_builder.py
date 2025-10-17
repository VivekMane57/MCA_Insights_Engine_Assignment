import os, datetime as dt
import pandas as pd

CHANGE_ALL = "outputs/daily_change_log_all.csv"
CHANGE_DAILY = "outputs/daily_change_log.csv"
MASTER = "outputs/master_current.csv"

def safe_read(p):
    return pd.read_csv(p, dtype=str, low_memory=False) if os.path.exists(p) else pd.DataFrame()

def main():
    today = dt.date.today().isoformat()
    out_md = f"outputs/report_{today}.md"

    ch = safe_read(CHANGE_ALL) if os.path.exists(CHANGE_ALL) else safe_read(CHANGE_DAILY)
    m  = safe_read(MASTER)

    new = (ch["Change_Type"]=="New_Incorporation").sum() if not ch.empty else 0
    rmv = (ch["Change_Type"]=="Removed").sum() if not ch.empty else 0
    upd = (ch["Change_Type"]=="Field_Update").sum() if not ch.empty else 0
    states = len(m["State"].dropna().unique()) if not m.empty and "State" in m.columns else 0

    lines = [
        f"# MCA Insights Daily Report – {today}",
        "",
        f"- Master companies: {len(m):,}",
        f"- States covered: {states}",
        f"- New incorporations: {new}",
        f"- Deregistered: {rmv}",
        f"- Field updates: {upd}",
        "",
        "## Notes",
        "- Generated automatically from change logs and master dataset.",
    ]
    os.makedirs("outputs", exist_ok=True)
    with open(out_md, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"Wrote {out_md}")

if __name__ == "__main__":
    main()
