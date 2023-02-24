import streamlit as st
from streamlit_option_menu import option_menu
import FoncAnalyse as fa

st.set_page_config(page_title="Stocks Screener",
                   page_icon=":chart_with_upwards_trend:",
                   layout="wide")


#---- Sidebar -----#


with st.sidebar:
    selected = option_menu(
        menu_title = "Menu principale",
        options=["Recherche", "Top Actions","Top Sous-Coté", "Calendrier Eco"],
    )

#### Recherche Action ####

if selected == "Recherche":
    st.title(f"Chercher une action ici")
    tick = st.text_input(label="Search for stocks", value=fa.top5TradableStocks[0])

    try:
        fa.main_page(tick)        
    except:
        st.header("Le ticker n'existe pas")


#### Top Actions ####

if selected == "Top Actions":
    st.title(f"Les tops actions du jour")
    tick = st.sidebar.radio("Top 5 Actions",
                       options=fa.top5TradableStocks)
    
    try:
        fa.main_page(tick)
    except:
        st.header("Le ticker n'existe pas")

#### Top Sous Coté ####

if selected == "Top Sous-Coté":
    st.title(f"Les tops sous-coté du jour")
    tick = st.sidebar.radio("Top 5 Sous-coté",
                       options=fa.top5UnderRateStocks)
    
    try:
        fa.main_page(tick)
    except:
        st.header("Le ticker n'existe pas")

#### Calendrier économique ####

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

