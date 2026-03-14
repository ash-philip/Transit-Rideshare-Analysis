from pathlib import Path
import streamlit as st


st.set_page_config(
    page_title="Transit Rideshare Analytics Pipeline",
    page_icon="📈",
    layout="wide",
)

BASE_DIR = Path(__file__).resolve().parent
ASSETS_DIR = BASE_DIR / "assets"
CSS_FILE = BASE_DIR / "styles.css"


def load_css() -> None:
    if CSS_FILE.exists():
        with open(CSS_FILE, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


def image_path(filename: str) -> Path:
    return ASSETS_DIR / filename


def section_title(title: str) -> None:
    st.markdown(f"<h2 class='section-title'>{title}</h2>", unsafe_allow_html=True)


def section_text(text: str) -> None:
    st.markdown(f"<p class='section-text'>{text}</p>", unsafe_allow_html=True)


load_css()

st.markdown(
    """
    <div class="hero">
        <div class="hero-inner">
            <div class="eyebrow">Portfolio Project • Synthetic Data • Transit Analytics</div>
            <h1 class="hero-title">Transit Rideshare Analytics Pipeline</h1>
            <p class="hero-subtitle">
                A story-driven analytics project using synthetic transit data to evaluate ridership recovery,
                financial sustainability, forecasting, and pricing tradeoffs.
            </p>
            <p class="hero-hook">
                From disruption to recovery to planning: how can a transit agency sustain performance
                and improve farebox recovery?
            </p>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("<div class='spacer'></div>", unsafe_allow_html=True)

section_title("Why This Matters")
section_text(
    """
    Public transit services are not evaluated through ridership alone. Agencies must balance demand,
    revenue, operating cost, and long-term financial sustainability. Even when a service begins to recover,
    leadership still needs to understand whether recent gains are durable and what actions could improve
    future outcomes.
    """
)
section_text(
    """
    This project explores that problem through a synthetic transit rideshare use case, using an end-to-end
    analytics pipeline that moves from data generation and ETL to forecasting and scenario analysis.
    """
)

st.markdown("<div class='spacer'></div>", unsafe_allow_html=True)

section_title("Performance Snapshot")
section_text(
    "At a glance, the service shows meaningful ridership volume, moderate cost recovery, and a cost structure that makes long-term financial monitoring important."
)

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(
        """
        <div class="kpi-card">
            <div class="kpi-value">551,895</div>
            <div class="kpi-label">Total Boardings</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with col2:
    st.markdown(
        """
        <div class="kpi-card">
            <div class="kpi-value">$2.31M</div>
            <div class="kpi-label">Total Revenue</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with col3:
    st.markdown(
        """
        <div class="kpi-card">
            <div class="kpi-value">74.76%</div>
            <div class="kpi-label">Avg Farebox Recovery</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with col4:
    st.markdown(
        """
        <div class="kpi-card">
            <div class="kpi-value">$5.94</div>
            <div class="kpi-label">Avg Cost per Boarding</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("<div class='spacer'></div>", unsafe_allow_html=True)

section_title("Chapter 1: Recovery Was Real, But Uneven")
section_text(
    """
    Ridership fell sharply during the disruption period and then recovered gradually over time. Revenue generally
    followed the same pattern, while total operating cost remained more stable. As a result, financial recovery
    lagged demand recovery in some periods and improved only as ridership became more consistent.
    """
)
section_text(
    """
    The recovery story was not just about demand returning. It was also about whether revenue could recover fast
    enough to close the gap with operating cost.
    """
)

c1, c2 = st.columns(2)
with c1:
    if image_path("monthly_boardings.png").exists():
        st.image(str(image_path("monthly_boardings.png")), caption="Monthly Boardings", use_container_width=True)
with c2:
    if image_path("revenue_vs_total_cost.png").exists():
        st.image(str(image_path("revenue_vs_total_cost.png")), caption="Revenue vs Total Cost", use_container_width=True)

if image_path("farebox_recovery_over_time.png").exists():
    st.image(
        str(image_path("farebox_recovery_over_time.png")),
        caption="Farebox Recovery Over Time",
        use_container_width=True,
    )

st.markdown(
    """
    <div class="takeaway-box">
        <strong>Takeaway:</strong> The service recovered meaningfully, but the improvement in financial performance
        was more gradual than the improvement in ridership alone.
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("<div class='spacer'></div>", unsafe_allow_html=True)

section_title("Chapter 2: The Next Year Looks Stable, But Not Fully Solved")
section_text(
    """
    To move beyond historical reporting, the project develops a forward-looking view of service demand and financial
    performance. The baseline forecast suggests that ridership remains relatively stable over the next year, while
    farebox recovery continues to fluctuate seasonally rather than improve in a straight line.
    """
)
section_text(
    """
    This matters because it shifts the agency’s challenge from short-term recovery to long-term sustainability.
    """
)

c3, c4 = st.columns(2)
with c3:
    if image_path("boardings_forecast_12m.png").exists():
        st.image(
            str(image_path("boardings_forecast_12m.png")),
            caption="12-Month Boardings Forecast",
            use_container_width=True,
        )
with c4:
    if image_path("farebox_recovery_history_forecast.png").exists():
        st.image(
            str(image_path("farebox_recovery_history_forecast.png")),
            caption="Historical and Forecasted Farebox Recovery",
            use_container_width=True,
        )

st.markdown(
    """
    <div class="takeaway-box">
        <strong>Takeaway:</strong> The baseline outlook is steady, but not fully optimized. Future pricing and cost
        assumptions still meaningfully affect long-term performance.
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("<div class='spacer'></div>", unsafe_allow_html=True)

section_title("Chapter 3: Pricing Helps, But Tradeoffs Matter")
section_text(
    """
    Scenario analysis was used to evaluate how alternative fare and cost assumptions affect boardings, revenue,
    and farebox recovery. Under the current assumptions, higher fares improve farebox recovery, but they also
    reduce ridership. This means that the strongest financial result is not automatically the best policy.
    """
)
section_text(
    """
    A moderate fare increase may offer a more balanced tradeoff between financial improvement and ridership preservation.
    """
)

c5, c6 = st.columns(2)
with c5:
    if image_path("avg_farebox_recovery_by_scenario.png").exists():
        st.image(
            str(image_path("avg_farebox_recovery_by_scenario.png")),
            caption="Average Farebox Recovery by Scenario",
            use_container_width=True,
        )
with c6:
    if image_path("avg_boardings_by_scenario.png").exists():
        st.image(
            str(image_path("avg_boardings_by_scenario.png")),
            caption="Average Boardings by Scenario",
            use_container_width=True,
        )

st.markdown(
    """
    <div class="takeaway-box">
        <strong>Key takeaway:</strong> Higher fare increases produce the strongest farebox recovery under the current
        assumptions, but moderate fare increases may represent a more balanced strategy when ridership preservation
        also matters.
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("<div class='spacer'></div>", unsafe_allow_html=True)

section_title("Final Takeaway")
section_text(
    """
    The rideshare service appears to have recovered meaningfully, but recent gains may be difficult to sustain without
    targeted action. Forecasting and scenario analysis suggest that future progress depends not just on continued demand,
    but on how pricing and cost pressure are managed together.
    """
)
section_text(
    """
    This project demonstrates how an analytics workflow can move beyond descriptive reporting and support more strategic,
    decision-oriented planning.
    """
)

st.markdown("<div class='spacer'></div>", unsafe_allow_html=True)

section_title("Methodology")

left, right = st.columns([2, 1])
with left:
    section_text(
        """
        This project was built as a full analytics pipeline using synthetic transit data designed to preserve realistic
        business structure and temporal behavior without using confidential source data.
        """
    )
with right:
    st.markdown(
        """
        <div class="method-box">
            <div class="method-title">Methods Used</div>
            <ul>
                <li>Synthetic monthly data generation</li>
                <li>ETL and monthly spine creation</li>
                <li>KPI engineering</li>
                <li>Descriptive and diagnostic analysis</li>
                <li>Time-series forecasting</li>
                <li>Scenario analysis using fare and cost assumptions</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("<div class='spacer'></div>", unsafe_allow_html=True)

section_title("Project Links")
section_text("Explore the repository, documentation, and project assets below.")

st.markdown(
    """
    <div class="links-box">
        <a href="https://github.com/ash-philip/Transit-Rideshare-Analysis" target="_blank">GitHub Repository</a>
    </div>
    """,
    unsafe_allow_html=True,
)

