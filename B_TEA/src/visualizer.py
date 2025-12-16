import matplotlib.pyplot as plt
import seaborn as sns

def plot_category(df):
    plt.figure(figsize=(10,6))
    sns.barplot(x=df.index, y=df.values, palette="viridis")
    plt.title("Spending by Category")
    plt.ylabel("Amount")
    plt.xlabel("Category")
    plt.xticks(rotation=45)
    plt.show()

def plot_over_time(df):
    plt.figure(figsize=(10,6))
    df.index = df.index.to_timestamp()
    sns.lineplot(x=df.index, y=df.values, marker="o")
    plt.title("Spending Over Time")
    plt.ylabel("Total Amount")
    plt.xlabel("Month")
    plt.show()
