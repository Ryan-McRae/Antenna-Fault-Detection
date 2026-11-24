# Antenna Fault Detection via Machine Learning & PostgreSQL

An end-to-end machine learning pipeline for detecting and classifying physical faults in antenna systems from their electromagnetic signatures. Built as a practical upskilling project combining **PostgreSQL-driven data engineering** with **Python machine learning**.

---

## Overview

Traditional antenna maintenance relies on slow, manual physical inspections. Using the **[Antenna Fault Detection Dataset](https://www.kaggle.com/datasets/amineipad/antenna-fault-detection-dataset)** from Kaggle, this project maps electromagnetic measurements (such as return loss, impedance, VSWR, gain, and efficiency) directly to underlying physical degradation states—including broken elements, bad connections, bending, length variations, and environmental humidity effects.

### Key Architectural Highlights
* **Database-First Data Engineering:** Rather than handling all preprocessing in memory with Pandas, data ingestion, cleaning, and deterministic train/validation/test splitting are executed directly inside **PostgreSQL**.
* **Modular Python Pipeline:** Clean separation between database/preprocessing utilities, model training/evaluation logic, and a single reproducible entry point (`main.py`).

---

## Project Structure

```text
├── data/
│   ├── raw/            # Original Kaggle dataset files (unmodified)
│   └── results/        # Generated evaluation plots, figures, and project write-up
├── src/
│   ├── models/         # Machine learning model definitions, training, and evaluation
│   └── utils/          # PostgreSQL connection helpers, SQL queries, and data utilities
├── main.py             # Main entry point to execute the pipeline
└── README.md
```

---

## Prerequisites

* **Python 3.10+**
* **PostgreSQL** (local instance or containerized database)
* **Kaggle Dataset:** Download the *Antenna Fault Detection Dataset* from Kaggle and place the raw file(s) inside `data/raw/`.

### Python Dependencies
Install the required packages (update or replace with `requirements.txt` / `pyproject.toml` if configured):

```bash
pip install pandas numpy scikit-learn matplotlib seaborn psycopg2-binary sqlalchemy python-dotenv
```

---

## Setup & Usage

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd <your-repo-directory>
   ```

2. **Add the raw dataset**
   Place the downloaded Kaggle CSV file(s) into `data/raw/`.

3. **Configure PostgreSQL**
   Ensure your PostgreSQL server is running and configure your connection credentials (e.g., via environment variables or a `.env` file used by `src/utils/`):
   ```env
   DB_HOST=localhost
   DB_PORT=5432
   DB_NAME=antenna_faults
   DB_USER=postgres
   DB_PASSWORD=your_password
   ```

4. **Run the pipeline**
   Execute the main entry point to load the data into PostgreSQL, perform the SQL-based train/test split, train the models, and export visual results:
   ```bash
   python main.py
   ```

---

## Workflow Summary

1. **Ingestion & Storage (`PostgreSQL`):** Raw RF measurements from `data/raw/` are loaded into structured PostgreSQL tables.
2. **In-Database Splitting (`PostgreSQL`):** Train, validation, and test splits are generated directly via SQL queries to keep data partitioning reproducible and decoupled from Python runtime state.
3. **Model Training & Evaluation (`src/models/`):** Models are trained on the queried splits and evaluated on classification accuracy, confusion matrices, and feature importance across fault classes.
4. **Reporting (`data/results/`):** Diagnostic figures, evaluation charts, and a detailed technical write-up of the findings are saved to `data/results/`.

---

## Results & Write-Up

All generated plots, confusion matrices, and the full analysis write-up documenting model performance and RF domain insights can be found in the [`data/results/`](data/results/) directory.