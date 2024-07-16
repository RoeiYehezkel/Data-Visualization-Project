import plotly.express as px
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib
import plotly.graph_objects as go
import numpy as np
import os

# Configure Streamlit to use a wide layout
st.set_page_config(layout="wide")

# Fixing Hebrew text orientation for Matplotlib plots
matplotlib.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.family'] = 'Arial'
plt.rcParams['axes.titlepad'] = 20

# Load the grouped data
grouped_data = os.path.join(os.path.dirname(__file__), 'grouped_data.csv')
g = pd.read_csv(grouped_data)

# Aggregating data by Quarter and PoliceDistrict
aggregated_data = g.groupby(['Quarter', 'PoliceDistrict'], as_index=False).sum()

# Load the grouped data by cluster
grouped_data_by_cluster = os.path.join(os.path.dirname(__file__), 'grouped_data_by_cluster.csv')
data = pd.read_csv(grouped_data_by_cluster)

# Load the preprocessed data
preprocessed_data = os.path.join(os.path.dirname(__file__), 'preprocessed_data.csv')
df = pd.read_csv(preprocessed_data)

# Custom CSS to set text direction to right-to-left
st.markdown("""<style>
        html {
            direction: RTL;
            text-align: right;
        }
        h1, h2, h3, h4, h5, h6 {
            text-align: right;
        }
    </style>""", unsafe_allow_html=True)

# Display the main title in Hebrew
st.markdown('<h1 class="rtl-text">כיצד משתנה היקף הפשיעה בישראל בהתאם לאזורים גיאוגרפיים שונים ולתקופות זמן שונות?</h1>', unsafe_allow_html=True)

# Display a description of the dashboard in Hebrew
st.markdown('''
<h3 class="rtl-text">
בדשבורד זה אנו מתמקדים בניתוח מגמות הפשיעה בישראל על פני תקופות זמן שונות ובאזורים גיאוגרפיים מגוונים. 
מטרת הדשבורד היא להבין כיצד היקף הפשיעה משתנה במרוצת השנים ובחלוקה למחוזות המשטרה השונים, כולל התייחסות לאירועים משמעותיים כמו סגרי הקורונה ומבצע שומר החומות.
באמצעות ויזואליזציה זו, ניתן לזהות תבניות ודפוסים בהתפלגות העבירות, ולהשוות בין האזורים השונים בארץ.
</h3>
''', unsafe_allow_html=True)

# Prompt the user to select a police district in Hebrew
st.markdown('''
<h5 class="rtl-text">
בחר את מחוז המשטרה(האם תוכל למצוא תופעות מעניינות במחוז מרכז?):
</h5>
''', unsafe_allow_html=True)

# Define color sequence for districts
color_sequence_district = ["#e41a1c","#377eb8","#4daf4a","#984ea3","#ff7f00","#e7298a","#a65628"]

# Create a line chart for all districts
fig_all_districts = px.line(
    aggregated_data, x='Quarter', y='TikimSum', color='PoliceDistrict',
    title="מגמות התיקים שנפתחו לפי מחוז משטרה",
    color_discrete_sequence=color_sequence_district,
    hover_data={'Quarter': True, 'TikimSum': ':.3s'}
)

# Update layout of the line chart
fig_all_districts.update_layout(
    yaxis_title=dict(
        text="כמות התיקים",
        font=dict(size=20),
        standoff=50  # Increase the text size
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

# Add vertical lines for significant events
fig_all_districts.add_vline(x=6, line=dict(dash='dash', color='blue'), annotation_text='מחאת יוצאי אתיופיה-סלומון טקה', annotation_position='top')
fig_all_districts.add_vline(x=9, line=dict(dash='dash', color='blue'), annotation_text='סגר ראשון', annotation_position='top')
fig_all_districts.add_vline(x=11, line=dict(dash='dash', color='blue'), annotation_text='סגר שני', annotation_position='top')
fig_all_districts.add_vline(x=12, line=dict(dash='dash', color='blue'), annotation_text='סגר שלישי', annotation_position='top')
fig_all_districts.add_vline(x=13, line=dict(dash='dash', color='blue'), annotation_text='שומר החומות', annotation_position='top')

# Update font size for axis ticks
fig_all_districts.for_each_yaxis(lambda yaxis: yaxis.update(tickfont=dict(size=20)))
fig_all_districts.for_each_xaxis(lambda xaxis: xaxis.update(tickfont=dict(size=20)))

# Update hover template for the line chart
fig_all_districts.update_traces(
    hovertemplate='%{x}<br>סכום התיקים=%{y:,}'
)

# Dropdown with an additional "כלל המחוזות" option
options = ["כלל המחוזות"] + list(g['PoliceDistrict'].unique())
selected_district = st.selectbox("", options)

# Display the chart for the selected district or all districts
if selected_district == "כלל המחוזות":
    st.plotly_chart(fig_all_districts)
else:
    # Filter data for the selected district
    district_data = g[g['PoliceDistrict'] == selected_district]
    
    # Aggregate data by Quarter to get the total TikimSum for each quarter
    quarter_totals = district_data.groupby('Quarter')['TikimSum'].sum().reset_index()
    quarter_totals.rename(columns={'TikimSum': 'TotalTikimSum'}, inplace=True)
    
    # Merge the total TikimSum with the district data
    district_data = pd.merge(district_data, quarter_totals, on='Quarter', how='left')
    
    # Create a line chart for the selected district
    fig = px.line(
        district_data, x='Quarter', y='TikimSum', color='PoliceMerhav',
        title=f'מגמות התיקים שנפתחו ב{selected_district}',
        color_discrete_sequence=color_sequence_district,
        hover_data={'Quarter': True, 'TikimSum': ':.3s', 'TotalTikimSum': True}
    )
    
    # Update layout of the line chart
    fig.update_layout(
        yaxis_title=dict(
            text="כמות התיקים",
            font=dict(size=20),
            standoff=75  # Increase the text size
        ), xaxis_title=dict(
            text="רבעון",
            font=dict(size=20)  # Increase the text size
        ), title_x=0.75, legend_title=dict(
            text="מרחב",
            font=dict(size=20)  # Increase the text size
        ), hoverlabel=dict(font_size=20),
        legend=dict(font=dict(size=18))
    )
    
    # Add vertical lines for significant events
    fig.add_vline(x=6, line=dict(dash='dash', color='blue'), annotation_text='מחאת יוצאי אתיופיה-סלומון טקה', annotation_position='top')
    fig.add_vline(x=9, line=dict(dash='dash', color='blue'), annotation_text='סגר ראשון', annotation_position='top')
    fig.add_vline(x=11, line=dict(dash='dash', color='blue'), annotation_text='סגר שני', annotation_position='top')
    fig.add_vline(x=12, line=dict(dash='dash', color='blue'), annotation_text='סגר שלישי', annotation_position='top')
    fig.add_vline(x=13, line=dict(dash='dash', color='blue'), annotation_text='שומר החומות', annotation_position='top')
    
    # Update font size for axis ticks
    fig.for_each_yaxis(lambda yaxis: yaxis.update(tickfont=dict(size=20)))
    fig.for_each_xaxis(lambda xaxis: xaxis.update(tickfont=dict(size=20)))
    
    # Update hover template for the line chart
    fig.update_traces(
        hovertemplate='%{x}<br>סכום התיקים=%{y:,}<br>סכום התיקים הכולל במחוז=%{customdata[0]:,}'
    )
    
    # Display the line chart for the selected district
    st.plotly_chart(fig)

# Prompt the user to select a crime group in Hebrew
st.markdown('''
<h5 class="rtl-text">
בחר את קבוצת הפשיעה:
</h5>
''', unsafe_allow_html=True)

# Get unique crime groups from the data
all_crime_groups = data['StatisticCrimeGroup'].unique()
selected_groups = st.multiselect("", all_crime_groups, default=all_crime_groups)

# Filter data based on selected groups
filtered_data = data[data['StatisticCrimeGroup'].isin(selected_groups)] if selected_groups else pd.DataFrame(columns=data.columns)

# Create a histogram for the selected crime groups
if not filtered_data.empty:
    fig = px.histogram(filtered_data, x='Cluster', y='norm', color='StatisticCrimeGroup', barmode='stack',
                       title=f'התפלגות העבירות הנ"ל לפי האשכול החברתי-כלכלי של היישוב', hover_data={'Cluster': False, 'StatisticCrimeGroup': True, 'norm':':.3s'})
else:
    # Create an empty figure with the same layout
    fig = go.Figure()
    fig.add_trace(go.Bar(x=[], y=[]))
    fig.update_layout(title=f'התפלגות העבירות הנ"ל לפי האשכול החברתי-כלכלי של היישוב')

# Update font size for axis ticks
fig.for_each_yaxis(lambda yaxis: yaxis.update(tickfont=dict(size=18)))
fig.for_each_xaxis(lambda xaxis: xaxis.update(tickfont=dict(size=18)))

# Update x-axis to show ticks for each cluster
fig.update_xaxes(tickmode='linear', tick0=1, dtick=1)

# Update layout of the histogram
fig.update_layout(barmode='relative', bargap=0.2, xaxis_title=dict(
        text="אשכול כלכלי-חברתי",
        font=dict(size=20)  # Increase the text size
    ), yaxis_title=dict(
        text="סכום התיקים המנורמל בגודל האוכלוסייה",
        font=dict(size=20),
        standoff=50  # Increase the text size
    ),
                  legend_title=dict(
        text="קבוצת העבירות",
        font=dict(size=20)  # Increase the text size
    ), title_x=0.7, height=650,hoverlabel=dict(font_size=20),
    legend=dict(font=dict(size=20)))

# Update hover template for the histogram
fig.update_traces(
    hovertemplate='קבוצת העבירה=%{fullData.name}<br>סכום התיקים המנורמל=%{y:,}'
)

# Hide legend if only one crime group is selected
if len(selected_groups) == 1:
    fig.update_layout(showlegend=False)

# Display the histogram
st.plotly_chart(fig)

# Convert 'Quarter' to 'Year' for further analysis
df['Year'] = df['Quarter'].str[:4].astype(int)
data['Year'] = data['Quarter'].str[:4].astype(int)

# Prompt the user to select a crime group in Hebrew
st.markdown('''
<h5 class="rtl-text">
בחר את קבוצת העבירה:
</h5>
''', unsafe_allow_html=True)

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
    color_sequence = [ '#cc4c02', '#ec7014', '#fe9929', '#fee391']
    
    # If 'כלל העבירות' is selected, compute relative crime for all crime groups
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
    fig.for_each_yaxis(lambda yaxis: yaxis.update(tickfont=dict(size=20)))
    fig.for_each_xaxis(lambda xaxis: xaxis.update(tickfont=dict(size=20)))
    
    # Update layout of the bar chart
    fig.update_layout(title_x=0.65, hoverlabel=dict(font_size=15),
                      legend=dict(font=dict(size=18)),
                      legend_title=dict(font=dict(size=20)),
                      yaxis_title=dict(
                          font=dict(size=20),  # Increase the text size
                          standoff=300
                      ),
                      yaxis=dict(
                          autorange='reversed'  # Reverse the y-axis order
                      ))
    
    # Display the bar chart
    st.plotly_chart(fig, use_container_width=True)

# Display a disclaimer in Hebrew
st.markdown('''
<h5 class="rtl-text">
בגרף זה המציגים אינם מנסים להעליל ביצוע עבירות על קבוצות מסוימות מהאוכלוסיה. הסיווג הוא ברמת היישוב, לפי נתוני הלמס
</h5>
''', unsafe_allow_html=True)

# Get unique years from the dataframe
unique_years = df['Year'].unique()

# Add a dropdown to select the crime group
crime_groups = sorted(['כלל העבירות'] + df['StatisticCrimeGroup'].unique().tolist())
selected_group = st.selectbox('', crime_groups)

# Call the function to plot the chart
plot_relative_crime_by_religion_and_group(df, data, selected_group)
