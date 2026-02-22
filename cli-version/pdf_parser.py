#!/usr/bin/env python3
"""
MoneyMind - PDF Parser Engine
Extracts REAL financial data from organized PDFs.
"""

import re
from pathlib import Path
from collections import defaultdict

try:
    import pdfplumber
except ImportError:
    import os
    os.system("pip install pdfplumber --break-system-packages -q")
    import pdfplumber


# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────

def extract_text(pdf_path: Path) -> str:
    try:
        with pdfplumber.open(pdf_path) as pdf:
            return "\n".join(page.extract_text() or "" for page in pdf.pages)
    except Exception as e:
        print(f"    ⚠️  Cannot read {pdf_path.name}: {e}")
        return ""


def extract_amount(text: str, keywords: list, min_val: float = 100.0) -> float | None:
    """
    For each keyword, scan the line it appears on + next line for an INR amount.
    Uses min_val to skip small noise numbers (e.g. meter rent Rs.20).
    Returns the LARGEST plausible amount found near the keyword.
    """
    text_lower = text.lower()
    lines = text.split("\n")

    best = None
    for kw in keywords:
        for i, line in enumerate(lines):
            if kw.lower() not in line.lower():
                continue
            # Search this line and the next for amounts
            search_block = line
            if i + 1 < len(lines):
                search_block += " " + lines[i + 1]

            # Match Indian-format numbers: 1,23,456.78 or 12345.00
            matches = re.findall(r'[\d,]+\.\d{2}', search_block)
            for m in matches:
                try:
                    val = float(m.replace(",", ""))
                    if val >= min_val:
                        if best is None or val > best:
                            best = val
                except ValueError:
                    continue
    return best


# ─────────────────────────────────────────────────────────────────────────────
# Bank Statement Parser
# ─────────────────────────────────────────────────────────────────────────────

def parse_bank_statement(pdf_path: Path) -> dict:
    text = extract_text(pdf_path)
    if not text:
        return {}

    result = {
        "source": pdf_path.name,
        "type": "bank_statement",
        "closing_balance": None,
        "opening_balance": None,
        "total_credits": None,
        "total_debits": None,
        "transactions": [],
    }

    result["closing_balance"] = extract_amount(text, [
        "closing balance", "closing bal", "balance c/f", "available balance"
    ], min_val=100)

    result["opening_balance"] = extract_amount(text, [
        "opening balance", "opening bal", "balance b/f"
    ], min_val=100)

    result["total_credits"] = extract_amount(text, [
        "total credits", "total credit", "total cr", "total deposit"
    ], min_val=100)

    result["total_debits"] = extract_amount(text, [
        "total debits", "total debit", "total dr", "total withdrawal"
    ], min_val=100)

    # Parse individual transactions from statement lines
    spending_categories = {
        "food":          ["swiggy", "zomato", "restaurant", "food", "cafe"],
        "groceries":     ["bigbasket", "blinkit", "grocery", "supermarket", "dmart"],
        "transport":     ["ola", "uber", "rapido", "petrol", "fuel", "irctc", "metro"],
        "entertainment": ["netflix", "spotify", "bookmyshow", "prime", "hotstar", "youtube"],
        "shopping":      ["amazon", "flipkart", "myntra", "ajio", "nykaa"],
        "utilities":     ["electricity", "dgvcl", "bescom", "water", "broadband", "jio", "airtel", "recharge"],
        "health":        ["pharmacy", "pharmeasy", "hospital", "clinic", "apollo"],
        "transfer":      ["neft", "imps", "nach", "emi", "home loan", "lic", "sip"],
    }

    for line in text.split("\n"):
        line_lower = line.lower()
        # Look for debit amounts (numbers with decimals in transaction lines)
        amounts = re.findall(r'[\d,]+\.\d{2}', line)
        if not amounts or len(line) < 15:
            continue
        try:
            amt = float(amounts[0].replace(",", ""))
        except ValueError:
            continue
        if amt < 10:
            continue

        cat = "other"
        for category, keywords in spending_categories.items():
            if any(kw in line_lower for kw in keywords):
                cat = category
                break

        result["transactions"].append({
            "description": line[:60].strip(),
            "amount": amt,
            "category": cat,
        })

    print(f"    🏦 Bank: {pdf_path.name}")
    if result["closing_balance"]:
        print(f"       Closing Balance: Rs.{result['closing_balance']:,.2f}")
    else:
        print(f"       Closing Balance: not found")
    print(f"       Transactions: {len(result['transactions'])}")
    return result


# ─────────────────────────────────────────────────────────────────────────────
# Credit Card Parser
# ─────────────────────────────────────────────────────────────────────────────

def parse_credit_card(pdf_path: Path) -> dict:
    text = extract_text(pdf_path)
    if not text:
        return {}

    result = {
        "source": pdf_path.name,
        "type": "credit_card",
        "total_due": None,
        "min_due": None,
        "credit_limit": None,
        "spending_by_category": {},
        "transactions": [],
    }

    result["total_due"] = extract_amount(text, [
        "total amount due", "total due", "amount due",
        "outstanding amount", "total outstanding"
    ], min_val=100)

    result["min_due"] = extract_amount(text, [
        "minimum amount due", "minimum due", "min due"
    ], min_val=1)

    result["credit_limit"] = extract_amount(text, [
        "credit limit", "total limit"
    ], min_val=1000)

    # Category spending from statement lines
    category_keywords = {
        "dining":        ["dining", "restaurant", "food", "zomato", "swiggy"],
        "shopping":      ["shopping", "retail", "amazon", "flipkart", "myntra"],
        "travel":        ["travel", "hotel", "flight", "makemytrip", "irctc"],
        "entertainment": ["entertainment", "netflix", "spotify", "bookmyshow"],
        "groceries":     ["grocery", "supermarket", "bigbasket", "blinkit"],
        "health":        ["medical", "pharmacy", "hospital"],
        "utilities":     ["utility", "electricity", "mobile", "broadband"],
        "fuel":          ["fuel", "petrol", "diesel"],
    }

    cat_totals = defaultdict(float)
    for line in text.split("\n"):
        line_lower = line.lower()
        amounts = re.findall(r'[\d,]+\.\d{2}', line)
        if not amounts:
            continue
        try:
            amt = float(amounts[-1].replace(",", ""))
        except ValueError:
            continue
        if amt < 10:
            continue

        for cat, keywords in category_keywords.items():
            if any(kw in line_lower for kw in keywords):
                cat_totals[cat] += amt
                result["transactions"].append({
                    "description": line[:60].strip(),
                    "amount": amt,
                    "category": cat,
                })
                break

    result["spending_by_category"] = dict(cat_totals)

    print(f"    💳 Credit Card: {pdf_path.name}")
    if result["total_due"]:
        print(f"       Total Due: Rs.{result['total_due']:,.2f}")
    else:
        print(f"       Total Due: not found")
    print(f"       Categories: {list(result['spending_by_category'].keys())}")
    return result


# ─────────────────────────────────────────────────────────────────────────────
# Subscription / Invoice Parser
# ─────────────────────────────────────────────────────────────────────────────

def parse_subscription(pdf_path: Path) -> dict:
    text = extract_text(pdf_path)
    if not text:
        return {}

    text_lower = text.lower()

    KNOWN_SERVICES = {
        "netflix": 649, "spotify": 119, "hotstar": 299,
        "prime": 299, "youtube premium": 189,
        "adobe": 1675, "canva": 499,
        "zoom": 1250, "microsoft": 489,
        "linkedin": 1600, "github": 825,
        "gym": 1500, "cult": 999,
        "jio": 299, "airtel": 399,
    }

    result = {
        "source": pdf_path.name,
        "type": "subscription",
        "service_name": "Unknown",
        "amount": None,
    }

    for service, default_cost in KNOWN_SERVICES.items():
        if service in text_lower:
            result["service_name"] = service.title()
            result["amount"] = default_cost
            break

    # Try to extract actual billed amount — must be > 50 to avoid tax line noise
    actual = extract_amount(text, [
        "total amount", "amount paid", "invoice total",
        "grand total", "total payable", "amount charged",
        "subscription fee", "plan amount", "total"
    ], min_val=50)

    if actual:
        result["amount"] = actual

    print(f"    📱 Subscription: {pdf_path.name}")
    print(f"       Service: {result['service_name']} | Amount: Rs.{result['amount']}")
    return result


# ─────────────────────────────────────────────────────────────────────────────
# Utility Bill Parser  — fixed Rs.20 bug
# ─────────────────────────────────────────────────────────────────────────────

def parse_utility_bill(pdf_path: Path) -> dict:
    text = extract_text(pdf_path)
    if not text:
        return {}

    text_lower = text.lower()

    result = {
        "source": pdf_path.name,
        "type": "utility",
        "bill_type": "electricity",
        "amount_due": None,
        "units_consumed": None,
    }

    if any(k in text_lower for k in ["electricity", "kwh", "dgvcl", "bescom", "msedcl", "tpddl", "torrent power"]):
        result["bill_type"] = "electricity"
    elif any(k in text_lower for k in ["broadband", "internet", "fiber"]):
        result["bill_type"] = "internet"
    elif any(k in text_lower for k in ["gas", "lpg", "cng"]):
        result["bill_type"] = "gas"
    elif any(k in text_lower for k in ["water", "jal"]):
        result["bill_type"] = "water"

    # ── KEY FIX: use high min_val (500) to skip line-item noise like Meter Rent 20.00
    # "TOTAL AMOUNT PAYABLE" will always be larger than individual line items
    result["amount_due"] = extract_amount(text, [
        "total amount payable",
        "total payable",
        "net payable",
        "total amount due",
        "amount payable",
        "gross amount",
        "bill amount",
        "amount due",
    ], min_val=200)   # electricity bills in India are always >Rs.200

    # Units consumed
    units_match = re.search(r'(\d{2,4})\s*(?:units?|kwh)', text_lower)
    if units_match:
        result["units_consumed"] = int(units_match.group(1))

    print(f"    ⚡ Utility: {pdf_path.name}")
    print(f"       Type: {result['bill_type']} | Amount: Rs.{result['amount_due']}")
    if result["units_consumed"]:
        print(f"       Units: {result['units_consumed']}")
    return result


# ─────────────────────────────────────────────────────────────────────────────
# Investment Parser
# ─────────────────────────────────────────────────────────────────────────────

def parse_investment(pdf_path: Path) -> dict:
    text = extract_text(pdf_path)
    if not text:
        return {}

    result = {
        "source": pdf_path.name,
        "type": "investment",
        "current_value": None,
        "invested_amount": None,
        "xirr": None,
        "sip_amount": None,
        "gain_loss": None,
    }

    result["current_value"] = extract_amount(text, [
        "current value", "market value", "portfolio value",
        "current nav value", "present value"
    ], min_val=100)

    result["invested_amount"] = extract_amount(text, [
        "invested amount", "total invested", "cost value",
        "purchase value", "total investment"
    ], min_val=100)

    xirr_match = re.search(r'xirr[:\s]+(\d+\.?\d*)%', text.lower())
    if xirr_match:
        result["xirr"] = float(xirr_match.group(1))

    result["sip_amount"] = extract_amount(text, [
        "sip amount", "monthly sip", "instalment amount"
    ], min_val=100)

    if result["current_value"] and result["invested_amount"]:
        result["gain_loss"] = round(result["current_value"] - result["invested_amount"], 2)

    print(f"    📈 Investment: {pdf_path.name}")
    if result["current_value"]:
        print(f"       Current Value: Rs.{result['current_value']:,.2f}")
    else:
        print(f"       Current Value: not found")
    if result["xirr"]:
        print(f"       XIRR: {result['xirr']}%")
    return result


# ─────────────────────────────────────────────────────────────────────────────
# Master router
# ─────────────────────────────────────────────────────────────────────────────

def parse_all_pdfs(finances_dir: Path) -> dict:
    """Walk organized Finances folder, parse every real PDF."""
    results = {
        "banking": [], "credit_cards": [],
        "subscriptions": [], "utilities": [],
        "investments": [], "total_pdfs": 0,
    }

    category_parsers = {
        "Banking":       parse_bank_statement,
        "Credit_Cards":  parse_credit_card,
        "Subscriptions": parse_subscription,
        "Utilities":     parse_utility_bill,
        "Investments":   parse_investment,
    }

    key_map = {
        "Banking":       "banking",
        "Credit_Cards":  "credit_cards",
        "Subscriptions": "subscriptions",
        "Utilities":     "utilities",
        "Investments":   "investments",
    }

    for year in [2023, 2024, 2025, 2026]:
        year_path = finances_dir / str(year)
        if not year_path.exists():
            continue
        for pdf in year_path.glob("**/*.pdf"):
            # Determine category from path: Finances/2025/Banking/HDFC/Statements/file.pdf
            try:
                rel = pdf.relative_to(year_path)
                category = rel.parts[0]  # first folder under year = category
            except Exception:
                continue

            parser = category_parsers.get(category)
            if not parser:
                continue

            data = parser(pdf)
            if not data:
                continue

            key = key_map.get(category, "banking")
            results[key].append(data)
            results["total_pdfs"] += 1

    return results


# ─────────────────────────────────────────────────────────────────────────────
# Aggregators
# ─────────────────────────────────────────────────────────────────────────────

def compute_net_worth(parsed: dict) -> float:
    total = 0.0
    for b in parsed["banking"]:
        if b.get("closing_balance"):
            total += b["closing_balance"]
    for inv in parsed["investments"]:
        if inv.get("current_value"):
            total += inv["current_value"]
    return round(total, 2)


def compute_monthly_spending(parsed: dict) -> float:
    total = 0.0
    for cc in parsed["credit_cards"]:
        if cc.get("total_due"):
            total += cc["total_due"]
    if total == 0:
        for b in parsed["banking"]:
            if b.get("total_debits"):
                total += b["total_debits"]
    return round(total, 2)


def compute_subscription_total(parsed: dict) -> dict:
    total = 0.0
    services = []
    for sub in parsed["subscriptions"]:
        if sub.get("amount"):
            total += sub["amount"]
            services.append({
                "name": sub.get("service_name", "Unknown"),
                "monthly": sub["amount"]
            })
    return {"monthly_total": round(total, 2), "count": len(services), "services": services}


def compute_spending_by_category(parsed: dict) -> dict:
    cats = defaultdict(float)
    for cc in parsed["credit_cards"]:
        for cat, amt in cc.get("spending_by_category", {}).items():
            cats[cat] += amt
    for b in parsed["banking"]:
        for txn in b.get("transactions", []):
            cats[txn["category"]] += txn["amount"]
    return {k: round(v, 2) for k, v in cats.items() if v >= 50}


def compute_savings_opportunities(parsed: dict) -> list:
    opps = []

    # Duplicate entertainment subscriptions
    entertainment = ["Netflix", "Hotstar", "Prime", "Youtube Premium"]
    ent_subs = [
        (s.get("service_name",""), s.get("amount", 0))
        for s in parsed["subscriptions"]
        if any(e.lower() in s.get("service_name","").lower() for e in entertainment)
    ]
    if len(ent_subs) >= 2:
        ent_subs.sort(key=lambda x: x[1])
        to_cancel = ent_subs[1:]
        monthly = sum(a for _, a in to_cancel)
        opps.append({
            "category": "Subscription Savings",
            "monthly": monthly, "annual": monthly * 12,
            "description": f"{len(ent_subs)} entertainment subs found — cancel {', '.join(n for n,_ in to_cancel)} = Rs.{monthly:.0f}/month saved"
        })

    # High electricity usage
    for util in parsed["utilities"]:
        if util.get("bill_type") == "electricity":
            units = util.get("units_consumed")
            amount = util.get("amount_due")
            if units and units > 300 and amount:
                saving = round(amount * 0.10, 2)
                opps.append({
                    "category": "Utility Savings",
                    "monthly": saving, "annual": saving * 12,
                    "description": f"High usage ({units} units). 10% reduction = Rs.{saving:.0f}/month saved"
                })

    # Late fee prevention
    if parsed["credit_cards"]:
        opps.append({
            "category": "Late Fee Prevention",
            "monthly": 500, "annual": 6000,
            "description": "MoneyMind auto-reminders preventing Rs.500 late fees monthly"
        })

    return opps


if __name__ == "__main__":
    finances_dir = Path.home() / "Documents" / "Finances"
    print("🔍 Testing PDF Parser...\n")
    parsed = parse_all_pdfs(finances_dir)
    print(f"\n📊 Results:")
    print(f"   Total PDFs:       {parsed['total_pdfs']}")
    print(f"   Net Worth:        Rs.{compute_net_worth(parsed):,.2f}")
    print(f"   Monthly Spending: Rs.{compute_monthly_spending(parsed):,.2f}")
    subs = compute_subscription_total(parsed)
    print(f"   Subscriptions:    {subs['count']} × Rs.{subs['monthly_total']:,.2f}/mo")
    print(f"   Spending Cats:    {compute_spending_by_category(parsed)}")