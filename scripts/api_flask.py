from flask import Flask, request, jsonify
import pandas as pd, os

app = Flask(__name__)

def load_master():
    p = "outputs/master_current.csv"
    return pd.read_csv(p, dtype=str, low_memory=False) if os.path.exists(p) else pd.DataFrame()

@app.get("/search_company")
def search_company():
    df = load_master()
    if df.empty:
        return jsonify([])
    q = (request.args.get("q") or "").lower()
    state = request.args.get("state")
    status = request.args.get("status")
    year = request.args.get("year")

    if q:
        cm = df["CIN"].str.lower().str.contains(q, na=False)
        nm = df["CompanyName"].str.lower().str.contains(q, na=False)
        df = df[cm | nm]
    if state:
        df = df[df.get("State","") == state]
    if status:
        df = df[df.get("Status","") == status]
    if year and "IncorporationDate" in df.columns:
        y = pd.to_datetime(df["IncorporationDate"], errors="coerce").dt.year.astype("Int64").astype(str)
        df = df[y == year]

    return jsonify(df.head(500).to_dict(orient="records"))

if __name__ == "__main__":
    app.run(port=8000, debug=True)
