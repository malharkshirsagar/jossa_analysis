# JoSAA 2026 Data Pipeline & Automated PDF Report Generator

An end-to-end data engineering pipeline built in Python to process, structure, cross-verify, and generate professional analytical PDF reports from multi-round JoSAA counseling datasets (**13,000+ records**).

---

##  Key Features

* **Robust ETL & Data Cleaning:** Restructures raw counseling records from multiple rounds into a clean wide relational format tracking round-wise (`R1`–`R5`) opening and closing ranks.
* **Automated Cross-Verification:** Programmatically audits master datasets against original source round files to ensure **100% data integrity** and zero discrepancy.
* **Advanced Analytical Metrics:** Calculates custom indicators such as cutoff expansions, seat stability trends, rounding/freezing points, and selectivity tier buckets.
* **Automated PDF & Excel Reporting:** Uses `ReportLab` to programmatically build publication-ready landscape A3 reports complete with custom canvas layouts, alongside multi-format exports (`.csv` and `.xlsx`).
* **Edge-Case Handling:** Preserves preparatory course (`P`) rank designations and handles missing round allocations gracefully.

---

##  Tech Stack & Prerequisites

* **Python 3.8+**
* `pandas` (for high-performance tabular transformations and joins)
* `numpy` (for vectorized conditional logic and analytics)
* `openpyxl` (for structured Excel workbook generation)
* `reportlab` (for automated programmatic PDF report layouts)

---

## 📦 Installation

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/malharkshirsagar/josaa-2026-pipeline.git](https://github.com/malharkshirsagar/josaa-2026-pipeline.git)
   cd josaa-2026-pipeline

2. Install the required dependencies:

    ```Bash
     pip install -r requirements.txt
---
##   Usage Workflow

Place your round-wise raw CSV files (e.g., 2026_round_1.csv through 2026_round_5.csv) in the project root directory.

Step 1: Build the Wide Master Dataset (Merges multi-round data using full outer joins):

Bash
python master_wide.py
Step 2: Cross-Verify Data Integrity (Audits records against raw round files):

Bash
python cross_ver.py
Step 3: Generate Analytical Metrics & Reports (Computes expansions, stability trends, and tiers):

Bash
python 3.py
---
##   Output Structure
The pipeline generates clean, production-ready assets:

josaa_2026_master_wide.csv: Relational wide-format multi-round merge.

josaa_2026_analytical_master.csv / .xlsx: Fully enriched analytical dataset containing expansion metrics and selectivity tiers.

JoSAA_2026_Master_Wide_Report.pdf: Programmatically compiled professional landscape PDF report.

