import pandas as pd, os, random

SOURCES = [
    ("ZaubaCorp","https://www.zaubacorp.com/company/{cin}"),
    ("API Setu","https://apisetu.gov.in/mca/{cin}"),
    ("GST Portal","https://services.gst.gov.in/services/searchtp?gstin={cin}"),
    ("MCA21","https://www.mca.gov.in/")
]

def mock(row):
    s = random.choice(SOURCES)
    return pd.Series({
        "CIN": row.get("CIN",""),
        "COMPANY_NAME": row.get("CompanyName",""),
        "STATE": row.get("State",""),
        "STATUS": row.get("Status",""),
        "SOURCE": s[0],
        "FIELD": "Directors/Sector",
        "SOURCE_URL": s[1].format(cin=row.get("CIN",""))
    })

def main():
    os.makedirs("outputs", exist_ok=True)
    if os.path.exists("outputs/master_current.csv"):
        df = pd.read_csv("outputs/master_current.csv", dtype=str, low_memory=False)
    else:
        df = pd.read_csv("data/snapshot_day3.csv", dtype=str, low_memory=False)
    if os.path.exists("outputs/daily_change_log.csv"):
        changed = pd.read_csv("outputs/daily_change_log.csv", dtype=str)["CIN"].unique().tolist()
        df = df[df["CIN"].isin(changed)]
    if os.path.exists("outputs/enriched_mca.csv") and os.path.getsize("outputs/enriched_mca.csv") > 0:
        return
    enr = df.apply(mock, axis=1)
    enr.to_csv("outputs/enriched_mca.csv", index=False)

if __name__ == "__main__":
    main()
