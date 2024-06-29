from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd
import logging


# Loading the data
df = pd.read_csv('/content/drive/Shareddrives/visualization/crimes updated.csv')
df = df[~df['Settlement_Council'].isin(['מקום', 'מקום אחר'])]

clusters = pd.read_excel('/content/drive/Shareddrives/visualization/cities_clusters.xlsx')

# Process clusters dataframe
clusters = clusters.iloc[4:]
clusters.columns = clusters.iloc[0]
clusters = clusters.iloc[1:]
clusters = clusters.iloc[:-5]
clusters = clusters.reset_index(drop=True)

# Define clusters
cluster_1 = ['נווה מדבר', 'ערערה-בנגב', 'תל שבע', 'כסיפה', 'אל קסום', 'מודיעין עילית', 'חורה', 'שגב-שלום', 'לקיה', 'ביתר עילית', 'רהט']
cluster_2 = ['עמנואל', 'רכסים', 'בני ברק', "ג'סר א-זרקא", 'כפר מנדא', 'עילוט', 'בית שמש', 'אלעד', 'אום אל-פחם', 'אל - בטוף', 'ביר אל-מכסור', 'צפת', 'משהד', 'עין מאהל', 'קריית יערים', 'מעלה עירון', 'יבנאל', 'נחף', 'שעב', 'ירושלים', 'כפר כנא', 'בסמ"ה', "בועיינה-נוג'ידאת", 'זרזיר', 'בענה', 'מסעדה']
cluster_3 = ['בוקעאתא', 'ריינה', "ע'ג'ר", "ג'לג'וליה", 'אכסאל', 'טובא-זנגרייה', "כעביה-טבאש-חג'אג'רה", "בוסתן אל -מרג'", 'קריית ארבע', 'יפיע', 'בסמת טבעון', 'טמרה', "ג'דיידה-מכר", 'עראבה', 'עין קנייא', 'פוריידיס', 'טורעאן', 'כאבול', 'מגאר', "מג'דל שמס", 'קלנסווה', 'מצפה רמון', 'שבלי - אום אל-גנם', "מג'ד אל-כרום", 'אבו סנאן', 'טייבה', 'שפרעם', 'כסרא-סמיע', 'ירכא', 'אבו גוש', 'אעבלין', 'נתיבות', 'ערד', 'ערערה', 'אופקים', 'כפר קאסם', 'נצרת']
cluster_4 = ['באקה אל-גרביה', 'בית אל', "סח'נין", 'דייר חנא', 'קריית מלאכי', 'דייר אל-אסד', 'טבריה', 'לוד', "סאג'ור", 'כפר ברא', 'מעלה אפרים', 'דבורייה', 'ירוחם', 'מזרעה', 'חצור הגלילית', 'זמר', "כאוכב אבו אל-היג'א", 'קריית גת', "בית ג'ן", 'עכו']
cluster_5 = ["יאנוח-ג'ת", 'טירה', 'חורפיש', 'רמלה', 'מגדל העמק', 'דימונה', 'עספיא', 'בית שאן', 'דאלית אל-כרמל', 'עפולה', 'כפר קרע', "ג'ולס", 'גבעת זאב', 'אשדוד', 'נוף הגליל', 'קצרין', 'קריית ים', 'בת ים', 'שדרות', 'ראמה', 'קריית שמונה', 'הגלבוע', 'כפר יאסיף', 'פקיעין (בוקייעה)', 'אשקלון', 'נחל שורק', "ג'ת", 'הר חברון', 'עיילבון', 'מעלות-תרשיחא', 'מטה בנימין', 'אור עקיבא', 'קדומים', 'באר שבע', 'חריש', 'חבל יבנה', 'חבל אילות', 'שפיר', 'מרום הגליל', 'טירת כרמל', 'זבולון', 'בני עי"ש', 'אור יהודה']
cluster_6 = ['קריית עקרון', 'נתניה', 'מגדל', 'כרמיאל', 'קריית אתא', 'שלומי', 'גוש עציון', 'שדות נגב', 'עמק לוד', 'קרני שומרון', 'גולן', 'אילת', 'חדרה', 'אריאל', 'נהרייה', 'פסוטה', 'מרחבים', 'עמק המעיינות', 'שומרון', 'כפר כמא', 'רמת נגב', 'מעלה אדומים', 'אשכול', 'ערבות הירדן', 'קריית ביאליק']
cluster_7 = ['אליכין', 'עמק הירדן', 'חיפה', 'חולון', 'קריית מוצקין', "ג'ש (גוש חלב)", 'מגידו', 'יבנה', 'אפרת', 'הגליל התחתון', 'מטה אשר', 'אזור', 'בית דגן', 'הגליל העליון', 'לכיש', 'פתח תקווה', 'משגב', 'ראש פינה', 'מנשה', 'נשר', 'רחובות', 'תמר', 'חוף אשקלון', 'מעלה יוסף', 'מגילות ים המלח', 'פרדס חנה-כרכור', 'גדרה', 'ראשון לציון', 'גן יבנה', 'מטה יהודה', 'יקנעם עילית', 'ראש העין', 'מבואות החרמון', 'כפר יונה', 'באר יעקב', 'מעיליא', 'הערבה התיכונה', 'באר טוביה', 'בית אריה-עופרים', 'חבל מודיעין', 'מטולה', 'שער הנגב', 'חוף הכרמל', 'בני שמעון', 'יסוד המעלה', 'יהוד']
cluster_8 = ['אלקנה', 'רמת גן', 'יואב', 'גבעת שמואל', 'עמק יזרעאל', 'גזר', 'זכרון יעקב', 'מבשרת ציון', 'אלונה', 'תל אביב -יפו', 'אלפי מנשה', 'לב השרון', 'עמק חפר', 'כפר סבא', 'רעננה', 'קריית טבעון', 'הרצלייה', 'קדימה-צורן', 'ברנר', 'מזכרת בתיה', 'בנימינה-גבעת עדה', 'אורנית', 'רמת ישי', 'נס ציונה', 'גן רווה', 'כפר תבור']
cluster_9 = ['חוף השרון', 'דרום השרון', 'מודיעין-מכבים-רעות', 'תל מונד', 'גני תקווה', 'פרדסייה', 'כפר ורדים', 'גבעתיים', 'אבן יהודה', 'מיתר', 'הוד השרון', 'קריית אונו', 'רמת השרון', 'שוהם', 'גדרות', 'הר אדר']
cluster_10 = ['כוכב יאיר', 'עומר', 'להבים', 'כפר שמריהו', 'סביון']

# Combine clusters into one dictionary
clusters = {
    1: cluster_1,
    2: cluster_2,
    3: cluster_3,
    4: cluster_4,
    5: cluster_5,
    6: cluster_6,
    7: cluster_7,
    8: cluster_8,
    9: cluster_9,
    10: cluster_10
}

# Update the DataFrame
for i in range(1, 11):
    df.loc[df['Settlement_Council'].isin(clusters[i]), 'Cluster'] = i

# Define Religion
cluster_jew = ["אבן יהודה", "אופקים", "אור יהודה", "אור עקיבא", "אורנית", "אזור", "אילת", "אלעד", "אלפי מנשה", "אפרת", "אריאל", "אשדוד", "אשקלון", "באר יעקב", "באר שבע", "בית אל", "בית אריה-עופרים", "בית דגן", "בית שאן", "בית שמש", "ביתר עילית", "בני ברק", "בני עיש", "בנימינה-גבעת עדה*", "בת חפר", "בת ים", "גבע בנימין", "גבעת זאב", "גבעת שמואל", "גבעתיים", "גדרה", "גן יבנה", "גני תקווה", "דימונה", "הוד השרון", "הרצלייה", "זכרון יעקב", "חדרה", "חולון", "חיפה", "חצור הגלילית", "חריש", "טבריה", "טירת כרמל", "טלמון", "יבנה", "יהוד-מונוסון", "יקנעם עילית", "ירוחם", "ירושלים", "כוכב יאיר", "כוכב יעקב", "כפר ורדים", "כפר חבד", "כפר יונה", "כפר סבא", "כרמיאל", "להבים", "לוד", "מבשרת ציון", "מגדל העמק", "מודיעין עילית", "מודיעין-מכבים-רעות*", "מזכרת בתיה", "מיתר", "מעלה אדומים", "מעלות-תרשיחא", "מצפה רמון", "נהרייה", "נוף הגליל", "נס ציונה", "נשר", "נתיבות", "נתניה", "עומר", "עכו", "עפולה", "ערד", "עתלית", "פרדס חנה-כרכור", "פרדסייה", "פתח תקווה", "צור הדסה", "צור יצחק", "צפת", "קדימה-צורן", "קיסריה", "קצרין", "קריית אונו", "קריית ארבע", "קריית אתא", "קריית ביאליק", "קריית גת", "קריית טבעון", "קריית ים", "קריית יערים", "קריית מוצקין", "קריית מלאכי", "קריית עקרון", "קריית שמונה", "קרני שומרון", "ראש העין", "ראשון לציון", "רחובות", "רכסים", "רמלה", "רמת גן", "רמת השרון", "רמת ישי", "רעננה", "שדרות", "שוהם", "שילה", "שלומי", "שערי תקווה", "תל אביב -יפו", "תל מונד"]
cluster_druzim = ["בוקעאתא", "בית ג'ן", "ג'ולס", "דאלית אל-כרמל", "חורפיש", "יאנוח-ג'ת", "ירכא", "כסרא-סמיע", "מג'דל שמס", "מגאר", "עספיא", "פקיעין (בוקייעה)"]
cluster_muslim = ["אבו גוש", "אבו סנאן", "אום אל-פחם", "אכסאל", "אל סייד", "אעבלין", "באקה אל-גרביה", "בועיינה-נוג'ידאת", "ביר אל-מכסור", "בסמה", "בסמת טבעון", "בענה", "ג'דיידה-מכר", "ג'לג'וליה", "ג'סר א-זרקא", "ג'ת", "גרים מחוץ ליישובים במחוז דרום", "דבורייה", "דייר אל-אסד", "דייר חנא", "זמר", "זרזיר", "חורה", "טובא-זנגרייה", "טורעאן", "טייבה", "טירה", "טמרה", "יפיע", "כאבול", "כסיפה", "כעביה-טבאש-חג'אג'רה", "כפר כנא", "כפר מנדא", "כפר קאסם", "כפר קרע", "לקיה", "מג'ד אל-כרום", "מעלה עירון", "משהד", "נחף", "נצרת", "סח'נין", "עילוט", "עין מאהל", "עראבה", "ערערה", "ערערה-בנגב", "פוריידיס", "קלנסווה", "רהט", "ריינה", "שבלי - אום אל-גנם", "שגב-שלום", "שעב", "שפרעם", "תל שבע"]

# Combine clusters into one dictionary
clusters = {
    "יהודים": cluster_jew,
    "דרוזים": cluster_druzim,
    "מוסלמים": cluster_muslim
}

# Update the DataFrame
for i, cluster in clusters.items():
    df.loc[df['Settlement_Council'].isin(cluster), 'Religion'] = i

# Define Religious Level
cluster_secular = ["אבן יהודה", "אור עקיבא", "אורנית", "אזור", "אילת", "אלפי מנשה", "אריאל", "אשדוד", "אשקלון", "באר יעקב", "באר שבע", "בית אריה-עופרים", "בית דגן", "בני עיש", "בנימינה-גבעת עדה*", "בת חפר", "בת ים", "גבעתיים", "גדרה", "גן יבנה", "גני תקווה", "הוד השרון", "הרצלייה", "זכרון יעקב", "חדרה", "חולון", "חיפה", "חריש", "טירת כרמל", "יבנה", "יהוד-מונוסון", "יקנעם עילית", "כוכב יאיר", "כפר ורדים", "כפר יונה", "כפר סבא", "כרמיאל", "להבים", "מבשרת ציון", "מגדל העמק", "מודיעין-מכבים-רעות*", "מזכרת בתיה", "מיתר", "מעלות-תרשיחא", "מצפה רמון", "נהרייה", "נוף הגליל", "נס ציונה", "נשר", "נתניה", "עומר", "עכו", "עפולה", "ערד", "עתלית", "פרדס חנה-כרכור", "פרדסייה", "פתח תקווה", "צור הדסה", "צור יצחק", "קדימה-צורן", "קיסריה", "קצרין", "קריית אונו", "קריית אתא", "קריית ביאליק", "קריית טבעון", "קריית ים", "קריית מוצקין", "ראמה", "ראש העין", "ראשון לציון", "רחובות", "רמת גן", "רמת השרון", "רמת ישי", "רעננה", "שוהם", "שלומי", "שערי תקווה", "תל אביב -יפו", "תל מונד"]
cluster_traditional = ["אבו סנאן", "אום אל-פחם", "אופקים", "אור יהודה", "אכסאל", "אל סייד", "אעבלין", "בועיינה-נוג'ידאת", "בוקעאתא", "ביר אל-מכסור", "בית ג'ן", "בית שאן", "בסמה", "בסמת טבעון", "בענה", "ג'דיידה-מכר", "ג'ולס", "ג'לג'וליה", "ג'סר א-זרקא", "ג'ת", "דאלית אל-כרמל", "דבורייה", "דייר אל-אסד", "דייר חנא", "דימונה", "זרזיר", "חורפיש", "חצור הגלילית", "טבריה", "טובא-זנגרייה", "טורעאן", "טייבה", "טירה", "טמרה", "יאנוח-ג'ת", "יפיע", "ירוחם", "ירכא", "כאבול", "כעביה-טבאש-חג'אג'רה", "כפר יאסיף", "כפר כנא", "כפר מנדא", "כפר קאסם", "כפר קרע", "לוד", "לקיה", "מג'ד אל-כרום", "מגאר", "מעלה אדומים", "מעלה עירון", "משהד", "נחף", "נצרת", "סח'נין", "עיילבון", "עילוט", "עין מאהל", "עספיא", "עראבה", "ערערה", "ערערה-בנגב", "פוריידיס", "פקיעין (בוקייעה)", "קלנסווה", "קריית גת", "קריית מלאכי", "קריית עקרון", "קריית שמונה", "ריינה", "רמלה", "שגב-שלום", "שדרות", "שעב", "שפרעם"]
cluster_religious = ["אבו גוש", "אפרת", "באקה אל-גרביה", "בית אל", "גבע בנימין", "גבעת שמואל", "זמר", "חורה", "טלמון", "ירושלים", "כסיפה", "כסרא-סמיע", "קריית ארבע", "קרני שומרון", "רהט", "שבלי - אום אל-גנם", "שילה", "תל שבע"]
cluster_haredim = ["אלעד", "בית שמש", "ביתר עילית", "בני ברק", "גבעת זאב", "כוכב יעקב", "כפר חבד", "מודיעין עילית", "נתיבות", "צפת", "קריית יערים", "רכסים"]

# Combine clusters into one dictionary
clusters = {
    "חילונים": cluster_secular,
    "מסורתיים": cluster_traditional,
    "דתיים": cluster_religious,
    "חרדים": cluster_haredim
}

# Update the DataFrame with cluster keys
for key, cluster in clusters.items():
    df.loc[df['Settlement_Council'].isin(cluster), 'Religious level'] = key

# Drop missing values
df = df.dropna()

# Load additional dataset
df2 = pd.read_csv('/content/drive/Shareddrives/visualization/selected-data-by-localities-and-statistical-areas-2022-census.csv')
df2 = df2[df2['StatArea'].isna()]
df2 = df2[df2['LocNameHeb'] != 'כלל ארצי']

# Group data
g = df.groupby(['Quarter', 'PoliceDistrict', 'PoliceMerhav']).agg({'TikimSum': 'sum'}).reset_index()

# Calculate normalized values
data = df.groupby(['StatisticCrimeGroup', 'Cluster', 'Quarter']).agg({'TikimSum': 'sum'}).reset_index()

dct = {}
for city in df['Settlement_Council'].unique():
    c = int(list(df[df['Settlement_Council'] == city]['Cluster'].unique())[0])
    try:
        pop = list(df2[df2['LocNameHeb'] == city]['pop_approx'])[0]
    except:
        if city == 'נהריה':
            pop = list(df2[df2['LocNameHeb'] == 'נהרייה']['pop_approx'])[0]
        elif city == 'בנימינה-גבעת עדה':
            pop = list(df2[df2['LocNameHeb'] == 'בנימינה-גבעת עדה*']['pop_approx'])[0]
        elif city == 'מודיעין-מכבים-רעות':
            pop = list(df2[df2['LocNameHeb'] == 'מודיעין-מכבים-רעות*']['pop_approx'])[0]
        elif city == 'תל אביב יפו':
            pop = list(df2[df2['LocNameHeb'] == 'תל אביב -יפו']['pop_approx'])[0]
        elif city == 'הרצליה':
            pop = list(df2[df2['LocNameHeb'] == 'הרצלייה']['pop_approx'])[0]
    t = df[df['Settlement_Council'] == city]['TikimSum'].sum()
    dct[city] = (c, pop, t)

df_new = pd.DataFrame.from_dict(dct, orient='index', columns=['Cluster', 'Population', 'TikimSum'])
df_new = df_new.reset_index().rename(columns={'index': 'Settlement_Council'})

new_g = df_new.groupby(['Cluster']).agg({'TikimSum': 'sum', 'Population': 'sum'}).reset_index()
gen_pop = new_g['Population'].sum()
new_g['norm'] = new_g['TikimSum'] / new_g['Population']
new_g['norm_fac'] = new_g['Population'] / gen_pop
new_g['norm_t'] = new_g['TikimSum'] * new_g['norm_fac']

for index, row in data.iterrows():
    norm_fac_value = new_g[new_g['Cluster'] == row['Cluster']]['norm_fac'].values
    if len(norm_fac_value) > 0:
        data.loc[index, 'norm'] = row['TikimSum'] * norm_fac_value[0]

df.loc[df['Settlement_Council'] == 'הרצליה', 'Settlement_Council'] = 'הרצלייה'
df.loc[df['Settlement_Council'] == 'נהריה', 'Settlement_Council'] = 'נהרייה'
df.loc[df['Settlement_Council'] == 'בנימינה-גבעת עדה', 'Settlement_Council'] = 'בנימינה-גבעת עדה*'
df.loc[df['Settlement_Council'] == 'תל אביב יפו', 'Settlement_Council'] = 'תל אביב -יפו'
df.loc[df['Settlement_Council'] == 'מודיעין-מכבים-רעות', 'Settlement_Council'] = 'מודיעין-מכבים-רעות*'

g3 = df.groupby(['Settlement_Council']).agg({'TikimSum': 'sum'}).reset_index()
j = g3.merge(df2, left_on='Settlement_Council', right_on='LocNameHeb', how='left')
j['normalized'] = j['TikimSum'] / j['pop_approx']

numeric_columns = j.select_dtypes(exclude=['object']).columns
numeric_df = j[numeric_columns]
correlation_matrix = numeric_df.corr()
correlations = numeric_df.corrwith(numeric_df['normalized']).sort_values(ascending=False)

# Save updated dataframe
df.to_csv('crimes_updated_n.csv', index=False)

# Scatter plot
px.scatter(j, x='own_pcnt', y='TikimSum')


# Assuming g, data, and df are your dataframes

app = Dash(__name__)

# Create the layout
app.layout = html.Div([
    html.H1("Crime Statistics Dashboard", style={'textAlign': 'center'}),

    html.Div([
        html.H2("App 1: Police District Trends"),
        dcc.Dropdown(g['PoliceDistrict'].unique(), id='dropdown-app1', placeholder="Select Police District"),
        dcc.Graph(id='line-chart-app1')
    ], style={'marginBottom': '40px'}),

    html.Div([
        html.H2("App 2: Crime Group Distribution"),
        dcc.Dropdown(data['StatisticCrimeGroup'].unique(), id='dropdown-app2', multi=True, value=['עבירות כלפי הרכוש'],
                     placeholder="Select Crime Groups"),
        dcc.Graph(id='bar-chart-app2')
    ], style={'marginBottom': '40px'}),

    html.Div([
        html.H2("App 3: Crime Type Boxplot"),
        dcc.Dropdown(df['StatisticCrimeGroup'].unique(), id='dropdown-app3', placeholder="Select Statistic Crime Group",
                     value='עבירות כלכליות'),
        dcc.RangeSlider(
            id='quarter-slider-app3',
            min=0,
            max=len(df['Quarter'].unique()) - 1,
            value=[0, len(df['Quarter'].unique()) - 1],
            marks={i: quarter for i, quarter in enumerate(sorted(df['Quarter'].unique()))},
            step=None
        ),
        dcc.Graph(id='boxplot-chart-app3')
    ])
])


# Callbacks for App 1
@app.callback(
    Output('line-chart-app1', 'figure'),
    [Input('dropdown-app1', 'value')]
)
def update_line_chart_app1(selected_column):
    if not selected_column:
        return px.line(title="Please select a Police District")
    fig = px.line(g[g['PoliceDistrict'] == selected_column], x='Quarter', y='TikimSum',
                  title=f'מגמות התיקים שנפתחו ב{selected_column}',
                  color='PoliceMerhav', color_discrete_sequence=px.colors.qualitative.Plotly,
                  hover_data={'Quarter': False})
    fig.update_layout(yaxis_title='כמות התיקים', xaxis_title='רבעון', hovermode="x unified", height=400)
    return fig


# Callbacks for App 2
@app.callback(
    Output('bar-chart-app2', 'figure'),
    [Input('dropdown-app2', 'value')]
)
def update_line_chart_app2(selected_columns):
    if not selected_columns:
        return px.bar(title="Please select at least one Crime Group")
    filtered_data = data[data['StatisticCrimeGroup'].isin(selected_columns)]
    total_norm = filtered_data.groupby('StatisticCrimeGroup')['norm'].sum().sort_values(ascending=False).index
    fig = px.histogram(filtered_data, x='Cluster', y='norm', color='StatisticCrimeGroup', barmode='stack',
                       color_discrete_sequence=px.colors.qualitative.Plotly,
                       category_orders={'StatisticCrimeGroup': total_norm},
                       title=f'התפלגות {", ".join(selected_columns)} על פני האשכול החברתי-כלכלי של יישובים',
                       hover_data={'Cluster': False})
    fig.update_xaxes(tickmode='linear', tick0=1, dtick=1)
    fig.update_traces(marker=dict(line=dict(color='black', width=0.5)))
    fig.update_layout(barmode='relative', xaxis_title='אשכול כלכלי-חברתי',
                      yaxis_title='סכום התיקים המנורמל בגודל האוכלוסיה', legend_title_text='Crime Group', height=400)
    fig.update_layout(hoverlabel=dict(bgcolor='rgba(255,255,255,0.8)', font_size=12, font_family='Arial'),
                      hovermode="x unified")
    return fig


# Callbacks for App 3
@app.callback(
    Output('boxplot-chart-app3', 'figure'),
    [Input('dropdown-app3', 'value'), Input('quarter-slider-app3', 'value')]
)
def update_boxplot_app3(selected_group, selected_quarter_range):
    try:
        if selected_group is None:
            return px.box(title="Please select a Statistic Crime Group")

        quarters = sorted(df['Quarter'].unique())
        selected_start_quarter = quarters[selected_quarter_range[0]]
        selected_end_quarter = quarters[selected_quarter_range[1]]

        filtered_data = df[(df['StatisticCrimeGroup'] == selected_group) &
                           (df['Quarter'] >= selected_start_quarter) &
                           (df['Quarter'] <= selected_end_quarter)]

        if filtered_data.empty:
            logging.warning("No data available for the selected filters.")
            return px.box(title="No data available for the selected filters")

        filtered_data_grouped = filtered_data.groupby(['Quarter', 'Settlement_Council', 'StatisticCrimeType']).agg(
            {'TikimSum': 'sum'}).reset_index()
        filtered_data_total = filtered_data.groupby(['Quarter', 'Settlement_Council']).agg(
            {'TikimSum': 'sum'}).reset_index().rename(columns={'TikimSum': 'TotalTikimSum'})
        filtered_data_merged = pd.merge(filtered_data_grouped, filtered_data_total,
                                        on=['Quarter', 'Settlement_Council'])
        filtered_data_merged['Ratio'] = filtered_data_merged['TikimSum'] / filtered_data_merged['TotalTikimSum']
        filtered_data_merged = pd.merge(filtered_data_merged, df[
            ['Quarter', 'Settlement_Council', 'StatisticCrimeType', 'Religion', 'Religious level',
             'Cluster']].drop_duplicates(),
                                        on=['Quarter', 'Settlement_Council', 'StatisticCrimeType'])
        filtered_data_merged = filtered_data_merged[filtered_data_merged['TotalTikimSum'] >= 3]

        fig = px.box(filtered_data_merged, x='StatisticCrimeType', y='Ratio', color='Religious level',
                     color_discrete_sequence=px.colors.qualitative.Plotly,
                     hover_data={'Settlement_Council': True, 'Religion': True, 'Religious level': False,
                                 'TikimSum': True, 'Quarter': True, 'StatisticCrimeType': False},
                     title=f'התפלגות {selected_group} from {selected_start_quarter} to {selected_end_quarter}')
        fig.update_layout(yaxis_title=f'החלק  מתוך {selected_group}', xaxis_title='העבירה', height=400)

        return fig

    except Exception as e:
        logging.error(f"Error updating boxplot: {e}")
        return px.box(title="Error generating the chart")


if __name__ == '__main__':
    app.run_server(debug=True)