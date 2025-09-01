Hackathon demo package
----------------------
Contents:
- run_demo.py         : generates demo data and integrated_dataset.csv (lightweight)
- streamlit_app.py    : interactive Streamlit app (Plotly) to explore integrated dataset
- demo_output/        : if you ran run_demo.py before packaging, demo data was copied here (optional)
- requirements.txt    : pip install -r requirements.txt

How to use:
1) (Optional) generate data locally:
   python run_demo.py
   This creates ./demo_output/data and ./demo_output/out/integrated_dataset.csv
2) Run Streamlit:
   pip install -r requirements.txt
   streamlit run streamlit_app.py
3) In the Streamlit sidebar, set Demo output directory to './demo_output' and click Load demo data

Files copied from the current session (if present) were included under demo_output/