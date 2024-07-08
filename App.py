import plotly.express as px
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib
import os
import plotly.graph_objects as go


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
def plot_relative_crime_by_religion_and_group(df, data, selected_group):
    # Merge the two dataframes on StatisticCrimeGroup, Cluster, and Quarter
    merged_df = pd.merge(df, data, on=['StatisticCrimeGroup', 'Quarter'], suffixes=('_original', '_norm'))

    # Ensure Quarter is treated as a categorical variable with a specific order
    merged_df['Quarter'] = pd.Categorical(merged_df['Quarter'], ordered=True, categories=sorted(df['Quarter'].unique()))

    # Set the order of the 'Religious level' column and use blue color saturation levels
    desired_order = ['חילונים', 'מסורתיים', 'דתיים', 'חרדים']
    merged_df['Religious level'] = pd.Categorical(merged_df['Religious level'], categories=desired_order, ordered=True)

    # Define color sequence with varying saturation levels of blue
    color_sequence = ['#0000FF', '#6666FF', '#9999FF', '#CCCCFF']

    if selected_group == 'All':
        # Compute the total number of crimes for each crime group and quarter
        total_crimes_per_group = merged_df.groupby(['StatisticCrimeGroup', 'Quarter'])['TikimSum_original'].sum().reset_index()
        total_crimes_per_group.columns = ['StatisticCrimeGroup', 'Quarter', 'TotalTikimSum']

        # Merge the total crimes with the merged dataframe
        df_merged = pd.merge(merged_df, total_crimes_per_group, on=['StatisticCrimeGroup', 'Quarter'])

        # Compute the relative number of crimes for each religious level within each crime group
        df_merged['RelativeTikimSum'] = df_merged['TikimSum_original'] / df_merged['TotalTikimSum']

        # Group by crime group, religious level, and quarter
        relative_crime_data = df_merged.groupby(['StatisticCrimeGroup', 'Religious level', 'Quarter']).agg({
            'RelativeTikimSum': 'sum',
            'TikimSum_original': 'sum'
        }).reset_index()

        fig = go.Figure()

        for level, color in zip(desired_order, color_sequence):
            for quarter in sorted(unique_quarters):
                df_quarter = relative_crime_data[
                    (relative_crime_data['Quarter'] == quarter) & (relative_crime_data['Religious level'] == level)]
                fig.add_trace(go.Bar(
                    x=df_quarter['RelativeTikimSum'],
                    y=df_quarter['StatisticCrimeGroup'],
                    name=f'{level} - {quarter}',
                    marker_color=color,
                    marker_line_color='black',
                    marker_line_width=1,
                    orientation='h',
                    hoverinfo='text',
                    hovertext=df_quarter.apply(
                        lambda row: f'קבוצת עבירה: {row["StatisticCrimeGroup"]}<br>אחוז הפשיעה: {row["RelativeTikimSum"]}<br>רמת דתיות: {row["Religious level"]}<br>סה"כ תיקים: {row["TikimSum_original"]}',
                        axis=1)
                ))

        fig.update_layout(
            title=f'הקשר בין רמת הדתיות לרמת הפשיעה לפי קבוצת עבירה',
            xaxis_title='אחוז הפשיעה',
            yaxis_title='קבוצת עבירה',
            barmode='stack',
            legend_title='רמת דתיות ותקופה',
            height=2500,
        )

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
        relative_crime_data = df_merged.groupby(['StatisticCrimeType', 'Religious level', 'Quarter']).agg({
            'RelativeTikimSum': 'sum',
            'TikimSum_original': 'sum'
        }).reset_index()
    
        fig = go.Figure()
    
        for level, color in zip(desired_order, color_sequence):
            for quarter in sorted(unique_quarters):
                df_quarter = relative_crime_data[
                    (relative_crime_data['Quarter'] == quarter) & (relative_crime_data['Religious level'] == level)]
                fig.add_trace(go.Bar(
                    x=df_quarter['RelativeTikimSum'],
                    y=df_quarter['StatisticCrimeType'],
                    name=f'{level} - {quarter}',
                    marker_color=color,
                    marker_line_color='black',
                    marker_line_width=1,
                    orientation='h',
                    hoverinfo='text',
                    hovertext=df_quarter.apply(
                        lambda row: f'סוג עבירה: {row["StatisticCrimeType"]}<br>אחוז הפשיעה: {row["RelativeTikimSum"]}<br>רמת דתיות: {row["Religious level"]}<br>סה"כ תיקים: {row["TikimSum_original"]}',
                        axis=1)
                ))

        fig.update_layout(
            title=f'הקשר בין מידת הדתיות של היישוב לרמת הפשיעה לפי {selected_group}',
            xaxis_title='אחוז הפשיעה',
            yaxis_title='סוג עבירה',
            barmode='stack',
            legend_title='רמת דתיות ותקופה',
            height=2500,
        )

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
