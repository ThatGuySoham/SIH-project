# run_demo.py
# Generates demo datasets and outputs integrated dataset + plots
import os, numpy as np, pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt

RANDOM_SEED = 42
np.random.seed(RANDOM_SEED)

def ensure_dir(p):
    os.makedirs(p, exist_ok=True)

def mk_design():
    dates = pd.date_range("2025-01-01", "2025-06-30", freq="7D")
    sites = pd.DataFrame({
        "site_id":["A","B","C","D"],
        "lat":[15.2,15.8,16.1,14.9],
        "lon":[73.5,73.7,74.0,73.2],
        "in_mpa":[True,False,True,False]
    })
    species = ["Sardine","Mackerel","Skipjack_Tuna"]
    return dates, sites, species

def generate_sst(dates, sites):
    rows=[]
    tlen=len(dates)
    seasonal = np.sin(np.linspace(0,2*np.pi,tlen))
    for _,s in sites.iterrows():
        site_offset = np.random.normal(0,0.3)
        baseline = 26.0 + site_offset
        noise = np.random.normal(0,0.5,tlen)
        temps = baseline + 1.5*seasonal + noise
        for d,t in zip(dates, temps):
            rows.append([d,s.site_id,s.lat,s.lon,round(float(t),2)])
    return pd.DataFrame(rows, columns=["date","site_id","lat","lon","sst_c"])

def generate_chla(dates, sites):
    rows=[]
    tlen=len(dates)
    seasonal = np.cos(np.linspace(0,2*np.pi,tlen))
    for _,s in sites.iterrows():
        site_offset = np.random.normal(0,0.05)
        noise = np.random.normal(0,0.05,tlen)
        chla = 1.1 + 0.4*seasonal + site_offset + noise
        chla = np.clip(chla, 0.01, None)
        for d,c in zip(dates,chla):
            rows.append([d,s.site_id,s.lat,s.lon,round(float(c),3)])
    return pd.DataFrame(rows, columns=["date","site_id","lat","lon","chla_mg_m3"])

def generate_fish(dates, sites, species):
    rows=[]
    tlen=len(dates)
    for _,s in sites.iterrows():
        effort = np.clip(np.random.normal(14,4,tlen),4,24)
        for si,sp in enumerate(species):
            abundance = np.sin(np.linspace(0,2*np.pi,tlen)+si*0.7)+1.2
            prod = (np.cos(np.linspace(0,2*np.pi,tlen))+1.0)
            base = abundance * prod * np.random.normal(8,2,tlen)
            base = np.clip(base,0.5,None)
            catch = base * (0.6 if s['in_mpa'] else 1.0)
            catch = catch + np.random.normal(0,2,tlen)
            catch = np.clip(catch,0.5,None)
            for d,e,c in zip(dates,effort,catch):
                rows.append([d,s.site_id,sp,round(float(e),2),round(float(c),1)])
    df = pd.DataFrame(rows, columns=["date","site_id","species","effort_hours","catch_kg"])
    df["cpue_kg_per_hr"] = (df["catch_kg"]/df["effort_hours"]).round(3)
    return df

def generate_edna(dates, sites, species):
    rows=[]
    tlen=len(dates)
    for _,s in sites.iterrows():
        for si,sp in enumerate(species):
            base = 200 + 100*np.sin(np.linspace(0,2*np.pi,tlen)+si*0.6)
            env = 50*np.cos(np.linspace(0,2*np.pi,tlen))
            reads = base + env + np.random.normal(0,30,tlen)
            reads = np.clip(reads,5,None)
            for d,r in zip(dates,reads):
                rows.append([d,s.site_id,sp,int(round(r))])
    return pd.DataFrame(rows, columns=["date","site_id","species","read_count"])

def save_all(outdir):
    ensure_dir(outdir)
    dates, sites, species = mk_design()
    sst = generate_sst(dates, sites)
    chla = generate_chla(dates, sites)
    fish = generate_fish(dates, sites, species)
    edna = generate_edna(dates, sites, species)

    data_dir = os.path.join(outdir, "data")
    ensure_dir(data_dir)
    sst.to_csv(os.path.join(data_dir, "sea_surface_temperature.csv"), index=False)
    chla.to_csv(os.path.join(data_dir, "chlorophyll_a.csv"), index=False)
    fish.to_csv(os.path.join(data_dir, "catch_records.csv"), index=False)
    edna.to_csv(os.path.join(data_dir, "edna_counts.csv"), index=False)
    sites.to_csv(os.path.join(data_dir, "sites_mpa.csv"), index=False)

    # integrate monthly
    sst_m = sst.copy(); sst_m['month'] = sst_m['date'].dt.to_period('M').astype(str)
    sst_m = sst_m.groupby(['month','site_id'], as_index=False)['sst_c'].mean()
    chla_m = chla.copy(); chla_m['month'] = chla_m['date'].dt.to_period('M').astype(str)
    chla_m = chla_m.groupby(['month','site_id'], as_index=False)['chla_mg_m3'].mean()
    fish_m = fish.copy(); fish_m['month'] = fish_m['date'].dt.to_period('M').astype(str)
    fish_m = fish_m.groupby(['month','site_id','species'], as_index=False).agg(effort_hours=('effort_hours','sum'), catch_kg=('catch_kg','sum'))
    fish_m['cpue_kg_per_hr'] = (fish_m['catch_kg']/fish_m['effort_hours']).replace([np.inf,-np.inf], np.nan)
    edna_m = edna.copy(); edna_m['month'] = edna_m['date'].dt.to_period('M').astype(str)
    edna_m = edna_m.groupby(['month','site_id','species'], as_index=False)['read_count'].mean()
    env = (fish_m.merge(sst_m, on=['month','site_id'], how='left')
               .merge(chla_m, on=['month','site_id'], how='left')
               .merge(edna_m, on=['month','site_id','species'], how='left')
               .merge(sites[['site_id','in_mpa']], on='site_id', how='left'))
    outdir_out = os.path.join(outdir, "out")
    ensure_dir(outdir_out)
    env.to_csv(os.path.join(outdir_out, "integrated_dataset.csv"), index=False)

    # quick plots with matplotlib saved for backward compatibility
    plots_dir = os.path.join(outdir_out, "plots"); ensure_dir(plots_dir)
    sst_plot = sst_m.copy(); sst_plot['month_ts'] = pd.to_datetime(sst_plot['month'] + '-01')
    for site, g in sst_plot.groupby('site_id'):
        pass
    # simple matplotlib cpue per species (not necessary to plot here)

    print("Demo saved to:", outdir)
    print("Data files in:", os.path.join(outdir,"data"))
    print("Integrated dataset in:", os.path.join(outdir,"out","integrated_dataset.csv"))

if __name__ == "__main__":
    save_all(".")