import streamlit as st
from streamlit_option_menu import option_menu
import mplfinance as mpf
import FoncAnalyse as fa

st.set_page_config(page_title="Stocks Screener",
                   page_icon=":chart_with_upwards_trend:",
                   layout="wide")


#---- Sidebar -----


with st.sidebar:
    selected = option_menu(
        menu_title = "Menu principale",
        options=["Recherche", "Top Actions", "Calendrier Eco"],
    )

if selected == "Recherche":
    st.title(f"Chercher une action ici")
    tick = st.text_input(label="Search for stocks", value=fa.top5TradableStocks[0])

    try:
        st.header(tick.upper())

        TDF = fa.tendancesDeF(tick)
        ATD = fa.Tradable(tick)

        leftColumn, rightColumn = st.columns(2)
        with leftColumn:
            st.subheader("Tendence de fond : ")
            st.subheader(TDF)

        with rightColumn:
            st.subheader("A Trader en ce moment : ")
            st.subheader(ATD)
    except:
        st.header("Le ticker n'existe pas")

if selected == "Top Actions":
    st.title(f"Les tops actions du jour")
    st.sidebar.header("Top 5 Stocks")
    tick = st.sidebar.radio("Pick one",
                       options=fa.top5TradableStocks)
    
    st.header(tick.upper())

    TDF = fa.tendancesDeF(tick)
    ATD = fa.Tradable(tick)

    leftColumn, rightColumn = st.columns(2)
    with leftColumn:
        st.subheader("Tendence de fond : ")
        st.subheader(TDF)

    with rightColumn:
        st.subheader("A Trader en ce moment : ")
        st.subheader(ATD)

if selected == "Calendrier Eco":
    st.title(f"Le calendrier économique")
    dfEco, DateCal = fa.scrapCalEco()

    devise = st.sidebar.multiselect(
        "Devise",
        options=dfEco["Currency"].unique(),
        default=dfEco["Currency"].unique()
    )

    impEvent = st.sidebar.multiselect(
        "Importance des évenements",
        options=dfEco["Importance"].unique(),
        default=dfEco["Importance"].unique()
    )

    df_selection = dfEco.query(
        "Currency == @devise & Importance == @impEvent"
    )

    st.dataframe(df_selection )

