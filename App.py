import plotly.express as px
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib
import plotly.graph_objects as go
import numpy as np
import os

st.set_page_config(layout="wide")
# Fixing Hebrew text orientation
matplotlib.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.family'] = 'Arial'
plt.rcParams['axes.titlepad'] = 20

grouped_data = os.path.join(os.path.dirname(__file__), 'grouped_data.csv')
g = pd.read_csv(grouped_data)

# Aggregating data by Quarter and PoliceDistrict
aggregated_data = g.groupby(['Quarter', 'PoliceDistrict'], as_index=False).sum()

grouped_data_by_cluster = os.path.join(os.path.dirname(__file__), 'grouped_data_by_cluster.csv')
data = pd.read_csv(grouped_data_by_cluster)

preprocessed_data = os.path.join(os.path.dirname(__file__), 'preprocessed_data.csv')
df = pd.read_csv(preprocessed_data)

# Custom CSS to set text direction to right-to-left
st.markdown(
    """
    <style>
    .rtl-text {
        direction: rtl;
        text-align: right;
    }
    .inline-buttons {
        display: flex;
        justify-content: flex-end;
        gap: 10px;
        margin-top: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)
st.markdown('<h1 class="rtl-text">כיצד משתנה היקף הפשיעה בישראל בהתאם לאזורים גיאוגרפיים שונים ולתקופות זמן שונות?</h1>', unsafe_allow_html=True)

color_sequence_district = ['#a65628', '#74c476', '#ff7f00', '#f768a1', '#e5d8bd', '#e41a1c', '#fec44f']

# Create the figure for all districts
fig_all_districts = px.line(
    aggregated_data, x='Quarter', y='TikimSum', color='PoliceDistrict',
    title='מגמות התיקים שנפתחו לפי מחוזות משטרה',
    color_discrete_sequence=color_sequence_district,
    hover_data={'Quarter': True, 'TikimSum': ':.3s'}
)
fig_all_districts.update_layout(
    yaxis_title=dict(
        text="כמות התיקים",
        font=dict(size=20)  # Increase the text size
    ), xaxis_title=dict(
        text="רבעון",
        font=dict(size=20)  # Increase the text size
    ), title_x=0.75, legend_title=dict(
        text="מחוז משטרה",
        font=dict(size=20)  # Increase the text size
    ),
    hoverlabel=dict(font_size=20),
    legend=dict(font=dict(size=18))
)
fig_all_districts.for_each_yaxis(lambda yaxis: yaxis.update(tickfont=dict(size=15)))
fig_all_districts.for_each_xaxis(lambda xaxis: xaxis.update(tickfont=dict(size=15)))
fig_all_districts.update_traces(
    hovertemplate='%{x}<br>סכום התיקים=%{y:,}'
)

# Dropdown with an additional "כלל המחוזות" option
options = ["כלל המחוזות"] + list(g['PoliceDistrict'].unique())
selected_district = st.selectbox("בחר את מחוז המשטרה", options)
if selected_district == "כלל המחוזות":
    st.plotly_chart(fig_all_districts)
else:
    district_data = g[g['PoliceDistrict'] == selected_district]
    
    # Aggregate data by Quarter to get the total TikimSum for each quarter
    quarter_totals = district_data.groupby('Quarter')['TikimSum'].sum().reset_index()
    quarter_totals.rename(columns={'TikimSum': 'TotalTikimSum'}, inplace=True)
    
    # Merge the total TikimSum with the district data
    district_data = pd.merge(district_data, quarter_totals, on='Quarter', how='left')
    
    fig = px.line(
        district_data, x='Quarter', y='TikimSum', color='PoliceMerhav',
        title=f'מגמות התיקים שנפתחו ב{selected_district}',
        color_discrete_sequence=color_sequence_district,
        hover_data={'Quarter': True, 'TikimSum': ':.3s', 'TotalTikimSum': True}
    )
    fig.update_layout(
        yaxis_title=dict(
            text="כמות התיקים",
            font=dict(size=20)  # Increase the text size
        ), xaxis_title=dict(
            text="רבעון",
            font=dict(size=20)  # Increase the text size
        ), title_x=0.75, legend_title=dict(
            text="מרחב",
            font=dict(size=20)  # Increase the text size
        ), hoverlabel=dict(font_size=20),
        legend=dict(font=dict(size=20))
    )
    fig.for_each_yaxis(lambda yaxis: yaxis.update(tickfont=dict(size=18)))
    fig.for_each_xaxis(lambda xaxis: xaxis.update(tickfont=dict(size=18)))
    fig.update_traces(
        hovertemplate='%{x}<br>סכום התיקים=%{y:,}<br>סכום התיקים הכולל במחוז=%{customdata[0]:,}'
    )
    st.plotly_chart(fig)

# Assuming 'data' is your DataFrame
all_crime_groups = data['StatisticCrimeGroup'].unique()

selected_groups = st.multiselect("בחר את קבוצות הפשיעה", all_crime_groups, default=all_crime_groups)

# Filter data based on selected groups
filtered_data = data[data['StatisticCrimeGroup'].isin(selected_groups)] if selected_groups else pd.DataFrame(columns=data.columns)

# Create the figure
if not filtered_data.empty:
    fig = px.histogram(filtered_data, x='Cluster', y='norm', color='StatisticCrimeGroup', barmode='stack',
                       title=f'התפלגות העבירות הנ"ל לפי האשכול החברתי-כלכלי של היישוב', hover_data={'Cluster': False, 'StatisticCrimeGroup': True, 'norm': ':.3s'})
else:
    # Create an empty figure with the same layout
    fig = go.Figure()
    fig.add_trace(go.Bar(x=[], y=[]))
    fig.update_layout(title=f'התפלגות העבירות הנ"ל לפי האשכול החברתי-כלכלי של היישוב')
fig.for_each_yaxis(lambda yaxis: yaxis.update(tickfont=dict(size=15)))
fig.for_each_xaxis(lambda xaxis: xaxis.update(tickfont=dict(size=15)))
fig.update_xaxes(tickmode='linear', tick0=1, dtick=1)
fig.update_layout(barmode='relative', bargap=0.2, xaxis_title=dict(
    text="אשכול כלכלי-חברתי",
    font=dict(size=20)  # Increase the text size
), yaxis_title=dict(
    text="סכום התיקים המנורמל בגודל האוכלוסייה",
    font=dict(size=20)  # Increase the text size
),
    legend_titlelegend_title=dict(
            text="קבוצת העבירות",
            font=dict(size=20)  # Increase the text size
        ), title_x=0.7, height=630, hoverlabel=dict(font_size=20),
    legend=dict(font=dict(size=18)))
fig.update_traces(
    hovertemplate='קבוצת העבירה=%{fullData.name}<br>סכום התיקים המנורמל=%{y:,}'
)
if len(selected_groups) == 1:
    fig.update_layout(showlegend=False)

st.plotly_chart(fig)

# Convert 'Quarter' to 'Year'
df['Year'] = df['Quarter'].str[:4].astype(int)
data['Year'] = data['Quarter'].str[:4].astype(int)

# Function to plot relative crime by religion and group
def plot_relative_crime_by_religion_and_group(df, data, selected_group):
    # Merge the two dataframes on StatisticCrimeGroup, Cluster, and Year
    merged_df = pd.merge(df, data, on=['StatisticCrimeGroup', 'Year'], suffixes=('_original', '_norm'))

    # Ensure Year is treated as a categorical variable with a specific order
    merged_df['Year'] = pd.Categorical(merged_df['Year'], ordered=True, categories=sorted(df['Year'].unique()))
    
    # Set the order of the 'Religious level' column and use blue color saturation levels
    desired_order = ['חילונים', 'מסורתיים', 'דתיים', 'חרדים']
    merged_df['Religious level'] = pd.Categorical(merged_df['Religious level'], categories=desired_order, ordered=True)
    
    # Define color sequence with varying saturation levels of blue
    color_sequence = ['#cc4c02', '#fe9929', '#fed98e', '#ffffd4']

    if selected_group == 'כלל העבירות':
        # Compute the total number of crimes for each crime group and year
        total_crimes_per_group = merged_df.groupby(['StatisticCrimeGroup', 'Year'])['TikimSum_original'].sum().reset_index()
        total_crimes_per_group.columns = ['StatisticCrimeGroup', 'Year', 'TotalTikimSum']

        # Merge the total crimes with the merged dataframe
        df_merged = pd.merge(merged_df, total_crimes_per_group, on=['StatisticCrimeGroup', 'Year'])

        # Compute the relative number of crimes for each religious level within each crime group
        df_merged['RelativeTikimSum'] = df_merged['TikimSum_original'] / df_merged['TotalTikimSum']

        # Group by crime group, religious level, and year
        relative_crime_data = df_merged.groupby(['StatisticCrimeGroup', 'Religious level', 'Year']).agg({'RelativeTikimSum': 'sum',
            'TikimSum_original': 'sum'}).reset_index()

        # Plot the relative bar chart with small multiples for each year
        fig = px.bar(relative_crime_data, x='RelativeTikimSum', y='StatisticCrimeGroup', color='Religious level',
                     title=f'הקשר בין רמת הדתיות לרמת הפשיעה לפי קבוצת עבירה',
                     labels={'StatisticCrimeGroup': 'קבוצת עבירה', 'RelativeTikimSum': 'חלק הפשיעה היחסי', 'Religious level': 'רמת דתיות', 'TikimSum_original': 'כמות התיקים'},
                     barmode='stack',  # Use stacked bar mode
                     hover_data={'StatisticCrimeGroup': False, 'Year': False, 'Religious level': False, 'TikimSum_original': True, 'RelativeTikimSum': True},
                     facet_col='Year',
                     color_discrete_sequence=color_sequence,
                     category_orders={'Year': sorted(unique_years), 'Religious level': desired_order},
                     facet_col_wrap=6,
                     height=700,  # Set the height to fit the page
                     facet_row_spacing=0.05)  # Adjust row spacing if needed
    else:
        # Filter the dataframe by selected crime group
        filtered_df = merged_df[merged_df['StatisticCrimeGroup'] == selected_group]

        # Compute the total number of crimes for each crime type and year within the selected crime group
        total_crimes_per_type = filtered_df.groupby(['StatisticCrimeType', 'Year'])['TikimSum_original'].sum().reset_index()
        total_crimes_per_type.columns = ['StatisticCrimeType', 'Year', 'TotalTikimSum']

        # Merge the total crimes with the filtered dataframe
        df_merged = pd.merge(filtered_df, total_crimes_per_type, on=['StatisticCrimeType', 'Year'])

        # Compute the relative number of crimes for each religious level within each crime type
        df_merged['RelativeTikimSum'] = df_merged['TikimSum_original'] / df_merged['TotalTikimSum']

        # Group by crime type, religious level, and year
        relative_crime_data = df_merged.groupby(['StatisticCrimeType', 'Religious level', 'Year']).agg({'RelativeTikimSum': 'sum',
            'TikimSum_original': 'sum'}).reset_index()

        # Plot the relative bar chart with small multiples for each year
        fig = px.bar(relative_crime_data, x='RelativeTikimSum', y='StatisticCrimeType', color='Religious level',
                     title=f'הקשר בין מידת הדתיות של היישוב לרמת הפשיעה לפי {selected_group}',
                     labels={'StatisticCrimeType': 'עבירה', 'RelativeTikimSum': 'חלק הפשיעה היחסי', 'Religious level': 'רמת דתיות', 'TikimSum_original': 'כמות התיקים'},
                     barmode='stack',  # Use stacked bar mode
                     hover_data={'StatisticCrimeType': False, 'Year': False, 'Religious level': False, 'TikimSum_original': True, 'RelativeTikimSum': True},
                     facet_col='Year',
                     color_discrete_sequence=color_sequence,
                     category_orders={'Year': sorted(unique_years), 'Religious level': desired_order},
                     facet_col_wrap=6,
                     height=700,  # Set the height to fit the page
                     facet_row_spacing=0.05)  # Adjust row spacing if needed

    # Update layout to show x-axis in all facets
    fig.for_each_yaxis(lambda yaxis: yaxis.update(tickfont=dict(size=18)))
    fig.update_layout(title_x=0.65, hoverlabel=dict(font_size=20),
                      legend=dict(font=dict(size=18)),
                      legend_title=dict(font=dict(size=20)),
                      yaxis_title=dict(
                          font=dict(size=20)  # Increase the text size
                      ))
    st.plotly_chart(fig, use_container_width=True)

# Example usage
# Get unique years from the dataframe
unique_years = df['Year'].unique()
# Add a dropdown to select the crime group
crime_groups = sorted(['כלל העבירות'] + df['StatisticCrimeGroup'].unique().tolist())
selected_group = st.selectbox('בחר את קבוצת העבירה', crime_groups)

# Call the function to plot the chart
plot_relative_crime_by_religion_and_group(df, data, selected_group)
