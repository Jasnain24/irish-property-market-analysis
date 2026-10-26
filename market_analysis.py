import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import sqlite3
import warnings
warnings.filterwarnings('ignore')

print("Libraries loaded successfully")

# Load raw data
df = pd.read_csv('/Users/jasnainkaur/Projects/Irish Property Market Analysis/market_irish_dataset.csv', encoding='latin-1')

# Check what we have
print("Shape:", df.shape)
print("\nColumns:", df.columns.tolist())
print("\nFirst few rows:")
df.head()

df.columns = [
    'date', 'address', 'county',
    'eircode', 'price', 'not_full_price',
    'vat_exclusive', 'description', 'property_size'
]

print("Columns renamed successfully")
print(df.columns.tolist())

# First, let's see exactly what the price column looks like
print("Sample raw prices:")
print(df['price'].head(20).tolist())

print("\nUnique non-numeric characters found:")
import re
# Extract any character that is not a digit, dot, comma or euro sign
weird_chars = set()
for val in df['price'].dropna():
    chars = re.findall(r'[^\d,\.€]', str(val))
    weird_chars.update(chars)
print(weird_chars)

df['price'] = (df['price']
               .str.replace('\x80', '', regex=False)
               .str.replace(',', '', regex=False)
               .str.strip()
               .astype(float))

print("Price cleaning successful")
print("Price range: €{:,.0f} to €{:,.0f}".format(
    df['price'].min(), df['price'].max()))

df['date'] = pd.to_datetime(df['date'], dayfirst=True)
df['year'] = df['date'].dt.year
df['month'] = df['date'].dt.month
df['month_name'] = df['date'].dt.strftime('%B')

print("Date range:", df['date'].min(), "to", df['date'].max())

# Remove unrealistic prices
df = df[df['price'] > 10000]
df = df[df['price'] < 5000000]

# Remove nulls in key columns
df = df.dropna(subset=['county', 'price', 'date'])

# Clean county names — trim whitespace
df['county'] = df['county'].str.strip()

print("Clean dataset shape:", df.shape)
print("\nCounties:", df['county'].nunique())
print("\nYear range:", df['year'].min(), "to", df['year'].max())

print("Missing values:")
print(df.isnull().sum())

# Drop columns we don't need and that have too many nulls
df = df.drop(columns=['eircode', 'property_size'])

# Confirm no missing values in columns we actually use
key_columns = ['date', 'address', 'county', 'price', 
               'description', 'year', 'month', 'month_name']
print("Missing values in key columns:")
print(df[key_columns].isnull().sum())

print("\nFinal dataset shape:", df.shape)
print("Ready to save")

df.to_csv('/Users/jasnainkaur/Projects/Irish Property Market Analysis/ppr_clean.csv', index=False)
print("Clean data saved successfully")
print("Total records:", len(df))