from pathlib import Path

import streamlit as st


BASE_DIR = Path(__file__).resolve().parents[1]
CSS_FILE = BASE_DIR / "styles.css"
PAGES = [
    "Executive Overview",
    "Program Health",
    "Forecast Center",
    "Scenario Simulator",
    "Planning Signals",
]


def load_css() -> None:
    if CSS_FILE.exists():
        with open(CSS_FILE, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


def page_header() -> str:
    if "selected_page" not in st.session_state:
        st.session_state.selected_page = PAGES[0]

    current_page = st.session_state.selected_page
    if current_page not in PAGES:
        current_page = PAGES[0]

    st.markdown("<div class='app-header-shell'>", unsafe_allow_html=True)
    menu_col, title_col = st.columns([0.12, 0.88], vertical_alignment="center")

    with menu_col:
        if hasattr(st, "popover"):
            with st.popover("☰", use_container_width=True):
                selected_page = st.radio(
                    "Page",
                    PAGES,
                    index=PAGES.index(current_page),
                    key="page_navigation_choice",
                )
        else:
            selected_page = st.selectbox(
                "Page",
                PAGES,
                index=PAGES.index(current_page),
                key="page_navigation_choice",
                label_visibility="collapsed",
            )

    with title_col:
        st.markdown(
            """
            <div class="hero">
                <div class="eyebrow">Interactive Dashboard • Synthetic Data • Planning Scenarios</div>
                <h1 class="hero-title">Rideshare Command Center</h1>
                <p class="hero-subtitle">
                    Monitor program health, review demand and financial trends, and compare sustainability scenarios
                    from one decision-support workspace.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("</div>", unsafe_allow_html=True)
    st.session_state.selected_page = selected_page
    return selected_page


def section_title(title: str) -> None:
    st.markdown(f"<h2 class='section-title'>{title}</h2>", unsafe_allow_html=True)


def section_text(text: str) -> None:
    st.markdown(f"<p class='section-text'>{text}</p>", unsafe_allow_html=True)


def takeaway(text: str) -> None:
    st.markdown(
        f"""
        <div class="takeaway-box">
            <strong>Dashboard signal:</strong> {text}
        </div>
        """,
        unsafe_allow_html=True,
    )


def spacer() -> None:
    st.markdown("<div class='spacer'></div>", unsafe_allow_html=True)


def view_selector(label: str, options: list[str], key: str | None = None) -> str:
    st.markdown(f"<div class='view-selector-label'>{label}</div>", unsafe_allow_html=True)
    return st.radio(
        label,
        options,
        key=key,
        label_visibility="collapsed",
    )
