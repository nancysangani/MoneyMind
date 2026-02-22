#!/usr/bin/env python3
"""
MoneyMind Demo Data Generator
Creates sample financial documents for demo purposes
"""

import os
from datetime import datetime, timedelta
from pathlib import Path

def create_sample_pdfs():
    """Create dummy PDF files with realistic names"""
    downloads = Path.home() / "Downloads"
    
    # Sample messy filenames (before MoneyMind)
    messy_files = [
        "document_2024.pdf",
        "statement.pdf",
        "invoice_jan.pdf",
        "IMG_1234.pdf",
        "receipt.pdf",
        "bill_2025.pdf",
        "download.pdf",
        "file_final.pdf",
        "doc_v2.pdf",
        "untitled.pdf",
        "scan_001.pdf",
        "bank.pdf",
        "credit.pdf",
        "payment_01.pdf",
        "statement_copy.pdf",
        "final_doc.pdf",
        "report.pdf",
        "taxes.pdf",
        "receipt_amazon.pdf",
        "bill.pdf"
    ]
    
    print("📄 Creating sample documents in Downloads...")
    print(f"📁 Location: {downloads}")
    print("")
    
    for filename in messy_files:
        filepath = downloads / filename
        # Create empty file as placeholder
        filepath.touch()
        print(f"   ✓ Created: {filename}")
    
    print(f"\n✅ Created {len(messy_files)} sample documents")
    print("\n💡 These files simulate a messy Downloads folder")
    print("   Run MoneyMind workflows in Accomplish to organize them!")

def create_metrics_log():
    """Create sample metrics tracking file"""
    metrics_dir = Path("metrics")
    metrics_dir.mkdir(exist_ok=True)
    
    # Time saved log
    time_saved = metrics_dir / "time_saved_log.csv"
    with open(time_saved, 'w') as f:
        f.write("Date,Task,Time_Before_Minutes,Time_After_Minutes,Time_Saved_Minutes\n")
        f.write("2025-02-16,Document Organization,45,0.5,44.5\n")
        f.write("2025-02-17,Subscription Audit,120,8,112\n")
        f.write("2025-02-18,Bill Tracker Setup,60,5,55\n")
        f.write("2025-02-18,Expense Analysis,180,3,177\n")
        f.write("2025-02-19,Dashboard Generation,240,0.75,239.25\n")
        f.write("2025-02-19,Tax Prep,480,8,472\n")
    
    # Money saved log
    money_saved = metrics_dir / "money_saved_log.csv"
    with open(money_saved, 'w') as f:
        f.write("Date,Category,Amount_Per_Month,Amount_Per_Year,Description\n")
        f.write("2025-02-17,Subscription Savings,47,564,Cancelled 2 unused subscriptions + negotiated gym rate\n")
        f.write("2025-02-18,Late Fee Prevention,8.75,105,Zero missed payments with bill tracker\n")
    
    print(f"\n✅ Created metrics tracking files")
    print(f"📊 Location: {metrics_dir}/")
    print(f"   - time_saved_log.csv")
    print(f"   - money_saved_log.csv")

def create_readme():
    """Create a demo README"""
    readme_content = """# MoneyMind Demo Data

This directory contains sample data for demonstrating MoneyMind.

## Files Created

### Sample Documents (~/Downloads/)
20 messy PDF files with unclear names, simulating a chaotic Downloads folder.

### Metrics Tracking (metrics/)
- `time_saved_log.csv` - Time savings from each workflow
- `money_saved_log.csv` - Money saved through automation

## Using This Demo Data

1. Run `python3 scripts/demo_data_generator.py` to create sample files
2. Open Accomplish
3. Run MoneyMind workflows to organize the files
4. See the before/after transformation!

## Real Usage

For real usage, simply:
1. Use your actual financial documents
2. Run the same workflows
3. Track your real metrics

The demo data is just to show the transformation visually.
"""
    
    with open("DEMO_DATA.md", 'w') as f:
        f.write(readme_content)
    
    print(f"\n✅ Created DEMO_DATA.md")

if __name__ == "__main__":
    print("🎬 MoneyMind Demo Data Generator")
    print("━" * 50)
    print("")
    
    create_sample_pdfs()
    create_metrics_log()
    create_readme()
    
    print("\n" + "━" * 50)
    print("🎉 Demo data generation complete!")
    print("\n📋 Next steps:")
    print("   1. Open Accomplish")
    print("   2. Run: 'organize all financial documents in my Downloads folder'")
    print("   3. Watch the magic happen!")
    print("\n💎 MoneyMind - Your AI Financial Analyst")