# 1. Clone or download the repo
git clone <your_repo_url>
cd hackathon_demo_package

# 2. Create & activate venv
python -m venv .venv
.\.venv\Scripts\activate.bat

# 3. Install dependencies
pip install -r requirements.txt

# 4. Generate demo data
python run_demo.py

# 5. Run dashboard
python -m streamlit run streamlit_app.py
