import pandas as pd
import glob
import os


def cross_check_your_logic():
    master_filename = "josaa_2026_master_wide.csv"

    if not os.path.exists(master_filename):
        print(f"❌ Cannot find {master_filename}.")
        return

    # 1. Load Master CSV
    master_df = pd.read_csv(master_filename)

    # 5 Static Columns (Primary Key)
    static_cols = ["Institute", "Academic Program Name", "Quota", "Seat Type", "Gender"]

    # Clean the master static keys (remove extra spaces for perfect matching)
    for col in static_cols:
        master_df[col] = master_df[col].astype(str).str.strip()

    print("🔍 Starting validation using your logic...\n")
    all_passed = True

    # 2. Loop through Rounds 1 to 5
    for i in range(1, 6):
        # Handle potential filename variations (2026_round_1.csv or round_1.csv)
        round_filename = f"2026_round_{i}.csv"
        if not os.path.exists(round_filename):
            round_filename = f"round_{i}.csv"
            if not os.path.exists(round_filename):
                print(f"⚠️ Could not find CSV for Round {i}. Skipping.")
                continue

        # Load the original round CSV
        original_df = pd.read_csv(round_filename)

        # Clean strings to prevent false mismatches due to hidden spaces
        for col in static_cols + ["Opening Rank", "Closing Rank"]:
            if col in original_df.columns:
                original_df[col] = original_df[col].astype(str).str.strip()

        # We also need to clean the specific Master columns for this round to compare them
        r_or = f"R{i}_Opening Rank"
        r_cr = f"R{i}_Closing Rank"
        master_df[r_or] = master_df[r_or].astype(str).str.strip()
        master_df[r_cr] = master_df[r_cr].astype(str).str.strip()

        # 3. Join Original against Master using the 5 Static Columns
        test_df = pd.merge(
            original_df,
            master_df[
                static_cols + [r_or, r_cr]
            ],  # Bring only the required master columns
            on=static_cols,
            how="left",
        )

        # 4. Check if the original ranks match the master ranks
        or_match = test_df["Opening Rank"] == test_df[r_or]
        cr_match = test_df["Closing Rank"] == test_df[r_cr]

        total_records = len(original_df)
        successful_matches = (or_match & cr_match).sum()

        if successful_matches == total_records:
            print(
                f"✅ Round {i} ({round_filename}): ALL {total_records} rows match perfectly!"
            )
        else:
            mismatches = total_records - successful_matches
            print(
                f"❌ Round {i} ({round_filename}): {mismatches} mismatches found out of {total_records} rows."
            )
            all_passed = False

            # Print the first few mismatched rows so you can see exactly what went wrong
            print("\n   --- First 5 Mismatched Rows ---")
            failed_rows = test_df[~(or_match & cr_match)]
            print(
                failed_rows[
                    static_cols + ["Opening Rank", r_or, "Closing Rank", r_cr]
                ].head()
            )
            print("   -------------------------------\n")

    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 SUCCESS! Master CSV is 100% accurate based on your logic.")
    else:
        print("⚠️ WARNING: Mismatches detected. See details above.")


if __name__ == "__main__":
    cross_check_your_logic()
