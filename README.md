# German Real Estate Market Analysis

## Dataset Overview

- The dataset, sourced from Kaggle, is 232 MB in size and focuses on analyzing the German real estate market
- It was created by scraping data from the immoscout24.de rental website, collected across four time periods between 2018 and 2020

## Repository Structure

### Data Folder
- `immo_data.csv` (original dataset, 232 MB, too large for GitHub's 100 MB upload limit)
- `plz_wohner.csv`: Merged with immo_data.csv to calculate the number of residents per zip code  
- `zuordnung_plz_ort.csv`: Maps postal codes (PLZ) to specific cities and states

### Data Processing Workflow

#### Raw Data Cleaning
The cleaning process starts with three input files: `immo_data.csv`, `plz_wohner.csv`, and `zuordnung_plz_ort.csv`. Using `Data_cleaning.ipynb`, these files are cleaned and merged to create `cleaned_data.csv`.

#### Exploratory Data Analysis (EDA)
The `EDA.ipynb` notebook analyzes `cleaned_data.csv` using functions from `eda_helper_functions.py`. The analysis results are saved in `eda_data.csv` with new analytical features.

#### Dashboard Creation 
Interactive visualizations are created in `plotly_dashboard.ipynb` using a 1000-row sample from `eda_data.csv` due to computational constraints. The resulting dashboard provides insights into German real estate market trends through a representative subset of the data. While not using the full dataset, this sampling approach allows for efficient visualization while maintaining meaningful pattern analysis.

#### Feature Engineering
The `feature_engineering.ipynb` notebook processes `eda_data.csv` to create new features. The output `preprocessed_data.csv` contains data ready for machine learning.

#### Model Training
Finally, `ModelTraining.ipynb` uses `preprocessed_data.csv` to train prediction models. The trained model is saved as `model.pkl` for real estate price predictions.

```python
German Real Estate Market Analysis/
├── Data/ 
├── GeoJSON/ # Geographic data files
├── Notebooks/ 
│ ├── Data_cleaning.ipynb # Data preprocessing notebook
│ ├── eda_helper_functions.py # Helper functions for EDA
│ ├── EDA.ipynb # Exploratory Data Analysis
│ ├── FeatureEngineering.ipynb # Feature creation and selection
│ ├── ModelTraining.ipynb # Model development notebook
│ └── plotly_dashboard.ipynb # Interactive visualization dashboard
├── .gitignore 
├── app.py 
├── model_training.log
├── model.pkl
└── requirements.txt 
```

**Data Source**: [Kaggle Dataset - Apartment Rental Offers in Germany](https://www.kaggle.com/datasets/corrieaar/apartment-rental-offers-in-germany)

> **Note:** the large data files are not included in the repository due to size limitations.

### Technologies Used
- **Python**
- **Pandas** for data manipulation
- **Plotly** for interactive visualizations
- **Jupyter Notebooks** for analysis
- **Statistical analysis libraries**

## Setup and Installation

1. Clone this repository
   ```python
   git clone https://github.com/Joon-hub/German-Real-state-Market-Analysis.git
   ```
3. install dependencies
   ```python
   pip install -r requirements.txt
   ```
4. run app.py
   ```python
   python app.py
   ```
 
