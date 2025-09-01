# streamlit_app.py
import streamlit as st
import pandas as pd, numpy as np, plotly.express as px, plotly.graph_objects as go, os
st.set_page_config(page_title="Ocean-Fish-eDNA Explorer", layout="wide", page_icon="🌊")

st.markdown("<style> .sidebar .sidebar-content {background-image: linear-gradient(#0f172a, #06203b);} .stApp { background: linear-gradient(180deg,#071029,#0b1220);} .css-1v3fvcr { color: white; } </style>", unsafe_allow_html=True)

st.title("🌊 Ocean — Fisheries — eDNA Explorer")
st.subheader("Interactive (Plotly) viewer — filters, MPA toggle, species selector")

data_dir = st.sidebar.text_input("Demo output directory", value="./demo_output")
if st.sidebar.button("Load demo data"):
    path = os.path.join(data_dir, "out", "integrated_dataset.csv")
    if not os.path.exists(path):
        st.sidebar.error("integrated_dataset.csv not found. Run run_demo.py first or set correct directory.")
    else:
        df = pd.read_csv(path)
        # prepare month_ts
        if 'month' in df.columns:
            df['month_ts'] = pd.to_datetime(df['month'].astype(str) + "-01")
        else:
            if 'date' in df.columns:
                df['month_ts'] = pd.to_datetime(df['date']).dt.to_period('M').dt.to_timestamp()
            else:
                df['month_ts'] = pd.to_datetime("2025-01-01")
        st.session_state['df'] = df
        st.sidebar.success("Loaded integrated dataset")

if 'df' not in st.session_state:
    st.info("No dataset loaded. Use the sidebar 'Load demo data'.")
    st.stop()

df = st.session_state['df']
# Filters
species_list = sorted(df['species'].dropna().unique().tolist())
selected_species = st.sidebar.multiselect("Species", species_list, default=species_list)
sites = sorted(df['site_id'].dropna().unique().tolist())
selected_sites = st.sidebar.multiselect("Sites", sites, default=sites)
mpa_opt = st.sidebar.selectbox("MPA filter", ["Both","Inside MPA","Outside MPA"])
if mpa_opt == "Inside MPA":
    df = df[df['in_mpa'] == True]
elif mpa_opt == "Outside MPA":
    df = df[df['in_mpa'] == False]
df = df[df['species'].isin(selected_species) & df['site_id'].isin(selected_sites)]
# layout
left, right = st.columns([2,1])
with left:
    st.markdown("### CPUE trends")
    if df.empty:
        st.write("No data for current filters.")
    else:
        fig = px.line(df, x='month_ts', y='cpue_kg_per_hr', color='species', markers=True, title="CPUE (kg/hr) by species")
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("### Environmental variables (site view)")
    site = st.selectbox("Choose site", selected_sites)
    sub = df[df['site_id'] == site]
    if not sub.empty:
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(x=sub['month_ts'], y=sub['sst_c'], mode='lines+markers', name='SST (°C)'))
        fig2.add_trace(go.Bar(x=sub['month_ts'], y=sub['chla_mg_m3'], name='Chl-a (mg/m3)', yaxis='y2', opacity=0.6))
        fig2.update_layout(title=f"Env variables at site {site}", yaxis=dict(title='SST (°C)'), yaxis2=dict(title='Chl-a', overlaying='y', side='right'))
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.write("No environmental data for this site & filters.")

    st.markdown("### Scatter: CPUE vs predictors")
    cols = st.columns(3)
    if not df[['cpue_kg_per_hr','sst_c']].dropna().empty:
        fig3 = px.scatter(df, x='sst_c', y='cpue_kg_per_hr', color='species', hover_data=['site_id','month'])
        fig3.update_traces(marker=dict(size=8))
        cols[0].plotly_chart(fig3, use_container_width=True)
    if not df[['cpue_kg_per_hr','chla_mg_m3']].dropna().empty:
        fig4 = px.scatter(df, x='chla_mg_m3', y='cpue_kg_per_hr', color='species', hover_data=['site_id','month'])
        cols[1].plotly_chart(fig4, use_container_width=True)
    if not df[['cpue_kg_per_hr','read_count']].dropna().empty:
        fig5 = px.scatter(df, x='read_count', y='cpue_kg_per_hr', color='species', hover_data=['site_id','month'])
        cols[2].plotly_chart(fig5, use_container_width=True)

with right:
    st.markdown("### Data & Downloads")
    st.write(f"Rows after filter: {len(df)}")
    st.dataframe(df.reset_index(drop=True))
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("Download filtered CSV", csv, file_name="filtered_integrated_dataset.csv", mime="text/csv")

    st.markdown("### Quick correlations (filtered)")
    def safe_corr(a,b):
        try:
            tmp = df[[a,b]].dropna()
            if len(tmp)>2:
                return float(tmp[a].corr(tmp[b]))
        except Exception:
            return None
    c1 = safe_corr('cpue_kg_per_hr','sst_c')
    c2 = safe_corr('cpue_kg_per_hr','chla_mg_m3')
    c3 = safe_corr('cpue_kg_per_hr','read_count')
    if c1 is not None: st.write(f"CPUE vs SST: {c1:.2f}")
    if c2 is not None: st.write(f"CPUE vs Chl-a: {c2:.2f}")
    if c3 is not None: st.write(f"CPUE vs eDNA: {c3:.2f}")

st.markdown("---")
st.caption("Made with ❤️ — Plotly & Streamlit. Ask me to add GLM or mixed-effects panel next!")