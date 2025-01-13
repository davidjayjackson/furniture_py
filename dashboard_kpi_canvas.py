import pandas as pd
import streamlit as st

# Load the data
data_path = 'furniture.xlsx'
sheets = pd.ExcelFile(data_path)
data = {sheet_name: sheets.parse(sheet_name) for sheet_name in sheets.sheet_names}

# Assuming the main data is in the first sheet
data_frame = list(data.values())[0]

# Dropdown options
if 'region' in data_frame.columns and 'sub_category' in data_frame.columns:
    dropdown1_options = data_frame['region'].dropna().unique().tolist()
    dropdown2_options = data_frame['sub_category'].dropna().unique().tolist()
else:
    dropdown1_options = ["No 'region' column found"]
    dropdown2_options = ["No 'sub_category' column found"]

# Streamlit app
st.title("Furniture Store Dashboard")

# Filters
st.header("Filters")
region = st.selectbox("Select Region:", dropdown1_options)
sub_category = st.selectbox("Select Sub-Category:", dropdown2_options)

# Filter data based on selections
filtered_data = data_frame[
    (data_frame['region'] == region) & 
    (data_frame['sub_category'] == sub_category)
]

# If filtered data is empty, provide defaults
if filtered_data.empty:
    st.warning("No data available for the selected filters.")
    kpi1 = kpi2 = kpi3 = kpi4 = kpi5 = kpi6 = kpi7 = kpi8 = kpi9 = 0
else:
    # Recalculate KPIs based on filtered data
    kpi1 = filtered_data['total_sales'].sum()  # Total Sales
    kpi2 = filtered_data['profit'].sum()       # Total Profit
    kpi3 = len(filtered_data['order_id'].unique())  # Total Orders
    kpi4 = filtered_data['quantity'].sum()    # Total Quantity Sold
    kpi5 = filtered_data['discount'].mean()   # Average Discount
    kpi6 = filtered_data['total_sales'].mean()  # Average Sales per Order
    kpi7 = filtered_data['profit'].mean()      # Average Profit per Order
    kpi8 = filtered_data['total_sales'].max()  # Highest Single Sale
    kpi9 = filtered_data['profit'].max()       # Highest Single Profit

# Display KPIs in a 3x3 layout
st.header("Key Performance Indicators (KPIs)")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Sales", f"${kpi1:,.2f}")
    st.metric("Total Quantity Sold", kpi4)
    st.metric("Highest Single Sale", f"${kpi8:,.2f}")
with col2:
    st.metric("Total Profit", f"${kpi2:,.2f}")
    st.metric("Average Discount", f"{kpi5:.2%}")
    st.metric("Highest Single Profit", f"${kpi9:,.2f}")
with col3:
    st.metric("Total Orders", kpi3)
    st.metric("Average Sales per Order", f"${kpi6:,.2f}")
    st.metric("Average Profit per Order", f"${kpi7:,.2f}")

# Display selected filters
st.write(f"Selected Region: {region}")
st.write(f"Selected Sub-Category: {sub_category}")
