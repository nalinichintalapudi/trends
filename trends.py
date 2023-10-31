import pandas as pd
import streamlit as st 
import plotly.express as px

@st.cache
def get_data_from_excel():
    df = pd.read_excel(
        io="OSEPIMARE_dataset.xlsx",
        engine="openpyxl",
        sheet_name="Sheet1",
        usecols="A:F",
        nrows=2907,
    )
    return df

# Load the data using the function
df = get_data_from_excel()

# Create four columns for filter widgets
col1, col2 = st.columns(2)

# Add filter widgets for "Cause", "Age", "Country", and "Rank" in the four columns
with col1:
    Diagnosis = st.selectbox("Select a Diagnosis:", options=sorted(df["Diagnosis"].unique()), index=0, key='Diagnosis')

with col2:
    Age = st.selectbox("Select an Age:", options=sorted(df["Age"].unique()), index=2)

col3, col4 = st.columns(2)

with col3:
    Nationality = st.selectbox("Select a Nationality:", options=sorted(df["Nationality"].unique()), index=2)

with col4:
    Rank = st.selectbox("Select a Rank:", options=sorted(df["Rank"].unique()), index=2)

# Filter the data based on user selections
df_selection = df.query(
    "Diagnosis ==@Diagnosis & Age ==@Age & Rank ==@Rank & Nationality==@Nationality"
)

# Sample data
data = df_selection  # Assuming you have df_selection
# Check if the dataframe is empty:
if df_selection.empty:
    st.warning("No data available based on the current filter settings!")
    st.stop() # This will halt the app from further execution.

# Create a dynamic title based on the selected filters
title = f"{Diagnosis}, {Age}, {Nationality}, {Rank}"
st.markdown(f"<h3 style='balck: red;text-align: center'> {title}</h3>", unsafe_allow_html=True)

pivot_table = data.pivot_table(index='Year', columns='Diagnosis', aggfunc='size', fill_value=0)

# Create a trend graph with lines and custom hover text using Plotly
fig = px.line(width=700, height=500)

# Set the line color to red
line_color = "red"

# Add lines for each category with custom hover text
# Add lines for each category with custom hover text
for column in pivot_table.columns:
    hover_text = [f" {column}: <b>{y}</b>" for y in pivot_table[column]]
    fig.add_scatter(
        x=pivot_table.index,
        y=pivot_table[column],
        mode='lines+markers',
        name='',
        line=dict(color='green'),
        hovertemplate="%{text}",  # Show custom hover text
        text=hover_text  # Custom hover text
    )

# Customize background grid color
background_grid_color = "light blue"
fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor=background_grid_color)
fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor=background_grid_color)

fig.update_yaxes(title='Count', tickvals=list(range(int(pivot_table.max().max()) + 1)))
fig.update_layout(legend_title_text='Diagnosis')

# Set hover label font size
fig.update_traces(hoverlabel_font_size=16, hoverlabel_font_color='red')

# Create a Streamlit app
st.plotly_chart(fig, use_container_width=True)




# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)


