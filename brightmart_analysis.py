import pandas as pd

# Load the CSV file
df = pd.read_csv("brightmart_sales.csv")

# Display first few rows
print("Preview of dataset:")
print(df.head())

# Basic info
print("\nDataset Info:")
print(df.info())

# Check for missing values
print("\nMissing Values:")
print(df.isnull().sum())
# --- Step 2: Exploratory Data Analysis (EDA) ---

print("\n--- Basic Statistics ---")
print(df.describe())

# 1️⃣ Total sales summary
total_sales = df["Total_Sales"].sum()
print(f"\nTotal Sales (All Regions): {total_sales:,}")

# 2️⃣ Sales by region
sales_by_region = df.groupby("Region")["Total_Sales"].sum().sort_values(ascending=False)
print("\nSales by Region:")
print(sales_by_region)

# 3️⃣ Sales by product
sales_by_product = df.groupby("Product")["Total_Sales"].sum().sort_values(ascending=False)
print("\nSales by Product:")
print(sales_by_product)

# 4️⃣ Average unit price per product
avg_price = df.groupby("Product")["Unit_Price"].mean().sort_values(ascending=False)
print("\nAverage Unit Price per Product:")
print(avg_price)

# 5️⃣ Top 5 highest single-day sales
top5_sales = df.sort_values("Total_Sales", ascending=False).head(5)
print("\nTop 5 Highest Single-Day Sales:")
print(top5_sales)
import matplotlib.pyplot as plt

# --- Step 3: Visualization ---

# 1️⃣ Sales by Region
sales_by_region.plot(kind="bar", title="Total Sales by Region", ylabel="Sales", xlabel="Region", rot=0)
plt.tight_layout()
plt.show()

# 2️⃣ Sales by Product
sales_by_product.plot(kind="bar", color="orange", title="Total Sales by Product", ylabel="Sales", xlabel="Product", rot=0)
plt.tight_layout()
plt.show()

# 3️⃣ Average Unit Price by Product
avg_price.plot(kind="bar", color="green", title="Average Unit Price per Product", ylabel="Average Price", xlabel="Product", rot=0)
plt.tight_layout()
plt.show()
