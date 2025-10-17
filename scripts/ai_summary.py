import pandas as pd, os, json

def main():
    p = "outputs/daily_change_log.csv"
    if not os.path.exists(p): 
        p = "outputs/daily_change_log_all.csv"
    if not os.path.exists(p):
        raise SystemExit("Run detect_changes.py or run_three_day.py first")
    df = pd.read_csv(p, dtype=str)
    s = {
        "New_incorporations": int((df["Change_Type"]=="New_Incorporation").sum()),
        "Deregistered_or_Removed": int((df["Change_Type"]=="Removed").sum()),
        "Field_updates": int((df["Change_Type"]=="Field_Update").sum())
    }
    os.makedirs("outputs", exist_ok=True)
    with open("outputs/daily_summary.json","w") as f: json.dump(s,f,indent=2)
    with open("outputs/daily_summary.txt","w") as f:
        f.write(f"New incorporations: {s['New_incorporations']}\nDeregistered: {s['Deregistered_or_Removed']}\nUpdated records: {s['Field_updates']}\n")

if __name__ == "__main__":
    main()
