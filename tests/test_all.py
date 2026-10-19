"""Tests for all three sections. Run: python -m unittest discover tests"""
import json
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from section1_clean import clean_readings
from section2_summary import load_rows, summarize


class TestSection1(unittest.TestCase):
    def test_mixed_values(self):
        self.assertEqual(clean_readings([10, "20.5", None, -3, "abc", 600]), [10.0, 20.5, 500.0])

    def test_empty_list(self):
        self.assertEqual(clean_readings([]), [])

    def test_all_invalid(self):
        self.assertEqual(clean_readings([None, "bad", -1, [], {}]), [])

    def test_none_input(self):
        self.assertEqual(clean_readings(None), [])

    def test_exactly_500_and_zero(self):
        self.assertEqual(clean_readings([500, 0, "500.1"]), [500.0, 0.0, 500.0])

    def test_nan_dropped(self):
        self.assertEqual(clean_readings(["nan", 5]), [5.0])


def write_csv(text):
    f = tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False)
    f.write(text)
    f.close()
    return f.name


class TestSection2(unittest.TestCase):
    def test_basic_stats(self):
        path = write_csv("device_id,status,temperature\nX,ACTIVE,70\nX,ERROR,74\n")
        result = summarize(load_rows(path))
        self.assertEqual(result, [{"device_id": "X", "total_records": 2,
                                   "avg_temperature": 72.0, "error_count": 1}])

    def test_hot_device_filtered(self):
        path = write_csv("device_id,status,temperature\nHOT,ACTIVE,90\nOK,ACTIVE,60\n")
        ids = [r["device_id"] for r in summarize(load_rows(path))]
        self.assertEqual(ids, ["OK"])

    def test_exactly_80_kept(self):
        path = write_csv("device_id,status,temperature\nE,ACTIVE,80\n")
        self.assertEqual(len(summarize(load_rows(path))), 1)

    def test_bad_temperature_skipped_but_counted(self):
        path = write_csv("device_id,status,temperature\nY,ERROR,abc\nY,ACTIVE,60\nY,ERROR,\n")
        r = summarize(load_rows(path))[0]
        self.assertEqual((r["total_records"], r["avg_temperature"], r["error_count"]), (3, 60.0, 2))

    def test_lowercase_status(self):
        path = write_csv("device_id,status,temperature\nZ,error,50\n")
        self.assertEqual(summarize(load_rows(path))[0]["error_count"], 1)

    def test_blank_device_ignored(self):
        path = write_csv("device_id,status,temperature\n,ACTIVE,50\n")
        self.assertEqual(summarize(load_rows(path)), [])

    def test_empty_csv(self):
        path = write_csv("")
        self.assertEqual(summarize(load_rows(path)), [])

    def test_missing_file_exits_cleanly(self):
        with self.assertRaises(SystemExit):
            load_rows("does_not_exist.csv")


class TestSection3(unittest.TestCase):
    def test_chart_created(self):
        import section3_chart
        with tempfile.TemporaryDirectory() as d:
            cwd = os.getcwd()
            os.chdir(d)
            try:
                with open("summary.json", "w") as f:
                    json.dump([{"device_id": "A", "total_records": 1,
                                "avg_temperature": 70.0, "error_count": 0}], f)
                section3_chart.main()
                self.assertTrue(os.path.exists("avg_temperature_chart.png"))
            finally:
                os.chdir(cwd)

    def test_missing_json_exits_cleanly(self):
        import section3_chart
        with tempfile.TemporaryDirectory() as d:
            cwd = os.getcwd()
            os.chdir(d)
            try:
                with self.assertRaises(SystemExit):
                    section3_chart.main()
            finally:
                os.chdir(cwd)


if __name__ == "__main__":
    unittest.main()
