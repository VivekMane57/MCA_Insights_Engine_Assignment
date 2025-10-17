import pandas as pd, os, argparse, datetime as dt

FIELDS_TO_COMPARE = ["Status","AuthorizedCapital","PaidUpCapital","Class"]

def load(p):
    return pd.read_csv(p, dtype=str, low_memory=False)

def detect_changes(old_df, new_df):
    merged = old_df.merge(new_df, on="CIN", how="outer", suffixes=("_old","_new"), indicator=True)
    new_incorp = merged[merged["_merge"]=="right_only"]["CIN"].tolist()
    removed = merged[merged["_merge"]=="left_only"]["CIN"].tolist()
    changes = []
    old_k = old_df.set_index("CIN")
    new_k = new_df.set_index("CIN")
    common = old_k.index.intersection(new_k.index)
    for cin in common:
        for field in FIELDS_TO_COMPARE:
            ov = old_k[field][cin] if field in old_k.columns else None
            nv = new_k[field][cin] if field in new_k.columns else None
            if (ov or "") != (nv or ""):
                changes.append({
                    "CIN": cin,
                    "Change_Type": "Field_Update",
                    "Field_Changed": field,
                    "Old_Value": ov,
                    "New_Value": nv,
                    "Date": dt.date.today().isoformat()
                })
    logs = [{"CIN":c,"Change_Type":"New_Incorporation","Field_Changed":"","Old_Value":"","New_Value":"","Date":dt.date.today().isoformat()} for c in new_incorp]
    logs += [{"CIN":c,"Change_Type":"Removed","Field_Changed":"","Old_Value":"","New_Value":"","Date":dt.date.today().isoformat()} for c in removed]
    logs += changes
    return pd.DataFrame(logs)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--old", required=True)
    ap.add_argument("--new", required=True)
    ap.add_argument("--out", default="outputs/daily_change_log.csv")
    args = ap.parse_args()

    old_df = load(args.old)
    new_df = load(args.new)

    os.makedirs("outputs", exist_ok=True)
    change_log = detect_changes(old_df, new_df)
    cols = ["CIN","Change_Type","Field_Changed","Old_Value","New_Value","Date"]
    if change_log.empty:
        change_log = pd.DataFrame(columns=cols)
    else:
        change_log = change_log.reindex(columns=cols)
    change_log.to_csv(args.out, index=False)

    new_df.drop_duplicates(subset=["CIN"]).to_csv("outputs/master_current.csv", index=False)

if __name__ == "__main__":
    main()
