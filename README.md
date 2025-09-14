# Load Scheduling Optimizer

Small Python tool to optimize appliance load scheduling, estimate energy consumption and cost, and export results/plots.

## Files in repo
- `load_scheduling_optimizer.py` — main script
- `sample_appliances.csv` — example input (appliance data)
- `sample_tariffs.csv` — example input (tariff/pricing)
- `requirements.txt` — Python dependencies
- `.gitignore`, `LICENSE`, `README.md`

> Running the script creates output files (not committed):  
`optimized_schedule.csv`, `cost_breakdown.csv`, `load_curve.png`, `cost_breakdown.png`

---

## Requirements
- Python 3.8+
- pip

## Quick start — run locally
1. Clone the repo:
```bash
git clone https://github.com/Rupakrc9776/power-consumption-analyzer.git
cd power-consumption-analyzer
