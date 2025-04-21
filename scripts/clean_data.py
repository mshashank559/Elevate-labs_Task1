import pandas as pd
from pathlib import Path

# File paths
RAW_DATA_PATH = Path("data/raw/netflix_titles.csv")
PROCESSED_DATA_PATH = Path("data/processed/netflix_titles_cleaned.csv")

def load_data(path):
    print("🔹 Loading raw dataset...")
    return pd.read_csv(path)

def clean_data(df):
    print("🔹 Starting data cleaning...")

    # Standardize column names
    df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]

    # Remove duplicates
    before = len(df)
    df = df.drop_duplicates()
    after = len(df)
    print(f"✔️ Removed {before - after} duplicate rows.")

    # Fill missing values
    df['director'].fillna('Unknown', inplace=True)
    df['cast'].fillna('Not Available', inplace=True)
    df['country'].fillna('Unknown', inplace=True)
    df['rating'].fillna('Not Rated', inplace=True)
    df['date_added'] = pd.to_datetime(df['date_added'], errors='coerce')

    # Drop rows with missing essential values
    df.dropna(subset=['title', 'type'], inplace=True)

    # Standardize values
    df['type'] = df['type'].str.title()
    df['rating'] = df['rating'].str.upper()

    return df

def save_data(df, path):
    print("🔹 Saving cleaned data...")
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)
    print(f"✅ Saved cleaned data to {path}")

def main():
    df = load_data(RAW_DATA_PATH)
    cleaned_df = clean_data(df)
    save_data(cleaned_df, PROCESSED_DATA_PATH)

if __name__ == "__main__":
    main()
