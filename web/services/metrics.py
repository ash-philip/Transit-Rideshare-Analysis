import pandas as pd


def _pct_change(current: float, previous: float) -> float:
    if previous == 0:
        return 0.0
    return (current - previous) / previous


def format_count(value: float) -> str:
    return f"{value:,.0f}"


def format_currency(value: float) -> str:
    return f"${value:,.0f}"


def format_currency_millions(value: float) -> str:
    return f"${value / 1_000_000:.2f}M"


def format_percent(value: float) -> str:
    return f"{value:.2%}"


def format_currency_unit(value: float) -> str:
    return f"${value:.2f}"


def format_delta_percent(value: float) -> str:
    sign = "+" if value > 0 else ""
    return f"{sign}{value:.1%}"


def format_delta_points(value: float) -> str:
    sign = "+" if value > 0 else ""
    return f"{sign}{value * 100:.1f} pts"


def performance_snapshot(master_df: pd.DataFrame) -> list[dict[str, str]]:
    total_boardings = int(master_df["boardings"].sum())
    total_revenue = master_df["revenue"].sum()
    avg_farebox_recovery = master_df["farebox_recovery"].mean()
    avg_cost_per_boarding = master_df["cost_per_boarding"].mean()

    return [
        {
            "label": "Total Boardings",
            "value": format_count(total_boardings),
        },
        {
            "label": "Total Revenue",
            "value": format_currency_millions(total_revenue),
        },
        {
            "label": "Avg Farebox Recovery",
            "value": format_percent(avg_farebox_recovery),
        },
        {
            "label": "Avg Cost per Boarding",
            "value": format_currency_unit(avg_cost_per_boarding),
        },
    ]


def executive_kpis(master_df: pd.DataFrame) -> list[dict[str, str]]:
    history = master_df.sort_values("date").reset_index(drop=True)
    latest = history.iloc[-1]
    previous = history.iloc[-2] if len(history) > 1 else latest

    return [
        {
            "label": "Latest Month Boardings",
            "value": format_count(latest["boardings"]),
            "delta": f"{format_delta_percent(_pct_change(latest['boardings'], previous['boardings']))} MoM",
        },
        {
            "label": "Revenue",
            "value": format_currency(latest["revenue"]),
            "delta": f"{format_delta_percent(_pct_change(latest['revenue'], previous['revenue']))} MoM",
        },
        {
            "label": "Total Cost",
            "value": format_currency(latest["total_cost"]),
            "delta": "Latest month",
        },
        {
            "label": "Farebox Recovery",
            "value": format_percent(latest["farebox_recovery"]),
            "delta": f"{format_delta_points(latest['farebox_recovery'] - previous['farebox_recovery'])} MoM",
        },
        {
            "label": "Cost per Boarding",
            "value": format_currency_unit(latest["cost_per_boarding"]),
            "delta": "Latest month",
        },
        {
            "label": "Active Vehicles",
            "value": format_count(latest["active_vehicles"]),
            "delta": "Latest month",
        },
    ]


def latest_program_metrics(master_df: pd.DataFrame) -> list[dict[str, str]]:
    latest = master_df.sort_values("date").iloc[-1]

    return [
        {
            "label": "Latest Boardings",
            "value": format_count(latest["boardings"]),
        },
        {
            "label": "Latest Revenue",
            "value": format_currency(latest["revenue"]),
        },
        {
            "label": "Latest Farebox Recovery",
            "value": format_percent(latest["farebox_recovery"]),
        },
        {
            "label": "Latest Cost per Boarding",
            "value": format_currency_unit(latest["cost_per_boarding"]),
        },
    ]


def program_health_status(master_df: pd.DataFrame) -> dict[str, str]:
    history = master_df.sort_values("date").reset_index(drop=True)
    latest = history.iloc[-1]
    previous = history.iloc[-2] if len(history) > 1 else latest

    boardings_delta = _pct_change(latest["boardings"], previous["boardings"])
    revenue_delta = _pct_change(latest["revenue"], previous["revenue"])
    recovery_delta = latest["farebox_recovery"] - previous["farebox_recovery"]

    if latest["farebox_recovery"] >= 0.9 and boardings_delta >= 0:
        status = "Stable"
        tone = "positive"
        summary = "Current ridership and recovery indicators are broadly stable."
    elif latest["farebox_recovery"] >= 0.8:
        status = "Watch"
        tone = "watch"
        summary = "The program remains serviceable, but recent financial recovery should be monitored."
    else:
        status = "Pressure"
        tone = "risk"
        summary = "Current recovery levels indicate financial pressure that may require planning attention."

    detail = (
        f"Latest month boardings changed {format_delta_percent(boardings_delta)} MoM, "
        f"revenue changed {format_delta_percent(revenue_delta)} MoM, and farebox recovery moved "
        f"{format_delta_points(recovery_delta)}."
    )

    return {
        "title": "Program Health",
        "status": status,
        "tone": tone,
        "summary": summary,
        "detail": detail,
    }


def forecast_outlook(business_forecast_df: pd.DataFrame) -> dict[str, str]:
    forecast = business_forecast_df.sort_values("date").reset_index(drop=True)
    avg_boardings = forecast["forecast_boardings"].mean()
    avg_recovery = forecast["forecast_farebox_recovery"].mean()
    avg_revenue = forecast["forecast_revenue"].mean()
    avg_cost = forecast["forecast_total_cost"].mean()

    return {
        "title": "12-Month Forecast Outlook",
        "status": "Planning baseline",
        "tone": "neutral",
        "summary": (
            f"The forecast baseline averages {format_count(avg_boardings)} monthly boardings "
            f"and {format_percent(avg_recovery)} farebox recovery."
        ),
        "detail": (
            f"Average monthly revenue is projected at {format_currency(avg_revenue)} against "
            f"{format_currency(avg_cost)} in total cost. Treat this as a planning view, not a guarantee."
        ),
    }


def scenario_recommendation(scenario_summary_df: pd.DataFrame) -> dict[str, str]:
    scenarios = scenario_summary_df.copy()
    base = scenarios.loc[scenarios["scenario_name"] == "Base Case"]
    moderate = scenarios.loc[scenarios["scenario_name"] == "Moderate Fare Increase"]

    if not moderate.empty:
        selected = moderate.iloc[0]
        label = "Moderate Fare Increase"
        posture = "Balanced planning case"
    else:
        selected = scenarios.sort_values("scenario_farebox_recovery", ascending=False).iloc[0]
        label = selected["scenario_name"]
        posture = "Highest recovery case"

    if not base.empty:
        base_row = base.iloc[0]
        boardings_delta = selected["scenario_boardings"] - base_row["scenario_boardings"]
        recovery_delta = selected["scenario_farebox_recovery"] - base_row["scenario_farebox_recovery"]
        detail = (
            f"Compared with the base case, this scenario changes average boardings by "
            f"{format_count(boardings_delta)} and farebox recovery by {format_delta_points(recovery_delta)}."
        )
    else:
        detail = "Base case comparison is unavailable in the current scenario summary."

    return {
        "title": "Scenario Recommendation",
        "status": posture,
        "tone": "watch",
        "summary": (
            f"{label} provides a practical planning reference with "
            f"{format_percent(selected['scenario_farebox_recovery'])} average farebox recovery."
        ),
        "detail": f"{detail} Scenario outputs are directional planning tools, not guaranteed outcomes.",
    }
