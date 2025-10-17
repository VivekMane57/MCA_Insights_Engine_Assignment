import pandas as pd, glob, os

RENAME_MAP = {
    "LLPIN/CIN":"CIN","CIN":"CIN",
    "Company / LLP Name":"CompanyName","CompanyName":"CompanyName","Company Name":"CompanyName",
    "State":"State","STATE":"State","CompanyROCcode":"State","ROC":"State",
    "Company Status":"Status","Status":"Status","CompanyStatus":"Status","COMPANY_STATUS":"Status","Company_Status":"Status","company status":"Status",
    "Authorized Capital":"AuthorizedCapital","AUTHORISED_CAP":"AuthorizedCapital",
    "Paid Up Capital":"PaidUpCapital","PAIDUP_CAP":"PaidUpCapital",
    "Date of Incorporation":"IncorporationDate","DATE_OF_REGISTRATION":"IncorporationDate",
    "Principal Business Activity (NIC)":"NIC","NIC Code":"NIC",
    "Class":"Class"
}

def read_any(path):
    ext = os.path.splitext(path)[1].lower()
    if ext == ".csv":
        return pd.read_csv(path, low_memory=False, dtype=str)
    if ext in (".xlsx", ".xls"):
        return pd.read_excel(path, dtype=str)
    raise ValueError(f"Unsupported file type: {path}")

def main():
    files = [f for f in glob.glob(os.path.join("data","states","*.*"))
             if os.path.splitext(f)[1].lower() in (".csv",".xlsx",".xls")]
    if not files:
        raise SystemExit("No state files found in data/states")
    dfs = []
    for f in files:
        df = read_any(f)
        df = df.rename(columns={c: RENAME_MAP.get(c, c) for c in df.columns})
        dfs.append(df)
    master = pd.concat(dfs, ignore_index=True).drop_duplicates(subset=["CIN"]).reset_index(drop=True)
    os.makedirs("outputs", exist_ok=True)
    master.to_csv("outputs/mca_master.csv", index=False)
    master.to_csv("outputs/master_current.csv", index=False)

if __name__ == "__main__":
    main()
