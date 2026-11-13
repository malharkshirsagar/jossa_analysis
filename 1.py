import pandas as pd
from functools import reduce
import glob


def build_master_cutoff_csv():
    # 1. Define the 5 static columns (your composite key)
    static_cols = ["Institute", "Academic Program Name", "Quota", "Seat Type", "Gender"]

    # Grab all 5 round CSVs (assuming they are named round_1.csv, round_2.csv, etc.)
    # Make sure they are sorted so R1 is first, R5 is last
    csv_files = sorted(glob.glob("2026_round_*.csv"))

    if not csv_files:
        print("No round CSV files found in the current directory.")
        return

    print(f"Found {len(csv_files)} files. Starting the merge process...")

    dataframes = []

    # 2. Load each round and rename its dynamic columns
    for i, file_path in enumerate(csv_files, start=1):
        df = pd.read_csv(file_path)

        # Rename Opening Rank and Closing Rank to include the specific Round number
        df = df.rename(
            columns={
                "Opening Rank": f"R{i}_Opening Rank",
                "Closing Rank": f"R{i}_Closing Rank",
            }
        )

        # Keep only the static columns and the newly renamed dynamic columns for this round
        cols_to_keep = static_cols + [f"R{i}_Opening Rank", f"R{i}_Closing Rank"]
        df = df[cols_to_keep]

        dataframes.append(df)
        print(f"Processed {file_path} as Round {i} (Rows: {len(df)})")

    # 3. Combine them all using a Full Outer Join
    # The reduce function applies the merge continuously: (R1 + R2) -> + R3 -> + R4 -> + R5
    master_df = reduce(
        lambda left, right: pd.merge(left, right, on=static_cols, how="outer"),
        dataframes,
    )

    # 4. Handle missing data for rows that didn't exist in certain rounds
    master_df = master_df.fillna("N/A")

    # 5. Export to a final master CSV
    output_filename = "josaa_2026_master_wide.csv"
    master_df.to_csv(output_filename, index=False)

    print(f"\nSuccess! Master CSV created: {output_filename}")
    print(f"Total Unique Records across all rounds: {len(master_df)}")


if __name__ == "__main__":
    build_master_cutoff_csv()
