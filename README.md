# Device Log Summarizer

A small CLI tool that cleans sensor data, summarizes device logs from a CSV,
and draws a bar chart of average temperature per device.

## Setup
```
pip install matplotlib
```

## How to run (in this order)
```
python make_dataset.py          # 1. creates device_telemetry.csv (43 rows, some bad on purpose)
python section1_clean.py        # 2. Section 1 (write clean_readings yourself first)
python section2_summary.py      # 3. writes summary.json and prints a table
python section3_chart.py        # 4. writes avg_temperature_chart.png
python -m unittest discover tests -v   # 5. runs all 16 tests
```

## Files
| File | What it does |
|---|---|
| section1_clean.py | Cleans a list of mixed values into floats (drops bad/negative, caps at 500) |
| section2_summary.py | Groups CSV by device: record count, avg temp, ERROR count; drops avg > 80 |
| section3_chart.py | Bar chart from summary.json |
| make_dataset.py | Generates the sample CSV |
| tests/test_all.py | Tests for all three sections |
| sample_output.txt | Terminal output from a full run |

## How bad data is handled
- Missing CSV or JSON file: prints an error and exits, no crash.
- Bad or empty temperature: skipped for the average, row still counted.
- Blank device ID: row ignored.
- Status is matched case-insensitively (`error` = `ERROR`).
