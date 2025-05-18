# MoonLight Energy Solutions - Strategic Solar Investment Analysis (Week 0 Challenge)

## Project Overview

This project, undertaken as part of the Week 0 Challenge, aims to support MoonLight Energy Solutions in developing a strategic approach to enhance operational efficiency and sustainability through targeted solar investments. As an Analytics Engineer, the primary task is to analyze environmental measurement data from various locations, identify key trends, and translate these observations into a data-driven strategy report. The core focus is on identifying high-potential regions for solar panel installations that align with the company's long-term sustainability goals.

## Business Objective

To perform a comprehensive analysis of environmental measurement data (solar irradiance, temperature, humidity, wind, etc.) for selected regions (Benin, Sierra Leone, Togo) and provide data-driven recommendations for identifying high-potential areas for solar energy investments, thereby enhancing MoonLight Energy Solutions' operational efficiency and sustainability.

## Dataset Overview

The data for this challenge is extracted and aggregated from Solar Radiation Measurement Data. Each row typically contains values for:
*   **Timestamp** (yyyy-mm-dd hh:mm)
*   **Solar Irradiance:** GHI (Global Horizontal Irradiance), DNI (Direct Normal Irradiance), DHI (Diffuse Horizontal Irradiance) in W/m².
*   **Module Readings:** ModA, ModB (W/m²) - measurements from specific solar modules/sensors.
*   **Meteorological Data:**
    *   Tamb (°C): Ambient Temperature.
    *   RH (%): Relative Humidity.
    *   WS (m/s), WSgust (m/s), WSstdev (m/s): Wind Speed, Gust, and Standard Deviation.
    *   WD (°N (to east)), WDstdev: Wind Direction and Standard Deviation.
    *   BP (hPa): Barometric Pressure.
    *   Precipitation (mm/min).
*   **Module Temperatures:** TModA (°C), TModB (°C).
*   **Operational Data:** Cleaning (1 or 0) - signifying if sensor/module cleaning occurred.
*   **Comments:** For additional notes (often found to be sparse or null).

Specific datasets analyzed:
*   `data/benin-malanville.csv`
*   `data/sierraleone-bumbuna.csv`
*   `data/togo-dapaong_qc.csv`
*(Note: The `data/` directory is gitignored as per project instructions; raw data files are stored locally.)*

## Project Structure & Methodology

The project follows a structured analytical workflow:

1.  **Task 1: Git & Environment Setup:**
    *   Initialized a GitHub repository (`solar-challenge-week1`) with appropriate `.gitignore`.
    *   Established a Python virtual environment (`venv`/`conda`) with necessary libraries listed in `requirements.txt`.
    *   Implemented a basic CI/CD pipeline using GitHub Actions for automated dependency checks.
    *   Organized the project with a logical folder structure (`notebooks/`, `data/` (local), `app/`, `scripts/`, etc.).

2.  **Task 2: Data Profiling, Cleaning & Exploratory Data Analysis (EDA) - Per Country:**
    *   **Branching:** Dedicated branches (e.g., `eda-benin`, `eda-sierraleone`, `eda-togo`) were used for individual country EDA.
    *   **Notebooks:** Jupyter Notebooks (e.g., `benin_eda.ipynb`) were created for each country in the `notebooks/` directory.
    *   **Process:**
        *   **Data Loading & Initial Inspection:** Loaded CSV data, checked data types, shape, and initial overview. Converted `Timestamp` to datetime objects.
        *   **Summary Statistics & Missing Value Reporting:** Generated descriptive statistics and identified missing values (e.g., `Comments` column was consistently 100% null and dropped).
        *   **Data Cleaning:** Handled missing values in key numeric columns (typically via median imputation). Addressed erroneous data, such as negative irradiance values (clipped to 0 W/m²).
        *   **Outlier Detection:** Used Z-scores (|Z|>3) to flag potential outliers in sensor readings (GHI, DNI, DHI, ModA, ModB) and wind data (WS, WSgust). Applied physical constraints (e.g., irradiance >= 0, RH between 0-100%).
        *   **Cleaned Data Export:** Exported cleaned DataFrames to local `data/` folder (e.g., `benin_clean.csv`), ensuring these are gitignored.
        *   **Visualization & Analysis:**
            *   Time Series Analysis (GHI, DNI, DHI, Tamb vs. Timestamp; monthly/hourly averages).
            *   Cleaning Impact (average ModA/ModB pre/post cleaning flag).
            *   Correlation Analysis (heatmap of key variables).
            *   Relationship Analysis (scatter plots for WS, RH, GHI, Tamb, etc.).
            *   Wind & Distribution Analysis (wind rose plots, histograms).
            *   Temperature Analysis (module temperature rise vs. ambient and GHI).
            *   Multivariate Bubble Charts (e.g., GHI vs. Tamb, size=RH, color=BP).
        *   **Documentation:** Insights and observations documented within each notebook.

3.  **Task 3: Cross-Country Comparison (In Progress / To Be Completed):**
    *   A dedicated branch (`compare-countries`) and notebook (`notebooks/compare_countries.ipynb`) will be used.
    *   Load cleaned datasets for Benin, Sierra Leone, and Togo.
    *   Perform comparative analysis:
        *   Side-by-side boxplots of GHI, DNI, DHI.
        *   Summary table of mean, median, std dev across countries.
        *   Statistical testing (e.g., ANOVA/Kruskal-Wallis) to assess significance of differences.
    *   Summarize key observations and rank countries based on solar potential metrics.

4.  **Bonus Task: Interactive Dashboard (Planned / In Progress):**
    *   A Streamlit application (`app/main.py`) will be developed on a `dashboard-dev` branch.
    *   The dashboard will visualize key insights from the EDA and cross-country comparison, allowing for interactive exploration (e.g., country selection, metric plotting).
    *   The aim is to deploy this dashboard to Streamlit Community Cloud.

## Key Performance Indicators (KPIs) Addressed:

*   **Dev Environment Setup:** Successfully completed in Task 1.
*   **EDA Techniques & Statistical Understanding:** Demonstrated through detailed EDA notebooks for each country, employing various visualization techniques and statistical summaries (Z-scores, correlations, descriptive stats).
*   **Cross-Country Comparison Metrics (Task 3):** Will include appropriate statistical tests, summary tables, and clear visualizations comparing all three countries.
*   **Dashboard Usability & Features (Bonus Task):** Will focus on intuitive navigation, interactive elements, and clear communication of insights.

## Current Status

*   **Task 1 (Git & Environment Setup):** Completed.
*   **Task 2 (Data Profiling, Cleaning & EDA):**
    *   EDA for Benin (Malanville): Completed.
    *   EDA for Sierra Leone (Bumbuna): Completed.
    *   EDA for Togo (Dapaong QC): Completed.
    *   Cleaned datasets for all three countries are available locally.
*   **Task 3 (Cross-Country Comparison):** [Specify current status, e.g., "Not Started", "In Progress", "Planning Phase"]
*   **Bonus Task (Interactive Dashboard):** [Specify current status, e.g., "Not Started", "Initial UI drafted", "Planning Phase"]

## Environment Setup (To Reproduce)

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/solar-challenge-week1.git
    cd solar-challenge-week1
    ```
2.  **Create and activate a virtual environment:**
    *   Using `venv`:
        ```bash
        python -m venv .venv
        source .venv/bin/activate  # On Windows: .venv\Scripts\activate
        ```
    *   Or using `conda`:
        ```bash
        # conda create -n solar_env python=3.9  # Or your preferred Python version
        # conda activate solar_env
        ```
3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Data:**
    *   Place the provided CSV files (`benin-malanville.csv`, `sierraleone-bumbuna.csv`, `togo-dapaong_qc.csv`) into a local `data/` directory at the root of the project. This directory is included in `.gitignore` and data files will not be committed.
5.  **Run Notebooks:**
    *   Navigate to the `notebooks/` directory to explore the EDA for each country.
    *   Ensure you have Jupyter Notebook or JupyterLab installed (`pip install notebook jupyterlab`).

## Next Steps

*   Complete Task 3: Cross-Country Comparison.
*   Develop and deploy the Streamlit Dashboard (Bonus Task).
*   Compile the Interim and Final Reports summarizing all findings and strategic recommendations.

## Contribution & Collaboration

This project is managed through GitHub.
*   **Branching:** Feature branches are used for distinct tasks and merged via Pull Requests.
*   **Commits:** Atomic commits with descriptive messages are encouraged.
*   **Issues:** GitHub Issues can be used to track bugs, enhancements, or specific sub-tasks.

---