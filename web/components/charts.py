import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


SCENARIO_ORDER = [
    "Base Case",
    "Moderate Fare Increase",
    "Higher Fare Increase",
    "Fare Increase + Cost Pressure",
]


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
            bgcolor="rgba(0,0,0,0)",
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


def monthly_boardings(master_df: pd.DataFrame) -> go.Figure:
    fig = px.line(master_df, x="date", y="boardings", title="Monthly Boardings")
    fig.update_traces(line=dict(color="#60a5fa", width=3))
    fig.update_yaxes(title="Boardings")
    fig.update_xaxes(title="Date")
    return style_plotly(fig)


def revenue_vs_total_cost(master_df: pd.DataFrame) -> go.Figure:
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=master_df["date"],
            y=master_df["revenue"],
            mode="lines",
            name="Revenue",
            line=dict(color="#60a5fa", width=3),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=master_df["date"],
            y=master_df["total_cost"],
            mode="lines",
            name="Total Cost",
            line=dict(color="#facc15", width=3),
        )
    )
    fig.update_layout(title="Revenue vs Total Cost")
    fig.update_yaxes(title="Amount ($)")
    fig.update_xaxes(title="Date")
    return style_plotly(fig)


def farebox_recovery(master_df: pd.DataFrame) -> go.Figure:
    fig = px.line(
        master_df,
        x="date",
        y="farebox_recovery",
        title="Farebox Recovery Over Time",
    )
    fig.update_traces(line=dict(color="#86efac", width=3))
    fig.update_yaxes(title="Farebox Recovery", tickformat=".0%")
    fig.update_xaxes(title="Date")
    return style_plotly(fig)


def forecast_boardings(business_forecast_df: pd.DataFrame) -> go.Figure:
    fig = px.line(
        business_forecast_df,
        x="date",
        y="forecast_boardings",
        title="12-Month Boardings Forecast",
    )
    fig.update_traces(line=dict(color="#60a5fa", width=3))
    fig.update_yaxes(title="Forecast Boardings")
    fig.update_xaxes(title="Date")
    return style_plotly(fig)


def historical_forecast_farebox(farebox_history_forecast_df: pd.DataFrame) -> go.Figure:
    fig = px.line(
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
    fig.update_traces(line=dict(width=3))
    fig.update_yaxes(title="Farebox Recovery", tickformat=".0%")
    fig.update_xaxes(title="Date")
    fig.update_layout(legend_title_text="")
    return style_plotly(fig)


def scenario_plot_data(scenario_summary_df: pd.DataFrame) -> pd.DataFrame:
    scenario_plot_df = scenario_summary_df.copy()
    scenario_plot_df["scenario_name"] = pd.Categorical(
        scenario_plot_df["scenario_name"],
        categories=SCENARIO_ORDER,
        ordered=True,
    )
    return scenario_plot_df.sort_values("scenario_name")


def scenario_farebox_recovery(scenario_summary_df: pd.DataFrame) -> go.Figure:
    fig = px.bar(
        scenario_plot_data(scenario_summary_df),
        x="scenario_name",
        y="scenario_farebox_recovery",
        title="Average Farebox Recovery by Scenario",
    )
    fig.update_traces(marker_color="#86efac")
    fig.update_yaxes(title="Avg Farebox Recovery", tickformat=".0%")
    fig.update_xaxes(title="Scenario")
    return style_plotly(fig)


def scenario_boardings(scenario_summary_df: pd.DataFrame) -> go.Figure:
    fig = px.bar(
        scenario_plot_data(scenario_summary_df),
        x="scenario_name",
        y="scenario_boardings",
        title="Average Boardings by Scenario",
    )
    fig.update_traces(marker_color="#facc15")
    fig.update_yaxes(title="Avg Boardings")
    fig.update_xaxes(title="Scenario")
    return style_plotly(fig)
