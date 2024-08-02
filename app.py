import streamlit as st
import pandas as pd
import preprocessor,helper
import plotly.express as px
import scipy
import plotly.figure_factory as ff

df = pd.read_csv('athlete_events.csv')
region_df = pd.read_csv('noc_regions.csv')
df = preprocessor.preprocess(df,region_df)
st.sidebar.title("Olympics Analysis")
user_menu = st.sidebar.radio(
    'Select an Option',
    ('Medal Tally','Overall Analysis','Country wise Analysis','Athlete wise Anaysis','Creator Details')
)
if user_menu == 'Medal Tally':
    st.sidebar.header("Medal Tally")
    years,country=helper.country_year_list(df)
    selected_year=st.sidebar.selectbox("Select Year",years)
    selected_country = st.sidebar.selectbox("Select country", country)
    medal_tally = helper.fetch_medal_tally(df,selected_year,selected_country)
    if selected_year == 'overall' and selected_country == 'overall':
        st.title("Overall Tally")
    if selected_year != 'overall' and selected_country == 'overall':
        st.title("Medal Tally in "+ str(selected_year)+" Olympics")
    if selected_year == 'overall' and selected_country != 'overall':
        st.title(selected_country+" overall performance")
    if selected_year != 'overall' and selected_country != 'overall':
        st.title(selected_country+" performance in " + str(selected_year)+" Olympics")
    st.table(medal_tally)
if user_menu == 'Creator Details':
    st.title("Creator Details")
    st.info("Name     : Deepak Shukla")
    st.info("Reg no. : 23BCE11422")
    st.info("ph no.   : 9450160224")
    st.info("Email    : dipakshukla158@gmail.com")
if user_menu == 'Overall Analysis':
    editions = df['Year'].unique().shape[0]-1
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    nations = df['region'].unique().shape[0]

    st.title("Top Statistics")

    col1, col2, col3= st.columns(3)
    with col1:
        st.header("Editions")
        st.title(editions)
    with col2:
        st.header("Hosts")
        st.title(cities)
    with col3:
        st.header("Sports")
        st.title(sports)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Events")
        st.title(events)
    with col2:
        st.header("Nations")
        st.title(nations)
    with col3:
        st.header("Athletes")
        st.title(athletes)
    nations_over_time= helper.data_over_time(df,'region')
    flg = px.line(nations_over_time, x="Year", y="count")
    st.title("Participating Nations Over The Year")
    st.plotly_chart(flg)

    events_over_time = helper.data_over_time(df, 'Event')
    flg = px.line(events_over_time, x="Year", y="count")
    st.title("Events Over The Year")
    st.plotly_chart(flg)

    athlete_over_time = helper.data_over_time(df, 'Name')
    flg = px.line(athlete_over_time, x="Year", y="count")
    st.title("Athletes Over The Year")
    st.plotly_chart(flg)

if user_menu == 'Country wise Analysis':

    st.sidebar.title('Country-wise Analysis')
    country_list=df['region'].dropna().unique().tolist()
    country_list.sort()

    selected_country=st.sidebar.selectbox('select a Country',country_list)

    country_df=helper.yearwise_medal_tally(df,selected_country)
    flg = px.line(country_df, x="Year", y="Medal")
    st.title(selected_country+" Medal Tally Over The Year")
    st.plotly_chart(flg)

if user_menu =='Athlete wise Anaysis':
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    x1 = athlete_df['Age'].dropna()
    x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()
    fig = ff.create_distplot([x1, x2, x3, x4], ['Overall Age', 'Gold Medalist', 'Silver Medalist', 'Bronze Meadlist'],show_hist=False,show_rug=False)
    fig.update_layout(autosize=False,width=1000,height=600)
    st.title("Distribution of Age")
    st.plotly_chart(fig)