"""Section 3: Bar chart of average temperature per device."""
import json
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

INPUT_FILE = "summary.json"
OUTPUT_FILE = "avg_temperature_chart.png"


def main():
    try:
        with open(INPUT_FILE) as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error reading {INPUT_FILE}: {e}")
        sys.exit(1)

    data = [d for d in data if d.get("avg_temperature") is not None]
    if not data:
        print("No data to plot.")
        return

    names = [d["device_id"] for d in data]
    temps = [d["avg_temperature"] for d in data]

    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.bar(names, temps, color="steelblue")
    ax.bar_label(bars, fmt="%.1f")
    ax.set_title("Average Temperature per Device")
    ax.set_xlabel("Device ID")
    ax.set_ylabel("Average Temperature")
    ax.set_ylim(0, max(temps) * 1.1)  # headroom so value labels don't touch the top
    plt.tight_layout()
    plt.savefig(OUTPUT_FILE)
    print(f"Chart saved to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
