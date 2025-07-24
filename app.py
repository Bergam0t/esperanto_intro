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
    pronouns["What"] = "Pronoun"
    adjectives = pd.read_excel("word_list.xlsx", sheet_name="adjectives")
    adjectives["What"] = "Adjective"
    nouns = pd.read_excel("word_list.xlsx", sheet_name="nouns")
    nouns["What"] = "Noun"
    colours = pd.read_excel("word_list.xlsx", sheet_name="colours")
    colours["What"] = "Adjective"
    verbs = pd.read_excel("word_list.xlsx", sheet_name="verbs")
    verbs["What"] = "Verb"

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

st.image("esperanto_summary.png", width=800)

tab2, tab1, tab3 = st.tabs(["Sentence Playground", "Sentence Practice", "Vocab Game"])

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

    st.markdown("How do you say 'the cat is brown'?")

    @st.fragment
    def q_sentence_1():
        correct = "La kato estas bruna"

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
                st.write("Click the play button to hear this sentence")
                play_sound(sentence_1, autoplay=False)
            elif word_2_sentence_1 == "Choose" or word_4_sentence_1 == "Choose":
                st.info("Choose your answers using the dropdown boxes")
            else:
                st.warning(f"Not quite - try again!\n\n{word_2_sentence_1_choices[word_2_sentence_1]}\n\n{word_4_sentence_1_choices[word_4_sentence_1]}")

    q_sentence_1()

    ########################################
    # SENTENCE 2
    #######################################

    st.divider()

    st.subheader("Sentence 2")

    st.markdown("How do you say 'She was dancing in the house'?")

    def q_sentence_2():
        correct = "Ŝi dancis en la domo"

        col_s2_1, col_s2_2, col_s2_3, col_s2_4, col_s2_5 = st.columns([0.1, 0.2, 0.1, 0.2, 0.4])

        col_s2_1.markdown("### Ŝi")

        word_2_sentence_2_choices = {
                "Choose": "",
                'danco': "Danco is a noun ending - you're on the right track, but are looking for one extra letter to get the future tense verb!",
                "dancas": "Dancis is a verb form, but the present tense, not the past",
                'dancis': "",
                "dancos": "Dancos is a verb form, but in the future tense, not the past"
            }


        word_2_sentence_2 = col_s2_2.selectbox("col_s2_2", word_2_sentence_2_choices, label_visibility="hidden")

        col_s2_3.markdown("### en la")

        word_4_sentence_2_choices = {
                "Choose": "",
                'doma': "In doma, the -a ending indicates an adjective, so this is like saying 'houselike'",
                'domo': "",
                "domos": "In domos, the -os ending is a verb that indicates something will be done in the future",
                "domoj": "In domoj, the -o ending does indicate a noun here, but the -j indicates multiple houses"
            }

        word_4_sentence_2 = col_s2_4.selectbox("col_s2_4", word_4_sentence_2_choices, label_visibility="hidden")

        sentence_2 = f"Ŝi {word_2_sentence_2} en la {word_4_sentence_2}"

        with col_s2_5:
            if sentence_2 == correct:
                st.success("Well done!")
                st.write("Click the play button to hear this sentence")
                play_sound(sentence_2, autoplay=False)
            elif word_2_sentence_2 == "Choose" or word_4_sentence_2 == "Choose":
                st.info("Choose your answers using the dropdown boxes")
            else:
                st.warning(f"Not quite - try again!\n\n{word_2_sentence_2_choices[word_2_sentence_2]}\n\n{word_4_sentence_2_choices[word_4_sentence_2]}")

    q_sentence_2()

# Replace with your actual vocabulary DataFrame
# all_vocab = pd.read_csv("vocab.csv")  # or however you're loading it

# Initialize game state
if "game_started" not in st.session_state:
    st.session_state.game_started = False
if "current_question" not in st.session_state:
    st.session_state.current_question = None


# List of word types (adjust as needed)
WORD_TYPES = ["Noun", "Verb", "Adjective", "Pronoun"]

@st.fragment
def generate_question():
    row = all_vocab.sample(1).iloc[0]

    # Randomly choose question type
    question_type = random.choice(["translation", "type"])

    if question_type == "translation":
        # Sample 2 wrong answers
        distractors = all_vocab[all_vocab["translation"] != row["translation"]].sample(2)["translation"].tolist()
        answers = [
            {"text": row["translation"], "is_correct": True},
            {"text": distractors[0], "is_correct": False},
            {"text": distractors[1], "is_correct": False},
        ]
        prompt = "TRANSLATE: What is the English translation of this word? Click the correct button."

    else:  # word type question
        correct_type = row["What"]
        distractors = [w for w in WORD_TYPES if w != correct_type]
        random_distractors = random.sample(distractors, 2)
        answers = [
            {"text": correct_type, "is_correct": True},
            {"text": random_distractors[0], "is_correct": False},
            {"text": random_distractors[1], "is_correct": False},
        ]
        prompt = "IDENTIFY: What type of word is this? Click the correct button."

    random.shuffle(answers)

    st.session_state.current_question = {
        "word": row["word"],
        "answers": answers,
        "prompt": prompt,
        "type": question_type,
    }


with tab3:
    if not st.session_state.game_started:
        if st.button("Generate Word"):
            st.session_state.game_started = True
            generate_question()

    if st.session_state.game_started and st.session_state.current_question:
        q = st.session_state.current_question
        st.subheader(q["prompt"])
        st.header(q["word"])
        hidden_col1, hidden_col2 = st.columns([0.01, 0.99])
        with hidden_col1:
            play_sound(q["word"], autoplay=True)  # Optional audio playback
        cols = st.columns(3)
        for col, ans in zip(cols, q["answers"]):
            if col.button(ans["text"]):
                if ans["is_correct"]:
                    st.success("Well done! Generating a new question.")
                    sleep(2)
                    generate_question()
                    st.rerun()
                else:
                    st.warning("Try again!")
