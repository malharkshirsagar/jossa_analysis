# JoSAA 2026 Data Pipeline & Automated PDF Report Generator

An automated data engineering pipeline built in Python to process, structure, and generate professional analytical PDF reports from multi-round JoSAA counseling datasets (13,000+ records).

# Features
- **ETL & Data Cleaning:** Restructures raw counseling records into a wide relational format tracking round-wise (R1–R5) opening and closing ranks.
- **Automated PDF Generation:** Uses `ReportLab` to programmatically build landscape A3 reports with custom canvas page numbering and professional styling.
- **Custom Metrics:** Ingests and preserves preparatory course (`P`) rank designations and institutional quotas.

#Tech Stack
- Python (Pandas, NumPy, ReportLab)