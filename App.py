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

# csv_path = os.path.join(os.path.dirname(__file__), 'crimes_updated.csv')
# df = pd.read_csv(csv_path)
# df = df[~df['Settlement_Council'].isin(['מקום', 'מקום אחר'])]


# excel_path = os.path.join(os.path.dirname(__file__), 'cities_clusters.xlsx')
# clusters = pd.read_excel(excel_path)


# # Define clusters
# cluster_1 = ['נווה מדבר', 'ערערה-בנגב', 'תל שבע', 'כסיפה', 'אל קסום', 'מודיעין עילית', 'חורה', 'שגב-שלום', 'לקיה', 'ביתר עילית', 'רהט']
# cluster_2 = ['עמנואל', 'רכסים', 'בני ברק', "ג'סר א-זרקא", 'כפר מנדא', 'עילוט', 'בית שמש', 'אלעד', 'אום אל-פחם', 'אל - בטוף', 'ביר אל-מכסור', 'צפת', 'משהד', 'עין מאהל', 'קריית יערים', 'מעלה עירון', 'יבנאל', 'נחף', 'שעב', 'ירושלים', 'כפר כנא', 'בסמ"ה', "בועיינה-נוג'ידאת", 'זרזיר', 'בענה', 'מסעדה']
# cluster_3 = ['בוקעאתא', 'ריינה', "ע'ג'ר", "ג'לג'וליה", 'אכסאל', 'טובא-זנגרייה', "כעביה-טבאש-חג'אג'רה", "בוסתן אל -מרג'", 'קריית ארבע', 'יפיע', 'בסמת טבעון', 'טמרה', "ג'דיידה-מכר", 'עראבה', 'עין קנייא', 'פוריידיס', 'טורעאן', 'כאבול', 'מגאר', "מג'דל שמס", 'קלנסווה', 'מצפה רמון', 'שבלי - אום אל-גנם', "מג'ד אל-כרום", 'אבו סנאן', 'טייבה', 'שפרעם', 'כסרא-סמיע', 'ירכא', 'אבו גוש', 'אעבלין', 'נתיבות', 'ערד', 'ערערה', 'אופקים', 'כפר קאסם', 'נצרת']
# cluster_4 = ['באקה אל-גרביה', 'בית אל', "סח'נין", 'דייר חנא', 'קריית מלאכי', 'דייר אל-אסד', 'טבריה', 'לוד', "סאג'ור", 'כפר ברא', 'מעלה אפרים', 'דבורייה', 'ירוחם', 'מזרעה', 'חצור הגלילית', 'זמר', "כאוכב אבו אל-היג'א", 'קריית גת', "בית ג'ן", 'עכו']
# cluster_5 = ["יאנוח-ג'ת", 'טירה', 'חורפיש', 'רמלה', 'מגדל העמק', 'דימונה', 'עספיא', 'בית שאן', 'דאלית אל-כרמל', 'עפולה', 'כפר קרע', "ג'ולס", 'גבעת זאב', 'אשדוד', 'נוף הגליל', 'קצרין', 'קריית ים', 'בת ים', 'שדרות', 'ראמה', 'קריית שמונה', 'הגלבוע', 'כפר יאסיף', 'פקיעין (בוקייעה)', 'אשקלון', 'נחל שורק', "ג'ת", 'הר חברון', 'עיילבון', 'מעלות-תרשיחא', 'מטה בנימין', 'אור עקיבא', 'קדומים', 'באר שבע', 'חריש', 'חבל יבנה', 'חבל אילות', 'שפיר', 'מרום הגליל', 'טירת כרמל', 'זבולון', 'בני עיש', 'אור יהודה']
# cluster_6 = ['קריית עקרון', 'נתניה', 'מגדל', 'כרמיאל', 'קריית אתא', 'שלומי', 'גוש עציון', 'שדות נגב', 'עמק לוד', 'קרני שומרון', 'גולן', 'אילת', 'חדרה', 'אריאל', 'נהרייה', 'פסוטה', 'מרחבים', 'עמק המעיינות', 'שומרון', 'כפר כמא', 'רמת נגב', 'מעלה אדומים', 'אשכול', 'ערבות הירדן', 'קריית ביאליק']
# cluster_7 = ['אליכין', 'עמק הירדן', 'חיפה', 'חולון', 'קריית מוצקין', "ג'ש (גוש חלב)", 'מגידו', 'יבנה', 'אפרת', 'הגליל התחתון', 'מטה אשר', 'אזור', 'בית דגן', 'הגליל העליון', 'לכיש', 'פתח תקווה', 'משגב', 'ראש פינה', 'מנשה', 'נשר', 'רחובות', 'תמר', 'חוף אשקלון', 'מעלה יוסף', 'מגילות ים המלח', 'פרדס חנה-כרכור', 'גדרה', 'ראשון לציון', 'גן יבנה', 'מטה יהודה', 'יקנעם עילית', 'ראש העין', 'מבואות החרמון', 'כפר יונה', 'באר יעקב', 'מעיליא', 'הערבה התיכונה', 'באר טוביה', 'בית אריה-עופרים', 'חבל מודיעין', 'מטולה', 'שער הנגב', 'חוף הכרמל', 'בני שמעון', 'יסוד המעלה', 'יהוד']
# cluster_8 = ['אלקנה', 'רמת גן', 'יואב', 'גבעת שמואל', 'עמק יזרעאל', 'גזר', 'זכרון יעקב', 'מבשרת ציון', 'אלונה', 'תל אביב -יפו', 'אלפי מנשה', 'לב השרון', 'עמק חפר', 'כפר סבא', 'רעננה', 'קריית טבעון', 'הרצלייה', 'קדימה-צורן', 'ברנר', 'מזכרת בתיה', 'בנימינה-גבעת עדה', 'אורנית', 'רמת ישי', 'נס ציונה', 'גן רווה', 'כפר תבור']
# cluster_9 = ['חוף השרון', 'דרום השרון', 'מודיעין-מכבים-רעות', 'תל מונד', 'גני תקווה', 'פרדסייה', 'כפר ורדים', 'גבעתיים', 'אבן יהודה', 'מיתר', 'הוד השרון', 'קריית אונו', 'רמת השרון', 'שוהם', 'גדרות', 'הר אדר']
# cluster_10 = ['כוכב יאיר', 'עומר', 'להבים', 'כפר שמריהו', 'סביון']

# # Combine clusters into one dictionary
# clusters = {
#     1: cluster_1,
#     2: cluster_2,
#     3: cluster_3,
#     4: cluster_4,
#     5: cluster_5,
#     6: cluster_6,
#     7: cluster_7,
#     8: cluster_8,
#     9: cluster_9,
#     10: cluster_10
# }

# # Update the DataFrame
# for i in range(1, 11):
#     df.loc[df['Settlement_Council'].isin(clusters[i]), 'Cluster'] = i


# Drop missing values
# df = df.dropna()

# # Load additional dataset
# csv_path_2 = os.path.join(os.path.dirname(__file__), 'selected-data-by-localities-and-statistical-areas-2022-census.csv')

# df2 = pd.read_csv(csv_path_2)
# df2 = df2[df2['StatArea'].isna()]
# df2 = df2[df2['LocNameHeb'] != 'כלל ארצי']

# df2 = df2[['LocNameHeb', 'ReligionHeb', 'hh_MidatDatiyut', 'pop_approx']]
# df2.rename(columns={'ReligionHeb': 'Religion', 'hh_MidatDatiyut': 'Religious level'}, inplace=True)

# # Merge only the necessary columns from df2 into df
# df = df.merge(df2[['LocNameHeb', 'Religion', 'Religious level', 'pop_approx']], left_on='Settlement_Council', right_on='LocNameHeb', how='left')
# # Drop the redundant 'LocNameHeb' column after the merge
# df.drop(columns=['LocNameHeb'], inplace=True)


grouped_data=os.path.join(os.path.dirname(__file__), 'grouped_data.csv')
g = pd.read_csv(grouped_data)


grouped_data_by_cluster=os.path.join(os.path.dirname(__file__), 'grouped_data_by_cluster.csv')
data = pd.read_csv(grouped_data_by_cluster)


# # Normalization and merging code
# dct = {}
# for city in df['Settlement_Council'].unique():
#     c = int(list(df[df['Settlement_Council'] == city]['Cluster'].unique())[0])
#     try:
#         pop = list(df2[df2['LocNameHeb'] == city]['pop_approx'])[0]
#     except:
#         if city == 'נהריה':
#             pop = list(df2[df2['LocNameHeb'] == 'נהרייה']['pop_approx'])[0]
#         elif city == 'בנימינה-גבעת עדה':
#             pop = list(df2[df2['LocNameHeb'] == 'בנימינה-גבעת עדה*']['pop_approx'])[0]
#         elif city == 'מודיעין-מכבים-רעות':
#             pop = list(df2[df2['LocNameHeb'] == 'מודיעין-מכבים-רעות*']['pop_approx'])[0]
#         elif city == 'תל אביב יפו':
#             pop = list(df2[df2['LocNameHeb'] == 'תל אביב -יפו']['pop_approx'])[0]
#         elif city == 'הרצליה':
#             pop = list(df2[df2['LocNameHeb'] == 'הרצלייה']['pop_approx'])[0]
#     t = df[df['Settlement_Council'] == city]['TikimSum'].sum()
#     dct[city] = (c, pop, t)

# df_new = pd.DataFrame.from_dict(dct, orient='index', columns=['Cluster', 'Population', 'TikimSum'])
# df_new = df_new.reset_index().rename(columns={'index': 'Settlement_Council'})

# new_g = df_new.groupby(['Cluster']).agg({'TikimSum': 'sum', 'Population': 'sum'}).reset_index()
# gen_pop = new_g['Population'].sum()
# new_g['norm'] = new_g['TikimSum'] / new_g['Population']
# new_g['norm_fac'] = new_g['Population'] / gen_pop
# new_g['norm_t'] = new_g['TikimSum'] * new_g['norm_fac']

# for index, row in data.iterrows():
#     norm_fac_value = new_g[new_g['Cluster'] == row['Cluster']]['norm_fac'].values
#     if len(norm_fac_value) > 0:
#         data.loc[index, 'norm'] = row['TikimSum'] * norm_fac_value[0]

# df.loc[df['Settlement_Council'] == 'הרצליה', 'Settlement_Council'] = 'הרצלייה'
# df.loc[df['Settlement_Council'] == 'נהריה', 'Settlement_Council'] = 'נהרייה'
# df.loc[df['Settlement_Council'] == 'בנימינה-גבעת עדה', 'Settlement_Council'] = 'בנימינה-גבעת עדה*'
# df.loc[df['Settlement_Council'] == 'תל אביב יפו', 'Settlement_Council'] = 'תל אביב -יפו'
# df.loc[df['Settlement_Council'] == 'מודיעין-מכבים-רעות', 'Settlement_Council'] = 'מודיעין-מכבים-רעות*'

# g3 = df.groupby(['Settlement_Council']).agg({'TikimSum': 'sum'}).reset_index()
# j = g3.merge(df2, left_on='Settlement_Council', right_on='LocNameHeb', how='left')
# j['normalized'] = j['TikimSum'] / j['pop_approx']

preprocessed_data=os.path.join(os.path.dirname(__file__), 'preprocessed_data.csv')
df = pd.read_csv(preprocessed_data)

geojson=os.path.join(os.path.dirname(__file__), 'geojson.json')
geojson_data = pd.read_json(geojson)


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
    merged_df = pd.merge(df, data, on=['StatisticCrimeGroup', 'Cluster', 'Quarter'], suffixes=('_original', '_norm'))

    # Ensure Quarter is treated as a categorical variable with a specific order
    merged_df['Quarter'] = pd.Categorical(merged_df['Quarter'], ordered=True, categories=sorted(df['Quarter'].unique()))
    # Sort the 'Religious level' column lexicographically
    merged_df['Religious level'] = pd.Categorical(merged_df['Religious level'], categories=sorted(merged_df['Religious level'].unique(), key=lambda x: x.encode('utf-8')), ordered=True)
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

