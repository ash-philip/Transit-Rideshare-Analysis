from pathlib import Path

import streamlit as st


BASE_DIR = Path(__file__).resolve().parents[1]
CSS_FILE = BASE_DIR / "styles.css"


def load_css() -> None:
    if CSS_FILE.exists():
        with open(CSS_FILE, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


def page_header() -> None:
    st.markdown(
        """
        <div class="hero">
            <div class="hero-inner">
                <div class="eyebrow">Leadership Analytics • Synthetic Data • Planning Scenarios</div>
                <h1 class="hero-title">Rideshare Command Center</h1>
                <p class="hero-subtitle">
                    A decision-support dashboard for monitoring rideshare program health, financial sustainability,
                    forecast trends, and fare scenario tradeoffs.
                </p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def sidebar_navigation() -> str:
    st.sidebar.markdown("### Rideshare Command Center")
    st.sidebar.caption("Program health, forecasts, and planning scenarios.")
    return st.sidebar.radio(
        "Navigate",
        [
            "Executive Overview",
            "Program Health",
            "Forecast Center",
            "Scenario Simulator",
            "Recommendations",
        ],
    )


def section_title(title: str) -> None:
    st.markdown(f"<h2 class='section-title'>{title}</h2>", unsafe_allow_html=True)


def section_text(text: str) -> None:
    st.markdown(f"<p class='section-text'>{text}</p>", unsafe_allow_html=True)


def takeaway(text: str) -> None:
    st.markdown(
        f"""
        <div class="takeaway-box">
            <strong>Agency takeaway:</strong> {text}
        </div>
        """,
        unsafe_allow_html=True,
    )


def spacer() -> None:
    st.markdown("<div class='spacer'></div>", unsafe_allow_html=True)
