import plotly.express as px
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib
# Loading the data
import os



st.set_page_config(layout="wide")
# Fixing Hebrew text orientation
matplotlib.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.family'] = 'Arial'
plt.rcParams['axes.titlepad'] = 20



grouped_data=os.path.join(os.path.dirname(__file__), 'grouped_data.csv')
g = pd.read_csv(grouped_data)


grouped_data_by_cluster=os.path.join(os.path.dirname(__file__), 'grouped_data_by_cluster.csv')
data = pd.read_csv(grouped_data_by_cluster)


preprocessed_data=os.path.join(os.path.dirname(__file__), 'preprocessed_data.csv')
df = pd.read_csv(preprocessed_data)


# Custom CSS to set text direction to right-to-left
st.markdown(
    """
    <style>
    .rtl-text {
        direction: rtl;
        text-align: right;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Title and subheader with right-to-left text direction
st.markdown('<h1 class="rtl-text">כיצד משתנה היקף הפשיעה בישראל בהתאם לאזורים גיאוגרפיים שונים ולתקופות זמן שונות?</h1>', unsafe_allow_html=True)
selected_district = st.selectbox("Select Police District", g['PoliceDistrict'].unique())
if selected_district:
    district_data = g[g['PoliceDistrict'] == selected_district]
    fig = px.line(district_data, x='Quarter', y='TikimSum', color='PoliceMerhav',
                  title=f'מגמות התיקים שנפתחו ב{selected_district}')
    fig.update_layout(yaxis_title='כמות התיקים', xaxis_title='רבעון', title_x=0.65, legend_title_text='מרחב')
    st.plotly_chart(fig)

#Crime Group Distribution
selected_groups = st.multiselect("Select Crime Groups", data['StatisticCrimeGroup'].unique(), default=['עבירות כלפי הרכוש'])
if selected_groups:
    filtered_data = data[data['StatisticCrimeGroup'].isin(selected_groups)]
    fig = px.histogram(filtered_data, x='Cluster', y='norm', color='StatisticCrimeGroup', barmode='stack',
                       title=f'התפלגות העבירות הנ"ל')
    fig.update_xaxes(tickmode='linear', tick0=1, dtick=1)
    fig.update_layout(barmode='relative', xaxis_title='אשכול כלכלי-חברתי', yaxis_title='סכום התיקים המנורמל בגודל האוכלוסיה',
                      legend_title_text='קבוצת העבירות', title_x=0.75)
    st.plotly_chart(fig)


def plot_relative_crime_by_religion_and_group(df, data, selected_group):
    # Merge the two dataframes on StatisticCrimeGroup, Cluster, and Quarter
    merged_df = pd.merge(df, data, on=['StatisticCrimeGroup', 'Quarter'], suffixes=('_original', '_norm'))

    # Ensure Quarter is treated as a categorical variable with a specific order
    merged_df['Quarter'] = pd.Categorical(merged_df['Quarter'], ordered=True, categories=sorted(df['Quarter'].unique()))
    # Define the desired order for the 'Religious level' column
    religious_order = ['חילונים', 'מסורתיים', 'חרדים', 'דתיים']
    merged_df['Religious level'] = pd.Categorical(merged_df['Religious level'], categories=religious_order)
    if selected_group == 'All':
        # Compute the total number of crimes for each crime group and quarter
        total_crimes_per_group = merged_df.groupby(['StatisticCrimeGroup', 'Quarter'])['TikimSum_original'].sum().reset_index()
        total_crimes_per_group.columns = ['StatisticCrimeGroup', 'Quarter', 'TotalTikimSum']

        # Merge the total crimes with the merged dataframe
        df_merged = pd.merge(merged_df, total_crimes_per_group, on=['StatisticCrimeGroup', 'Quarter'])

        # Compute the relative number of crimes for each religious level within each crime group
        df_merged['RelativeTikimSum'] = df_merged['TikimSum_original'] / df_merged['TotalTikimSum']

        # Group by crime group, religious level, and quarter
        relative_crime_data = df_merged.groupby(['StatisticCrimeGroup', 'Religious level', 'Quarter']).agg({'RelativeTikimSum': 'sum',
            'TikimSum_original': 'sum'}).reset_index()

        # Sort by StatisticCrimeGroup alphabetically
        relative_crime_data = relative_crime_data.sort_values(by='Religious level', key=lambda x: x.str.encode('utf-8'))
        # Plot the relative bar chart with small multiples for each quarter
        fig = px.bar(relative_crime_data, x='RelativeTikimSum', y='StatisticCrimeGroup', color='Religious level',
                     title=f'הקשר בין רמת הדתיות לרמת הפשיעה לפי קבוצת עבירה',
                     labels={'StatisticCrimeGroup': 'קבוצת עבירה', 'RelativeTikimSum': 'אחוז הפשיעה', 'Religious level': 'רמת דתיות'},
                     barmode='stack',  # Use stacked bar mode
                     hover_data=['RelativeTikimSum', 'TikimSum_original'],
                     facet_col='Quarter',
                     category_orders={'Quarter': sorted(unique_quarters)},
                     facet_col_wrap=4,
                     height=2500,  # Set the height to fit the page
                     facet_row_spacing=0.05)  # Adjust row spacing if needed
    else:
        # Filter the dataframe by selected crime group
        filtered_df = merged_df[merged_df['StatisticCrimeGroup'] == selected_group]

        # Compute the total number of crimes for each crime type and quarter within the selected crime group
        total_crimes_per_type = filtered_df.groupby(['StatisticCrimeType', 'Quarter'])['TikimSum_original'].sum().reset_index()
        total_crimes_per_type.columns = ['StatisticCrimeType', 'Quarter', 'TotalTikimSum']

        # Merge the total crimes with the filtered dataframe
        df_merged = pd.merge(filtered_df, total_crimes_per_type, on=['StatisticCrimeType', 'Quarter'])

        # Compute the relative number of crimes for each religious level within each crime type
        df_merged['RelativeTikimSum'] = df_merged['TikimSum_original'] / df_merged['TotalTikimSum']

        # Group by crime type, religious level, and quarter
        relative_crime_data = df_merged.groupby(['StatisticCrimeType', 'Religious level', 'Quarter']).agg({'RelativeTikimSum': 'sum',
            'TikimSum_original': 'sum'}).reset_index()
        # Sort by StatisticCrimeType alphabetically
        relative_crime_data = relative_crime_data.sort_values(by='StatisticCrimeType', key=lambda x: x.str.encode('utf-8'))

        # Plot the relative bar chart with small multiples for each quarter
        fig = px.bar(relative_crime_data, x='RelativeTikimSum', y='StatisticCrimeType', color='Religious level',
                     title=f'הקשר בין מידת הדתיות של היישוב לרמת הפשיעה לפי {selected_group}',
                     labels={'StatisticCrimeType': 'סוג עבירה', 'RelativeTikimSum': 'אחוז הפשיעה', 'Religious level': 'רמת דתיות'},
                     barmode='stack',  # Use stacked bar mode
                     hover_data=['RelativeTikimSum', 'TikimSum_original'],
                     facet_col='Quarter',
                     category_orders={'Quarter': sorted(unique_quarters)},
                     facet_col_wrap=4,
                     height=2500,  # Set the height to fit the page
                     facet_row_spacing=0.05)  # Adjust row spacing if needed
    
    # Update layout to show x-axis in all facets
    fig.for_each_xaxis(lambda xaxis: xaxis.update(showticklabels=True, title_text='אחוז הפשיעה'))
    fig.update_layout(title_x=0.45)
    st.plotly_chart(fig, use_container_width=True)

# Example usage
# Assuming df is your DataFrame containing the relevant data
# Assuming data is your DataFrame containing the norm column

# Get unique quarters from the dataframe
unique_quarters = df['Quarter'].unique()
# Add a dropdown to select the crime group
crime_groups = sorted(['All'] + df['StatisticCrimeGroup'].unique().tolist())
selected_group = st.selectbox('Select Crime Group', crime_groups)

# Call the function to plot the chart
plot_relative_crime_by_religion_and_group(df, data, selected_group)

