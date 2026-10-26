import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from pathlib import Path
import plotly.express as px


# Project directories
BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "output"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Load clean data
df = pd.read_csv(BASE_DIR / 'ppr_clean.csv')

print("Data loaded:", df.shape)

# Create SQLite database
conn = sqlite3.connect(BASE_DIR / 'property.db')

# Load data into database
df.to_sql('sales', conn, if_exists='replace', index=False)

print("Database created successfully")
print("Total records loaded:", len(df))

# Calculate yearly average price
yearly = df.groupby('year')['price'].mean().reset_index()

# Create chart
fig, ax = plt.subplots(figsize=(12, 6))

ax.plot(
    yearly['year'],
    yearly['price'],
    color='#2E8B57',
    linewidth=2.5,
    marker='o',
    markersize=6
)

ax.fill_between(
    yearly['year'],
    yearly['price'],
    alpha=0.15,
    color='#2E8B57'
)

# Format prices as euros
ax.yaxis.set_major_formatter(
    mticker.FuncFormatter(lambda x, p: f'€{x:,.0f}')
)

ax.set_title(
    'Average Irish Property Price by Year',
    fontsize=16,
    fontweight='bold',
    pad=15
)

ax.set_xlabel('Year', fontsize=12)
ax.set_ylabel('Average Price (€)', fontsize=12)

plt.tight_layout()

# Save chart
output_file = OUTPUT_DIR / '01_price_trend.png'
plt.savefig(output_file, dpi=150, bbox_inches='tight')

plt.show()

print(f"Chart saved to: {output_file}")

county_avg = (df.groupby('county')['price']
              .mean()
              .sort_values(ascending=True)
              .tail(15)
              .reset_index())

fig, ax = plt.subplots(figsize=(12, 8))

bars = ax.barh(
    county_avg['county'],
    county_avg['price'],
    color='#2E8B57',
    alpha=0.85
)

ax.xaxis.set_major_formatter(
    mticker.FuncFormatter(lambda x, p: f'€{x:,.0f}')
)

ax.set_title(
    'Average Property Price by County (Top 15)',
    fontsize=16,
    fontweight='bold',
    pad=15
)

ax.set_xlabel('Average Price (€)', fontsize=12)

plt.tight_layout()

# Save using the project output directory
plt.savefig(
    OUTPUT_DIR / '02_price_by_county.png',
    dpi=150,
    bbox_inches='tight'
)

plt.show()

print("County price chart saved")

dublin = df[df['county'] == 'Dublin'].groupby('year')['price'].mean()
rest = df[df['county'] != 'Dublin'].groupby('year')['price'].mean()

fig, ax = plt.subplots(figsize=(12, 6))

ax.plot(
    dublin.index,
    dublin.values,
    color='#1a5276',
    linewidth=2.5,
    marker='o',
    label='Dublin',
    markersize=6
)

ax.plot(
    rest.index,
    rest.values,
    color='#2E8B57',
    linewidth=2.5,
    marker='s',
    label='Rest of Ireland',
    markersize=6
)

ax.yaxis.set_major_formatter(
    mticker.FuncFormatter(lambda x, p: f'€{x:,.0f}')
)

ax.set_title(
    'Dublin vs Rest of Ireland — Average Price Over Time',
    fontsize=16,
    fontweight='bold',
    pad=15
)

ax.set_xlabel('Year', fontsize=12)
ax.set_ylabel('Average Price (€)', fontsize=12)
ax.legend(fontsize=12)

plt.tight_layout()

# Save chart
plt.savefig(
    OUTPUT_DIR / '03_dublin_vs_rest.png',
    dpi=150,
    bbox_inches='tight'
)

plt.show()

print("Dublin vs Rest chart saved")

month_order = [
    'January', 'February', 'March', 'April',
    'May', 'June', 'July', 'August',
    'September', 'October', 'November', 'December'
]

monthly = (
    df.groupby('month_name')['price']
      .count()
      .reindex(month_order)
      .reset_index()
)

monthly.columns = ['month', 'sales']

fig, ax = plt.subplots(figsize=(12, 6))

ax.bar(
    monthly['month'],
    monthly['sales'],
    color='#2E8B57',
    alpha=0.85
)

ax.set_title(
    'Property Sales Volume by Month',
    fontsize=16,
    fontweight='bold',
    pad=15
)

ax.set_xlabel('Month', fontsize=12)
ax.set_ylabel('Number of Sales', fontsize=12)

plt.xticks(rotation=45)

plt.tight_layout()

# Save chart
plt.savefig(
    OUTPUT_DIR / '04_sales_by_month.png',
    dpi=150,
    bbox_inches='tight'
)

plt.show()

print("Monthly sales chart saved")

yearly_plotly = df.groupby('year')['price'].mean().reset_index()
yearly_plotly.columns = ['Year', 'Average Price']

fig = px.line(
    yearly_plotly,
    x='Year',
    y='Average Price',
    title='Irish Property Price Trend (Interactive)',
    template='plotly_dark',
    color_discrete_sequence=['#2E8B57']
)

fig.update_traces(
    mode='lines+markers',
    line_width=2.5
)

fig.update_layout(
    yaxis_tickformat='€,.0f',
    title_font_size=18
)

# Save interactive HTML chart
fig.write_html(OUTPUT_DIR / 'interactive_chart.html')

fig.show()

print("Interactive chart saved as HTML")