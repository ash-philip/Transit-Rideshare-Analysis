from pathlib import Path
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


st.set_page_config(
    page_title="Transit Rideshare Analytics Pipeline",
    page_icon="📈",
    layout="wide",
)

BASE_DIR = Path(__file__).resolve().parent
ASSETS_DIR = BASE_DIR / "assets"
CSS_FILE = BASE_DIR / "styles.css"
PROJECT_ROOT = BASE_DIR.parent
DATA_DIR = PROJECT_ROOT / "data" / "processed"


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

def load_master_data() -> pd.DataFrame:
    df = pd.read_csv(DATA_DIR / "rs_monthly_master.csv")
    df["date"] = pd.to_datetime(df["year_month"] + "-01")
    return df


def load_business_forecast() -> pd.DataFrame:
    df = pd.read_csv(DATA_DIR / "business_forecast_12m.csv")
    df["date"] = pd.to_datetime(df["date"])
    return df


def load_farebox_history_forecast() -> pd.DataFrame:
    df = pd.read_csv(DATA_DIR / "farebox_recovery_history_forecast.csv")
    df["date"] = pd.to_datetime(df["date"])
    return df


def load_scenario_summary() -> pd.DataFrame:
    return pd.read_csv(DATA_DIR / "scenario_summary.csv")

def style_plotly(fig: go.Figure) -> go.Figure:
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(255,255,255,0.02)",
        font=dict(color="#e5e7eb", family="Inter, sans-serif"),
        margin=dict(l=20, r=20, t=60, b=20),
        title=dict(font=dict(size=22)),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1.0,
            bgcolor="rgba(0,0,0,0)"
        ),
    )
    fig.update_xaxes(
        showgrid=False,
        zeroline=False,
        title_font=dict(size=14),
        tickfont=dict(size=12),
    )
    fig.update_yaxes(
        gridcolor="rgba(255,255,255,0.08)",
        zeroline=False,
        title_font=dict(size=14),
        tickfont=dict(size=12),
    )
    return fig

load_css()
master_df = load_master_data()
business_forecast_df = load_business_forecast()
farebox_history_forecast_df = load_farebox_history_forecast()
scenario_summary_df = load_scenario_summary()

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

section_title("Performance Snapshot")
section_text(
    "The service carries substantial ridership volume, generates meaningful revenue, and shows moderate cost recovery, but the financial outlook remains sensitive to pricing and operating cost assumptions."
)

total_boardings = int(master_df["boardings"].sum())
total_revenue = master_df["revenue"].sum()
avg_farebox_recovery = master_df["farebox_recovery"].mean()
avg_cost_per_boarding = master_df["cost_per_boarding"].mean()

formatted_total_boardings = f"{total_boardings:,.0f}"
formatted_total_revenue = f"${total_revenue / 1_000_000:.2f}M"
formatted_avg_farebox = f"{avg_farebox_recovery:.2%}"
formatted_avg_cost_per_boarding = f"${avg_cost_per_boarding:.2f}"

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-value">{formatted_total_boardings}</div>
            <div class="kpi-label">Total Boardings</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-value">{formatted_total_revenue}</div>
            <div class="kpi-label">Total Revenue</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col3:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-value">{formatted_avg_farebox}</div>
            <div class="kpi-label">Avg Farebox Recovery</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col4:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-value">{formatted_avg_cost_per_boarding}</div>
            <div class="kpi-label">Avg Cost per Boarding</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("<div class='spacer'></div>", unsafe_allow_html=True)

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
        master_df,
        x="date",
        y="boardings",
        title="Monthly Boardings",
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
    master_df,
    x="date",
    y="farebox_recovery",
    title="Farebox Recovery Over Time",
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
        color_discrete_map={
            "Historical": "#38bdf8",
            "Forecast": "#a7f3d0",
        },
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

scenario_order = [
    "Base Case",
    "Moderate Fare Increase",
    "Higher Fare Increase",
    "Fare Increase + Cost Pressure",
]

scenario_plot_df = scenario_summary_df.copy()
scenario_plot_df["scenario_name"] = pd.Categorical(
    scenario_plot_df["scenario_name"],
    categories=scenario_order,
    ordered=True,
)
scenario_plot_df = scenario_plot_df.sort_values("scenario_name")

with c5:
    fig_scenario_recovery = px.bar(
        scenario_plot_df,
        x="scenario_name",
        y="scenario_farebox_recovery",
        title="Average Farebox Recovery by Scenario",
    )
    fig_scenario_recovery.update_traces(marker_color="#86efac")
    fig_scenario_recovery.update_yaxes(title="Avg Farebox Recovery", tickformat=".0%")
    fig_scenario_recovery.update_xaxes(title="Scenario")
    st.plotly_chart(
        style_plotly(fig_scenario_recovery),
        use_container_width=True,
        config={"displayModeBar": False, "responsive": True},
    )

with c6:
    fig_scenario_boardings = px.bar(
        scenario_plot_df,
        x="scenario_name",
        y="scenario_boardings",
        title="Average Boardings by Scenario",
    )
    fig_scenario_boardings.update_traces(marker_color="#facc15")
    fig_scenario_boardings.update_yaxes(title="Avg Boardings")
    fig_scenario_boardings.update_xaxes(title="Scenario")
    st.plotly_chart(
        style_plotly(fig_scenario_boardings),
        use_container_width=True,
        config={"displayModeBar": False, "responsive": True},
    )

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

