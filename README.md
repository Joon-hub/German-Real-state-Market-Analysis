# German Real Estate Market Analysis

## Project Overview
As part of Data visualisation course in MSc Data Science, I developed this project to analyze the German real estate market using a dataset sourced from Kaggle. The dataset, sized at 232 MB, was collected by scraping rental listings from immoscout24.de across four time periods between 2018 and 2020. This project provided an opportunity to apply data engineering techniques to a substantial real-world dataset, strengthening my skills in data processing, analysis, and visualization.

## Repository Structure
The repository is structured as follows:

- **Data/**: Houses the original and processed datasets.
  - `immo_data.csv`: Original dataset (232 MB, not included due to size constraints).
  - `plz_wohner.csv`: Merged with `immo_data.csv` to compute residents per zip code.
  - `zuordnung_plz_ort.csv`: Maps postal codes to cities and states.
- **GeoJSON/**: Contains geographic data files for mapping purposes.
- **Notebooks/**: Includes Jupyter notebooks for each project phase.
  - `Data_cleaning.ipynb`: Cleans and merges raw data.
  - `eda_helper_functions.py`: Provides helper functions for exploratory data analysis.
  - `EDA.ipynb`: Conducts exploratory data analysis.
  - `FeatureEngineering.ipynb`: Generates and selects features for modeling.
  - `ModelTraining.ipynb`: Trains predictive models.
  - `plotly_dashboard.ipynb`: Develops an interactive visualization dashboard.
- **.gitignore**: Excludes large files from version control.
- **app.py**: Executes the dashboard application.
- **model_training.log**: Records logs from model training.
- **model.pkl**: Stores the trained model for price predictions.
- **requirements.txt**: Lists Python dependencies.

**Data Source**: [Kaggle Dataset - Apartment Rental Offers in Germany](https://www.kaggle.com/datasets/corrieaar/apartment-rental-offers-in-germany)

> **Note:** Large data files are excluded from the repository due to size limitations.

## Data Processing Workflow
The project follows a systematic data processing pipeline:

1. **Raw Data Cleaning**:
   - Inputs: `immo_data.csv`, `plz_wohner.csv`, `zuordnung_plz_ort.csv`
   - Process: Cleaned and merged via `Data_cleaning.ipynb`
   - Output: `cleaned_data.csv`

2. **Exploratory Data Analysis (EDA)**:
   - Input: `cleaned_data.csv`
   - Process: Analyzed in `EDA.ipynb` using `eda_helper_functions.py`
   - Output: `eda_data.csv` with derived analytical features

3. **Dashboard Creation**:
   - Input: 1000-row sample from `eda_data.csv`
   - Process: Visualized in `plotly_dashboard.ipynb`
   - Output: Interactive dashboard offering market trend insights

4. **Feature Engineering**:
   - Input: `eda_data.csv`
   - Process: Processed in `FeatureEngineering.ipynb`
   - Output: `preprocessed_data.csv` prepared for modeling

5. **Model Training**:
   - Input: `preprocessed_data.csv`
   - Process: Executed in `ModelTraining.ipynb`
   - Output: `model.pkl` for real estate price predictions

## Technologies Used
- **Python**: Primary programming language
- **Pandas**: Data manipulation and analysis
- **Plotly**: Interactive visualization tool
- **Jupyter Notebooks**: Environment for analysis and documentation
- **Statistical Analysis Libraries**: Tools for deriving data insights

## Setup and Installation
To set up and run the project, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/Joon-hub/German-Real-state-Market-Analysis.git
   ```
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Launch the dashboard application:
   ```bash
   python app.py
   ```

## Conclusion
This project served as a significant learning milestone, enabling me to implement data engineering methodologies on a complex dataset. Through this work, I enhanced my expertise in data cleaning, exploratory analysis, feature engineering, and predictive modeling. The resulting interactive dashboard offers valuable insights into the German real estate market, underscoring the potential of data-driven approaches. This experience has prepared me to tackle more advanced data engineering challenges in the future.
