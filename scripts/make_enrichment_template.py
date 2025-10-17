import pandas as pd, os

log_path = "outputs/daily_change_log_all.csv"
master_path = "outputs/master_current.csv"

if not (os.path.exists(log_path) and os.path.exists(master_path)):
    raise SystemExit("Run the three-day pipeline first")

cl = pd.read_csv(log_path, dtype=str, low_memory=False)
m  = pd.read_csv(master_path, dtype=str, low_memory=False)

needed = ["CIN","CompanyName","State","Status"]
for c in needed:
    if c not in m.columns:
        m[c] = ""

master_sub = m[["CIN","CompanyName","State","Status"]]
changed = cl.merge(master_sub, on="CIN", how="left")

priority = pd.Categorical(changed["Change_Type"], ["New_Incorporation","Field_Update","Removed"])
changed["__prio"] = priority
template = (changed.sort_values(["__prio"])
                  .drop(columns=["__prio"])
                  .drop_duplicates("CIN")
                  .head(120))

template = template.assign(Sector="", Directors="", RegisteredAddress="", SOURCE="", SOURCE_URL="")

cols = ["CIN","CompanyName","State","Status","Change_Type","Field_Changed","Old_Value","New_Value","Date",
        "Sector","Directors","RegisteredAddress","SOURCE","SOURCE_URL"]
for c in cols:
    if c not in template.columns: template[c] = ""

template = template[cols]
os.makedirs("outputs", exist_ok=True)
template.to_csv("outputs/enrichment_template.csv", index=False)
print("Wrote outputs/enrichment_template.csv")
