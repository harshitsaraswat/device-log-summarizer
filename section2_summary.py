"""Section 2: Summarize device telemetry from a CSV file."""
import csv
import json
import sys

INPUT_FILE = "device_telemetry.csv"
OUTPUT_FILE = "summary.json"
MAX_AVG_TEMP = 80.0


def load_rows(path):
    try:
        with open(path, newline="") as f:
            return list(csv.DictReader(f))
    except FileNotFoundError:
        print(f"Error: file '{path}' not found.")
        sys.exit(1)


def summarize(rows):
    devices = {}
    for row in rows:
        device_id = (row.get("device_id") or "").strip()
        if not device_id:
            continue
        stats = devices.setdefault(device_id, {"records": 0, "temps": [], "errors": 0})
        stats["records"] += 1
        if (row.get("status") or "").strip().upper() == "ERROR":
            stats["errors"] += 1
        try:
            stats["temps"].append(float(row.get("temperature")))
        except (TypeError, ValueError):
            pass  # bad or missing temperature: still counted as a record

    results = []
    for device_id, stats in sorted(devices.items()):
        temps = stats["temps"]
        avg = round(sum(temps) / len(temps), 2) if temps else None
        if avg is not None and avg > MAX_AVG_TEMP:
            continue
        results.append({
            "device_id": device_id,
            "total_records": stats["records"],
            "avg_temperature": avg,
            "error_count": stats["errors"],
        })
    return results


def print_table(results):
    print(f"{'Device':<10}{'Records':>10}{'Avg Temp':>12}{'Errors':>10}")
    print("-" * 42)
    for r in results:
        avg = "N/A" if r["avg_temperature"] is None else f"{r['avg_temperature']:.2f}"
        print(f"{r['device_id']:<10}{r['total_records']:>10}{avg:>12}{r['error_count']:>10}")


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else INPUT_FILE
    results = summarize(load_rows(path))
    with open(OUTPUT_FILE, "w") as f:
        json.dump(results, f, indent=2)
    print_table(results)
    print(f"\nSaved {len(results)} devices to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
