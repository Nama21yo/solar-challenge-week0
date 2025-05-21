import pandas as pd
import os
import streamlit as st # For caching

# Define a base path relative to where utils.py is.
# If main.py is in app/ and data/ is ../data/, this should work.
# If running app/main.py from the root, then it would be 'data/'
# Let's assume main.py will be run from the 'app' directory.
# If streamlit run app/main.py is run from project root, path is 'data/'
# If cd app; streamlit run main.py, path is '../data/'
# We'll make it robust by checking a couple of common relative paths.

def get_data_path(filename):
    """Tries to find the data file in common relative locations."""
    path_option1 = os.path.join('../data', filename) # If running from app/
    path_option2 = os.path.join('data', filename)    # If running from project root
    
    if os.path.exists(path_option1):
        return path_option1
    elif os.path.exists(path_option2):
        return path_option2
    else:
        return None # Or raise an error

@st.cache_data(ttl=3600) # Cache data for 1 hour to avoid reloading on every interaction
def load_cleaned_data(country_name_full):
    """
    Loads a single cleaned dataset for a given country.
    country_name_full should be like 'Benin (Malanville)'
    """
    file_map = {
        'Benin (Malanville)': 'benin-malanville_clean.csv',
        'Sierra Leone (Bumbuna)': 'sierraleone-bumbuna_clean.csv',
        'Togo (Dapaong QC)': 'togo-dapaong_qc_clean.csv'
    }
    
    filename_short = file_map.get(country_name_full)
    if not filename_short:
        st.error(f"No file mapping found for country: {country_name_full}")
        return pd.DataFrame()

    file_path = get_data_path(filename_short)
    
    if file_path and os.path.exists(file_path):
        try:
            df = pd.read_csv(file_path)
            if 'Timestamp' in df.columns:
                 df['Timestamp'] = pd.to_datetime(df['Timestamp'])
            df['Country'] = country_name_full # Add country name for combined use if needed
            return df
        except Exception as e:
            st.error(f"Error loading data for {country_name_full} from {file_path}: {e}")
            return pd.DataFrame()
    else:
        st.error(f"Cleaned data file not found for {country_name_full} (expected {filename_short} in data/). Searched: {file_path}")
        return pd.DataFrame()

@st.cache_data(ttl=3600)
def load_all_cleaned_data(countries_to_load):
    """Loads and concatenates cleaned data for selected countries."""
    all_dfs = []
    for country_name in countries_to_load:
        df = load_cleaned_data(country_name)
        if not df.empty:
            all_dfs.append(df)
    
    if not all_dfs:
        return pd.DataFrame() # Return empty DataFrame if no data loaded
    
    combined_df = pd.concat(all_dfs, ignore_index=True)
    return combined_df