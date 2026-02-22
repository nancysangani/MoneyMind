#!/usr/bin/env python3
"""
MoneyMind - Dynamic Metrics Generator
Reads REAL organized PDFs → writes metrics/money_saved_log.csv
                           → writes metrics/time_saved_log.csv

Run after: python moneymind.py organize
"""

import csv
import sys
from pathlib import Path
from datetime import date

# Import our PDF parser
sys.path.insert(0, str(Path(__file__).parent))
from pdf_parser import (
    parse_all_pdfs,
    compute_savings_opportunities,
)

FINANCES_DIR = Path.home() / "Documents" / "Finances"
METRICS_DIR  = Path("metrics")
METRICS_DIR.mkdir(exist_ok=True)
TODAY = date.today().isoformat()

# Minutes saved per document type (manual vs MoneyMind)
TASK_BENCHMARKS = {
    "Banking":       {"task": "Bank Statement Analysis",    "manual": 45,  "auto": 1},
    "Credit_Cards":  {"task": "Credit Card Reconciliation", "manual": 60,  "auto": 2},
    "Investments":   {"task": "Investment Review",          "manual": 90,  "auto": 2},
    "Subscriptions": {"task": "Subscription Audit",         "manual": 120, "auto": 5},
    "Utilities":     {"task": "Utility Bill Tracking",      "manual": 30,  "auto": 1},
    "Tax_Prep":      {"task": "Tax Document Organisation",  "manual": 180, "auto": 5},
    "Receipts":      {"task": "Receipt Filing",             "manual": 40,  "auto": 1},
}


def generate_time_rows() -> list:
    rows = []
    seen_categories = set()
    total_pdfs = 0

    for year in [2024, 2025, 2026]:
        year_path = FINANCES_DIR / str(year)
        if not year_path.exists():
            continue
        for cat_path in year_path.iterdir():
            if not cat_path.is_dir():
                continue
            category = cat_path.name
            bench = TASK_BENCHMARKS.get(category)
            if not bench:
                continue
            pdf_count = len(list(cat_path.glob("**/*.pdf")))
            if pdf_count == 0:
                continue
            total_pdfs += pdf_count
            if category not in seen_categories:
                rows.append({
                    "Date": TODAY,
                    "Task": bench["task"],
                    "Time_Before_Minutes": bench["manual"] * pdf_count,
                    "Time_After_Minutes":  bench["auto"]   * pdf_count,
                    "Time_Saved_Minutes":  (bench["manual"] - bench["auto"]) * pdf_count,
                })
                seen_categories.add(category)

    if total_pdfs > 0:
        rows.append({
            "Date": TODAY,
            "Task": "Document Organization (AI Auto-sort)",
            "Time_Before_Minutes": total_pdfs * 5,
            "Time_After_Minutes":  round(total_pdfs * 0.1, 1),
            "Time_Saved_Minutes":  round(total_pdfs * 4.9, 1),
        })

    return rows


def generate_money_rows(parsed: dict) -> list:
    opportunities = compute_savings_opportunities(parsed)
    rows = []
    for opp in opportunities:
        rows.append({
            "Date": TODAY,
            "Category": opp["category"],
            "Amount_Per_Month": round(opp["monthly"], 2),
            "Amount_Per_Year":  round(opp["annual"],  2),
            "Description": opp["description"],
        })
    return rows


def write_csv_no_duplicates(filepath: Path, fieldnames: list, new_rows: list):
    existing = []
    existing_keys = set()
    key_field = "Task" if "Task" in fieldnames else "Category"

    if filepath.exists():
        with open(filepath, newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                k = (row.get("Date", ""), row.get(key_field, ""))
                existing_keys.add(k)
                existing.append(row)

    added = 0
    for row in new_rows:
        k = (row.get("Date", ""), row.get(key_field, ""))
        if k not in existing_keys:
            existing.append(row)
            existing_keys.add(k)
            added += 1

    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(existing)

    return len(existing), added


def generate_metrics():
    print("\n💎 MoneyMind — Dynamic Metrics Generator")
    print("=" * 50)
    print("\n🔍 Parsing organized PDFs...\n")

    parsed = parse_all_pdfs(FINANCES_DIR)

    if parsed["total_pdfs"] == 0:
        print("⚠️  No organized PDFs found.")
        print("   Run: python moneymind.py organize  then try again.")
        print("   Dashboard will show zeros until real PDFs are processed.")
        return

    print(f"\n✅ Parsed {parsed['total_pdfs']} PDFs")

    # Time CSV
    time_rows = generate_time_rows()
    time_file  = METRICS_DIR / "time_saved_log.csv"
    time_fields = ["Date", "Task", "Time_Before_Minutes", "Time_After_Minutes", "Time_Saved_Minutes"]
    total_t, added_t = write_csv_no_duplicates(time_file, time_fields, time_rows)
    total_min = sum(float(r["Time_Saved_Minutes"]) for r in time_rows)
    print(f"\n✅ time_saved_log.csv  — {total_t} rows ({added_t} new)")
    print(f"   Time saved: {total_min:.0f} min  ({total_min/60:.1f} h)")

    # Money CSV
    money_rows  = generate_money_rows(parsed)
    money_file  = METRICS_DIR / "money_saved_log.csv"
    money_fields = ["Date", "Category", "Amount_Per_Month", "Amount_Per_Year", "Description"]
    total_m, added_m = write_csv_no_duplicates(money_file, money_fields, money_rows)
    total_rs = sum(float(r["Amount_Per_Year"]) for r in money_rows)
    print(f"\n✅ money_saved_log.csv — {total_m} rows ({added_m} new)")
    print(f"   Savings found: Rs.{total_rs:,.2f}/year")

    if not money_rows:
        print("   ℹ️  No savings detected yet — add more PDFs and re-run.")

    print(f"\n🎯 Done. Now run: python moneymind.py dashboard\n")


if __name__ == "__main__":
    generate_metrics()