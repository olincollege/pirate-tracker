import camelot
import os
import pandas as pd

def parse_and_combine_pdf_tables(pdf_path, pages="1", flavor="stream", output_csv="combined_tables_cleaned.csv"):
    tables = camelot.read_pdf(pdf_path, pages=pages, flavor=flavor)
    print(f" Total tables found: {tables.n}")

    combined_df = pd.concat([table.df for table in tables], ignore_index=True)

    combined_df = combined_df.applymap(lambda x: x.strip() if isinstance(x, str) else x)

    combined_df.to_csv(output_csv, index=False)
    print(f"💾 Cleaned combined table saved to: {output_csv}")

    return combined_df

combined_table = parse_and_combine_pdf_tables("/Users/hongyizhang/Downloads/Pirate_Incidents_2024.pdf", pages="1")
