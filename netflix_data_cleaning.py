# Netflix Data Cleaning & Preparation
# -----------------------------------
# This script takes the raw Netflix dataset and cleans it up
# so it's ready for proper analysis and reporting.

import pandas as pd
import os

# ============================================================
# STEP 1 : Load the dataset
# ============================================================

file_path = "Dataset.csv"
df = pd.read_csv(file_path)

print("--- Raw Dataset Overview ---")
print(f"Total rows    : {df.shape[0]}")
print(f"Total columns : {df.shape[1]}")
print(f"\nColumn names  : {list(df.columns)}")
print(f"\nFirst 5 rows :")
print(df.head())

# quick look at data types
print("\n--- Data Types ---")
print(df.dtypes)

# ============================================================
# STEP 2 : Check and handle missing values
# ============================================================

print("\n\n--- Missing Values (before cleaning) ---")
missing = df.isnull().sum()
missing_pct = (missing / len(df) * 100).round(2)
missing_info = pd.DataFrame({"Missing Count": missing, "Percentage": missing_pct})
print(missing_info[missing_info["Missing Count"] > 0])

# director – lots of entries have "Not Given" or are blank.
# We'll treat "Not Given" as missing too, then fill blanks with "Unknown".
df["director"] = df["director"].replace("Not Given", pd.NA)
df["director"] = df["director"].fillna("Unknown")

# country – same deal, "Not Given" should be treated as unknown
df["country"] = df["country"].replace("Not Given", pd.NA)
df["country"] = df["country"].fillna("Unknown")

# date_added – a few entries might not have a date. Drop those rows
# because we can't really guess when something was added.
before = len(df)
df = df.dropna(subset=["date_added"])
after = len(df)
print(f"\nDropped {before - after} rows where 'date_added' was missing.")

# rating – fill missing ratings with "Not Rated"
df["rating"] = df["rating"].fillna("Not Rated")

# duration – fill any remaining blanks with "Unknown"
df["duration"] = df["duration"].fillna("Unknown")

# listed_in (genres) – fill blanks
df["listed_in"] = df["listed_in"].fillna("Uncategorized")

print("\n--- Missing Values (after cleaning) ---")
print(df.isnull().sum())

# ============================================================
# STEP 3 : Remove duplicates & fix formatting issues
# ============================================================

# check for duplicate show_id entries
dup_count = df.duplicated(subset=["show_id"]).sum()
print(f"\n\nDuplicate show_id entries found : {dup_count}")
df = df.drop_duplicates(subset=["show_id"], keep="first")
print(f"Rows after removing duplicates  : {len(df)}")

# also check full-row duplicates just in case
full_dup = df.duplicated().sum()
if full_dup > 0:
    df = df.drop_duplicates(keep="first")
    print(f"Removed {full_dup} fully duplicated rows as well.")

# strip extra whitespace from all string columns
str_cols = df.select_dtypes(include=["object", "string"]).columns
for col in str_cols:
    df[col] = df[col].str.strip()

# title sometimes has weird double spaces inside – clean that up
df["title"] = df["title"].str.replace(r"\s+", " ", regex=True)

# ============================================================
# STEP 4 : Standardize key columns
# ============================================================

# --- Type column ---
# Make sure it's consistently "Movie" or "TV Show"
df["type"] = df["type"].str.strip().str.title()
# .title() turns "TV Show" into "Tv Show" – fix that
df["type"] = df["type"].replace({"Tv Show": "TV Show"})
print(f"\nUnique values in 'type' : {df['type'].unique()}")

# --- Country column ---
# Some rows list multiple countries like "United States, India"
# We'll keep the first country as the primary one in a new column
df["primary_country"] = df["country"].apply(
    lambda x: x.split(",")[0].strip() if x != "Unknown" else "Unknown"
)

# fix common inconsistencies in country names
country_fixes = {
    "United States": "United States",
    "US": "United States",
    "USA": "United States",
    "UK": "United Kingdom",
    "West Germany": "Germany",
    "East Germany": "Germany",
    "Soviet Union": "Russia",
}
df["primary_country"] = df["primary_country"].replace(country_fixes)
print(f"Top 10 countries :\n{df['primary_country'].value_counts().head(10)}")

# --- Rating column ---
# standardize rating labels – some might have trailing spaces or odd casing
df["rating"] = df["rating"].str.strip().str.upper()

# map any weird/old rating labels to standard ones
rating_fixes = {
    "TV-Y7-FV": "TV-Y7",   # they're basically the same thing
    "UR": "NOT RATED",
    "NR": "NOT RATED",
}
df["rating"] = df["rating"].replace(rating_fixes)
print(f"\nUnique ratings : {sorted(df['rating'].unique())}")

# --- date_added column ---
# convert to proper datetime so it's easier to work with later
df["date_added"] = df["date_added"].str.strip()
df["date_added"] = pd.to_datetime(df["date_added"], format="mixed", dayfirst=False)

# pull out year and month for easier grouping in reports
df["year_added"] = df["date_added"].dt.year.astype("Int64")
df["month_added"] = df["date_added"].dt.month.astype("Int64")

# --- Duration column ---
# movies show "90 min", shows say "2 Seasons" – split into number + unit
df["duration_value"] = df["duration"].str.extract(r"(\d+)").astype(float)
df["duration_unit"] = df["duration"].str.extract(r"([A-Za-z]+)")
# clean up the unit names
df["duration_unit"] = df["duration_unit"].str.strip().str.lower()
df["duration_unit"] = df["duration_unit"].replace({
    "season": "seasons",
    "min": "minutes",
})

print("\n--- Sample of cleaned data ---")
print(df[["title", "type", "primary_country", "rating", "date_added",
          "duration_value", "duration_unit"]].head(10))

# ============================================================
# STEP 5 : Export the cleaned dataset
# ============================================================

output_file = "Netflix_Cleaned.csv"
df.to_csv(output_file, index=False)
print(f"\n\nCleaned dataset saved to '{output_file}'")
print(f"Final shape : {df.shape[0]} rows x {df.shape[1]} columns")

# quick summary of what we did
print("\n" + "=" * 55)
print("  CLEANING SUMMARY")
print("=" * 55)
print(f"  Original columns     : show_id, type, title, director,")
print(f"                         country, date_added, release_year,")
print(f"                         rating, duration, listed_in")
print(f"  New columns added    : primary_country, year_added,")
print(f"                         month_added, duration_value,")
print(f"                         duration_unit")
print(f"  Missing values       : handled (filled / dropped)")
print(f"  Duplicates removed   : yes")
print(f"  Columns standardized : type, country, rating, date_added")
print(f"  Output file          : {output_file}")
print("=" * 55)
