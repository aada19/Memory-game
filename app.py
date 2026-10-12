import streamlit as st
import random
import time

# ============================================================
# AI MEMORY MATCH
# ============================================================

st.set_page_config(
    page_title="AI Memory Match",
    page_icon="🧠",
    layout="centered"
)

# ------------------------------------------------------------
# CSS
# ------------------------------------------------------------

st.markdown("""
<style>

.main-title {
    text-align: center;
    font-size: 42px;
    font-weight: bold;
    margin-bottom: 5px;
}

.subtitle {
    text-align: center;
    color: #777;
    margin-bottom: 25px;
}

.card-button {
    width: 100%;
    height: 90px;
    font-size: 35px !important;
    border-radius: 15px;
}

</style>
""", unsafe_allow_html=True)


# ------------------------------------------------------------
# TITLE
# ------------------------------------------------------------

st.markdown(
    '<div class="main-title">🧠 AI MEMORY MATCH</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Human Memory vs AI Memory</div>',
    unsafe_allow_html=True
)


# ------------------------------------------------------------
# DIFFICULTY
# ------------------------------------------------------------

difficulty = st.selectbox(
    "🎯 Choose Difficulty",
    ["Easy", "Medium", "Hard"]
)


# Number of pairs
if difficulty == "Easy":
    pairs_count = 4

elif difficulty == "Medium":
    pairs_count = 6

else:
    pairs_count = 8


# ------------------------------------------------------------
# CARD SYMBOLS
# ------------------------------------------------------------

symbols = [
    "🐶", "🐱", "🦊", "🐼",
    "🐸", "🐵", "🦁", "🐯",
    "🐨", "🐰", "🐻", "🐧",
    "🦄", "🐝", "🦋", "🐙"
]


# ------------------------------------------------------------
# INITIALIZE GAME
# ------------------------------------------------------------

if "game_started" not in st.session_state:
    st.session_state.game_started = False

if "cards" not in st.session_state:
    st.session_state.cards = []

if "revealed" not in st.session_state:
    st.session_state.revealed = []

if "matched" not in st.session_state:
    st.session_state.matched = []

if "moves" not in st.session_state:
    st.session_state.moves = 0

if "score" not in st.session_state:
    st.session_state.score = 0

if "ai_memory" not in st.session_state:
    st.session_state.ai_memory = {}

if "game_over" not in st.session_state:
    st.session_state.game_over = False

if "start_time" not in st.session_state:
    st.session_state.start_time = None


# ------------------------------------------------------------
# START / RESTART GAME
# ------------------------------------------------------------

def start_game():

    selected_symbols = symbols[:pairs_count]

    cards = selected_symbols * 2

    random.shuffle(cards)

    st.session_state.cards = cards
    st.session_state.revealed = []
    st.session_state.matched = []
    st.session_state.moves = 0
    st.session_state.score = 0
    st.session_state.ai_memory = {}
    st.session_state.game_over = False
    st.session_state.game_started = True
    st.session_state.start_time = time.time()


if st.button("🔄 Start / Restart Game", use_container_width=True):
    start_game()


# ------------------------------------------------------------
# GAME STATUS
# ------------------------------------------------------------

if st.session_state.game_started:

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "🎯 Score",
            st.session_state.score
        )

    with col2:
        st.metric(
            "🔄 Moves",
            st.session_state.moves
        )

    with col3:
        st.metric(
            "🧠 AI Memory",
            len(st.session_state.ai_memory)
        )


    st.write("")


    # --------------------------------------------------------
    # GAME BOARD
    # --------------------------------------------------------

    columns = 4

    for row in range(0, len(st.session_state.cards), columns):

        cols = st.columns(columns)

        for col_index in range(columns):

            index = row + col_index

            if index >= len(st.session_state.cards):
                continue

            card = st.session_state.cards[index]

            # Decide what should be displayed
            if (
                index in st.session_state.revealed
                or index in st.session_state.matched
            ):
                display_card = card

            else:
                display_card = "❓"


            with cols[col_index]:

                if st.button(
                    display_card,
                    key=f"card_{index}",
                    use_container_width=True
                ):

                    # Ignore already revealed/matched cards
                    if (
                        index not in st.session_state.revealed
                        and index not in st.session_state.matched
                    ):

                        # ------------------------------------------------
                        # AI MEMORY
                        # ------------------------------------------------

                        st.session_state.ai_memory[index] = card

                        st.session_state.revealed.append(index)


                        # ------------------------------------------------
                        # TWO CARDS SELECTED
                        # ------------------------------------------------

                        if len(st.session_state.revealed) == 2:

                            first = st.session_state.revealed[0]
                            second = st.session_state.revealed[1]

                            st.session_state.moves += 1


                            # ------------------------------------------------
                            # MATCH
                            # ------------------------------------------------

                            if (
                                st.session_state.cards[first]
                                ==
                                st.session_state.cards[second]
                            ):

                                st.session_state.matched.extend(
                                    [first, second]
                                )

                                st.session_state.score += 10

                                st.session_state.revealed = []


                            # ------------------------------------------------
                            # NOT A MATCH
                            # ------------------------------------------------

                            else:

                                st.session_state.score = max(
                                    0,
                                    st.session_state.score - 2
                                )

                                # Save the two cards temporarily
                                time.sleep(0.8)

                                st.session_state.revealed = []


                        st.rerun()


    # --------------------------------------------------------
    # AI MEMORY DISPLAY
    # --------------------------------------------------------

    st.divider()

    st.subheader("🧠 AI Memory Bank")

    if st.session_state.ai_memory:

        memory_text = ""

        for position, card in st.session_state.ai_memory.items():

            memory_text += (
                f"**Card {position + 1}:** {card}   "
            )

        st.markdown(memory_text)

    else:

        st.info(
            "The AI has not seen any cards yet."
        )


    # --------------------------------------------------------
    # GAME COMPLETION
    # --------------------------------------------------------

    if len(st.session_state.matched) == len(
        st.session_state.cards
    ):

        st.session_state.game_over = True

        st.balloons()

        st.success("🎉 YOU WON!")

        st.write(
            f"### Final Score: {st.session_state.score}"
        )

        st.write(
            f"### Total Moves: {st.session_state.moves}"
        )

        if st.session_state.moves <= pairs_count + 2:

            st.success(
                "🧠 Amazing memory! You remembered the cards extremely well."
            )

        elif st.session_state.moves <= pairs_count * 2:

            st.info(
                "👍 Good memory! Try to improve your score."
            )

        else:

            st.warning(
                "😅 The AI Memory Bank had to work hard!"
            )


else:

    st.info(
        "👆 Choose a difficulty and click "
        "**Start / Restart Game** to begin."
    )


# ------------------------------------------------------------
# ABOUT THE AI
# ------------------------------------------------------------

with st.expander("🤖 How does the AI work?"):

    st.write("""
    This game contains a simple AI-style memory system.

    Whenever a card is revealed, the system records:

    • Which card was revealed  
    • Where the card was located  
    • Which symbols have already been seen  

    The AI Memory Bank therefore becomes larger as the
    player explores the board.

    The objective is to compare human memory with the
    computer's ability to store and recall information.
    """)


# ------------------------------------------------------------
# FOOTER
# ------------------------------------------------------------

st.divider()

st.caption(
    "🧠 AI Club Exhibition Project | AI Memory Match"
)
