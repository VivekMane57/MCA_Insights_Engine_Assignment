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

## 📸 Project Screenshots

Below are the major pages and features of the **MCA Insights Engine** Streamlit app.

---

### 🧭 Dashboard Overview — MCA Insights Engine  
Shows KPIs such as total companies, states covered, last change date, daily change trends, and AI-generated daily summaries.  
![Dashboard Overview]<img width="1919" height="1079" alt="image" src="https://github.com/user-attachments/assets/292cde70-6e75-4925-887e-c5a217fe9f29" />


---

### 🔍 Browse / Search Companies  
Search or filter companies by CIN, name, state, or status. Displays company details with pagination and sorting options.  
![Browse Companies]<img width="1919" height="1079" alt="image" src="https://github.com/user-attachments/assets/7a4ca3ae-0d29-4a02-9919-729b7068b9df" />


---

### 🏢 Company Detail View  
Displays complete details for a selected company including CIN, status, class, authorized capital, paid-up capital, and recent change history.  
![Company Detail]<img width="1919" height="1078" alt="image" src="https://github.com/user-attachments/assets/fb99b104-1c90-4bd4-874b-1f02ee45a652" />


---

### 📊 Visual Analytics — Change & Capital Charts  
Interactive donut/bar charts showing type-wise and capital breakdown analysis of MCA data.  
![Visual Analytics]<img width="1919" height="1079" alt="image" src="https://github.com/user-attachments/assets/d31e0c3d-d175-41e1-95b3-10b194abfc7d" />


---

### 📈 Change Timeline & Export Options  
Visualizes daily changes in data. Includes export buttons for CSV/JSON and bookmarking options.  
![Change Timeline]<img width="1919" height="1079" alt="image" src="https://github.com/user-attachments/assets/f471a9b5-ec66-4be8-b7f9-06b70519ab0b" />


---

### 🔄 Change Log Page  
Lists all field updates (e.g., Authorized Capital, Status) with old/new values and timestamps for auditing.  
![Change Log]<img width="1919" height="1079" alt="image" src="https://github.com/user-attachments/assets/83635b5e-3498-4ff4-ba99-a34bca3e7389" />


---

### 🌐 Enrichment Dashboard  
Shows enriched company records fetched from public APIs such as APISetu, GST Portal, and ZaubaCorp with source URLs.  
![Enrichment Page]<img width="1919" height="1079" alt="image" src="https://github.com/user-attachments/assets/5f969c7e-a069-405f-b273-a4a565cb9229" />


---

### 💬 Rule-based Chat Interface  
Allows users to query the MCA dataset conversationally (e.g., “New incorporations in Maharashtra”) with instant table responses.  
![Chat Interface]<img width="1919" height="1079" alt="image" src="https://github.com/user-attachments/assets/2f746a17-2332-4b96-9ddd-aee6a082ab64" />






---
 
## 📁 Folder Structure

````markdown
MCA_Insights_Engine/
├── data/
│   ├── states/
│   │   ├── Delhi.csv
│   │   ├── Gujarat.csv
│   │   ├── Maharashtra.csv
│   │   ├── Karnataka.csv
│   │   └── Tamil Nadu.csv
│   ├── snapshot_2025-10-14.csv
│   ├── snapshot_2025-10-15.csv
│   └── snapshot_2025-10-16.csv
│
├── outputs/
│   ├── change_log_d1_d2.csv
│   ├── change_log_d2_d3.csv
│   ├── daily_change_log_all.csv
│   ├── enriched_mca.csv
│   ├── enrichment_template.csv
│   ├── daily_summary.txt
│   ├── daily_summary.json
│   ├── master_current.csv
│   └── report_2025-10-16.md
│
├── scripts/
│   ├── merge_data.py
│   ├── detect_changes.py
│   ├── make_snapshots.py
│   ├── make_three_snapshots.py
│   ├── run_three_day.py
│   ├── enrich_data.py
│   ├── ai_summary.py
│   ├── app_streamlit.py
│   ├── api_flask.py
│   ├── report_builder.py
│   ├── make_enrichment_template.py
│   └── run_all.py
│
├── .streamlit/config.toml
├── requirements.txt
└── README.md


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






