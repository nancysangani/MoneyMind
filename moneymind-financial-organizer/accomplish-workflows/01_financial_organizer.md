# Workflow 1: Financial Document Organizer

## Purpose
Automatically organize financial PDFs from Downloads into a structured folder hierarchy with intelligent naming.

## Problem Solved
- 40+ financial PDFs scattered in Downloads with names like "document_2024.pdf"
- No consistent naming convention
- Files mixed with other downloads
- Takes 45 minutes to organize manually

## Accomplish Command

```
Organize all financial documents in my Downloads folder:

1. Scan ~/Downloads for any files that are financial documents (bank statements, 
   credit card bills, invoices, receipts, tax forms, investment statements, etc.)

2. For each financial document:
   - Extract metadata: institution name, document type, month, year
   - Rename following this pattern: {Institution}_{Type}_{MonthYear}.pdf
   - Examples:
     * "Chase_CreditCard_Statement_Feb2025.pdf"
     * "BankOfAmerica_Checking_Statement_Jan2025.pdf"
     * "Vanguard_Investment_Statement_Q4_2024.pdf"
     * "Amazon_Receipt_Feb15_2025.pdf"

3. Create organized folder structure in ~/Documents/Finances/:
   Finances/
   ├── 2025/
   │   ├── Banking/
   │   │   ├── Chase/
   │   │   │   ├── Statements/
   │   │   │   └── Receipts/
   │   │   └── BankOfAmerica/
   │   │       ├── Statements/
   │   │       └── Notices/
   │   ├── Credit_Cards/
   │   │   ├── Chase_Sapphire/
   │   │   └── AmEx/
   │   ├── Investments/
   │   │   ├── Vanguard/
   │   │   └── Fidelity/
   │   ├── Utilities/
   │   ├── Subscriptions/
   │   └── Receipts/
   └── 2024/
       └── [same structure]

4. Move each renamed file to its appropriate folder:
   - Banking statements → Finances/{Year}/Banking/{Institution}/Statements/
   - Credit card bills → Finances/{Year}/Credit_Cards/{Institution}/
   - Investment reports → Finances/{Year}/Investments/{Institution}/
   - Receipts → Finances/{Year}/Receipts/
   - Utilities → Finances/{Year}/Utilities/

5. Generate a summary report (~/Documents/Finances/organization_summary.txt):
   - Total documents organized: [count]
   - Files by institution: [breakdown]
   - Files by type: [breakdown]
   - Date range: [earliest to latest]
   - Any files that couldn't be categorized: [list with reasons]

6. Leave non-financial files in Downloads untouched.
```

## Expected Results

- **Time taken:** ~30 seconds
- **Time saved:** 44 minutes vs manual organization
- **Documents processed:** 40-50 typical
- **Success rate:** 95%+ with clear document types

## Demo Talking Points

- "Watch Accomplish scan 47 messy PDFs in my Downloads"
- "It's reading each document, extracting the institution and date"
- "Creating the perfect folder structure automatically"
- "This used to take me 45 minutes. Accomplish did it in 32 seconds."

## Edge Cases Handled

✅ Password-protected PDFs (skips with note)  
✅ Scanned documents with poor OCR (best-effort naming)  
✅ Duplicate files (adds timestamp suffix)  
✅ Unknown institutions (creates "Other" folder)  
✅ Multi-page statements (keeps as single file)