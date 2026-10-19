
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

if difficulty == "Easy":
    pairs_count = 4
    memorize_time = 5

elif difficulty == "Medium":
    pairs_count = 6
    memorize_time = 5

else:
    pairs_count = 8
    memorize_time = 7


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
# SESSION STATE
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

if "memorizing" not in st.session_state:
    st.session_state.memorizing = False

if "memorize_end" not in st.session_state:
    st.session_state.memorize_end = None


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

    # Start memorization phase
    st.session_state.memorizing = True
    st.session_state.memorize_end = time.time() + memorize_time


# ------------------------------------------------------------
# START BUTTON
# ------------------------------------------------------------

if st.button(
    "🔄 Start / Restart Game",
    use_container_width=True
):
    start_game()
    st.rerun()


# ------------------------------------------------------------
# MEMORIZATION PHASE
# ------------------------------------------------------------

if (
    st.session_state.game_started
    and st.session_state.memorizing
):
    pass


# ------------------------------------------------------------
# ACTUALLY START AFTER BUTTON
# ------------------------------------------------------------

# Detect if cards exist after start
if len(st.session_state.cards) > 0:

    # --------------------------------------------------------
    # MEMORIZATION COUNTDOWN
    # --------------------------------------------------------

    if st.session_state.memorizing:

        remaining = int(
            st.session_state.memorize_end - time.time()
        )

        if remaining <= 0:

            st.session_state.memorizing = False

            st.rerun()

        else:

            st.session_state.game_started = True

            st.markdown(
                f"""
                <div style="
                    text-align:center;
                    padding:15px;
                    border-radius:15px;
                    background:#eef6ff;
                    margin-bottom:15px;
                ">
                    <h2>👀 MEMORIZE THE CARDS!</h2>
                    <h3>⏱️ {remaining} seconds</h3>
                    <p>Remember the symbols and their positions.</p>
                </div>
                """,
                unsafe_allow_html=True
            )

            # Display ALL cards
            columns = 4

            for row in range(
                0,
                len(st.session_state.cards),
                columns
            ):

                cols = st.columns(columns)

                for col_index in range(columns):

                    index = row + col_index

                    if index >= len(st.session_state.cards):
                        continue

                    card = st.session_state.cards[index]

                    with cols[col_index]:

                        # Disabled button so player cannot click
                        st.button(
                            card,
                            key=f"memory_card_{index}",
                            use_container_width=True,
                            disabled=True
                        )

            # Automatically refresh countdown
            time.sleep(1)
            st.rerun()


    # --------------------------------------------------------
    # NORMAL GAME PHASE
    # --------------------------------------------------------

    else:

        st.session_state.game_started = True

        # ----------------------------------------------------
        # GAME STATUS
        # ----------------------------------------------------

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

        st.info(
            "🧠 The cards are hidden! "
            "Click two cards to find a matching pair."
        )


        # ----------------------------------------------------
        # GAME BOARD
        # ----------------------------------------------------

        columns = 4

        for row in range(
            0,
            len(st.session_state.cards),
            columns
        ):

            cols = st.columns(columns)

            for col_index in range(columns):

                index = row + col_index

                if index >= len(st.session_state.cards):
                    continue

                card = st.session_state.cards[index]


                # ------------------------------------------------
                # DECIDE WHAT TO DISPLAY
                # ------------------------------------------------

                if (
                    index in st.session_state.revealed
                    or index in st.session_state.matched
                ):
                    display_card = card

                else:
                    display_card = "❓"


                # ------------------------------------------------
                # CARD BUTTON
                # ------------------------------------------------

                with cols[col_index]:

                    if st.button(
                        display_card,
                        key=f"card_{index}",
                        use_container_width=True
                    ):

                        # Ignore cards already visible
                        if (
                            index not in st.session_state.revealed
                            and index not in st.session_state.matched
                        ):

                            # ------------------------------------
                            # AI MEMORY
                            # ------------------------------------

                            st.session_state.ai_memory[index] = card

                            st.session_state.revealed.append(index)


                            # ------------------------------------
                            # TWO CARDS SELECTED
                            # ------------------------------------

                            if len(
                                st.session_state.revealed
                            ) == 2:

                                first = (
                                    st.session_state.revealed[0]
                                )

                                second = (
                                    st.session_state.revealed[1]
                                )

                                st.session_state.moves += 1


                                # --------------------------------
                                # MATCH
                                # --------------------------------

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

                                    st.rerun()


                                # --------------------------------
                                # NOT A MATCH
                                # --------------------------------

                                else:

                                    st.session_state.score = max(
                                        0,
                                        st.session_state.score - 2
                                    )

                                    # Show both cards briefly
                                    st.rerun()


        # ----------------------------------------------------
        # HANDLE INCORRECT MATCH
        # ----------------------------------------------------

        if len(st.session_state.revealed) == 2:

            st.warning(
                "❌ Not a match! The cards will turn over..."
            )

            time.sleep(1)

            st.session_state.revealed = []

            st.rerun()


        # ----------------------------------------------------
        # AI MEMORY DISPLAY
        # ----------------------------------------------------

        st.divider()

        st.subheader("🧠 AI Memory Bank")

        if st.session_state.ai_memory:

            memory_text = ""

            for position, card in (
                st.session_state.ai_memory.items()
            ):

                memory_text += (
                    f"**Card {position + 1}:** {card}   "
                )

            st.markdown(memory_text)

        else:

            st.info(
                "The AI has not seen any cards yet."
            )


        # ----------------------------------------------------
        # GAME COMPLETION
        # ----------------------------------------------------

        if len(st.session_state.matched) == len(
            st.session_state.cards
        ):

            st.session_state.game_over = True

            st.balloons()

            st.success("🎉 YOU WON!")

            st.write(
                f"### Final Score: "
                f"{st.session_state.score}"
            )

            st.write(
                f"### Total Moves: "
                f"{st.session_state.moves}"
            )

            if st.session_state.moves <= pairs_count + 2:

                st.success(
                    "🧠 AMAZING MEMORY! "
                    "You remembered the cards extremely well."
                )

            elif st.session_state.moves <= pairs_count * 2:

                st.info(
                    "👍 GOOD MEMORY! "
                    "Try to improve your score."
                )

            else:

                st.warning(
                    "😅 The AI Memory Bank had to work hard!"
                )


# ------------------------------------------------------------
# INITIAL SCREEN
# ------------------------------------------------------------

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

    The AI Memory Bank therefore becomes larger as
    the player explores the board.

    The objective is to compare human memory with
    the computer's ability to store and recall information.
    """)


# ------------------------------------------------------------
# FOOTER
# ------------------------------------------------------------

st.divider()

st.caption(
    "🧠 AI Club Exhibition Project | AI Memory Match"
)

