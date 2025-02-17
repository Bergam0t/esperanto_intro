import streamlit as st
import pandas as pd
from _helper import change_svg_color
import io

st.title("An Introduction to Esperanto")

adjectives = pd.read_excel("word_list.xlsx", "adjectives")

nouns = pd.read_excel("word_list.xlsx", sheet_name="nouns")

colours = pd.read_excel("word_list.xlsx", sheet_name="colours")


tab1, tab2, tab3 = st.tabs(["Sentence Playground", "Word Types", "Sentence Game"])

col_la_e, col_adjective_1_e, col_noun_e, col_estas_e, col_adjective_2_e = st.columns(5)


with col_la_e:
    st.header("La")

with col_adjective_1_e:
    adjective_1 = st.selectbox("Select", 
                               list(colours.colour), 
                               key="adjective_1",
                               label_visibility="hidden")

with col_noun_e:
    noun = st.selectbox("Select", list(nouns.noun), key="noun",
                               label_visibility="hidden")

with col_estas_e:
    st.header("estas")


with col_adjective_2_e:
    # new_adjectives = list(adjectives.adjective)
    # new_adjectives.remove(adjective_1) 
    adjective_2 = st.selectbox("Select", adjectives, key="adjective_2",
                               label_visibility="hidden")
    
col_la_en, col_adjective_1_en, col_noun_en, col_estas_en, col_adjective_2_en = st.columns(5)

with col_la_e: 
    st.markdown("The")

with col_adjective_1_en:
    adjective_1_translated = colours[colours["colour"] == adjective_1]['translation'].values[0]
    st.markdown(adjective_1_translated)
    colour_hex =  colours[colours["colour"] == adjective_1]['hex'].values[0]

with col_noun_en:
    noun_translated = nouns[nouns["noun"] == noun]['translation'].values[0]
    # svg_io = io.BytesIO(change_svg_color(f"assets/{noun_translated}.svg", colour_hex, string=True))
    # st.image(svg_io)
    st.markdown(f'<div>{change_svg_color(f"assets/{noun_translated}.svg", colour_hex, string=True)}</div>', unsafe_allow_html=True)
    