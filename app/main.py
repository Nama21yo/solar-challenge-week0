# app/main.py
import streamlit as st
import pandas as pd
import plotly.express as px # Using Plotly for interactive plots
from utils import load_all_cleaned_data # Import from local utils.py

# --- Page Configuration ---
st.set_page_config(
    page_title="MoonLight Solar Analysis Dashboard",
    page_icon="☀️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Load Data (Cached) ---
AVAILABLE_COUNTRIES = ['Benin (Malanville)', 'Sierra Leone (Bumbuna)', 'Togo (Dapaong QC)']

# --- Sidebar for Filters ---
st.sidebar.title("🌍 Country & Data Filters")
selected_countries = st.sidebar.multiselect(
    "Select Countries:",
    options=AVAILABLE_COUNTRIES,
    default=AVAILABLE_COUNTRIES # Default to all selected
)

# Load data only for selected countries
if not selected_countries:
    st.warning("Please select at least one country from the sidebar to view data.")
    st.stop() # Stop execution if no country is selected

combined_df = load_all_cleaned_data(selected_countries)

if combined_df.empty:
    st.error("Failed to load data for the selected countries. Please ensure CSV files are present in the 'data/' directory and accessible.")
    st.stop()

# Filter for daytime data for irradiance comparisons
daytime_df = combined_df[combined_df['GHI'] > 10].copy()
if daytime_df.empty and not combined_df.empty : # If combined_df was not empty but daytime_df is
    st.warning("No data points with GHI > 10 W/m² found for the selected countries. Plots might be based on all data or appear empty.")
    # Fallback or specific handling if no "daytime" data
    daytime_df_for_plots = combined_df.copy() 
else:
    daytime_df_for_plots = daytime_df


# --- Main Dashboard Title ---
st.title("☀️ MoonLight Energy Solutions - Solar Investment Dashboard")
st.markdown("Comparative analysis of solar potential across selected regions.")

# --- Section 1: Irradiance Comparison ---
st.header("📊 Solar Irradiance Comparison (Daytime GHI > 10 W/m²)")

if not daytime_df_for_plots.empty:
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("GHI Distribution")
        if 'GHI' in daytime_df_for_plots.columns:
            fig_ghi_box = px.box(daytime_df_for_plots, x='Country', y='GHI', color='Country',
                                 title="Global Horizontal Irradiance (GHI)", labels={'GHI':'GHI (W/m²)'},
                                 points=False) # 'all', 'outliers', or False
            fig_ghi_box.update_layout(xaxis_tickangle=-30)
            st.plotly_chart(fig_ghi_box, use_container_width=True)
        else:
            st.write("GHI data not available for selected countries.")

    with col2:
        st.subheader("DNI Distribution")
        if 'DNI' in daytime_df_for_plots.columns:
            fig_dni_box = px.box(daytime_df_for_plots, x='Country', y='DNI', color='Country',
                                 title="Direct Normal Irradiance (DNI)", labels={'DNI':'DNI (W/m²)'},
                                 points=False)
            fig_dni_box.update_layout(xaxis_tickangle=-30)
            st.plotly_chart(fig_dni_box, use_container_width=True)
        else:
            st.write("DNI data not available for selected countries.")
    
    # DHI can be added similarly if desired
    # st.subheader("DHI Distribution")
    # if 'DHI' in daytime_df_for_plots.columns:
    # ...

else:
    st.write("No daytime data available for selected countries to display irradiance comparison.")


# --- Section 2: Top Regions Table (Summary Statistics) ---
st.header("🏆 Top Regions Summary (Daytime Averages)")

if not daytime_df_for_plots.empty:
    metrics_for_summary = ['GHI', 'DNI', 'DHI', 'Tamb', 'TModA']
    # Filter to only include metrics present in the dataframe
    available_metrics = [m for m in metrics_for_summary if m in daytime_df_for_plots.columns]

    if available_metrics:
        # Create a dictionary for the aggregation functions
        agg_dict = {metric: ['mean', 'median', 'std'] for metric in available_metrics}
        
        summary_table_multi_index = daytime_df_for_plots.groupby('Country').agg(agg_dict)
        
        if not summary_table_multi_index.empty:
            # Flatten the MultiIndex columns
            summary_table = summary_table_multi_index.copy()  # Avoid modifying original
            summary_table.columns = ['_'.join(col).strip() for col in summary_table.columns.values]
            summary_table = summary_table.reset_index()  # Bring 'Country' back as a column

            st.markdown("Mean, Median, and Standard Deviation of key metrics during daytime (GHI > 10 W/m²).")
            
            # Ensure numeric formatting only applies to numeric columns
            numeric_columns = summary_table.select_dtypes(include=['float', 'int']).columns
            formatted_table = summary_table.copy()
            for col in numeric_columns:
                formatted_table[col] = formatted_table[col].apply(lambda x: f"{x:.2f}")
            
            sort_metric = 'GHI_mean'  # This will be the column name after flattening
            
            if sort_metric in summary_table.columns:
                st.dataframe(formatted_table.sort_values(by=sort_metric, ascending=False))
            elif not summary_table.empty:  # If GHI_mean not there, but table exists, show unsorted
                st.dataframe(formatted_table)
            else:
                st.write("Summary table could not be generated or is empty after aggregation.")
        else:
            st.write("Aggregation resulted in an empty table.")
             
    else:
        st.write("No suitable metrics available for the summary table in selected data.")
else:
    st.write("No daytime data available to generate the top regions summary table.")

# --- Section 3: Time Series Viewer (Optional Advanced Feature) ---
st.header("🕰️ Time Series Viewer")
if not combined_df.empty and 'Timestamp' in combined_df.columns:
    selected_metric_ts = st.selectbox(
        "Select Metric for Time Series:",
        options=[col for col in combined_df.columns if pd.api.types.is_numeric_dtype(combined_df[col]) and col not in ['Country', 'Cleaning'] and not col.endswith('_zscore')],
        index=0 # Default to GHI if available, otherwise first numeric
    )

    if selected_metric_ts and selected_metric_ts in combined_df.columns:
        # Resample data to daily mean for a cleaner time series plot, if too granular
        # User could select resampling frequency too
        # For now, plot as is or simple resample
        # df_to_plot_ts = combined_df.set_index('Timestamp').groupby('Country')[selected_metric_ts].resample('D').mean().reset_index()
        # If no resampling:
        df_to_plot_ts = combined_df[['Timestamp', 'Country', selected_metric_ts]].copy()


        fig_ts = px.line(df_to_plot_ts, x='Timestamp', y=selected_metric_ts, color='Country',
                         title=f"{selected_metric_ts} Over Time",
                         labels={selected_metric_ts: f'{selected_metric_ts} (Units)'}) # Add units if known
        st.plotly_chart(fig_ts, use_container_width=True)
    else:
        st.write(f"Metric '{selected_metric_ts}' not available for time series plot.")
else:
    st.write("Combined data or Timestamp column not available for time series viewer.")

# --- Footer ---
st.markdown("---")
st.markdown("Dashboard developed for MoonLight Energy Solutions by Natnael Yohanes")