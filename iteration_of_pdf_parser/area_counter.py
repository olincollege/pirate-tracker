import pandas as pd

def most_common_area_keywords(df, keywords=None):
    """
    Count how often each keyword appears in the 'Area' column using only pandas.

    Args:
        df: A pandas DataFrame with an 'Area' column.
        keywords: A list of keywords to search for (case-insensitive).

    Returns:
        A pandas Series with keyword counts.
    """
    if keywords is None:
        keywords = [
            "straits of malacca",
            "indonesia",
            "philippines",
            "bangladesh",
            "vietnam",
            "south china sea",
            "india",
        ]

    df["Area"] = df["Area"].fillna("").astype(str).str.lower()

    counts = {}
    for kw in keywords:
        mask = df["Area"].str.contains(rf"\b{kw.lower()}\b", regex=True)
        counts[kw] = mask.sum()

    return pd.Series(counts).sort_values(ascending=False)

def test_area_keyword_counts(csv_path):
    """
    Load a CSV and print the most common area keywords.
    
    Args:
        csv_path: Path to the CSV file containing the 'Area' column.
    """
    df = pd.read_csv(csv_path)
    print("Most common area keywords:\n")
    print(most_common_area_keywords(df))


# test:
test_area_keyword_counts("lat_long_area_description.csv")
