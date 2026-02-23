# Workflow 5: Financial Dashboard Generator

## Purpose
Create a real-time, interactive financial dashboard aggregating all financial data.

## Problem Solved
- No centralized view of financial health
- Data scattered across statements, emails, folders
- Quarterly manual updates in spreadsheet
- No visual representation of financial trends

## Accomplish Command

```
Generate my comprehensive financial dashboard:

1. Aggregate data from all sources:
   - Organized financial documents (~/Documents/Finances/)
   - Subscription audit report
   - Bill tracker data
   - Expense analysis data
   - Email confirmations for recent transactions

2. Calculate key financial metrics:
   
   NET WORTH TRACKING:
   - Extract account balances from latest statements
   - Track month-over-month changes
   - Calculate year-to-date growth
   - Project end-of-year net worth based on current trends
   
   CASH FLOW ANALYSIS:
   - Monthly income (from bank deposits)
   - Monthly expenses (from credit cards + bills)
   - Savings rate: (Income - Expenses) / Income
   - Monthly surplus/deficit
   
   SPENDING BREAKDOWN:
   - Total monthly spending
   - Essential vs discretionary split
   - Top 5 spending categories
   - Comparison to 6-month average
   
   SUBSCRIPTION TRACKING:
   - Total monthly subscription cost
   - Number of active subscriptions
   - Savings opportunities identified
   - Upcoming renewals
   
   BILL PAYMENT STATUS:
   - Upcoming bills (next 30 days)
   - Bills on auto-pay vs manual
   - Payment success rate
   - Late fees avoided

3. Use the dashboard template at ~/Documents/Finances/Dashboard/index.html and populate it with:
   - Hero metrics (Net Worth, Monthly Spending, Savings Rate, Subscriptions)
   - Interactive charts (spending by category, net worth trend)
   - Recent activity feed
   - Quick insights and alerts
   - Action items (bills due, renewals coming up)

4. Create supporting visualizations:
   - Net worth trend (line chart, last 12 months)
   - Spending by category (donut chart)
   - Income vs expenses (stacked bar chart)
   - Savings rate over time (area chart)
   - Monthly spending comparison (bar chart)

5. Add real-time data:
   - Last updated timestamp
   - Days until next paycheck
   - Days until next major bill
   - Recent transaction highlights

6. Generate insights:
   - "You're saving X% of your income (compare to Y% target)"
   - "Dining spending up/down X% this month"
   - "On track to reach $X net worth by December"
   - "X bills due this week totaling $X"

7. Save dashboard and open in default browser automatically
```

## Expected Results

- **Time taken:** ~45 seconds
- **Data sources aggregated:** 6+
- **Metrics calculated:** 20+
- **Charts generated:** 5
- **Update frequency:** On-demand or daily

## Demo Talking Points

- "This is the MoneyMind dashboard - my financial command center"
- "It pulls data from statements, emails, bill trackers, everything"
- "Look at this net worth trend - up 12.5% this year"
- "These insights update in real-time as new documents arrive"
- "I used to update a spreadsheet quarterly. Now this happens automatically."

## Edge Cases Handled

✅ Missing data (shows "N/A" with explanation)  
✅ Stale data (warns if statements are old)  
✅ Incomplete months (prorates calculations)  
✅ Multiple accounts (aggregates correctly)  
✅ Foreign currencies (converts to USD)