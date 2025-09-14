# ⚡ Power Consumption Analyzer

[![Python](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Open Issues](https://img.shields.io/github/issues/<Rupakrc9776>/energy-analyzer)](https://github.com/<Rupakrc9776>/energy-analyzer/issues)

A small Python tool to analyze daily energy usage, estimate bills, and visualize consumption trends.  
Perfect as a **3rd-semester mini-project** and a good foundation for **IoT/ML-based smart energy monitoring**.

---

![Usage Graph](usage.png)

## 🚀 Features
- Reads data from `data.csv` or manual input
- Calculates **total energy consumed** & estimated bill
- Highlights **peak usage day**
- Exports `output_summary.txt`, `output_data.csv`, `usage.png`

---

## 📁 Project Structure
energy-analyzer/
├── energy_analyzer.py
├── data.csv
├── output_data.csv
├── output_summary.txt
├── usage.png
├── requirements.txt
├── .gitignore
├── LICENSE
└── README.md

---

## 🛠 Requirements
- Python 3.8+
- `pandas`
- `matplotlib`

Install dependencies:
```powershell
pip install -r requirements.txt
