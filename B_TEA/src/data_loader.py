from src.data_loader import load_expenses

# Load CSV
df = load_expenses("../data/expenses.csv")

# Clean amount
df['amount'] = df['amount'].abs()

# Quick check
print(df[['date','category','amount']].head())
