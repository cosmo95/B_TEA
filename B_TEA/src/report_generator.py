import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set(style="whitegrid")

def run_report(csv_path: str):
    """
    Run full B_TEA analysis:
    - Loads and cleans data
    - Calculates totals
    - Shows monthly and category spending
    - Detects spikes and suggests savings
    - Plots graphs
    """

    # --- Load Data ---
    df = pd.read_csv(csv_path, parse_dates=['Date'], dayfirst=True, keep_default_na=True)

    df = df.loc[:, ~df.columns.duplicated()]

    # --- Clean Data ---
    if 'Money Out' in df.columns and 'Money In' in df.columns:
        df['amount'] = df['Money In'].fillna(0) + df['Money Out'].fillna(0)
    elif 'Amount' in df.columns:
        df['amount'] = df['Amount']
    else:
        raise ValueError("No valid column found for amount")
    
    df['amount'] = pd.to_numeric(df['amount'], errors='coerce')
    df = df.dropna(subset=['amount'])
    df['category'] = df['Category'].fillna("General")
    df['date'] = pd.to_datetime(df['Date'], dayfirst=True, errors='coerce')

    # --- Totals ---
    total_expenses = df[df['amount'] < 0]['amount'].abs().sum()
    total_income = df[df['amount'] > 0]['amount'].sum()
    print(f"Total expenses: £{total_expenses:,.2f}")
    print(f"Total income: £{total_income:,.2f}")

    # --- Spending by Category ---
    expenses = df[df['amount'] < 0].copy()
    expenses['amount'] = expenses['amount'].abs()
    category_summary = expenses.groupby('category')['amount'].sum().sort_values(ascending=False)
    print("\nSpending by Category:")
    print(category_summary)

    plt.figure(figsize=(10,6))
    sns.barplot(x=category_summary.values, y=category_summary.index, palette="viridis")
    plt.title("Spending by Category")
    plt.xlabel("Amount (£)")
    plt.ylabel("Category")
    plt.show()

    # --- Monthly Spending ---
    expenses['month'] = expenses['date'].dt.to_period('M')
    monthly_summary = expenses.groupby('month')['amount'].sum()
    print("\nMonthly Spending:")
    print(monthly_summary)

    plt.figure(figsize=(12,6))
    monthly_summary.plot(kind='bar', color='salmon')
    plt.title("Monthly Spending")
    plt.xlabel("Month")
    plt.ylabel("Amount (£)")
    plt.xticks(rotation=45)
    plt.show()

    # --- Category vs Month ---
    category_monthly = expenses.pivot_table(index='month', columns='category', values='amount', aggfunc='sum', fill_value=0)
    plt.figure(figsize=(12,8))
    sns.heatmap(category_monthly, annot=True, fmt=".2f", cmap="YlGnBu")
    plt.title("Monthly Spending by Category")
    plt.xlabel("Category")
    plt.ylabel("Month")
    plt.show()

    # --- AI-Assisted Insights ---
    category_avg = expenses.groupby('category')['amount'].mean()
    category_std = expenses.groupby('category')['amount'].std()
    expenses['spike'] = expenses.apply(
        lambda row: row['amount'] > category_avg.get(row['category'],0) + 2*category_std.get(row['category'],0),
        axis=1
    )
    spikes = expenses[expenses['spike']]
    print("\nUnusually high transactions:")
    print(spikes[['date','category','amount','Name']])

    top_saving_candidates = category_avg.sort_values(ascending=False).head(3)
    top_categories = category_summary.head(3)
    balance = total_income - total_expenses
    max_month = monthly_summary.idxmax()
    max_amount = monthly_summary.max()

    summary = f"""
📝 Summary:

- Total Income: £{total_income:,.2f}
- Total Expenses: £{total_expenses:,.2f}
- Balance: £{balance:,.2f}
- Top 3 Spending Categories: {', '.join(top_categories.index.tolist())}
- Month with highest spending: {max_month} (£{max_amount:,.2f})
- Suggested saving areas: {', '.join(top_saving_candidates.index.tolist())}
"""
    print(summary)
