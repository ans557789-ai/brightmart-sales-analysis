from fpdf import FPDF
import pandas as pd
import matplotlib.pyplot as plt

# Load your analyzed data
df = pd.read_csv("brightmart_sales.csv")

# --- Compute summaries ---
sales_by_region = df.groupby("Region")["Total_Sales"].sum().sort_values(ascending=False)
sales_by_product = df.groupby("Product")["Total_Sales"].sum().sort_values(ascending=False)
total_sales = df["Total_Sales"].sum()

# --- Save charts for the PDF ---
plt.figure(figsize=(6, 4))
sales_by_region.plot(kind="bar", title="Total Sales by Region")
plt.tight_layout()
plt.savefig("sales_by_region.png")
plt.close()

plt.figure(figsize=(6, 4))
sales_by_product.plot(kind="bar", color="orange", title="Total Sales by Product")
plt.tight_layout()
plt.savefig("sales_by_product.png")
plt.close()

# --- Create PDF ---
class PDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 16)
        self.cell(0, 10, "BrightMart Sales Report (Q3 2024)", ln=True, align="C")
        self.ln(10)

    def chapter_title(self, title):
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, title, ln=True)
        self.ln(5)

    def chapter_body(self, text):
        self.set_font("Arial", "", 11)
        self.multi_cell(0, 8, text)
        self.ln(5)

pdf = PDF()
pdf.add_page()

# --- Text summary ---
summary = (
    f"Total Sales: {total_sales:,}\n\n"
    f"Top Region: {sales_by_region.index[0]} ({sales_by_region.iloc[0]:,})\n"
    f"Top Product: {sales_by_product.index[0]} ({sales_by_product.iloc[0]:,})\n\n"
    "This report provides a breakdown of sales performance by region and product, "
    "highlighting the top performers and helping guide future business decisions."
)

pdf.chapter_title("Summary")
pdf.chapter_body(summary)

# --- Add charts ---
pdf.chapter_title("Sales by Region")
pdf.image("sales_by_region.png", w=150)
pdf.ln(10)

pdf.chapter_title("Sales by Product")
pdf.image("sales_by_product.png", w=150)

# --- Save final PDF ---
pdf.output("BrightMart_Sales_Report.pdf")

print("✅ PDF report created successfully: BrightMart_Sales_Report.pdf")
import os
print("CWD:", os.getcwd())
print("\nFiles here:")
for f in os.listdir():
    print("-", f)
# make_pdf_summary.py
from fpdf import FPDF
import pandas as pd
import matplotlib.pyplot as plt
import os
from datetime import datetime

# Paths (change if your project path is different)
PROJECT_DIR = r"D:\PythonProject"
CSV_PATH = os.path.join(PROJECT_DIR, "brightmart_sales.csv")
REPORTS_DIR = os.path.join(PROJECT_DIR, "reports")
LOGO_PATH = os.path.join(PROJECT_DIR, "logo.png")  # optional logo file

os.makedirs(REPORTS_DIR, exist_ok=True)

# Load data
df = pd.read_csv(CSV_PATH)

# Summaries
sales_by_region = df.groupby("Region")["Total_Sales"].sum().sort_values(ascending=False)
sales_by_product = df.groupby("Product")["Total_Sales"].sum().sort_values(ascending=False)
total_sales = df["Total_Sales"].sum()
top5_products = sales_by_product.head(5)

# Save charts to reports folder
region_img = os.path.join(REPORTS_DIR, "sales_by_region.png")
product_img = os.path.join(REPORTS_DIR, "sales_by_product.png")

plt.figure(figsize=(6, 4))
sales_by_region.plot(kind="bar", title="Total Sales by Region", rot=0)
plt.tight_layout()
plt.savefig(region_img)
plt.close()

plt.figure(figsize=(6, 4))
sales_by_product.plot(kind="bar", title="Total Sales by Product", rot=0)
plt.tight_layout()
plt.savefig(product_img)
plt.close()

# PDF builder
class PDF(FPDF):
    def header(self):
        # Optional logo on the left
        if os.path.exists(LOGO_PATH):
            self.image(LOGO_PATH, x=10, y=8, w=25)
            self.set_x(40)
        self.set_font("Arial", "B", 14)
        title = "BrightMart Sales Report (Q3 2024)"
        self.cell(0, 10, title, ln=True, align="C")
        # date on header
        self.set_font("Arial", "", 10)
        self.cell(0, 6, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}", ln=True, align="C")
        self.ln(6)

    def chapter_title(self, title):
        self.set_font("Arial", "B", 12)
        self.cell(0, 8, title, ln=True)
        self.ln(2)

    def chapter_body(self, text):
        self.set_font("Arial", "", 11)
        self.multi_cell(0, 7, text)
        self.ln(3)

pdf = PDF()
pdf.set_auto_page_break(auto=True, margin=15)
pdf.add_page()

# Summary text
summary = (
    f"Total Sales: {total_sales:,}\n\n"
    f"Top Region: {sales_by_region.index[0]} ({sales_by_region.iloc[0]:,})\n"
    f"Top Product: {sales_by_product.index[0]} ({sales_by_product.iloc[0]:,})\n\n"
    "This report provides a breakdown of sales performance by region and product, "
    "highlighting the top performers and helping guide future business decisions."
)

pdf.chapter_title("Summary")
pdf.chapter_body(summary)

# Insert region chart
pdf.chapter_title("Sales by Region")
# Fit image width to page minus margins (190 is safe for A4 with FPDF defaults)
pdf.image(region_img, w=170)
pdf.ln(6)

# Insert product chart
pdf.chapter_title("Sales by Product")
pdf.image(product_img, w=170)
pdf.ln(6)

# Top 5 products table
pdf.chapter_title("Top 5 Products by Sales")
pdf.set_font("Arial", "B", 11)
pdf.cell(90, 8, "Product", border=1)
pdf.cell(90, 8, "Total Sales", border=1, ln=True)
pdf.set_font("Arial", "", 11)
for prod, val in top5_products.items():
    pdf.cell(90, 8, str(prod), border=1)
    pdf.cell(90, 8, f"{val:,}", border=1, ln=True)

# Save PDF
output_pdf = os.path.join(REPORTS_DIR, f"BrightMart_Sales_Report_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf")
pdf.output(output_pdf)

print("✅ Report saved to:", output_pdf)
# make_pdf_summary.py (Windows paths)
from fpdf import FPDF
import pandas as pd
import matplotlib.pyplot as plt
import os
from datetime import datetime
import unicodedata

def sanitize(text):
    if not isinstance(text, str):
        return text
    text = unicodedata.normalize("NFKD", text)
    text = text.replace("—", "-").replace("–", "-").replace("…", "...")
    return text.encode("latin-1", errors="ignore").decode("latin-1")

PROJECT_DIR = r"D:\PythonProject"
CSV_PATH = os.path.join(PROJECT_DIR, "brightmart_sales.csv")
REPORTS_DIR = os.path.join(PROJECT_DIR, "reports")
LOGO_PATH = os.path.join(PROJECT_DIR, "logo.png")  # optional
os.makedirs(REPORTS_DIR, exist_ok=True)

df = pd.read_csv(CSV_PATH, parse_dates=["Date"])
# (rest of script identical to what I ran)
# ...
# Save PDF to:
# output_pdf = os.path.join(REPORTS_DIR, f"BrightMart_Professional_Report_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf")
# pdf.output(output_pdf)
