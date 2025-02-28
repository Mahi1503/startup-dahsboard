import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout="wide",page_title="StartUp Analysis")

df = pd.read_csv("startup_cleaned.csv")
#data cleaning
df["date"] = pd.to_datetime(df["date"],errors="coerce")
df["year"] = df["date"].dt.year
df["month"] = df["date"].dt.month

def load_overall_analysis():
    st.title("Overall Analysis")

    col1,col2,col3,col4 = st.columns(4)

    with col1:
        #total investment
        total = round(df["amount"].sum())
        st.metric("Total",str(total)+"Cr")

    with col2:
        #max investment
        max_invest = round(df.groupby("startup")["amount"].sum().sort_values(ascending=False)[0])
        st.metric("Maximum Investment", str(max_invest) + "Cr")

    with col3:
        # Avg funding
        avg_funding = round(df.groupby("startup")["amount"].sum().mean())
        st.metric("Avg Investment", str(avg_funding) + "Cr")

    with col4:
        # Total funded startup
        total_startup = df["startup"].nunique()
        st.metric("Funded Startups", total_startup)

    st.header("MOM Graph")
    selected_option = st.selectbox("Select Type",["None","MOM Amount Graph","MOM Count Graph"])

    if selected_option == "MOM Amount Graph":
        temp_df = df.groupby(["year", "month"])["amount"].sum().reset_index()
        temp_df["x-axis"] = temp_df["year"].astype(str) + "-" + temp_df["month"].astype(str)
        fig4, ax4 = plt.subplots()
        ax4.plot(temp_df["x-axis"],temp_df["amount"])
        st.pyplot(fig4)
    elif selected_option == "MOM Count Graph":
        temp_df = df.groupby(["year", "month"])["startup"].count().reset_index()
        temp_df["x-axis"] = temp_df["year"].astype(str) + "-" + temp_df["month"].astype(str)
        fig4, ax4 = plt.subplots()
        ax4.plot(temp_df["x-axis"], temp_df["startup"])
        st.pyplot(fig4)
    else:
        pass


def load_investor_details(investor):
    st.title(investor)
    #load recent 5 investments of investor
    last5_df = df[df["investors"].str.contains(investor)].head()[
        ["date", "startup", "vertical", "city", "round", "amount"]].reset_index().drop(columns=["index"])
    st.subheader("Most Recent Investments")
    st.dataframe(last5_df)

    col1,col2 = st.columns(2)

    with col1:
        #Biggest investments
        big_series = df[df["investors"].str.contains(investor)].groupby("startup")["amount"].sum().sort_values(ascending=False).head()
        st.subheader("Biggest Investments")
        fig,ax = plt.subplots()
        ax.bar(big_series.index, big_series.values)
        st.pyplot(fig)

    with col2:
        vertical_series = df[df["investors"].str.contains(investor)].groupby("vertical")["amount"].sum()

        st.subheader("Invested in sectors")
        fig1, ax1 = plt.subplots()
        ax1.pie(vertical_series,labels=vertical_series.index,autopct="%0.01f%%")
        st.pyplot(fig1)

    col3, col4 = st.columns(2)

    with col3:
        stage_series = df[df["investors"].str.contains(investor)].groupby("round")["amount"].sum()

        st.subheader("Invested in stage")
        fig0, ax0 = plt.subplots()
        ax0.pie(stage_series,labels=stage_series.index,autopct="%0.01f%%")
        st.pyplot(fig0)

    with col4:
        city_series = df[df["investors"].str.contains(investor)].groupby("city")["amount"].sum()

        st.subheader("Invested in city")
        fig2, ax2 = plt.subplots()
        ax2.pie(city_series,labels=city_series.index,autopct="%0.01f%%")
        st.pyplot(fig2)


    year_series = df[df["investors"].str.contains(investor)].groupby("year")["amount"].sum()
    st.subheader("YOY Investment")
    fig3, ax3 = plt.subplots()
    ax3.plot(year_series.index,year_series.values)
    st.pyplot(fig3)


st.sidebar.title("Startup Funding Analysis")

option = st.sidebar.selectbox("Select One",["None","Overall Analysis","StartUp","Investor"])

if option == "Overall Analysis":
    load_overall_analysis()
elif option == "StartUp":
    st.sidebar.selectbox("Select StartUp",["None"]+ sorted(df["startup"].unique().tolist()))
    btn1 = st.sidebar.button("Find StartUp Details")
    st.title("StartUp Analysis")
elif option == "Investor":
    selected_investor = st.sidebar.selectbox("Select Investor",["None"]+ sorted(set(df["investors"].str.split(",").sum())))
    btn2 = st.sidebar.button("Find Investor Details")
    if btn2:
        load_investor_details(selected_investor)

