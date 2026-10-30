# Netflix Data Cleaning & Preparation

Prepare and organize the Netflix dataset for business analytics and reporting.

## About

This project takes a raw Netflix catalog dataset and cleans it up so it's actually usable for analysis. The original data has issues like missing directors, inconsistent country names, messy ratings, and dates stored as plain text — all of which get fixed here.

## Dataset

The dataset contains **8,790 records** of Netflix titles (Movies and TV Shows) with details like title, director, country, release year, rating, duration, and genre.

**Source:** [Netflix Movies and TV Shows Dataset](https://www.kaggle.com/datasets/shivamb/netflix-shows) (Kaggle)

## What the Script Does

| Step | Task | Details |
|------|------|---------|
| 1 | **Import Data** | Load `Dataset.csv` using Pandas and inspect its structure |
| 2 | **Handle Missing Values** | Replace "Not Given" entries with proper labels, fill blanks in director/country/rating, drop rows without dates |
| 3 | **Remove Duplicates & Fix Formatting** | Drop duplicate `show_id` records, strip whitespace, clean double spaces in titles |
| 4 | **Standardize Columns** | Normalize type (Movie/TV Show), country names (US→United States), ratings (NR→NOT RATED), parse dates, split duration into value + unit |
| 5 | **Export Cleaned Data** | Save the final dataset as `Netflix_Cleaned.csv` |

## Files

```
├── Dataset.csv                  # Raw Netflix dataset
├── netflix_data_cleaning.py     # Main cleaning script
├── Netflix_Cleaned.csv          # Cleaned output (ready for analysis)
└── README.md
```

## New Columns Added

The cleaning process adds these derived columns for easier analysis:

- **primary_country** — First country from multi-country entries
- **year_added** — Year the title was added to Netflix
- **month_added** — Month the title was added
- **duration_value** — Numeric part of duration (e.g., 90 from "90 min")
- **duration_unit** — Unit of duration (minutes / seasons)

## How to Run

```bash
# make sure you have pandas installed
pip install pandas

# run the script
python netflix_data_cleaning.py
```

The script will print a step-by-step summary to the console and save the cleaned file as `Netflix_Cleaned.csv` in the same folder.

## Tech Stack

- Python 3.x
- Pandas

## Skills Demonstrated

- Data Import & Inspection
- Missing Value Detection and Handling
- Duplicate Removal
- String Cleaning & Standardization
- Date Parsing & Feature Extraction
- Data Export
