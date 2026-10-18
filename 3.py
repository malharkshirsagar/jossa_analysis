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

    print("📊 Stripping hidden spaces and calculating the 5 Analytical Columns...")

    # Define the dynamic rank column names
    rank_cols = [
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

    # 1. Normalize all string fields to ensure exact cell equality comparisons
    for col in rank_cols:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()

    # Helper function to convert rank columns safely to numbers for math
    def get_numeric_ranks(col_name):
        return pd.to_numeric(df[col_name].str.replace("P", ""), errors="coerce")

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
    df["Seat_Stability_Trend"] = np.select(conditions, choices, default="N/A")

    # --- Column 4: Round_When_Frozen (Replaces Active_Rounds_Count) ---
    r1_c = df["R1_Closing Rank"]
    r2_c = df["R2_Closing Rank"]
    r3_c = df["R3_Closing Rank"]
    r4_c = df["R4_Closing Rank"]
    r5_c = df["R5_Closing Rank"]

    frozen_conditions = [
        (r1_c == r2_c)
        & (r2_c == r3_c)
        & (r3_c == r4_c)
        & (r4_c == r5_c)
        & (r1_c != "N/A"),
        (r2_c == r3_c) & (r3_c == r4_c) & (r4_c == r5_c) & (r2_c != "N/A"),
        (r3_c == r4_c) & (r4_c == r5_c) & (r3_c != "N/A"),
        (r4_c == r5_c) & (r4_c != "N/A"),
        (r5_c != "N/A"),
    ]
    frozen_choices = [
        "Froze in Round 1",
        "Froze in Round 2",
        "Froze in Round 3",
        "Froze in Round 4",
        "Moved through Round 5",
    ]
    df["Round_When_Frozen"] = np.select(
        frozen_conditions, frozen_choices, default="N/A"
    )

    # --- Column 5: Selectivity_Tier ---
    bins = [0, 5000, 20000, 50000, np.inf]
    labels = [
        "Ultra-Elite (<5k)",
        "Elite (5k-20k)",
        "Mid-Tier (20k-50k)",
        "Accessible (>50k)",
    ]
    df["Selectivity_Tier"] = pd.cut(r1_cr, bins=bins, labels=labels)
    df["Selectivity_Tier"] = df["Selectivity_Tier"].astype(str).replace("nan", "N/A")

    # Clean up NaNs for clean UI rendering
    df["CR_Expansion_R1_R5"] = df["CR_Expansion_R1_R5"].fillna("N/A")
    df["OR_Expansion_R1_R5"] = df["OR_Expansion_R1_R5"].fillna("N/A")

    # Reorder columns to form the final 20-column master format
    static_cols = ["Institute", "Academic Program Name", "Quota", "Seat Type", "Gender"]
    analytics_cols = [
        "CR_Expansion_R1_R5",
        "OR_Expansion_R1_R5",
        "Seat_Stability_Trend",
        "Round_When_Frozen",
        "Selectivity_Tier",
    ]

    df = df[static_cols + rank_cols + analytics_cols]

    # --- File Exports ---
    print("\n💾 Saving output files...")

    df.to_csv(output_csv, index=False)
    print(f"✅ CSV saved: {output_csv}")

    try:
        with pd.ExcelWriter(output_excel, engine="openpyxl") as writer:
            df.to_excel(writer, sheet_name="2026 Cutoffs Analytics", index=False)
        print(f"✅ Excel saved: {output_excel}")
    except Exception as e:
        print(
            f"⚠️ Excel export failed. Ensure openpyxl is installed (`pip install openpyxl`). Error: {e}"
        )

    print("\n🎉 Complete! Final 20-column master dataset successfully generated.")


if __name__ == "__main__":
    generate_analytical_dataset()
