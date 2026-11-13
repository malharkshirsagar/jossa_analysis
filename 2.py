import pandas as pd
import numpy as np


def generate_analytical_dataset():
    input_file = "josaa_2026_master_wide.csv"
    output_csv = "josaa_2026_analytical_master.csv"
    output_excel = "josaa_2026_analytical_master.xlsx"

    try:
        df = pd.read_csv(input_file)
        print(f"✅ Successfully loaded {input_file} ({len(df)} rows).")
    except FileNotFoundError:
        print(f"❌ Error: {input_file} not found. Please check the file name.")
        return

    print("📊 Calculating the 5 Analytical Columns...")

    # Helper function to convert rank columns safely to numbers for math
    # Coerces 'N/A' and Prep ranks ('P') to NaN temporarily for clean calculations
    def get_numeric_ranks(col_name):
        return pd.to_numeric(
            df[col_name].astype(str).str.replace("P", ""), errors="coerce"
        )

    r1_or = get_numeric_ranks("R1_Opening Rank")
    r1_cr = get_numeric_ranks("R1_Closing Rank")
    r5_or = get_numeric_ranks("R5_Opening Rank")
    r5_cr = get_numeric_ranks("R5_Closing Rank")

    # --- Column 1: CR_Expansion_R1_R5 ---
    df["CR_Expansion_R1_R5"] = r5_cr - r1_cr

    # --- Column 2: OR_Expansion_R1_R5 ---
    df["OR_Expansion_R1_R5"] = r5_or - r1_or

    # --- Column 3: Seat_Stability_Trend ---
    conditions = [
        (df["CR_Expansion_R1_R5"] == 0),
        (df["CR_Expansion_R1_R5"] > 0),
        (df["CR_Expansion_R1_R5"] < 0),
    ]
    choices = [
        "Frozen / Stable",
        "Expanding (Cutoff Dropped)",
        "Contracting (Cutoff Rose)",
    ]
    # If a seat doesn't have data in R1 or R5, mark as N/A
    df["Seat_Stability_Trend"] = np.select(conditions, choices, default="N/A")

    # --- Column 4: Active_Rounds_Count ---
    # Count how many rounds actually have a Closing Rank (not equal to "N/A")
    round_cols = [
        "R1_Closing Rank",
        "R2_Closing Rank",
        "R3_Closing Rank",
        "R4_Closing Rank",
        "R5_Closing Rank",
    ]
    df["Active_Rounds_Count"] = df[round_cols].apply(
        lambda row: (row != "N/A").sum(), axis=1
    )

    # --- Column 5: Selectivity_Tier ---
    # Define tier buckets based on Round 1 Closing Rank
    bins = [0, 5000, 20000, 50000, np.inf]
    labels = [
        "Ultra-Elite (<5k)",
        "Elite (5k-20k)",
        "Mid-Tier (20k-50k)",
        "Accessible (>50k)",
    ]
    df["Selectivity_Tier"] = pd.cut(r1_cr, bins=bins, labels=labels)
    # Convert empty tier values to "N/A" (happens if R1 was missing)
    df["Selectivity_Tier"] = df["Selectivity_Tier"].astype(str).replace("nan", "N/A")

    # Clean up Expansions for presentation (Fill NaNs with "N/A")
    df["CR_Expansion_R1_R5"] = df["CR_Expansion_R1_R5"].fillna("N/A")
    df["OR_Expansion_R1_R5"] = df["OR_Expansion_R1_R5"].fillna("N/A")

    # Reorder columns to ensure the 5 analytics columns are at the very end
    static_cols = ["Institute", "Academic Program Name", "Quota", "Seat Type", "Gender"]
    dynamic_cols = [
        "R1_Opening Rank",
        "R1_Closing Rank",
        "R2_Opening Rank",
        "R2_Closing Rank",
        "R3_Opening Rank",
        "R3_Closing Rank",
        "R4_Opening Rank",
        "R4_Closing Rank",
        "R5_Opening Rank",
        "R5_Closing Rank",
    ]
    analytics_cols = [
        "CR_Expansion_R1_R5",
        "OR_Expansion_R1_R5",
        "Seat_Stability_Trend",
        "Active_Rounds_Count",
        "Selectivity_Tier",
    ]

    # Apply final column order
    df = df[static_cols + dynamic_cols + analytics_cols]

    # --- Export Files ---
    print("\n💾 Saving files...")

    # 1. Save CSV
    df.to_csv(output_csv, index=False)
    print(f"✅ CSV saved: {output_csv} (Ready for Streamlit/DuckDB)")

    # 2. Save Excel (Ideal for PDF conversion)
    try:
        with pd.ExcelWriter(output_excel, engine="openpyxl") as writer:
            df.to_excel(writer, sheet_name="2026 Cutoffs Analytics", index=False)
        print(f"✅ Excel saved: {output_excel} (Open this in Excel to export as PDF)")
    except Exception as e:
        print(
            f"⚠️ Could not save Excel file. Ensure 'openpyxl' is installed (pip install openpyxl). Error: {e}"
        )

    print("\n🎉 Done! Your 20-column Master Analytical Dataset is ready.")


if __name__ == "__main__":
    generate_analytical_dataset()
