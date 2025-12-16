import pandas as pd

def total_spent(df: pd.DataFrame) -> float:
    return df["amount"].sum()

def spent_by_category(df: pd.DataFrame) -> pd.DataFrame:
    return df.groupby("category")["amount"].sum().sort_values(ascending=False)

def spent_by_month(df: pd.DataFrame) -> pd.DataFrame:
    df["month"] = df["date"].dt.to_period("M")
    return df.groupby("month")["amount"].sum()
