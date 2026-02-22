#!/usr/bin/env python3
"""
Quick Fix: Move Dashboard Files to Correct Location
Solves CORS issue by putting HTML and JSON in same folder
"""

import shutil
from pathlib import Path

def fix_dashboard_location():
    """Move dashboard files to correct location"""
    
    home = Path.home()
    
    # Source locations
    html_source = Path("templates/dashboard/index.html")
    json_source = Path("~/Documents/Finances/Dashboard/dashboard_data.json").expanduser()
    
    # Target location (where they should BOTH be)
    dashboard_dir = home / "Documents" / "Finances" / "Dashboard"
    dashboard_dir.mkdir(parents=True, exist_ok=True)
    
    print("🔧 Fixing dashboard file locations...")
    print()
    
    # Copy HTML to Dashboard folder
    if html_source.exists():
        html_dest = dashboard_dir / "index.html"
        shutil.copy2(html_source, html_dest)
        print(f"✅ Copied HTML to: {html_dest}")
    else:
        print(f"⚠️  HTML not found at: {html_source}")
    
    # Check JSON exists
    if json_source.exists():
        print(f"✅ JSON exists at: {json_source}")
    else:
        print(f"⚠️  JSON not found at: {json_source}")
        print(f"   Run: python moneymind.py dashboard")
    
    print()
    print("📂 Dashboard files should now be together:")
    print(f"   📄 {dashboard_dir / 'index.html'}")
    print(f"   📊 {dashboard_dir / 'dashboard_data.json'}")
    print()
    print("🌐 Open dashboard:")
    print(f"   file:///{dashboard_dir / 'index.html'}")
    print()
    print(f"   Or run: explorer {dashboard_dir}")

if __name__ == "__main__":
    fix_dashboard_location()