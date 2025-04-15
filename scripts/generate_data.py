# scripts/generate_data.py

import pandas as pd
import numpy as np
import os

np.random.seed(42)
n = 500

data = {
    "Order ID": np.random.randint(1000, 2000, size=n),
    "Order Date": pd.date_range(start="2023-01-01", periods=n, freq="D"),
    "Region": np.random.choice(["North", "South", "East", "West"], size=n),
    "Customer Name": np.random.choice(["Alice", "Bob", "Charlie", "Diana", "Ethan", "Fiona"], size=n),
    "Product Category": np.random.choice(["Electronics", "Clothing", "Home", "Toys"], size=n),
    "Product Name": np.random.choice(["Item A", "Item B", "Item C", "Item D"], size=n),
    "Sales": np.round(np.random.uniform(10, 500, size=n), 2),
    "Quantity": np.random.randint(1, 5, size=n)
}

df = pd.DataFrame(data)
df["Profit"] = np.round(df["Sales"] * np.random.uniform(0.05, 0.3), 2)

os.makedirs("data", exist_ok=True)
df.to_csv("data/retail_sales_data.csv", index=False)
print("✅ Data saved to data/retail_sales_data.csv")
