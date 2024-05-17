import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title('Gapminder')
st.write("Unlocking Lifetimes: Visualizing Progress in Longevity and Poverty Eradication")

@st.cache_data
def load_and_preprocess_data():
    # Load CSV files
    data1 = pd.read_csv('pop.csv')
    data2 = pd.read_csv('lex.csv')
    data3 = pd.read_csv('ny_gnp_pcap_pp_cd.csv')

    # Forward fill missing values
    data1.ffill(inplace=True)
    data2.ffill(inplace=True)
    data3.ffill(inplace=True)

    # Transform data to tidy format
    data1 = data1.melt(id_vars=["country"], var_name="year", value_name="life_expectancy")
    data2 = data2.melt(id_vars=["country"], var_name="year", value_name="population")
    data3 = data3.melt(id_vars=["country"], var_name="year", value_name="gni_per_capita")

    # Merge dataframes
    merged_data = pd.merge(data1, data2, on=["country", "year"])
    merged_data = pd.merge(merged_data, data3, on=["country", "year"])

    return merged_data

# Load and preprocess data
data = load_and_preprocess_data()

# Year slider
selected_year = st.slider('Select a year', min_value=int(data['year'].min()), max_value=int(data['year'].max()), value=int(data['year'].min()))

# Multiselect widget for selecting countries
selected_countries = st.multiselect('Select countries', data['country'].unique())

# Filter data based on selected year and countries
filtered_data = data[(data['year'] == str(selected_year)) & (data['country'].isin(selected_countries))]

# Display the filtered data
st.title('Gapminder Dashboard')
if not filtered_data.empty:
    st.write(filtered_data)
else:
    st.write('No data available for the selected year and countries.')


# Bubble chart based on specified KPIs
st.title('Bubble Chart')

# Plot bubble chart
fig, ax = plt.subplots()

# Plot bubbles for each country
for country, group in filtered_data.groupby('country'):
    ax.scatter(group['gni_per_capita'], group['life_expectancy'], s=group['population'], alpha=0.5, label=country)

# Set logarithmic scale for x-axis
ax.set_xscale('log')

# Set axis labels
ax.set_xlabel('GNI per capita (PPP)')
ax.set_ylabel('Life Expectancy')

# Set axis ticks and labels for x-axis
ax.set_xticks([1, 10, 100, 1000, 10000, 100000])
ax.set_xticklabels(['$1', '$10', '$100', '$1K', '$10K', '$100K'])

# Set axis ticks and labels for y-axis
ax.set_yticks([20, 40, 60, 80])
ax.set_yticklabels(['20', '40', '60', '80'])

# Set title and legend
ax.set_title('Bubble Chart')
ax.legend()

# Show the plot
st.pyplot(fig)