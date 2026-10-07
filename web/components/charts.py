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


def set_chart_height(fig: go.Figure, height: int = 430) -> go.Figure:
    fig.update_layout(height=height)
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


def cost_per_boarding(master_df: pd.DataFrame) -> go.Figure:
    fig = px.line(
        master_df,
        x="date",
        y="cost_per_boarding",
        title="Cost per Boarding Over Time",
    )
    fig.update_traces(line=dict(color="#fb7185", width=3))
    fig.update_yaxes(title="Cost per Boarding ($)")
    fig.update_xaxes(title="Date")
    return style_plotly(fig)


def service_hours_active_vehicles(master_df: pd.DataFrame) -> go.Figure:
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=master_df["date"],
            y=master_df["service_hours"],
            mode="lines",
            name="Service Hours",
            line=dict(color="#38bdf8", width=3),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=master_df["date"],
            y=master_df["active_vehicles"],
            mode="lines",
            name="Active Vehicles",
            yaxis="y2",
            line=dict(color="#facc15", width=3),
        )
    )
    fig.update_layout(
        title="Service Hours and Active Vehicles",
        yaxis=dict(title="Service Hours"),
        yaxis2=dict(title="Active Vehicles", overlaying="y", side="right", showgrid=False),
    )
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


def boardings_forecast_with_interval(
    forecast_df: pd.DataFrame,
    title: str,
    historical_df: pd.DataFrame | None = None,
) -> go.Figure:
    fig = go.Figure()

    if historical_df is not None:
        fig.add_trace(
            go.Scatter(
                x=historical_df["date"],
                y=historical_df["boardings"],
                mode="lines",
                name="Historical",
                line=dict(color="#64748b", width=2),
            )
        )

    fig.add_trace(
        go.Scatter(
            x=forecast_df["date"],
            y=forecast_df["upper_ci"],
            mode="lines",
            line=dict(width=0),
            showlegend=False,
            hoverinfo="skip",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=forecast_df["date"],
            y=forecast_df["lower_ci"],
            mode="lines",
            name="Confidence Interval",
            fill="tonexty",
            fillcolor="rgba(96,165,250,0.18)",
            line=dict(width=0),
            hoverinfo="skip",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=forecast_df["date"],
            y=forecast_df["forecast_boardings"],
            mode="lines",
            name="Forecast",
            line=dict(color="#60a5fa", width=3),
        )
    )
    fig.update_layout(title=title)
    fig.update_yaxes(title="Boardings")
    fig.update_xaxes(title="Date")
    return style_plotly(fig)


def forecast_revenue_vs_cost(business_forecast_df: pd.DataFrame) -> go.Figure:
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=business_forecast_df["date"],
            y=business_forecast_df["forecast_revenue"],
            mode="lines",
            name="Forecast Revenue",
            line=dict(color="#60a5fa", width=3),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=business_forecast_df["date"],
            y=business_forecast_df["forecast_total_cost"],
            mode="lines",
            name="Forecast Total Cost",
            line=dict(color="#facc15", width=3),
        )
    )
    fig.update_layout(title="12-Month Revenue and Cost Planning View")
    fig.update_yaxes(title="Amount ($)")
    fig.update_xaxes(title="Date")
    return style_plotly(fig)


def projected_avg_fare(business_forecast_df: pd.DataFrame) -> go.Figure:
    fig = px.line(
        business_forecast_df,
        x="date",
        y="projected_avg_fare",
        title="Projected Average Fare Assumption",
    )
    fig.update_traces(line=dict(color="#a78bfa", width=3))
    fig.update_yaxes(title="Average Fare ($)")
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


def selected_scenario_boardings(adjusted_scenario_df: pd.DataFrame) -> go.Figure:
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=adjusted_scenario_df["date"],
            y=adjusted_scenario_df["scenario_boardings"],
            mode="lines",
            name="Preset Case",
            line=dict(color="#64748b", width=2, dash="dash"),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=adjusted_scenario_df["date"],
            y=adjusted_scenario_df["selected_boardings"],
            mode="lines",
            name="Selected Assumptions",
            line=dict(color="#60a5fa", width=3),
        )
    )
    fig.update_layout(title="Scenario Boardings Over Time")
    fig.update_yaxes(title="Boardings")
    fig.update_xaxes(title="Date")
    return style_plotly(fig)


def selected_scenario_recovery(adjusted_scenario_df: pd.DataFrame) -> go.Figure:
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=adjusted_scenario_df["date"],
            y=adjusted_scenario_df["selected_farebox_recovery"],
            mode="lines",
            name="Selected Recovery",
            line=dict(color="#86efac", width=3),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=adjusted_scenario_df["date"],
            y=adjusted_scenario_df["target_recovery"],
            mode="lines",
            name="Target",
            line=dict(color="#facc15", width=2, dash="dot"),
        )
    )
    fig.update_layout(title="Farebox Recovery vs Target")
    fig.update_yaxes(title="Farebox Recovery", tickformat=".0%")
    fig.update_xaxes(title="Date")
    return style_plotly(fig)


def selected_scenario_revenue_cost(adjusted_scenario_df: pd.DataFrame) -> go.Figure:
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=adjusted_scenario_df["date"],
            y=adjusted_scenario_df["selected_revenue"],
            mode="lines",
            name="Projected Revenue",
            line=dict(color="#60a5fa", width=3),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=adjusted_scenario_df["date"],
            y=adjusted_scenario_df["selected_total_cost"],
            mode="lines",
            name="Projected Total Cost",
            line=dict(color="#facc15", width=3),
        )
    )
    fig.update_layout(title="Revenue vs Total Cost")
    fig.update_yaxes(title="Amount ($)")
    fig.update_xaxes(title="Date")
    return style_plotly(fig)


def scenario_comparison_summary(
    scenario_summary_df: pd.DataFrame,
    adjusted_scenario_df: pd.DataFrame,
    selected_name: str,
) -> go.Figure:
    summary = scenario_plot_data(scenario_summary_df)[
        ["scenario_name", "scenario_farebox_recovery"]
    ].copy()
    selected = pd.DataFrame(
        {
            "scenario_name": ["Selected Assumptions"],
            "scenario_farebox_recovery": [adjusted_scenario_df["selected_farebox_recovery"].mean()],
        }
    )
    comparison = pd.concat([summary, selected], ignore_index=True)
    comparison["color"] = comparison["scenario_name"].apply(
        lambda name: "#60a5fa" if name == "Selected Assumptions" else "#64748b"
    )

    fig = px.bar(
        comparison,
        x="scenario_name",
        y="scenario_farebox_recovery",
        title=f"Recovery Comparison: {selected_name}",
    )
    fig.update_traces(marker_color=comparison["color"])
    fig.update_yaxes(title="Avg Farebox Recovery", tickformat=".0%")
    fig.update_xaxes(title="Planning Case")
    return style_plotly(fig)
