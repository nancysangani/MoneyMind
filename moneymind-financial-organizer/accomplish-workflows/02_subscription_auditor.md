# Workflow 2: Subscription Auditor

## Purpose
Find hidden subscription costs, compare your rates to current pricing, and identify savings opportunities.

## Problem Solved
- 9 active subscriptions across different platforms
- No tracking of renewal dates or price changes
- Overpaying $47/month due to price increases and unused services
- Takes 2 hours to manually research and compare

## Accomplish Command

```
Audit my subscriptions and find savings opportunities:

1. Scan my email inbox for the past 12 months for subscription charges:
   - Search terms: "subscription", "recurring", "monthly charge", "annual renewal", 
     "payment received", "invoice", "billing", "membership"
   - Look for: Netflix, Spotify, Amazon Prime, Adobe, gym memberships, software tools, 
     streaming services, etc.

2. For each subscription found, extract:
   - Service name
   - Current amount charged
   - Billing frequency (monthly/annual)
   - Last charge date
   - Next renewal date (if available)
   - Email address associated with the subscription

3. For each active subscription, browse the service's website to find:
   - Current pricing for new customers
   - Available plans and features
   - Any promotional offers or discounts
   - Student/military/family plan options

4. Calculate potential savings:
   - Compare my rate vs. new customer rate
   - Identify price increases since I signed up
   - Flag subscriptions with no recent usage (check email for login confirmations)
   - Find cheaper alternative services for similar features

5. Generate a comprehensive audit report (~/Documents/Finances/subscription_audit.html):
   
   Include sections:
   - Summary (total cost, number of subscriptions, potential savings)
   - Active subscriptions table (service, your rate, new rate, difference)
   - Savings opportunities (prioritized by impact)
   - Upcoming renewals (next 30 days)
   - Recommendations (cancel, downgrade, negotiate, keep)

6. Create calendar reminders:
   - For each renewal date, create a reminder 7 days before
   - Include: service name, amount, link to cancel/manage subscription

7. Save raw data in JSON format (~/Documents/Finances/subscriptions.json) for tracking over time
```

## Expected Results

- **Time taken:** ~8 minutes
- **Time saved:** 112 minutes vs manual research
- **Subscriptions found:** 8-12 typical
- **Savings identified:** $30-70/month average

## Demo Talking Points

- "Accomplish is scanning my email for every subscription charge in the past year"
- "Now it's browsing each company's website to check current pricing"
- "Look at this - I'm overpaying $20/month on my gym membership!"
- "This report just saved me $564 per year. In 8 minutes."

## Edge Cases Handled

✅ Cancelled subscriptions (marks as inactive)  
✅ Promotional periods ending (flags when rate will increase)  
✅ Annual vs monthly billing comparisons  
✅ Family/shared plans (notes if applicable)  
✅ Student discounts (checks eligibility)