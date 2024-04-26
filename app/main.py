import datetime
import re
import matplotlib.pyplot as plt
import utils
import numpy as np 
import streamlit as st
import pandas as pd


st.set_page_config(page_title="EDA",
                   page_icon=":bar_chart:",
                   layout="wide"
                   )

st.title("10Academy-AIM")

selected_option = st.selectbox(label="Choose a dataset (.CSV):", options=utils.get_list_of_csvs())

df = utils.fetch_data(f"./data/{selected_option}")


st.title("MoonLight Energy Solutions Dashboard")
st.markdown(
    "MoonLight Energy Solutions aims to develop a strategic approach to significantly enhance" + 
    "its operational efficiency and sustainability through targeted solar investments. " +
    "This dashboard allows you to analysis of an environmental measurement provided and " +
    "translate observation. It focuss on identifying key trends and learn valuable insights that " + 
    "will support data-driven case - it has recommendations based on the statistical analysis and EDA. " +  
    "In particular, the analysis and recommendation present a strategy focusing on identifying high-potential " +
    "regions for solar installation that align with the company's long-term sustainability goals. "+ 
    "The report provide an insight to help realize the overarching objectives of MoonLight Energy Solutions. "+ 
    "Here, you can compare diffrent measurements side-by-side."
)

data = utils.clean_data(df)

st.sidebar.header("Customize the Dashboard")
plot_type = st.sidebar.selectbox(
    "Select Plot Type", ["Line Plot", "Scatter Plot", "Box Plot", "Histogram"]
)

x_column = st.sidebar.selectbox("Measurement (X-Axis)", data.columns)
y_column = st.sidebar.selectbox("Measurement (Y-Axis)", data.columns)

#Customize Display
st.subheader("Customize Display")

if plot_type == "Line Plot":
    utils.generate_line_plot(data, x_column, y_column, "Line Plot")

elif plot_type == "Scatter Plot":
    hue_column = st.sidebar.selectbox("Hue", ["None"] + list(data.columns))
    hue = None if hue_column == "None" else hue_column
    utils.generate_scatter_plot(data, x_column, y_column, "Scatter Plot", hue=hue)

elif plot_type == "Box Plot":
    utils.generate_box_plot(data, x_column, "Box Plot")

elif plot_type == "Histogram":
    utils.generate_histogram(data, x_column, "Histogram")


#Data Quality Check
st.subheader("Data Quality Check")
category = st.selectbox("Select Category", ["Missing values", "Negative values"])
filtered_data = None
if category == "Missing values":
    filtered_data = df.isnull().sum()
if category == "Negative values":
    filtered_data = df[(df["GHI"] < 0) | (df["DNI"] < 0) | (df["DHI"] < 0)]

st.write(filtered_data)



#Summary Statistics
st.header("General statistics analysis of datasets")
st.write(utils.get_summary_stats(data))

#Time Series Analysis
st.subheader("Time Series Analysis")
df["Timestamp"] = pd.to_datetime(df["Timestamp"])
df.set_index("Timestamp", inplace=True)
plt.figure(figsize=(12, 8))
plt.subplot(2, 2, 1)
plt.plot(df["GHI"], color="blue")
plt.title(x_column)
plt.xlabel(x_column)
plt.ylabel(y_column)

st.pyplot(plt)

#Temperature Analysis
st.subheader("Temperature Analysis")

btn1 = st.button("TModA analysis")
btn2 = st.button("TModB analysis")

if btn1:
    hue_column = st.sidebar.selectbox("Hue", ["None"] + list(data.columns))
    hue = None if hue_column == "None" else hue_column
    utils.generate_scatter_plot(data, 'Tamb', 'TModA', "Scatter Plot", hue=hue)

if btn2:
    hue_column = st.sidebar.selectbox("Hue", ["None"] + list(data.columns))
    hue = None if hue_column == "None" else hue_column
    utils.generate_scatter_plot(data, 'Tamb', 'TModB', "Scatter Plot", hue=hue)


