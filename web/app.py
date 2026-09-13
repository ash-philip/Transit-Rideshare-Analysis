from pathlib import Path
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(
    page_title="Transit Rideshare Analytics Pipeline",
    page_icon="📈",
    layout="wide",
)

# --- DIRECTORY CONFIGURATION ---
BASE_DIR = Path(__file__).resolve().parent
ASSETS_DIR = BASE_DIR / "assets"
CSS_FILE = BASE_DIR / "styles.css"
PROJECT_ROOT = BASE_DIR.parent
DATA_DIR = PROJECT_ROOT / "data" / "processed"


# --- PERFORMANCE: CACHED IO & DATA INGESTION ---
@st.cache_data(show_spinner=False)
def get_custom_css() -> str:
    """Cache stylesheet in memory so disk is not accessed on rerun."""
    if CSS_FILE.exists():
        with open(CSS_FILE, "r", encoding="utf-8") as f:
            return f.read()
    return ""


def apply_css() -> None:
    css = get_custom_css()
    if css:
        st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)


@st.cache_data(show_spinner=False)
def load_all_data():
    """Load, parse, and pre-structure all datasets in a single cached pass."""
    # 1. Master Historical Data
    master_df = pd.read_csv(DATA_DIR / "rs_monthly_master.csv")
    master_df["date"] = pd.to_datetime(master_df["year_month"] + "-01")

    # Pre-calculated KPI string formatting
    kpis = {
        "boardings": f"{int(master_df['boardings'].sum()):,.0f}",
        "revenue": f"${master_df['revenue'].sum() / 1_000_000:.2f}M",
        "farebox": f"{master_df['farebox_recovery'].mean():.2%}",
        "cost_per_boarding": f"${master_df['cost_per_boarding'].mean():.2f}",
    }

    # 2. Business Forecast
    forecast_df = pd.read_csv(DATA_DIR / "business_forecast_12m.csv")
    forecast_df["date"] = pd.to_datetime(forecast_df["date"])

    # 3. Farebox Recovery History vs Forecast
    farebox_df = pd.read_csv(DATA_DIR / "farebox_recovery_history_forecast.csv")
    farebox_df["date"] = pd.to_datetime(farebox_df["date"])

    # 4. Scenario Summary with Ordered Categoricals
    scenario_df = pd.read_csv(DATA_DIR / "scenario_summary.csv")
    scenario_order = [
        "Base Case",
        "Moderate Fare Increase",
        "Higher Fare Increase",
        "Fare Increase + Cost Pressure",
    ]
    scenario_df["scenario_name"] = pd.Categorical(
        scenario_df["scenario_name"], categories=scenario_order, ordered=True
    )
    scenario_df = scenario_df.sort_values("scenario_name").reset_index(
        drop=True
    )

    return master_df, forecast_df, farebox_df, scenario_df, kpis


# Static Plotly template configuration
PLOTLY_TEMPLATE = go.layout.Template(
    layout=go.Layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(255,255,255,0.02)",
        font=dict(color="#e5e7eb", family="Inter, sans-serif"),
        margin=dict(l=20, r=20, t=60, b=20),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1.0,
            bgcolor="rgba(0,0,0,0)",
        ),
        xaxis=dict(
            showgrid=False,
            zeroline=False,
            title_font=dict(size=14),
            tickfont=dict(size=12),
        ),
        yaxis=dict(
            gridcolor="rgba(255,255,255,0.08)",
            zeroline=False,
            title_font=dict(size=14),
            tickfont=dict(size=12),
        ),
    )
)


def style_plotly(fig: go.Figure) -> go.Figure:
    fig.update_layout(template=PLOTLY_TEMPLATE)
    return fig


def section_title(title: str) -> None:
    st.markdown(f"<h2 class='section-title'>{title}</h2>", unsafe_allow_html=True)


def section_text(text: str) -> None:
    st.markdown(f"<p class='section-text'>{text}</p>", unsafe_allow_html=True)


# --- INITIALIZATION ---
apply_css()
(
    master_df,
    business_forecast_df,
    farebox_history_forecast_df,
    scenario_summary_df,
    kpis,
) = load_all_data()

# --- HERO SECTION ---
st.markdown(
    """
    <div class="hero">
        <div class="hero-inner">
            <div class="eyebrow">Portfolio Project • Synthetic Data • Transit Analytics</div>
            <h1 class="hero-title">Transit Rideshare Analytics Pipeline</h1>
            <p class="hero-subtitle">
                An end-to-end analytics project using synthetic transit rideshare data to evaluate service recovery,
                financial sustainability, forecasted performance, and pricing tradeoffs.
            </p>
            <p class="hero-hook">
                As demand returns, transit agencies still face a harder question: are recent gains sustainable, and what
                policy choices improve long-term cost recovery without undermining ridership?
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
    Transit agencies are expected to provide reliable, accessible service while operating within financial constraints.
    For rideshare and vanpool programs in particular, performance depends not only on ridership, but also on how
    operating cost, pricing, and recovery trends evolve over time.
    """
)
section_text(
    """
    Even when demand begins to recover, agency leadership still needs to determine whether that recovery is strong enough
    to support long-term financial sustainability. This project approaches that challenge through a synthetic transit
    rideshare use case, using an end-to-end analytics pipeline that moves from data generation and ETL to forecasting
    and scenario analysis.
    """
)

st.markdown("<div class='spacer'></div>", unsafe_allow_html=True)

# --- KPI METRIC STRIP ---
section_title("Performance Snapshot")
section_text(
    "The service carries substantial ridership volume, generates meaningful revenue, and shows moderate cost recovery, but the financial outlook remains sensitive to pricing and operating cost assumptions."
)

col1, col2, col3, col4 = st.columns(4)
col1.markdown(
    f"""<div class="kpi-card"><div class="kpi-value">{kpis['boardings']}</div><div class="kpi-label">Total Boardings</div></div>""",
    unsafe_allow_html=True,
)
col2.markdown(
    f"""<div class="kpi-card"><div class="kpi-value">{kpis['revenue']}</div><div class="kpi-label">Total Revenue</div></div>""",
    unsafe_allow_html=True,
)
col3.markdown(
    f"""<div class="kpi-card"><div class="kpi-value">{kpis['farebox']}</div><div class="kpi-label">Avg Farebox Recovery</div></div>""",
    unsafe_allow_html=True,
)
col4.markdown(
    f"""<div class="kpi-card"><div class="kpi-value">{kpis['cost_per_boarding']}</div><div class="kpi-label">Avg Cost per Boarding</div></div>""",
    unsafe_allow_html=True,
)

st.markdown("<div class='spacer'></div>", unsafe_allow_html=True)

# --- CHAPTER 1: HISTORICAL RECOVERY ---
section_title("Chapter 1: Recovery Was Real, But Uneven")
section_text(
    """
    Service demand declined sharply during the pandemic period and then recovered gradually over time. Revenue moved
    in the same direction, but total operating cost remained more stable, which created sustained pressure on cost
    recovery during lower-demand periods.
    """
)
section_text(
    """
    For an agency, this distinction matters. Recovery is not defined by ridership alone. It also depends on whether
    returning demand is sufficient to improve financial performance and narrow the gap between revenue and operating cost.
    """
)

c1, c2 = st.columns(2)
with c1:
    fig_boardings = px.line(
        master_df, x="date", y="boardings", title="Monthly Boardings"
    )
    fig_boardings.update_traces(line=dict(color="#60a5fa", width=3))
    fig_boardings.update_yaxes(title="Boardings")
    fig_boardings.update_xaxes(title="Date")
    st.plotly_chart(
        style_plotly(fig_boardings),
        use_container_width=True,
        config={"displayModeBar": False, "responsive": True},
    )

with c2:
    fig_rev_cost = go.Figure()
    fig_rev_cost.add_trace(
        go.Scatter(
            x=master_df["date"],
            y=master_df["revenue"],
            mode="lines",
            name="Revenue",
            line=dict(color="#60a5fa", width=3),
        )
    )
    fig_rev_cost.add_trace(
        go.Scatter(
            x=master_df["date"],
            y=master_df["total_cost"],
            mode="lines",
            name="Total Cost",
            line=dict(color="#facc15", width=3),
        )
    )
    fig_rev_cost.update_layout(title="Revenue vs Total Cost")
    fig_rev_cost.update_yaxes(title="Amount ($)")
    fig_rev_cost.update_xaxes(title="Date")
    st.plotly_chart(
        style_plotly(fig_rev_cost),
        use_container_width=True,
        config={"displayModeBar": False, "responsive": True},
    )

fig_farebox = px.line(
    master_df, x="date", y="farebox_recovery", title="Farebox Recovery Over Time"
)
fig_farebox.update_traces(line=dict(color="#86efac", width=3))
fig_farebox.update_yaxes(title="Farebox Recovery", tickformat=".0%")
fig_farebox.update_xaxes(title="Date")
st.plotly_chart(
    style_plotly(fig_farebox),
    use_container_width=True,
    config={"displayModeBar": False, "responsive": True},
)

st.markdown(
    """
    <div class="takeaway-box">
        <strong>Agency takeaway:</strong> Ridership recovery was meaningful, but financial recovery was slower and less
        consistent because operating cost remained comparatively stable throughout the recovery period.
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("<div class='spacer'></div>", unsafe_allow_html=True)

# --- CHAPTER 2: FORECAST ---
section_title("Chapter 2: The Next Year Looks Stable, But Not Fully Solved")
section_text(
    """
    Looking ahead, the baseline forecast suggests that ridership remains relatively stable over the next 12 months.
    However, farebox recovery continues to fluctuate seasonally rather than improve in a straight line, which indicates
    that recent progress may be leveling off rather than accelerating.
    """
)
section_text(
    """
    For agency planning, this shifts the challenge from short-term recovery to long-term sustainability. A stable outlook
    is encouraging, but it does not eliminate the need to test how future pricing or cost changes could alter the agency’s
    financial position.
    """
)

c3, c4 = st.columns(2)
with c3:
    fig_forecast_boardings = px.line(
        business_forecast_df,
        x="date",
        y="forecast_boardings",
        title="12-Month Boardings Forecast",
    )
    fig_forecast_boardings.update_traces(line=dict(color="#60a5fa", width=3))
    fig_forecast_boardings.update_yaxes(title="Forecast Boardings")
    fig_forecast_boardings.update_xaxes(title="Date")
    st.plotly_chart(
        style_plotly(fig_forecast_boardings),
        use_container_width=True,
        config={"displayModeBar": False, "responsive": True},
    )

with c4:
    fig_hist_forecast = px.line(
        farebox_history_forecast_df,
        x="date",
        y="farebox_recovery_value",
        color="series_type",
        title="Historical and Forecasted Farebox Recovery",
        color_discrete_map={"Historical": "#38bdf8", "Forecast": "#a7f3d0"},
    )
    fig_hist_forecast.update_traces(line=dict(width=3))
    fig_hist_forecast.update_yaxes(title="Farebox Recovery", tickformat=".0%")
    fig_hist_forecast.update_xaxes(title="Date")
    fig_hist_forecast.update_layout(legend_title_text="")
    st.plotly_chart(
        style_plotly(fig_hist_forecast),
        use_container_width=True,
        config={"displayModeBar": False, "responsive": True},
    )

st.markdown(
    """
    <div class="takeaway-box">
        <strong>Agency takeaway:</strong> The baseline outlook is stable, but not fully resolved. Future gains remain
        sensitive to pricing assumptions and ongoing operating cost pressure.
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("<div class='spacer'></div>", unsafe_allow_html=True)

# --- CHAPTER 3: SCENARIO ANALYSIS ---
section_title("Chapter 3: Pricing Helps, But Tradeoffs Matter")
section_text(
    """
    Scenario analysis was used to test how alternative fare and cost assumptions affect ridership and cost recovery.
    Under the current assumptions, higher fares improve farebox recovery, but they also reduce boardings. That means
    the strongest financial result is not automatically the most balanced operational strategy.
    """
)
section_text(
    """
    From an agency perspective, the more practical question is not simply which scenario maximizes recovery, but which
    scenario improves financial performance while preserving enough ridership to support service goals and long-term demand.
    """
)

c5, c6 = st.columns(2)

with c5:
    st.markdown(
        """
        <div class="chart-card">
            <div class="chart-header">
                <div>
                    <p class="chart-title">Farebox Recovery Rate</p>
                    <p class="chart-caption">Simulated agency cost-recovery across policy levers</p>
                </div>
            </div>
    """,
        unsafe_allow_html=True,
    )

    st.plotly_chart(
        style_plotly(fig_scenario_recovery),
        use_container_width=True,
        config={"displayModeBar": False, "responsive": True},
    )
    st.markdown("</div>", unsafe_allow_html=True)

with c6:
    st.markdown(
        """
        <div class="chart-card">
            <div class="chart-header">
                <div>
                    <p class="chart-title">Projected Monthly Boardings</p>
                    <p class="chart-caption">Estimated demand elasticity impact by scenario</p>
                </div>
            </div>
    """,
        unsafe_allow_html=True,
    )

    st.plotly_chart(
        style_plotly(fig_scenario_boardings),
        use_container_width=True,
        config={"displayModeBar": False, "responsive": True},
    )
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown(
    """
    <div class="takeaway-box">
        <strong>Agency takeaway:</strong> Higher fare increases produce the strongest recovery under current assumptions,
        but a moderate fare increase may offer a more balanced path by improving cost recovery while limiting ridership loss.
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("<div class='spacer'></div>", unsafe_allow_html=True)

# --- CONCLUSION & METHODOLOGY ---
section_title("Final Takeaway")
section_text(
    """
    The rideshare service appears to have recovered meaningfully, but the analysis suggests that recent gains may be
    difficult to sustain without targeted action. Forecasting and scenario analysis indicate that future performance will
    depend not only on continued demand, but also on how pricing and operating cost pressure are managed together.
    """
)
section_text(
    """
    In practice, this means the agency’s challenge is no longer simply restoring service performance. It is determining
    which decisions can improve long-term financial sustainability without undermining ridership and service value.
    """
)

st.markdown("<div class='spacer'></div>", unsafe_allow_html=True)

section_title("Methodology")
left, right = st.columns([2, 1])
with left:
    section_text(
        """
        This project was built as a full analytics pipeline using synthetic transit data designed to preserve realistic
        service, cost, and recovery patterns without using confidential or proprietary agency data. The workflow combines
        data generation, ETL, KPI development, forecasting, and scenario analysis to support a more decision-oriented view
        of transit performance.
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
