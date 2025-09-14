
import argparse
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def load_inputs(appliance_csv, tariff_csv):
    appliances = pd.read_csv(appliance_csv)
    tariffs = pd.read_csv(tariff_csv)
    required_cols = {"Name","Power_W","Duration_h","EarliestStart","LatestEnd","Priority","Flexible","MustRun"}
    if not required_cols.issubset(set(appliances.columns)):
        raise ValueError("Appliance CSV missing required columns")
    if "Tariff_Rs_per_kWh" not in tariffs.columns or "Hour" not in tariffs.columns:
        raise ValueError("Tariff CSV must include ['Hour','Tariff_Rs_per_kWh']")
    if len(tariffs) != 24 or not set(tariffs['Hour'].tolist()) == set(range(24)):
        raise ValueError("Tariff CSV must have 24 rows with Hour = 0..23")
    appliances["Duration_h"] = appliances["Duration_h"].clip(lower=0).astype(int)
    appliances["EarliestStart"] = appliances["EarliestStart"].clip(lower=0, upper=23).astype(int)
    appliances["LatestEnd"] = appliances["LatestEnd"].clip(lower=1, upper=24).astype(int)
    appliances["Priority"] = appliances["Priority"].clip(lower=1, upper=5).astype(int)
    appliances["Flexible"] = appliances["Flexible"].astype(bool)
    appliances["MustRun"] = appliances["MustRun"].astype(bool)
    return appliances, tariffs

def optimize_schedule(appliances, tariffs, alpha=1.0, beta=1.0, seed=42):
    schedule = {h: [] for h in range(24)}
    load_kw = np.zeros(24, dtype=float)
    tariff = tariffs.set_index("Hour")["Tariff_Rs_per_kWh"].to_dict()

    df = appliances.copy()
    df["Power_kW"] = df["Power_W"] / 1000.0
    df = df.sort_values(by=["MustRun","Priority","Power_kW"], ascending=[False, False, False])

    placements = []
    for _, row in df.iterrows():
        name = row["Name"]
        p_kw = row["Power_kW"]
        dur = int(row["Duration_h"])
        es, le = int(row["EarliestStart"]), int(row["LatestEnd"])
        flex = bool(row["Flexible"])
        if dur == 0:
            placements.append((name, []))
            continue

        if le <= es:
            window_hours = list(range(es,24)) + list(range(0,le))
        else:
            window_hours = list(range(es, le))

        normalized_load = (load_kw - load_kw.min()) / (load_kw.max() - load_kw.min() + 1e-9)
        score_vector = {h: alpha * tariff[h] + beta * normalized_load[h] for h in range(24)}

        assigned_hours = []

        if flex:
            feasible = list(window_hours)
            need = min(dur, len(feasible))
            hours = sorted(feasible, key=lambda h: score_vector[h])[:need]
            for h in hours:
                load_kw[h] += p_kw
                schedule[h].append(name)
            assigned_hours = hours
        else:
            def in_window_block(start, dur):
                block = [(start + i) % 24 for i in range(dur)]
                return all((h in window_hours) for h in block), block

            best_block, best_score = None, float("inf")
            for start in window_hours:
                ok, block = in_window_block(start, dur)
                if not ok:
                    continue
                score = sum(score_vector[h] for h in block)
                if score < best_score:
                    best_score, best_block = score, block

            if best_block is None:
                feasible = list(window_hours)
                need = min(dur, len(feasible))
                best_block = sorted(feasible, key=lambda h: score_vector[h])[:need]

            for h in best_block:
                load_kw[h] += p_kw
                schedule[h].append(name)
            assigned_hours = best_block

        placements.append((name, sorted(assigned_hours)))

    schedule_rows = []
    for h in range(24):
        schedule_rows.append({
            "Hour": h,
            "Tariff_Rs_per_kWh": tariff[h],
            "Load_kW": round(load_kw[h], 4),
            "Appliances": ", ".join(schedule[h]) if schedule[h] else "-"
        })
    schedule_df = pd.DataFrame(schedule_rows)

    cost_rows = []
    for name, hours in placements:
        if not hours:
            energy_kwh = 0.0
            cost = 0.0
        else:
            p_kw = float(df[df["Name"]==name]["Power_kW"].iloc[0])
            energy_kwh = p_kw * len(hours)
            cost = sum(p_kw * tariff[h] for h in hours)
        cost_rows.append({"Name": name, "Hours": len(hours), "Energy_KWh": round(energy_kwh,4), "Cost_Rs": round(cost,2)})
    cost_df = pd.DataFrame(cost_rows).sort_values(by="Cost_Rs", ascending=False).reset_index(drop=True)

    return schedule_df, cost_df

def plot_load(schedule_df, out_png):
    plt.figure()
    plt.plot(schedule_df["Hour"], schedule_df["Load_kW"], marker="o")
    plt.xlabel("Hour of Day")
    plt.ylabel("Total Load (kW)")
    plt.title("Optimized Load Curve (24h)")
    plt.grid(True, which="both", linestyle="--", linewidth=0.5)
    plt.savefig(out_png, bbox_inches="tight")
    plt.close()

def plot_cost(cost_df, out_png, top_n=10):
    top = cost_df.head(top_n)
    plt.figure()
    plt.bar(top["Name"], top["Cost_Rs"])
    plt.xlabel("Appliance")
    plt.ylabel("Cost (Rs)")
    plt.title(f"Cost Contribution (Top {top_n})")
    plt.xticks(rotation=45, ha="right")
    plt.savefig(out_png, bbox_inches="tight")
    plt.close()

def main():
    parser = argparse.ArgumentParser(description="Load Scheduling & Energy Optimization (Python-only)")
    parser.add_argument("--appliances", default="sample_appliances.csv")
    parser.add_argument("--tariffs", default="sample_tariffs.csv")
    parser.add_argument("--alpha", type=float, default=1.0)
    parser.add_argument("--beta", type=float, default=1.0)
    parser.add_argument("--schedule_out", default="optimized_schedule.csv")
    parser.add_argument("--cost_out", default="cost_breakdown.csv")
    parser.add_argument("--plot_load_png", default="load_curve.png")
    parser.add_argument("--plot_cost_png", default="cost_breakdown.png")
    args = parser.parse_args()

    appliances, tariffs = load_inputs(args.appliances, args.tariffs)
    schedule_df, cost_df = optimize_schedule(appliances, tariffs, alpha=args.alpha, beta=args.beta)

    schedule_df.to_csv(args.schedule_out, index=False)
    cost_df.to_csv(args.cost_out, index=False)

    plot_load(schedule_df, args.plot_load_png)
    plot_cost(cost_df, args.plot_cost_png)

    peak_kw = schedule_df["Load_kW"].max()
    total_energy_kwh = schedule_df["Load_kW"].sum()
    approx_cost = (schedule_df["Load_kW"] * schedule_df["Tariff_Rs_per_kWh"]).sum()

    print("=== Optimization Summary ===")
    print(f"Peak Load (kW): {round(peak_kw,3)}")
    print(f"Total Energy (kWh): {round(total_energy_kwh,3)}")
    print(f"Approx Cost (Rs): {round(approx_cost,2)}")
    print(f"Schedule saved to: {args.schedule_out}")
    print(f"Cost breakdown saved to: {args.cost_out}")
    print(f"Plots saved to: {args.plot_load_png}, {args.plot_cost_png}")

if __name__ == "__main__":
    main()
