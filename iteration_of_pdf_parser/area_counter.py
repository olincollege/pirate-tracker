import pandas as pd


def most_common_area_keywords(df, keywords=None):
    """
    Count how often each keyword appears in the 'Area Location' column using only pandas.

    Args:
        df: A pandas DataFrame with an 'Area Location' column.
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
            "malaysia",
        ]

    # Use the correct column name: 'Area Location'
    df["Area Location"] = df["Area Location"].fillna("").astype(str).str.lower()

    counts = {}
    for kw in keywords:
        mask = df["Area Location"].str.contains(
            rf"\b{kw.lower()}\b", regex=True
        )
        counts[kw] = mask.sum()

    return pd.Series(counts).sort_values(ascending=False)


def test_area_keyword_counts(csv_path):
    """
    Load a CSV and print the most common area keywords.

    Args:
        csv_path: Path to the CSV file containing the 'Area Location' column.
    """
    df = pd.read_csv(csv_path)
    print("Most common area keywords:\n")
    print(most_common_area_keywords(df))


# test:
test_area_keyword_counts("pirate_locations.csv")
