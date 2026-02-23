---
name: moneymind-financial-organizer
description: Organizes financial documents from Downloads into structured folders with intelligent categorization and renaming. Processes PDFs by reading content, identifying institution/type/date, renaming files clearly, creating organized folder structure, and generating summary reports. Handles banking statements, credit cards, investments, receipts, utilities, and tax documents automatically.
user-invokable: true
disable-model-invocation: false
---

# MoneyMind Financial Organizer

Automatically organizes financial PDFs from Downloads into a clean, structured system.

## Trigger This Skill

Say any of these to activate:
- "organize my finances"
- "organize financial documents" 
- "organize my PDFs"
- "clean up my financial documents"
- "sort my bank statements"

## What This Does

### Before
```
~/Downloads/
├── document_2024.pdf
├── statement.pdf
├── IMG_1234.pdf
├── receipt.pdf
└── bill_2025.pdf
```

### After
```
~/Documents/Finances/
├── 2025/
│   ├── Banking/
│   │   └── Chase/
│   │       └── Statements/
│   │           └── Chase_Checking_Statement_Feb2025.pdf
│   ├── Credit_Cards/
│   │   └── Chase_Sapphire/
│   │       └── Chase_CreditCard_Statement_Feb2025.pdf
│   └── Investments/
│       └── Vanguard/
│           └── Vanguard_Investment_Statement_Q4_2024.pdf
└── 2024/
    └── [same structure]
```

---

## Instructions for Accomplish

### Step 1: Scan Downloads
- Look in `~/Downloads` for PDF files
- Identify which ones are financial documents
- Types: bank statements, credit card bills, invoices, receipts, tax forms, investment statements

### Step 2: Extract Metadata
For each financial PDF:
- Read the content
- Identify:
  * Institution name (Chase, BofA, Vanguard, Amazon, etc.)
  * Document type (Statement, Receipt, Invoice, Tax Form)
  * Date (Month and Year)

### Step 3: Rename Files
Use this format: `Institution_Type_MonthYear.pdf`

Examples:
- `Chase_CreditCard_Statement_Feb2025.pdf`
- `BankOfAmerica_Checking_Statement_Jan2025.pdf`
- `Vanguard_Investment_Statement_Q4_2024.pdf`
- `Amazon_Receipt_Feb15_2025.pdf`

### Step 4: Create Folder Structure
Base path: `~/Documents/Finances/`

Structure: `[Year]/[Category]/[Institution]/[SubType]/`

**Categories:**
- **Banking** - checking accounts, savings accounts
- **Credit_Cards** - credit card statements
- **Investments** - stocks, 401k, brokerage accounts
- **Utilities** - electric, water, internet bills
- **Subscriptions** - Netflix, Spotify, gym memberships
- **Receipts** - Amazon, retail purchases
- **Tax_Prep** - W-2, 1099, tax forms

**Examples:**
- Banking statement → `Finances/2025/Banking/Chase/Statements/`
- Credit card → `Finances/2025/Credit_Cards/Chase_Sapphire/`
- Investment → `Finances/2025/Investments/Vanguard/`
- Receipt → `Finances/2025/Receipts/`

### Step 5: Move Files
- Move each renamed file to its appropriate folder
- Create subfolders as needed
- Preserve file metadata (date modified, etc.)

### Step 6: Generate Summary
Create file: `~/Documents/Finances/organization_summary.txt`

Include:
```
MoneyMind Organization Summary
Generated: [current timestamp]

Total files organized: [count]

By Institution:
- Chase: X files
- BankOfAmerica: X files
- Vanguard: X files
[etc.]

By Type:
- Credit Card Statements: X
- Bank Statements: X
- Receipts: X
- Investment Statements: X
[etc.]

Date Range: [earliest date] to [latest date]

Unable to categorize:
- [list any files that couldn't be processed]
```

### Step 7: Non-Financial Files
- Leave non-financial files in Downloads untouched
- Only process obvious financial documents

---

## Edge Cases to Handle

### Password-Protected PDFs
- Skip these files
- Note in summary: "Skipped (password-protected)"

### Poor Quality Scans
- Try best effort to categorize
- If unclear, move to `Unknown` institution folder

### Duplicate Files
- If file already exists in destination, add timestamp suffix
- Example: `Chase_Statement_Feb2025_1645123456.pdf`

### Unknown Institutions
- Create folder: `Other` or `Unknown`
- Still organize by document type

### Non-PDF Financial Documents
- Handle if possible (.xlsx, .csv, .txt statements)
- Skip if format can't be processed

---

## Expected Performance

- **Time:** ~30 seconds for 40-50 files
- **Success Rate:** 90%+ with clear PDFs
- **Accuracy:** High for major institutions

---

## Success Indicators

After completion, verify:
- ✓ Files moved from Downloads to organized folders
- ✓ Files renamed with clear, consistent format
- ✓ Folder structure created correctly
- ✓ Summary report generated
- ✓ No files lost or corrupted
- ✓ Non-financial files left untouched

---

## Example Workflow Execution

**User says:** "organize my finances"

**Accomplish does:**
1. Scans ~/Downloads → finds 47 PDFs
2. Reads each PDF → identifies 42 as financial
3. Extracts metadata → categorizes all 42
4. Renames files → clear naming format
5. Creates folders → organized structure
6. Moves files → proper locations
7. Generates summary → ~/Documents/Finances/organization_summary.txt

**Result:** 
- 42 files organized in 32 seconds
- 5 non-financial PDFs left in Downloads
- Complete summary report available
- Time saved: 44 minutes vs manual organization