import streamlit as st
import pandas as pd
import plotly.express as px

st.title("Interact with Climate Change Data")


# importing the csv datasets and converting them into dataframes
df_temp = pd.read_csv("GlobalLandTemperaturesByCountry.csv")
df_emmisions = pd.read_csv("co-emissions-per-capita.csv")

# Temperature dataframe converting the date


def date_converter(date):
    if isinstance(date, str):  # checks if the date is of string type
        year = float(date[:4])
    return year


# Renaming dt column to Year
df_temp = df_temp.rename(columns={"dt": "Year"})

df_temp['Year'] = df_temp['Year'].apply(date_converter).astype(int).astype(str)
# df_temp.head()

# Gets rid of rows in the dataframe with a NaN element
no_NaN_df = df_temp.dropna()


#
df_temp = no_NaN_df.groupby(['Country', 'Year'], as_index=False).mean()

# Dropping Code column from the emissions dataframe
df_emmisions = df_emmisions.drop(['Code'], axis=1)

# Changing df_emmisions dataframe column Entity to Country
df_emmisions = df_emmisions.rename(columns={"Entity": "Country"})

# Converting the year column in df_emmisions dataset into a string instead of integer type
df_emmisions['Year'] = df_emmisions['Year'].values.astype(str)

# Combining the two dataframes into one
emission_years = df_emmisions['Year'].to_list()
emission_distinct_years = list(set(emission_years))

df_combined = pd.merge(df_temp, df_emmisions, on=["Year", "Country"])

countries = list(set(df_combined['Country'].to_list()))
metrics_list = ["AverageTemperature", "Per capita CO2 emissions"]

with st.sidebar:
    st.subheader("Configure the plot")
    # widget to choose whcih country to look at
    country_choice = st.sidebar.selectbox('Select a country:', countries)
    # widget to choose which metric to display
    metric = st.selectbox(label="Choose the metric", options=metrics_list)

df_filtered = df_combined[df_combined["Country"] == country_choice]

title1 = f"{metric} per Year in {country_choice}"
fig = px.line(df_filtered, x="Year", y=metric, title=title1)

st.plotly_chart(fig, use_container_width=True)
