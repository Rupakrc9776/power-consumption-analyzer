# ⚡ Power Consumption Analyzer

A small Python tool to analyze appliance energy consumption, optimize scheduling, and estimate electricity costs.  
This project demonstrates load scheduling optimization — a great foundation for **IoT/ML-based smart energy monitoring**.

---

## ✨ Features
- Reads input data from **CSV files** (`sample_appliances.csv`, `sample_tariffs.csv`)
- Calculates:
  - ✅ Total energy consumption  
  - ✅ Approximate electricity cost  
  - ✅ Peak load usage  
- Produces detailed outputs:
  - `optimized_schedule.csv` — optimized appliance usage schedule  
  - `cost_breakdown.csv` — cost details  
  - `load_curve.png` — load demand curve  
  - `cost_breakdown.png` — cost distribution visualization  

---

## 📂 Project Structure
power-consumption-analyzer/
├── load_scheduling_optimizer.py # main script
├── sample_appliances.csv # input: appliances data
├── sample_tariffs.csv # input: tariff/pricing data
├── requirements.txt # Python dependencies
├── README.md # documentation
├── LICENSE # license info
├── .gitignore # ignore venv + outputs
> Running the script generates:  
`optimized_schedule.csv`, `cost_breakdown.csv`, `load_curve.png`, `cost_breakdown.png`

---

## 🛠 Requirements
- Python **3.8+**
- pip (Python package manager)

Dependencies are listed in `requirements.txt`:

---

## 🚀 How to Run

### 1. Clone this repo
```bash
git clone https://github.com/Rupakrc9776/power-consumption-analyzer.git
cd power-consumption-analyzer
python -m venv venv
# macOS / Linux
source venv/bin/activate
# Windows (PowerShell)
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python load_scheduling_optimizer.py \
  --appliances sample_appliances.csv \
  --tariffs sample_tariffs.csv \
  --schedule_out optimized_schedule.csv \
  --cost_out cost_breakdown.csv \
  --plot_load load_curve.png \
  --plot_cost cost_breakdown.png
