# 🐬 Hackathon Demo – Setup & Run Guide

This guide explains how to **download, set up, and run** our demo project. Follow these steps carefully — you don’t need deep coding knowledge, just copy-paste the commands as shown.

---

## 🔽 1. Download the Project

1. Open our GitHub repo link.
2. Click the green **Code → Download ZIP** button.
3. Extract the ZIP to your Desktop (or any folder you like).

   * After extraction, you should see files like:

     * `run_demo.py`
     * `streamlit_app.py`
     * `requirements.txt`
     * `demo_output/` folder

---

## ⚙️ 2. Install Python (if not already installed)

1. Download Python 3.10+ from [python.org](https://www.python.org/downloads/).
2. During installation, check ✅ **Add Python to PATH**.
3. Open **PowerShell** and verify:

   ```powershell
   python --version
   ```

   It should show something like `Python 3.10.11`.

---

## 🛠 3. Create & Activate Virtual Environment

1. In PowerShell, go into the project folder:

   ```powershell
   cd "C:\Users\<YourName>\Desktop\hackathon_demo_package"
   ```
2. Create a virtual environment (only first time):

   ```powershell
   python -m venv .venv
   ```
3. Activate it:

   ```powershell
   .\.venv\Scripts\activate.bat
   ```

   ✅ If successful, you’ll see `(.venv)` at the start of the prompt.

---

## 📦 4. Install All Requirements

Inside the activated venv, run:

```powershell
pip install -r requirements.txt
```

If that fails, use the fallback one-shot installer:

```powershell
pip install streamlit plotly pandas numpy matplotlib seaborn openpyxl xlrd scikit-learn geopandas shapely folium
```

---

## 🧪 5. Generate the Demo Dataset

Run:

```powershell
python run_demo.py
```

This will create `integrated_dataset.csv` inside the `demo_output` folder.

---

## 📊 6. Run the Dashboard

Start Streamlit:

```powershell
python -m streamlit run streamlit_app.py
```

* This will open a link like:

  ```
  Local URL: http://localhost:8501
  ```
* Open it in your browser (Chrome/Edge).

---

## 🖥 7. Load the Data in the Dashboard

1. In the sidebar of the app, enter:

   ```
   ./
   ```

   (this tells it to look for the dataset in the current folder).
2. Click **Load Demo Data**.
3. ✅ You should now see graphs and outputs.

---

## 🛑 Common Problems & Fixes

**🔴 Problem 1: Script execution disabled**

```
cannot be loaded because running scripts is disabled
```

✅ Fix: Run this once in PowerShell:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Then activate again.

---

**🔴 Problem 2: 'pip' not recognized**
✅ Fix: Use:

```powershell
python -m pip install --upgrade pip
```

---

**🔴 Problem 3: ModuleNotFoundError (e.g. 'plotly' missing)**
✅ Fix: Run:

```powershell
pip install plotly
```

(or re-run the one-shot install command above).

---

**🔴 Problem 4: integrated\_dataset.csv not found**
✅ Fix:

* Make sure you ran:

  ```powershell
  python run_demo.py
  ```
* In the app sidebar, try both:

  ```
  ./ 
  ./demo_output
  ./demo_output/out
  ```

---

## 🎯 Quick Shortcut for Presentations

You can make a file called `start_demo.bat` with this content:

```bat
@echo off
cd %~dp0
call .venv\Scripts\activate.bat
python -m streamlit run streamlit_app.py
```

Save it in the project folder → double-click it → app runs instantly.

---

✅ That’s it — if followed step-by-step, the demo will run smoothly on any Windows laptop with Python installed.

---

👉 Do you want me to also make a **short "Quick Start" version** (5 lines max) that you can paste into your PPT/README for judges, so they don’t get scared by too many steps?
