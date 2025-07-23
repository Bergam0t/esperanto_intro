import streamlit as st
import pandas as pd
from gtts import gTTS
from io import BytesIO
from time import sleep
import random

st.set_page_config(layout="wide")

st.title("An Introduction to Esperanto")

if "game_started" not in st.session_state:
    st.session_state.game_started = False
if "current_question" not in st.session_state:
    st.session_state.current_question = None


@st.cache_data
def read_in():
    pronouns = pd.read_excel("word_list.xlsx", sheet_name="pronouns")
    adjectives = pd.read_excel("word_list.xlsx", sheet_name="adjectives")
    nouns = pd.read_excel("word_list.xlsx", sheet_name="nouns")
    colours = pd.read_excel("word_list.xlsx", sheet_name="colours")
    verbs = pd.read_excel("word_list.xlsx", sheet_name="verbs")
    all_vocab = pd.concat(
        [pronouns.rename(columns={"pronoun":"word"}),
        verbs.rename(columns={"verb":"word", "translation_singular":"translation"}),
        adjectives.rename(columns={"adjective":"word"}),
        colours.rename(columns={"colour":"word"}),
        nouns.rename(columns={"noun":"word"})]
        )

    nouns["emoji"] = ["🐦", "⚽", "🐈", "🐕", "🚗", "🐢", "🐇", "🐍", "🖥️"]
    colours["emoji"] = ["🟤", "⚪", "🟡", "🟢",  "🔵", "🟣"]
    adjectives["emoji"] = ["😃", "😭", "⬆️", "⬇️", "🏃", "🚶"]

    return pronouns, adjectives, nouns, colours, verbs, all_vocab

pronouns, adjectives, nouns, colours, verbs, all_vocab = read_in()

tab1, tab2, tab3 = st.tabs(["Sentence Playground", "Sentence Practice", "Vocab Game"])

def play_sound(text, autoplay=True):
    sound_file = BytesIO()
    tts = gTTS(text, lang='fr')
    tts.write_to_fp(sound_file)
    st.audio(sound_file, autoplay=autoplay)

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

            # play_sound(pronoun)

        with col_adjective_1_es:
            st.subheader("Adjective")

            colour_list = list(colours.colour)

            if plural:
                colour_list = [f"{colour}j" for colour in colour_list]

            adjective_1 = st.selectbox("Select",
                                    colour_list,
                                    key="adjective_1",
                                    label_visibility="hidden")

            # play_sound(adjective_1)

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

            # play_sound(noun)

            if plural:
                noun = noun[:-1]

        with col_estas_es:
            st.subheader("Verb")

            verb = st.selectbox("Select", list(verbs.verb),
                                key="verb",
                                label_visibility="hidden")

            # play_sound(verb)


        with col_adjective_2_es:
            st.subheader("Adjective")
            adjective_2_list = list(adjectives.adjective)

            if plural:
                adjective_2_list = [f"{adjective}j" for adjective in adjective_2_list]

            adjective_2 = st.selectbox("Select", adjective_2_list, key="adjective_2",
                                    label_visibility="hidden")

            # play_sound(adjective_2)

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

        full_sentence = f"{pronoun} {adjective_1} {noun} {verb} {adjective_2}"

        play_sentence_button = st.button("Click to hear the sentence")


        if play_sentence_button:
            play_sound(full_sentence)

    playground()


with tab2:
    st.subheader("Sentence 1")

    correct = "La kato estas bruna"

    st.markdown("How do you say 'the cat is brown'?")

    col_s_1, col_s_2, col_s_3, col_s_4, col_s_5 = st.columns([0.1, 0.2, 0.1, 0.2, 0.4])

    col_s_1.markdown("### La")

    word_2_sentence_1_choices = {
            "Choose": "",
            'katas': "In katas, the -as ending indicates a verb",
            'kata': "Kata is an adjective because of the 'a' ending, so this would be 'catlike'",
            "katoj": "Katoj is a noun - but the -j ending is a plural, and we only have one cat here",
            "kato": ""

        }

    word_2_sentence_1 = col_s_2.selectbox("col_s_2", word_2_sentence_1_choices, label_visibility="hidden")

    col_s_3.markdown("### estas")

    word_4_sentence_1_choices = {
            "Choose": "",
            'bruni': "In bruni, the -as ending indicates a verb",
            'brunaj': "Brunaj is almost correct, but the -j ending would be used for multiple cats, not just one",
            "bruna": "",
            "bruno": "The -o ending in 'bruno' means this is a noun, not an adjective"

        }

    word_4_sentence_1 = col_s_4.selectbox("col_s_4", ["Choose", "bruni", "brunaj", "bruna", "bruno"], label_visibility="hidden")

    sentence_1 = f"La {word_2_sentence_1} estas {word_4_sentence_1}"

    with col_s_5:
        if sentence_1 == correct:
            st.success("Well done!")
            play_sound(sentence_1)
        elif word_2_sentence_1 == "Choose" or word_4_sentence_1 == "Choose":
            st.info("Choose your answers using the dropdown boxes")
        else:
            st.warning(f"Not quite - try again!\n\n{word_2_sentence_1_choices[word_2_sentence_1]}\n\n{word_4_sentence_1_choices[word_4_sentence_1]}")


    ########################################
    # SENTENCE 2
    #######################################

    st.divider()

    st.subheader("Sentence 2")

    correct = "Ŝi legas en la domo"

    st.markdown("How do you say 'She is reading in the house'?")

    col_s2_1, col_s2_2, col_s2_3, col_s2_4, col_s2_5 = st.columns([0.1, 0.2, 0.1, 0.2, 0.4])

    col_s2_1.markdown("### Ŝi")

    word_2_sentence_2_choices = {
            "Choose": "",
            'legis': "Legis is a verb form, but the present tense, not the future",
            'lego': "Lego is a noun ending - you're on the right track, but are looking for one extra letter to get the future tense verb!",
            "legas": "Legas is a verb form, but the present tense, not the future",
            "legos": ""
        }


    word_2_sentence_2 = col_s2_2.selectbox("col_s2_2", ["Choose", "legis", "lego", "legas", "legos"], label_visibility="hidden")

    col_s2_3.markdown("### en la")

    word_4_sentence_2_choices = {
            "Choose": "",
            'doma': "In libra, the -a ending indicates an adjective, so this is like saying 'houselike'",
            'domo': "",
            "domos": "The -os ending is a verb that indicates something will be done in the future",
            "domoj": "The -o ending does indicate a noun here, but the -j indicates multiple houses"
        }

    word_4_sentence_2 = col_s2_4.selectbox("col_s2_4", word_4_sentence_2_choices, label_visibility="hidden")


    sentence_2 = f"La {word_2_sentence_2} estas {word_4_sentence_2}"

    with col_s2_5:
        if sentence_2 == correct:
            st.success("Well done!")
        elif word_2_sentence_2 == "Choose" or word_4_sentence_2 == "Choose":
            st.info("Choose your answers using the dropdown boxes")
        else:
            st.warning(f"Not quite - try again!\n\n{word_2_sentence_2_choices[word_2_sentence_2]}\n\n{word_4_sentence_2_choices[word_4_sentence_2]}")


    with tab3:
        button_text = "Generate Word"

        @st.fragment
        def generate_new_word():
            sampled_rows = all_vocab.sample(3)
            chosen_row = sampled_rows.head(1)
            st.header(chosen_row["word"].values[0])


            correct = chosen_row["translation"].values[0]
            dummy_1 = sampled_rows[1:2]["translation"].values[0]
            dummy_2 = sampled_rows[2:]["translation"].values[0]

            col_ans_1, col_ans_2, col_ans_3 = st.columns([0.2, 0.2, 0.2])
            answer_cols = [col_ans_1, col_ans_2, col_ans_3]
            random.shuffle(answer_cols)

            correct_button = answer_cols[0].button(correct)
            dummy_button_1 = answer_cols[1].button(dummy_1)
            dummy_button_2 = answer_cols[2].button(dummy_2)

            play_sound(chosen_row["word"].values[0], autoplay=True)

            if correct_button:
                st.success("Well done!")
                with st.spinner():
                    sleep(2)
                generate_new_word()
            elif dummy_button_1 or dummy_button_2:
                st.warning("Try again!")


        vocab_game = st.button(button_text)
        if vocab_game:
            generate_new_word()
