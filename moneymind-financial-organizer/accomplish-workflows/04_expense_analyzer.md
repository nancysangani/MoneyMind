# Workflow 4: Expense Analysis Engine

## Purpose
Automatically categorize and analyze spending patterns from credit card statements.

## Problem Solved
- Manual categorization of 200+ monthly transactions
- No visibility into spending patterns
- Takes 3 hours to create monthly spending report
- Can't identify spending anomalies or trends

## Accomplish Command

```
Analyze my expenses and generate spending insights:

1. Scan all credit card statements in ~/Documents/Finances/2025/Credit_Cards/

2. Extract all transactions:
   - Date
   - Merchant name
   - Amount
   - Transaction type (purchase, refund, fee)
   - Card used

3. Categorize each transaction into these categories:
   
   ESSENTIAL SPENDING:
   - Groceries (Whole Foods, Safeway, Trader Joe's, etc.)
   - Utilities (PG&E, water, internet, phone)
   - Rent/Mortgage
   - Insurance (health, car, home)
   - Transportation (gas, Uber, parking, tolls)
   - Healthcare (pharmacy, doctor, dental)
   
   DISCRETIONARY SPENDING:
   - Dining Out (restaurants, delivery, coffee shops)
   - Entertainment (movies, concerts, events)
   - Shopping (clothing, electronics, home goods)
   - Travel (flights, hotels, vacation)
   - Hobbies & Recreation
   - Personal Care (haircut, gym, spa)
   
   FINANCIAL:
   - Subscriptions (Netflix, Spotify, etc.)
   - Fees (late fees, ATM fees, interest)
   - Investments/Savings
   
   OTHER:
   - Uncategorized (manual review needed)

4. Generate comprehensive expense analysis report (~/Documents/Finances/expense_analysis.html):
   
   Include sections:
   - Spending Overview (total, number of transactions, averages)
   - Spending by Category (pie chart + table with percentages)
   - Month-over-Month Trends (vs last month, same month last year)
   - Top Spending Categories (top 5 with details)
   - Spending Insights (patterns, frequency analysis)
   - Alerts & Anomalies (unusual charges, duplicates, spikes)
   - Recommendations (categories to reduce, good control, watch list)

5. Create visual charts:
   - Spending by category (pie chart)
   - Monthly trend line (past 6 months)
   - Essential vs Discretionary breakdown
   - Top 10 merchants (bar chart)

6. Export raw transaction data to CSV for additional analysis if needed

7. Compare current month to:
   - Previous month
   - Same month last year
   - 6-month average
```

## Expected Results

- **Time taken:** ~3 minutes
- **Time saved:** 177 minutes vs manual categorization
- **Transactions analyzed:** 100-200 typical
- **Insights generated:** 10-15 actionable

## Demo Talking Points

- "Accomplish is reading my credit card statements"
- "Automatically categorizing 127 transactions"
- "Look at this breakdown - 21% of my spending is dining out!"
- "It even caught a potential duplicate charge"
- "This analysis found $3,216 in annual savings potential"

## Edge Cases Handled

✅ Refunds and returns (tracked separately)  
✅ Foreign transactions (currency conversion)  
✅ Recurring vs one-time purchases  
✅ Split transactions (gas + snacks)  
✅ Merchant name variations (AMZN vs Amazon)