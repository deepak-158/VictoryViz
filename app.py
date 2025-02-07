import streamlit as st
import pandas as pd
import preprocessor, helper
import plotly.express as px
import plotly.figure_factory as ff


st.markdown("""
    <style>
    /* Set Background Color */
    .main {
        background-color:rgb(100, 159, 248);
    }

    /* Sidebar Styling */
    .sidebar .sidebar-content {
        background: #003366;
        color: white;
        font-family: 'Arial', sans-serif;
    }
    .sidebar .css-1d391kg {
        color: white;
        font-size: 16px;
        font-weight: bold;
    }

    /* Titles & Headers */
    h1, h2, h3, h4 {
        color: #003366;
        font-family: 'Georgia', serif;
    }

    /* Metric Box Styling */
    .st-emotion-cache-1kyxreq {
        border: 2px solid #003366 !important;
        border-radius: 10px;
        background: #e3eaf5;
        font-family: 'Verdana', sans-serif;
        font-weight: bold;
    }

    /* Buttons */
    .stButton>button {
        background-color: #003366;
        color: white;
        border-radius: 10px;
        font-size: 16px;
        font-family: 'Arial', sans-serif;
        font-weight: bold;
    }

    /* Tables */
    .dataframe {
        font-family: 'Courier New', monospace;
        font-size: 14px;
        color: #333;
    }

    </style>
    """, unsafe_allow_html=True)


df = pd.read_csv('athlete_events.csv')
region_df = pd.read_csv('noc_regions.csv')
df = preprocessor.preprocess(df, region_df)
st.markdown("<h1 style='text-align: center; color: #2C3E50; margin-bottom: 0;'>🏅 VictoryViz</h1>", unsafe_allow_html=True)

st.sidebar.title("    🏅 Victory Viz")
st.sidebar.subheader("The Ultimate Olympic Analysis")

user_menu = st.sidebar.radio(
    '📊 Select an Option:',
    ('🏆 Medal Tally', '🌎 Overall Analysis', '📌 Country-wise Analysis', '🏅 Athlete-wise Analysis')
)


if user_menu == '🏆 Medal Tally':
    st.sidebar.header("🏅 Medal Tally")
    years, country = helper.country_year_list(df)
    
    selected_year = st.sidebar.selectbox("Select Year", years)
    selected_country = st.sidebar.selectbox("Select Country", country)
    
    medal_tally = helper.fetch_medal_tally(df, selected_year, selected_country)

   
    st.title(f"🎖️ {selected_country} Performance in {selected_year} Olympics" if selected_year != 'overall' else "🏅 Overall Medal Tally")
    
    
    col1, col2, col3 = st.columns(3)
    col1.metric(label="🥇 Gold", value=medal_tally['Gold'].sum())
    col2.metric(label="🥈 Silver", value=medal_tally['Silver'].sum())
    col3.metric(label="🥉 Bronze", value=medal_tally['Bronze'].sum())

    st.table(medal_tally)




if user_menu == '🌎 Overall Analysis':
    st.title("📊 Top Statistics")
    editions = df['Year'].nunique() - 1
    cities = df['City'].nunique()
    sports = df['Sport'].nunique()
    events = df['Event'].nunique()
    athletes = df['Name'].nunique()
    nations = df['region'].nunique()

    col1, col2, col3 = st.columns(3)
    col1.metric(label="🎉 Editions", value=editions)
    col2.metric(label="🏟️ Hosts", value=cities)
    col3.metric(label="🏋️ Sports", value=sports)

    col1, col2, col3 = st.columns(3)
    col1.metric(label="🎯 Events", value=events)
    col2.metric(label="🌎 Nations", value=nations)
    col3.metric(label="🏅 Athletes", value=athletes)

    
    st.title("📈 Trends Over Time")
    nations_over_time = helper.data_over_time(df, 'region')
    st.plotly_chart(px.line(nations_over_time, x="Year", y="count", title="🌎 Participating Nations Over Years"))

    events_over_time = helper.data_over_time(df, 'Event')
    st.plotly_chart(px.line(events_over_time, x="Year", y="count", title="🎯 Events Over Years"))

    athlete_over_time = helper.data_over_time(df, 'Name')
    st.plotly_chart(px.line(athlete_over_time, x="Year", y="count", title="🏅 Athletes Over Years"))


if user_menu == '📌 Country-wise Analysis':
    st.sidebar.title("📌 Country-wise Analysis")
    country_list = sorted(df['region'].dropna().unique().tolist())
    selected_country = st.sidebar.selectbox('Select a Country', country_list)

    country_df = helper.yearwise_medal_tally(df, selected_country)
    st.title(f"📊 {selected_country} Medal Tally Over The Years")
    st.plotly_chart(px.line(country_df, x="Year", y="Medal", title=f"🏅 {selected_country} Medal Tally"))


if user_menu == '🏅 Athlete-wise Analysis':
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    x1 = athlete_df['Age'].dropna()
    x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()

    fig = ff.create_distplot([x1, x2, x3, x4], ['Overall Age', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'], show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=1000, height=600)
    
    st.title("📊 Age Distribution of Athletes")
    st.plotly_chart(fig)
st.sidebar.markdown("---")
st.sidebar.markdown("<div style='text-align: center; color: #BDC3C7;'>", unsafe_allow_html=True)
st.sidebar.caption("Developed by Deepak Shukla")
st.sidebar.caption("23BCE11422")
st.sidebar.markdown("</div>", unsafe_allow_html=True)
