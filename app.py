import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu #navbar

st.set_page_config(layout="wide")
st.title("Cric info app")

#loading data

df=pd.read_csv("newfile.csv")

#__________Navbar___________#

select = option_menu(
    menu_title=None,
    options=["Home","Player Analysis","Country Insights","Comparison","Data Explorer"],
    icons=["house","person","globe","bar-chart","table"], 
    orientation="horizontal"  

)



##__________________Home______________

if select == "Home":
    st.title("Cricket Analysis Dashboard")

    col1,col2,col3 = st.columns(3)
    col1.metric("Total Players", df["Player"].nunique())
    col2.metric("Total Runs", df["Runs"].sum())
    col3.metric("Countries", df["Country"].nunique())

    st.dataframe(df.head())


#___________Player Analysis_______

elif select == "Player Analysis":
 
    st.title("Player Analysis")

    player = st.selectbox("Select Player", df["Player"])

    pdata = df[df["Player"]==player]

    stats=["100","50","4s","6s"]

    chart_data = (
        pdata[stats].iloc[0].reset_index()
    )

    chart_data.columns = ["Stat","Value"]

    fig=px.bar(
        chart_data,
        x="Stat",
        y="Value"
       
    )


    col4,col5,col6,col7,col8,col9=st.columns(6)

    total_runs=pdata["Runs"].sum()
    total_matches=pdata["Matches"]
    hundreds=pdata["100"].sum()
    sixes=pdata["6s"].sum()
    avg=pdata["Ave"].sum()
    innings=pdata["innings"].nunique()


    col4.metric(label="Total Runs",value=total_runs)
    col5.metric(label="Total Matches",value=total_matches)
    col6.metric(label="Total 100's",value=hundreds)
    col7.metric(label="Total 6's",value=sixes)
    col8.metric(label="Total Average",value=avg)
    col9.metric(label="Innings",value=innings)


    st.plotly_chart(fig,use_container_width=True)


    #_______________Country_______________

elif select == "Country Insights":
    st.title("Country Insights")

    country_runs = df.groupby("Country")["Runs"].sum().reset_index()

    fig = px.pie(country_runs,names="Country",values="Runs")

    st.plotly_chart(fig,use_container_width=True)


elif select == "Comparison":
    st.title("Player Comparison")   

    players = st.multiselect(
        "compare player", 
        df["Player"], 
        default=df["Player"].head(5)
        )
    compare = df[df["Player"].isin(players)]

    fig=px.scatter(
        compare,
        x="Strike_rate",
        y="Ave",
        size="Runs",
        color="Country"
    )

    st.plotly_chart(fig,use_container_width=True)


    #_______________Data Explore___________

elif select == "Data Explorer":

    st.title("Data Explore")
    st.dataframe(df)