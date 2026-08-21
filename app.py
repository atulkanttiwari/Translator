import re

import streamlit as st
from serve import chain


st.set_page_config(
    page_title="Lingo Forge",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Fraunces:opsz,wght@9..144,600&display=swap');

    :root {
        --ink: #172321;
        --muted: #63736e;
        --paper: #f7f4ed;
        --card: #fffdf8;
        --line: #dce4dd;
        --mint: #c9e5d3;
        --coral: #ed745b;
    }

    .stApp {
        background: radial-gradient(circle at 90% 4%, #dceee0 0, transparent 28%), var(--paper);
        color: var(--ink);
        font-family: 'DM Sans', sans-serif;
    }
    [data-testid="stSidebar"] {
        background: #203a35;
        color: #f7f4ed;
    }
    [data-testid="stSidebar"] * { color: #f7f4ed; }
    [data-testid="stSidebar"] .stCaption { color: #b8cbc1; }
    .hero { padding: 2.6rem 0 1.4rem; }
    .eyebrow { color: var(--coral); font-size: .75rem; font-weight: 700; letter-spacing: .13em; text-transform: uppercase; }
    h1, h2, h3 { color: var(--ink); font-family: 'Fraunces', Georgia, serif; }
    h1 { font-size: clamp(2.6rem, 5vw, 4.8rem); line-height: .98; margin: .35rem 0 .8rem; }
    .hero-copy { color: var(--muted); font-size: 1.06rem; max-width: 38rem; }
    .panel { background: rgba(255,253,248,.8); border: 1px solid var(--line); border-radius: 8px; padding: 1.2rem; min-height: 18rem; }
    .panel-label { color: var(--muted); font-size: .74rem; font-weight: 700; letter-spacing: .1em; text-transform: uppercase; margin-bottom: .7rem; }
    .result { background: #e4f1e6; border-left: 4px solid var(--coral); border-radius: 4px; min-height: 10rem; padding: 1.1rem 1.2rem; white-space: pre-wrap; font-size: 1.12rem; line-height: 1.6; }
    .empty { color: var(--muted); padding-top: 2.5rem; }
    div.stButton > button { background: var(--coral); border: 0; border-radius: 4px; color: white; font-weight: 700; min-height: 2.8rem; }
    div.stButton > button:hover { background: #d85e49; color: white; }
    textarea { background: var(--card) !important; border-color: var(--line) !important; }
    </style>
    """,
    unsafe_allow_html=True,
)


def clean_response(response: str) -> str:
    """Remove hidden reasoning if the selected model returns it."""
    cleaned = re.sub(r"<think>.*?</think>", "", response, flags=re.DOTALL | re.IGNORECASE)
    return cleaned.strip()


if "history" not in st.session_state:
    st.session_state.history = []

with st.sidebar:
    st.markdown("## Lingo Forge")
    st.caption("A quiet workspace for fast, natural translation.")
    st.divider()
    st.markdown("### Recent translations")
    if st.session_state.history:
        for item in st.session_state.history[-5:][::-1]:
            st.caption(f"{item['language']}  ·  {item['source'][:38]}")
    else:
        st.caption("Your completed translations will appear here.")
    st.divider()
    st.caption("Powered by Groq + LangChain")

st.markdown(
    """
    <div class="hero">
      <div class="eyebrow">English translation studio</div>
      <h1>Make every word<br>travel well.</h1>
      <div class="hero-copy">Translate a thought, a message, or a whole paragraph into the language your reader speaks.</div>
    </div>
    """,
    unsafe_allow_html=True,
)

left, right = st.columns(2, gap="large")
with left:
    st.markdown('<div class="panel-label">From English</div>', unsafe_allow_html=True)
    source_text = st.text_area(
        "Source text",
        placeholder="Type or paste your English text here...",
        height=220,
        label_visibility="collapsed",
    )

with right:
    st.markdown('<div class="panel-label">Translation</div>', unsafe_allow_html=True)
    if "translation" in st.session_state:
        st.markdown(f'<div class="result">{st.session_state.translation}</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="result empty">Your translation will appear here.</div>', unsafe_allow_html=True)

st.divider()
settings, action = st.columns([3, 1], vertical_alignment="bottom")
with settings:
    language = st.selectbox(
        "Translate into",
        ["French", "Spanish", "German", "Italian", "Portuguese", "Hindi", "Japanese", "Arabic"],
    )
with action:
    translate = st.button("Translate  →", use_container_width=True, type="primary")

if translate:
    if not source_text.strip():
        st.warning("Enter some English text first.")
    else:
        with st.spinner("Finding the right words..."):
            try:
                raw_translation = chain.invoke({"language": language, "text": source_text})
                translation = clean_response(str(raw_translation))
                st.session_state.translation = translation
                st.session_state.history.append({"language": language, "source": source_text})
                st.rerun()
            except Exception as error:
                st.error(f"Translation failed: {error}")

if st.session_state.get("translation"):
    st.download_button(
        "Download translation",
        data=st.session_state.translation,
        file_name=f"translation-{language.lower()}.txt",
        mime="text/plain",
    )
