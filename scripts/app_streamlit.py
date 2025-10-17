#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
import streamlit as st
import pandas as pd
import altair as alt

# Plotly is optional; app will fall back to Altair if missing
try:
    import importlib
    px = importlib.import_module("plotly.express")
except Exception:
    px = None

# ---------- Streamlit ----------
st.set_page_config(page_title="MCA Insights Engine", layout="wide", page_icon="📊")

# ---------- Utils ----------
@st.cache_data(show_spinner=False)
def read_csv_safe(path: str, dtypes=None) -> pd.DataFrame:
    if not os.path.exists(path) or os.path.getsize(path) == 0:
        return pd.DataFrame()
    kw = {"low_memory": False}
    if dtypes:
        kw["dtype"] = dtypes
    try:
        return pd.read_csv(path, **kw)
    except Exception:
        return pd.read_csv(path, dtype=str, low_memory=False)

def ensure_cols(df: pd.DataFrame, cols: list[str]) -> pd.DataFrame:
    df = df.copy()
    for c in cols:
        if c not in df.columns:
            df[c] = ""
    return df

def add_year(df: pd.DataFrame) -> pd.DataFrame:
    if "IncorporationDate" in df.columns:
        y = pd.to_datetime(df["IncorporationDate"], errors="coerce").dt.year.astype("Int64").astype(str)
        df = df.assign(Year=y)
    return df

def paginate(df: pd.DataFrame, page: int, size: int) -> pd.DataFrame:
    if df.empty:
        return df
    start = (page - 1) * size
    return df.iloc[start:start + size]

def date_range_selector(series: pd.Series, label: str = "Date range"):
    s = series.dropna()
    if s.empty:
        return None, None
    dmin = s.min().to_pydatetime().date()
    dmax = s.max().to_pydatetime().date()
    if dmin == dmax:
        st.caption(f"Only one change date available: **{dmin.isoformat()}**")
        return dmin, dmax
    return st.slider(label, min_value=dmin, max_value=dmax, value=(dmin, dmax))

def to_bytes_csv(df: pd.DataFrame) -> bytes:
    return df.to_csv(index=False).encode()

def to_bytes_json(obj: dict) -> bytes:
    return json.dumps(obj, indent=2).encode("utf-8")

def row_by_cin(df: pd.DataFrame, cin: str) -> dict:
    if df.empty or "CIN" not in df.columns:
        return {}
    r = df[df["CIN"] == cin].head(1)
    return {} if r.empty else r.iloc[0].to_dict()

def set_query_param(cin: str):
    st.query_params.update({"cin": cin})

def get_query_param() -> str | None:
    return st.query_params.get("cin", None)

# ---------- Charts (overview) ----------
def show_daily_change_chart(changes: pd.DataFrame):
    if changes.empty or "Date" not in changes.columns:
        st.info("No change data yet.")
        return
    trend = (
        changes.dropna(subset=["Date"])
               .groupby([pd.Grouper(key="Date", freq="D"), "Change_Type"])
               .size().reset_index(name="Count")
    )
    if trend.empty:
        st.info("No change data yet.")
        return

    if px:
        fig = px.line(
            trend, x="Date", y="Count", color="Change_Type",
            markers=True, title="Daily change history"
        )
        fig.update_layout(height=420, template="plotly_white")
        st.plotly_chart(fig, use_container_width=True)
    else:
        chart = (alt.Chart(trend).mark_line(point=True)
                 .encode(x="Date:T", y="Count:Q", color="Change_Type:N")
                 .properties(height=420, title="Daily change history"))
        st.altair_chart(chart, use_container_width=True)

def show_top_states_chart(master: pd.DataFrame, state_col: str, chart_type: str = "Treemap"):
    if master.empty:
        st.info("No data.")
        return
    tops = (master[state_col]
            .fillna("Unknown")
            .value_counts()
            .rename_axis("State")
            .reset_index(name="Companies")
            .head(12))
    if tops.empty:
        st.info("No data.")
        return

    if px:  # Plotly
        if chart_type == "Treemap":
            fig = px.treemap(
                tops, path=["State"], values="Companies",
                color="Companies", color_continuous_scale="Blues",
                title="Top states by master size"
            )
            fig.update_layout(height=520, margin=dict(l=0, r=0, t=40, b=0), template="plotly_white")
            st.plotly_chart(fig, use_container_width=True)

        elif chart_type == "Donut":
            fig = px.pie(
                tops, names="State", values="Companies", hole=0.45,
                title="Top states by master size (donut)"
            )
            fig.update_traces(textposition="inside", textinfo="percent+label")
            fig.update_layout(height=520, template="plotly_white")
            st.plotly_chart(fig, use_container_width=True)

        else:  # Bar
            fig = px.bar(
                tops.sort_values("Companies"),
                x="Companies", y="State", orientation="h",
                color="Companies", color_continuous_scale="Blues",
                title="Top states by master size"
            )
            fig.update_layout(height=520, template="plotly_white")
            st.plotly_chart(fig, use_container_width=True)

    else:  # Altair fallback
        if chart_type == "Donut":
            chart = (
                alt.Chart(tops)
                .mark_arc(innerRadius=90)
                .encode(theta="Companies:Q", color="State:N", tooltip=["State:N", "Companies:Q"])
                .properties(height=520, width=520, title="Top states by master size (donut)")
            )
            st.altair_chart(chart, use_container_width=True)
        else:
            chart = (
                alt.Chart(tops)
                .mark_bar()
                .encode(x="Companies:Q", y=alt.Y("State:N", sort="-x"),
                        tooltip=["State:N", "Companies:Q"])
                .properties(height=520, title="Top states by master size")
            )
            st.altair_chart(chart, use_container_width=True)

# ---------- Company visuals (new) ----------
def show_company_change_mix(hist: pd.DataFrame, chart_style: str = "Donut"):
    if hist.empty or "Change_Type" not in hist.columns:
        st.info("No change data for this company.")
        return
    mix = hist["Change_Type"].value_counts().rename_axis("Change_Type").reset_index(name="Count")
    if mix.empty:
        st.info("No change data for this company.")
        return

    if px and chart_style == "Donut":
        fig = px.pie(mix, names="Change_Type", values="Count", hole=0.45,
                     title="Change mix (by type)")
        fig.update_traces(textposition="inside", textinfo="percent+label")
        fig.update_layout(height=420, template="plotly_white")
        st.plotly_chart(fig, use_container_width=True)
    elif px and chart_style == "Bar":
        fig = px.bar(mix, x="Count", y="Change_Type", orientation="h",
                     color="Count", color_continuous_scale="Blues",
                     title="Change mix (by type)")
        fig.update_layout(height=420, template="plotly_white")
        st.plotly_chart(fig, use_container_width=True)
    else:
        if chart_style == "Donut":
            chart = (alt.Chart(mix)
                     .mark_arc(innerRadius=80)
                     .encode(theta="Count:Q", color="Change_Type:N", tooltip=["Change_Type:N", "Count:Q"])
                     .properties(height=420, width=420, title="Change mix (by type)"))
            st.altair_chart(chart, use_container_width=True)
        else:
            chart = (alt.Chart(mix)
                     .mark_bar()
                     .encode(x="Count:Q", y=alt.Y("Change_Type:N", sort="-x"),
                             tooltip=["Change_Type:N", "Count:Q"])
                     .properties(height=420, title="Change mix (by type)"))
            st.altair_chart(chart, use_container_width=True)

def show_company_capitals(row: dict, chart_style: str = "Donut"):
    try:
        a = float(str(row.get("AuthorizedCapital", "")).replace(",", "").strip() or 0)
        p = float(str(row.get("PaidUpCapital", "")).replace(",", "").strip() or 0)
    except Exception:
        a, p = 0.0, 0.0

    df_cap = pd.DataFrame({"Metric": ["AuthorizedCapital", "PaidUpCapital"], "Value": [a, p]})
    if (a + p) == 0:
        st.info("No numeric capital values found.")
        return

    if px and chart_style == "Donut":
        fig = px.pie(df_cap, names="Metric", values="Value", hole=0.45, title="Capital breakdown")
        fig.update_traces(textposition="inside", textinfo="percent+label")
        fig.update_layout(height=420, template="plotly_white")
        st.plotly_chart(fig, use_container_width=True)
    elif px and chart_style == "Bar":
        fig = px.bar(df_cap, x="Value", y="Metric", orientation="h",
                     color="Value", color_continuous_scale="Blues",
                     title="Capital breakdown")
        fig.update_layout(height=420, template="plotly_white")
        st.plotly_chart(fig, use_container_width=True)
    else:
        if chart_style == "Donut":
            chart = (alt.Chart(df_cap)
                     .mark_arc(innerRadius=80)
                     .encode(theta="Value:Q", color="Metric:N", tooltip=["Metric:N", "Value:Q"])
                     .properties(height=420, width=420, title="Capital breakdown"))
            st.altair_chart(chart, use_container_width=True)
        else:
            chart = (alt.Chart(df_cap)
                     .mark_bar()
                     .encode(x="Value:Q", y=alt.Y("Metric:N", sort="-x"),
                             tooltip=["Metric:N", "Value:Q"])
                     .properties(height=420, title="Capital breakdown"))
            st.altair_chart(chart, use_container_width=True)

def show_company_timeline(hist: pd.DataFrame):
    if hist.empty or "Date" not in hist.columns:
        return
    ts = (hist.dropna(subset=["Date"])
              .groupby(pd.Grouper(key="Date", freq="D"))
              .size()
              .reset_index(name="Count"))
    if ts.empty:
        return

    if px:
        fig = px.line(ts, x="Date", y="Count", markers=True, title="Change timeline (daily)")
        fig.update_layout(height=300, template="plotly_white")
        st.plotly_chart(fig, use_container_width=True)
    else:
        chart = (alt.Chart(ts)
                 .mark_line(point=True)
                 .encode(x="Date:T", y="Count:Q")
                 .properties(height=300, title="Change timeline (daily)"))
        st.altair_chart(chart, use_container_width=True)

# ---------- Paths ----------
MASTER_PATH = "outputs/master_current.csv"
CHANGE_ALL_PATH = "outputs/daily_change_log_all.csv"
CHANGE_PATH = CHANGE_ALL_PATH if os.path.exists(CHANGE_ALL_PATH) else "outputs/daily_change_log.csv"
ENRICHED_PATH = "outputs/enriched_mca.csv"
SUMMARY_TXT = "outputs/daily_summary.txt"
SUMMARY_JSON = "outputs/daily_summary.json"

# ---------- Load ----------
master = read_csv_safe(MASTER_PATH) if os.path.exists(MASTER_PATH) else read_csv_safe("data/snapshot_day3.csv")
master = ensure_cols(
    master,
    [
        "CIN", "CompanyName", "State", "CompanyROCcode", "Status",
        "AuthorizedCapital", "PaidUpCapital", "IncorporationDate",
        "CompanyCategory", "CompanySubCategory", "Class"
    ]
)
master = add_year(master)

changes = read_csv_safe(CHANGE_PATH)
changes = ensure_cols(changes, ["CIN", "Change_Type", "Field_Changed", "Old_Value", "New_Value", "Date"])
if "Date" in changes.columns:
    changes["Date"] = pd.to_datetime(changes["Date"], errors="coerce")

enriched = read_csv_safe(ENRICHED_PATH)

# ---------- Session ----------
if "bookmarks" not in st.session_state:
    st.session_state.bookmarks = set()
if "selected_cin" not in st.session_state:
    st.session_state.selected_cin = get_query_param()

# ---------- Header / KPIs ----------
st.title("MCA Insights Engine")
st.caption("Consolidate MCA master data, detect daily changes, enrich with public sources, and explore with AI.")

left, mid, right = st.columns(3)
with left:
    st.metric("Companies in master", f"{len(master):,}")
states_all = sorted([s for s in master["State"].dropna().unique().tolist() if s])
with mid:
    st.metric("States covered", len(states_all))
latest_dt = (
    changes["Date"].dropna().max().date().isoformat()
    if ("Date" in changes.columns and changes["Date"].notna().any())
    else "—"
)
with right:
    st.metric("Latest change date", latest_dt)

# ---------- Tabs ----------
t_over, t_browse, t_changes, t_enr, t_chat, t_favs = st.tabs(
    ["📚 Overview", "🔎 Browse", "🧾 Changes", "🧩 Enrichment", "💬 Chat", "⭐ Bookmarks"]
)

# ================= OVERVIEW =================
with t_over:
    c1, c2 = st.columns([2, 1])
    with c1:
        show_daily_change_chart(changes)
    with c2:
        if not changes.empty:
            kpi = (
                changes.groupby("Change_Type").size()
                       .reindex(["New_Incorporation", "Removed", "Field_Update"])
                       .fillna(0).astype(int)
            )
            st.subheader("Today’s counts")
            st.dataframe(pd.DataFrame({"Change_Type": kpi.index, "Count": kpi.values}), width="stretch")
        st.subheader("AI daily summary")
        if os.path.exists(SUMMARY_TXT):
            st.code(open(SUMMARY_TXT, "r", encoding="utf-8").read())
        elif os.path.exists(SUMMARY_JSON):
            st.json(pd.read_json(SUMMARY_JSON).to_dict())
        else:
            st.info("Run ai_summary.py to generate daily summary.")

    st.markdown("—")
    base_state_col = "CompanyROCcode" if "CompanyROCcode" in master.columns else "State"
    chart_type = st.radio("Choose chart style", ["Treemap", "Bar", "Donut"], index=0, horizontal=True)
    show_top_states_chart(master, base_state_col, chart_type)

# ---------- Company panel (with visuals) ----------
def company_panel(cin: str):
    if not cin:
        st.info("Pick a company from the selector below.")
        return

    row = row_by_cin(master, cin)
    if not row:
        st.warning("Company not found in master.")
        return

    with st.container(border=True):
        st.subheader(f"{row.get('CompanyName', '—')}")
        st.caption(f"CIN: {cin}")

        a, b, c = st.columns(3)
        a.metric("State", row.get("State", "—"))
        b.metric("Status", row.get("Status", "—"))
        c.metric("Class", row.get("Class", "—"))

        a, b, c = st.columns(3)
        a.metric("Authorized Capital", row.get("AuthorizedCapital", "—"))
        b.metric("Paid-up Capital", row.get("PaidUpCapital", "—"))
        c.metric("Incorporation", row.get("IncorporationDate", "—"))

        st.markdown("**Recent changes**")
        hist = pd.DataFrame()
        if not changes.empty:
            hist = changes[changes["CIN"] == cin].sort_values("Date", ascending=False).head(200)
            st.dataframe(hist if not hist.empty else pd.DataFrame(), width="stretch")
        else:
            st.write("No change log available.")

        st.markdown("**Enrichment**")
        if not enriched.empty and "CIN" in enriched.columns:
            enr = enriched[enriched["CIN"] == cin]
            st.dataframe(enr if not enr.empty else pd.DataFrame(), width="stretch")
        else:
            st.write("No enrichment yet for this CIN.")

        st.markdown("—")
        st.subheader("Visuals")
        col_style1, col_style2 = st.columns(2)
        with col_style1:
            style_mix = st.radio("Change mix chart", ["Donut", "Bar"], horizontal=True, key=f"mix_{cin}")
        with col_style2:
            style_cap = st.radio("Capital chart", ["Donut", "Bar"], horizontal=True, key=f"cap_{cin}")

        viz1, viz2 = st.columns(2)
        with viz1:
            show_company_change_mix(hist, style_mix)
            show_company_timeline(hist)
        with viz2:
            show_company_capitals(row, style_cap)

        col_a, col_b, col_c, col_d = st.columns(4)
        if col_a.button("⭐ Bookmark", key=f"bm_{cin}"):
            st.session_state.bookmarks.add(cin)
            st.toast("Bookmarked")
        if col_b.button("Copy permalink", key=f"pl_{cin}"):
            set_query_param(cin)
            st.toast("Permalink set in URL")
        col_c.download_button("Export JSON", to_bytes_json(row), file_name=f"{cin}.json", mime="application/json")
        col_d.download_button("Export CSV", to_bytes_csv(pd.DataFrame([row])), file_name=f"{cin}.csv", mime="text/csv")

# ================= BROWSE =================
with t_browse:
    st.subheader("Search / Filter (Master)")
    q = st.text_input("Search by CIN or Company Name")
    state_opt = ["All"] + states_all
    status_opt = sorted([s for s in master["Status"].dropna().unique().tolist() if s])
    year_opt = ["All"] + sorted([y for y in master.get("Year", pd.Series()).dropna().unique().tolist() if y and y != "<NA>"])

    a, b, c, d = st.columns(4)
    with a:
        state_sel = st.selectbox("State", state_opt)
    with b:
        status_sel = st.multiselect("Status", status_opt)
    with c:
        year_sel = st.selectbox("Year", year_opt)
    with d:
        page_size = st.selectbox("Rows per page", [50, 100, 200, 500], index=1)
        page = st.number_input("Page", min_value=1, value=1, step=1)

    df = master
    if q:
        qq = q.lower()
        df = df[
            df["CIN"].str.lower().str.contains(qq, na=False) |
            df["CompanyName"].str.lower().str.contains(qq, na=False)
        ]
    if state_sel != "All":
        df = df[df["State"] == state_sel]
    if status_sel:
        df = df[df["Status"].isin(status_sel)]
    if year_sel != "All" and "Year" in df.columns:
        df = df[df["Year"] == year_sel]

    st.caption(f"Showing {min(len(df), page_size)} of {len(df):,} (page {page})")
    st.dataframe(paginate(df, page, page_size), width="stretch")
    st.download_button("Download filtered CSV", to_bytes_csv(df), "filtered_master.csv", "text/csv")

    st.markdown("—")
    st.subheader("Company picker")
    slim = df[["CIN", "CompanyName"]].dropna().head(1000).reset_index(drop=True)
    if not slim.empty:
        opts = slim["CIN"].tolist()
        labels = {row["CIN"]: f'{row["CIN"]} — {row["CompanyName"]}' for _, row in slim.iterrows()}
        if st.session_state.selected_cin in opts:
            default_idx = int(opts.index(st.session_state.selected_cin))
        else:
            default_idx = 0
        chosen_cin = st.selectbox(
            "Select a company",
            options=opts,
            index=default_idx,
            format_func=lambda cin: labels.get(cin, cin)
        )
        st.session_state.selected_cin = chosen_cin
        set_query_param(chosen_cin)
        company_panel(chosen_cin)
    else:
        st.info("No rows in current filter. Adjust filters above.")

# ================= CHANGES =================
with t_changes:
    st.subheader("Change Log")
    if changes.empty or not changes["Date"].notna().any():
        st.info("No changes found (or Date column missing). Generate logs using the three-day script.")
    else:
        types = ["All"] + [t for t in changes["Change_Type"].dropna().unique().tolist()]
        tsel = st.selectbox("Change type", types)

        d_from, d_to = date_range_selector(changes["Date"], "Date range")

        c1, c2 = st.columns(2)
        with c1:
            page_size_c = st.selectbox("Rows per page", [50, 100, 200, 500], index=0, key="chg_ps")
        with c2:
            page_c = st.number_input("Page", min_value=1, value=1, step=1, key="chg_pg")

        ch = changes
        if tsel != "All":
            ch = ch[ch["Change_Type"] == tsel]
        ch = ch.dropna(subset=["Date"])
        if d_from is not None and d_to is not None:
            ch = ch[(ch["Date"].dt.date >= d_from) & (ch["Date"].dt.date <= d_to)]

        if "State" not in ch.columns and "CIN" in ch.columns:
            ch = ch.merge(master[["CIN", "State"]], on="CIN", how="left")

        st.caption(f"Showing {min(len(ch), page_size_c)} of {len(ch):,} (page {page_c})")
        st.dataframe(paginate(ch, page_c, page_size_c), width="stretch")
        st.download_button("Download change log CSV", to_bytes_csv(ch), "changes_filtered.csv", "text/csv")

        st.markdown("—")
        st.subheader("Changes by state")
        if not ch.empty and "State" in ch.columns:
            agg = ch.groupby(["State", "Change_Type"]).size().reset_index(name="Count")
            if px:
                fig = px.bar(
                    agg, x="Count", y="State", color="Change_Type",
                    orientation="h", barmode="group",
                    color_discrete_sequence=px.colors.qualitative.Set2,
                    title="Changes by state"
                )
                fig.update_layout(height=520, template="plotly_white")
                st.plotly_chart(fig, use_container_width=True)
            else:
                chart = (alt.Chart(agg).mark_bar()
                         .encode(x="Count:Q", y=alt.Y("State:N", sort="-x"),
                                 color="Change_Type:N")
                         .properties(height=520, title="Changes by state"))
                st.altair_chart(chart, use_container_width=True)

# ================= ENRICHMENT =================
with t_enr:
    st.subheader("Enriched Companies (sample)")
    if enriched.empty:
        st.info("No enriched file found. Fill and save outputs/enriched_mca.csv")
    else:
        e_ps = st.selectbox("Rows per page", [50, 100, 200, 500], index=0, key="enr_ps")
        e_pg = st.number_input("Page", min_value=1, value=1, step=1, key="enr_pg")
        st.dataframe(paginate(enriched, e_pg, e_ps), width="stretch")
        st.download_button("Download enriched CSV", to_bytes_csv(enriched), "enriched_mca.csv", "text/csv")

# ================= CHAT (rule-based) =================
with t_chat:
    st.subheader("Chat with MCA Data (rule-based)")
    user_q = st.text_input("Ask a question (e.g., 'new incorporations in Maharashtra')")
    if st.button("Ask") and user_q:
        q = user_q.lower()
        log = changes.copy()
        if log.empty and os.path.exists("outputs/daily_change_log.csv"):
            log = read_csv_safe("outputs/daily_change_log.csv")
        if log.empty:
            st.warning("No change log available.")
        else:
            base = ensure_cols(master, ["CIN", "CompanyName", "State", "Status"])[["CIN", "CompanyName", "State", "Status"]]
            log = log.merge(base, on="CIN", how="left")

            if any(k in q for k in ["new", "incorporation", "naya"]):
                resp = log[log["Change_Type"] == "New_Incorporation"]
            elif any(k in q for k in ["removed", "strike", "deregister", "hat"]):
                resp = log[log["Change_Type"] == "Removed"]
            elif any(k in q for k in ["update", "capital", "status"]):
                resp = log[log["Change_Type"] == "Field_Update"]
            else:
                resp = log

            for stname in states_all:
                if stname.lower() in q:
                    resp = resp[resp["State"] == stname]

            if "how many" in q or "count" in q:
                st.success(f"Count: {len(resp)}")
            else:
                st.write(f"Results: {len(resp)} rows")
                st.dataframe(resp.head(300), width="stretch")

# ================= BOOKMARKS =================
with t_favs:
    st.subheader("⭐ Your bookmarked companies")
    if not st.session_state.bookmarks:
        st.info("No bookmarks yet. Open a company and click ⭐ Bookmark.")
    else:
        favs = master[master["CIN"].isin(list(st.session_state.bookmarks))][["CIN", "CompanyName", "State", "Status"]]
        st.dataframe(favs, width="stretch")
        if st.button("Clear bookmarks"):
            st.session_state.bookmarks.clear()
            st.success("Bookmarks cleared.")
