import streamlit as st
import pandas as pd

st.title("An Introduction to Esperanto")

st.set_page_config(layout="wide")

@st.cache_data
def read_in():
    pronouns = pd.read_excel("word_list.xlsx", sheet_name="pronouns")
    adjectives = pd.read_excel("word_list.xlsx", sheet_name="adjectives")
    nouns = pd.read_excel("word_list.xlsx", sheet_name="nouns")
    colours = pd.read_excel("word_list.xlsx", sheet_name="colours")
    verbs = pd.read_excel("word_list.xlsx", sheet_name="verbs")

    nouns["emoji"] = ["🐦", "⚽", "🐈", "🐕", "🚗", "🐢", "🐇", "🐍", "🖥️"]
    colours["emoji"] = ["🟤", "⚪", "🟡", "🟢",  "🔵", "🟣"]
    adjectives["emoji"] = ["😃", "😭", "⬆️", "⬇️", "🏃", "🚶"]

    return pronouns, adjectives, nouns, colours, verbs

pronouns, adjectives, nouns, colours, verbs = read_in()

tab1, tab2 = st.tabs(["Sentence Playground", "Sentence Game"])

with tab1:

    st.success(
        """
        Try out the sentence playground below by using the dropdown boxes to select words.

        1. What do you notice about the regularity of the words in Esperanto vs English?
        2. What's going on with the pairs of adjectives in the rightmost box?
        3. Do you recognise any words - from English or other languages?
        4. What changes when you toggle the 'plural' button? What stays the same?
        """
    )

    @st.fragment
    def playground():

        plural = st.toggle("Click to toggle plurals")

        col_la_es, col_adjective_1_es, col_noun_es, col_estas_es, col_adjective_2_es = st.columns(5)


        with col_la_es:
            st.subheader("Pronoun")

            pronoun = st.selectbox("Select",
                                    list(pronouns.pronoun),
                                    key="pronoun",
                                    label_visibility="hidden")

        with col_adjective_1_es:
            st.subheader("Adjective")

            colour_list = list(colours.colour)

            if plural:
                colour_list = [f"{colour}j" for colour in colour_list]

            adjective_1 = st.selectbox("Select",
                                    colour_list,
                                    key="adjective_1",
                                    label_visibility="hidden")

            if plural:
                adjective_1 = adjective_1[:-1]

        with col_noun_es:
            st.subheader("Noun")

            noun_list = list(nouns.noun)

            if plural:
                noun_list = [f"{noun}j" for noun in noun_list]

            noun = st.selectbox("Select", noun_list,
                                key="noun",
                                label_visibility="hidden")

            if plural:
                noun = noun[:-1]

        with col_estas_es:
            st.subheader("Verb")

            verb = st.selectbox("Select", list(verbs.verb),
                                key="verb",
                                label_visibility="hidden")


        with col_adjective_2_es:
            st.subheader("Adjective")
            adjective_2_list = list(adjectives.adjective)

            if plural:
                adjective_2_list = [f"{adjective}j" for adjective in adjective_2_list]

            adjective_2 = st.selectbox("Select", adjective_2_list, key="adjective_2",
                                    label_visibility="hidden")

            if plural:
                adjective_2 = adjective_2[:-1]

        st.markdown("")
        st.markdown("")

        col_la_en, col_adjective_1_en, col_noun_en, col_estas_en, col_adjective_2_en = st.columns(5)

        with col_la_en:
            pronoun_translated = pronouns[pronouns["pronoun"] == pronoun]
            st.markdown(pronoun_translated['translation'].values[0])

        with col_adjective_1_en:
            adjective_1_translated = colours[colours["colour"] == adjective_1]
            st.markdown(adjective_1_translated['translation'].values[0])
            st.header(adjective_1_translated['emoji'].values[0])

        with col_noun_en:
            noun_translated = nouns[nouns["noun"] == noun]
            noun_output = noun_translated['translation'].values[0]
            if plural:
                st.markdown(f"{noun_output}s")
            else:
                st.markdown(noun_output)
            st.header(noun_translated['emoji'].values[0])

        with col_estas_en:
            verb_translated = verbs[verbs["verb"] == verb]
            if plural:
                st.markdown(verb_translated['translation_plural'].values[0])
            else:
                st.markdown(verb_translated['translation_singular'].values[0])

        with col_adjective_2_en:
            adjective_2_translated = adjectives[adjectives["adjective"] == adjective_2]
            st.markdown(adjective_2_translated['translation'].values[0])
            st.header(adjective_2_translated['emoji'].values[0])

    playground()
