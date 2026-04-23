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

    df2=pdata[["Runs","Matches","innings","6s","4s","100","50","Ave","High_score"]]
    df2=df2.T.reset_index() #T means transposed k rows wli values columns me ajaingi or columns wli rows me #reset_index- data frame kos ort krega
    st.dataframe(df2)
    fig=px.bar(df2,x="index",y=df2.columns[1],color="index")  #colunms[1]- exampls- column hyn 5 ek table me/unko hmne index(list)me lelia/or ab jo column chhye hai usme hm list ki index wise select krengy islie likha


      #----------------KEY METRICS-------------
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


    #_______________Country Analysis_______________

elif select == "Country Insights":
    st.title("Country Insights")

    country_runs = df.groupby("Country")["Runs"].sum().reset_index()

    fig = px.pie(
    country_runs,
    names="Country",
    values="Runs"
    )

    st.plotly_chart(fig,use_container_width=True)

    

    country_select = st.selectbox("Select Country", df["Country"].unique())
    cdata=df[df["Country"]==country_select] #cdata-country data , country-select country islie kiu k select country me se country ko select kia hai

    fig_runs=px.pie(             #sbky alag alag bar chart bnenge
        cdata, 
        names="Player",
        values="Runs",
    )

    st.plotly_chart(fig_runs,use_container_width=True)




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