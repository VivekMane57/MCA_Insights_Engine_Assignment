# 📊 MCA Insights Engine  
### Consolidated MCA Data, Automated Change Detection, and AI-Powered Daily Insights  

---

## 🚀 Overview  
**MCA Insights Engine** is a Python + Streamlit-based data analysis system that automates the process of:
- Consolidating MCA (Ministry of Corporate Affairs) master company data across states  
- Detecting daily additions, removals, and updates  
- Enriching records with public API / portal data (like GST, API Setu)  
- Generating AI-powered daily summaries  
- Providing an interactive, analytics-rich dashboard  

This project helps analyze **company incorporation trends**, **state-level insights**, and **daily activity** in Indian company registrations.

---

## 🧩 Tech Stack  
| Layer | Tools/Frameworks |
|-------|-------------------|
| Frontend | Streamlit (Dashboard UI) |
| Backend | Python (Pandas, Plotly, Altair, JSON, OS, Glob) |
| Data | CSV-based Snapshots + Outputs |
| AI Summary | Rule-based NLP Summary Generator |
| Enrichment | Public data via CSV/API template |
| Environment | Python 3.13.7 + Virtualenv (.venv) |

---

## 🗂️ Folder Structure  

MCA_Insights_Engine/
│
├── data/
│ ├── states/
│ │ ├── Delhi.csv|
│ │ ├── Gujarat.csv|,
│ │ ├── Maharashtra.csv
│ │ ├── Karnataka.csv
│ │ ├── Tamil Nadu.csv
│ ├── snapshot_2025-10-14.csv
│ ├── snapshot_2025-10-15.csv
│ ├── snapshot_2025-10-16.csv
│
├── outputs/
│ ├── change_log_d1_d2.csv
│ ├── change_log_d2_d3.csv
│ ├── daily_change_log_all.csv
│ ├── enriched_mca.csv
│ ├── enrichment_template.csv
│ ├── daily_summary.txt
│ ├── daily_summary.json
│ ├── master_current.csv
│ ├── report_2025-10-16.md
│
├── scripts/
│ ├── merge_data.py
│ ├── detect_changes.py
│ ├── make_snapshots.py
│ ├── make_three_snapshots.py
│ ├── run_three_day.py
│ ├── enrich_data.py
│ ├── ai_summary.py
│ ├── app_streamlit.py
│ ├── api_flask.py
│ ├── report_builder.py
│ ├── make_enrichment_template.py
│ ├── run_all.py
│
├── .streamlit/config.toml
├── requirements.txt
├── README.md

## ⚙️ Setup Instructions  

### 1️⃣ Create Environment  
```bash
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
python scripts/merge_data.py
python scripts/make_three_snapshots.py
python scripts/run_three_day.py
python scripts/enrich_data.py
python scripts/ai_summary.py
streamlit run scripts/app_streamlit.py

💡 Dashboard Features

| Section               | Description                                          |
| --------------------- | ---------------------------------------------------- |
| **Overview**          | KPIs: Company count, States covered, Latest date     |
| **Browse**            | Search/filter companies by name, CIN, or state       |
| **Changes**           | Visualizes New Incorporations, Updates, and Removals |
| **Enrichment**        | Shows enriched company records with API/GST links    |
| **Chat (Rule-based)** | Ask simple queries like "status update Karnataka"    |
| **Bookmarks**         | Save and revisit selected company profiles           |
| **AI Summary**        | Auto-generated summary of daily activities           |
