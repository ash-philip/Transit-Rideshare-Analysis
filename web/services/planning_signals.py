import pandas as pd

from services.metrics import (
    format_count,
    format_currency,
    format_currency_unit,
    format_delta_percent,
    format_delta_points,
    format_percent,
)


def _empty_signal(title: str, detail: str = "Required data is not available for this signal.") -> dict[str, object]:
    return {
        "title": title,
        "status": "Unavailable",
        "tone": "neutral",
        "metrics": [{"label": "Data status", "value": "Unavailable"}],
        "summary": detail,
    }


def _pct_change(current: float, previous: float) -> float:
    if previous == 0:
        return 0.0
    return (current - previous) / previous


def program_health_signal(master_df: pd.DataFrame) -> dict[str, object]:
    required = {"date", "boardings", "revenue", "total_cost", "farebox_recovery", "cost_per_boarding"}
    if master_df.empty or not required.issubset(master_df.columns):
        return _empty_signal("Program Health Signal")

    history = master_df.sort_values("date").reset_index(drop=True)
    latest = history.iloc[-1]
    previous = history.iloc[-2] if len(history) > 1 else latest
    boardings_mom = _pct_change(latest["boardings"], previous["boardings"])
    cost_mom = _pct_change(latest["cost_per_boarding"], previous["cost_per_boarding"])
    revenue_gap = latest["revenue"] - latest["total_cost"]

    if latest["farebox_recovery"] >= 0.95 and boardings_mom >= 0:
        status = "Stable"
        tone = "positive"
    elif latest["farebox_recovery"] < 0.9 or cost_mom > 0.03:
        status = "Pressure"
        tone = "risk"
    else:
        status = "Watch"
        tone = "watch"

    return {
        "title": "Program Health Signal",
        "status": status,
        "tone": tone,
        "metrics": [
            {"label": "Boardings MoM", "value": format_delta_percent(boardings_mom)},
            {"label": "Latest Recovery", "value": format_percent(latest["farebox_recovery"])},
            {"label": "Cost / Boarding", "value": format_currency_unit(latest["cost_per_boarding"])},
        ],
        "summary": (
            f"Latest revenue is {format_currency(revenue_gap)} relative to total cost, "
            "with ridership and recovery moving as current operating signals."
        ),
    }


def demand_outlook_signal(
    boardings_forecast_12m_df: pd.DataFrame,
    boardings_forecast_24m_df: pd.DataFrame,
) -> dict[str, object]:
    required = {"date", "forecast_boardings"}
    if boardings_forecast_12m_df.empty or not required.issubset(boardings_forecast_12m_df.columns):
        return _empty_signal("Demand Outlook Signal")

    demand_12m = boardings_forecast_12m_df.sort_values("date").reset_index(drop=True)
    demand_24m = (
        boardings_forecast_24m_df.sort_values("date").reset_index(drop=True)
        if not boardings_forecast_24m_df.empty and required.issubset(boardings_forecast_24m_df.columns)
        else demand_12m
    )
    near_delta = _pct_change(demand_12m["forecast_boardings"].iloc[-1], demand_12m["forecast_boardings"].iloc[0])
    long_delta = _pct_change(demand_24m["forecast_boardings"].iloc[-1], demand_24m["forecast_boardings"].iloc[0])

    if near_delta >= 0.03:
        status = "Improving"
        tone = "positive"
    elif near_delta < -0.03:
        status = "Watch"
        tone = "watch"
    else:
        status = "Stable"
        tone = "neutral"

    return {
        "title": "Demand Outlook Signal",
        "status": status,
        "tone": tone,
        "metrics": [
            {"label": "12M Direction", "value": format_delta_percent(near_delta)},
            {"label": "24M Direction", "value": format_delta_percent(long_delta)},
            {"label": "12M Avg Boardings", "value": format_count(demand_12m["forecast_boardings"].mean())},
        ],
        "summary": "Demand outlook is based on precomputed forecast outputs and should be read as a planning view.",
    }


def cost_recovery_signal(farebox_history_forecast_df: pd.DataFrame) -> dict[str, object]:
    required = {"date", "farebox_recovery_value", "series_type"}
    if farebox_history_forecast_df.empty or not required.issubset(farebox_history_forecast_df.columns):
        return _empty_signal("Cost Recovery Signal")

    recovery = farebox_history_forecast_df.sort_values("date").reset_index(drop=True)
    historical = recovery.loc[recovery["series_type"] == "Historical"]
    forecast = recovery.loc[recovery["series_type"] == "Forecast"]
    latest_historical = historical.iloc[-1] if not historical.empty else recovery.iloc[-1]
    forecast_window = forecast if not forecast.empty else recovery.tail(min(12, len(recovery)))
    avg_forecast = forecast_window["farebox_recovery_value"].mean()
    final_forecast = forecast_window["farebox_recovery_value"].iloc[-1]
    recovery_delta = final_forecast - latest_historical["farebox_recovery_value"]

    if avg_forecast >= 0.95:
        status = "Stable"
        tone = "positive"
    elif avg_forecast >= 0.9:
        status = "Watch"
        tone = "watch"
    else:
        status = "Needs Review"
        tone = "risk"

    return {
        "title": "Cost Recovery Signal",
        "status": status,
        "tone": tone,
        "metrics": [
            {"label": "Latest Actual", "value": format_percent(latest_historical["farebox_recovery_value"])},
            {"label": "Forecast Avg", "value": format_percent(avg_forecast)},
            {"label": "End vs Actual", "value": format_delta_points(recovery_delta)},
        ],
        "summary": "Farebox recovery remains the core sustainability signal to monitor across the planning window.",
    }


def scenario_signal(
    scenario_summary_df: pd.DataFrame,
    scenario_detail_df: pd.DataFrame | None = None,
) -> dict[str, object]:
    required = {"scenario_name", "scenario_boardings", "scenario_farebox_recovery"}
    if scenario_summary_df.empty or not required.issubset(scenario_summary_df.columns):
        return _empty_signal("Scenario Signal")

    scenarios = scenario_summary_df.copy()
    base = scenarios.loc[scenarios["scenario_name"] == "Base Case"]
    moderate = scenarios.loc[scenarios["scenario_name"] == "Moderate Fare Increase"]
    selected = moderate.iloc[0] if not moderate.empty else scenarios.sort_values("scenario_farebox_recovery").iloc[-1]
    base_row = base.iloc[0] if not base.empty else selected
    boardings_delta = selected["scenario_boardings"] - base_row["scenario_boardings"]
    recovery_delta = selected["scenario_farebox_recovery"] - base_row["scenario_farebox_recovery"]

    horizon = None
    if scenario_detail_df is not None and not scenario_detail_df.empty and {"scenario_name", "date"}.issubset(scenario_detail_df.columns):
        horizon = int(scenario_detail_df.groupby("scenario_name")["date"].nunique().max())

    return {
        "title": "Scenario Signal",
        "status": "Scenario Comparison",
        "tone": "watch",
        "metrics": [
            {"label": "Case to Review", "value": str(selected["scenario_name"])},
            {"label": "Recovery vs Base", "value": format_delta_points(recovery_delta)},
            {"label": "Boardings vs Base", "value": format_count(boardings_delta)},
        ],
        "summary": (
            f"{selected['scenario_name']} is a planning comparison case"
            f"{f' over the {horizon}-month scenario horizon' if horizon else ''}, not a final recommendation."
        ),
    }


def watch_areas(
    master_df: pd.DataFrame,
    business_forecast_df: pd.DataFrame,
    farebox_history_forecast_df: pd.DataFrame,
) -> list[dict[str, str]]:
    areas: list[dict[str, str]] = []

    if not master_df.empty and {"date", "boardings", "cost_per_boarding", "farebox_recovery"}.issubset(master_df.columns):
        history = master_df.sort_values("date").reset_index(drop=True)
        latest = history.iloc[-1]
        previous = history.iloc[-2] if len(history) > 1 else latest
        areas.extend(
            [
                {
                    "label": "Ridership momentum",
                    "value": f"{format_delta_percent(_pct_change(latest['boardings'], previous['boardings']))} MoM",
                    "status": "Monitor demand direction",
                },
                {
                    "label": "Cost per boarding",
                    "value": format_currency_unit(latest["cost_per_boarding"]),
                    "status": "Watch cost pressure",
                },
            ]
        )

    if not business_forecast_df.empty and "forecast_farebox_recovery" in business_forecast_df.columns:
        areas.append(
            {
                "label": "Forecast recovery",
                "value": format_percent(business_forecast_df["forecast_farebox_recovery"].mean()),
                "status": "Track sustainability baseline",
            }
        )

    if not farebox_history_forecast_df.empty and "farebox_recovery_value" in farebox_history_forecast_df.columns:
        areas.append(
            {
                "label": "Recovery volatility",
                "value": format_percent(farebox_history_forecast_df["farebox_recovery_value"].tail(12).mean()),
                "status": "Review monthly threshold performance",
            }
        )

    return areas[:4]


def leadership_planning_view(signals: list[dict[str, object]], scenario_card: dict[str, object]) -> list[dict[str, str]]:
    positive = next(
        (
            signal
            for tone in ("positive", "neutral", "watch", "risk")
            for signal in signals
            if signal.get("tone") == tone
        ),
        signals[0],
    )
    watch = next((signal for signal in signals if signal.get("tone") in {"risk", "watch"}), signals[-1])
    scenario_case = "Current scenario set"
    scenario_metrics = scenario_card.get("metrics", [])
    if scenario_metrics:
        scenario_case = str(scenario_metrics[0].get("value", scenario_case))

    return [
        {"label": "Strongest Positive Signal", "value": str(positive["title"])},
        {"label": "Main Watch Area", "value": str(watch["title"])},
        {"label": "Scenario Case to Review", "value": scenario_case},
        {"label": "Next Metric to Monitor", "value": "Farebox recovery"},
    ]


def build_planning_signals(
    master_df: pd.DataFrame,
    business_forecast_df: pd.DataFrame,
    boardings_forecast_12m_df: pd.DataFrame,
    boardings_forecast_24m_df: pd.DataFrame,
    farebox_history_forecast_df: pd.DataFrame,
    scenario_summary_df: pd.DataFrame,
    scenario_detail_df: pd.DataFrame | None = None,
) -> dict[str, object]:
    signal_cards = [
        program_health_signal(master_df),
        demand_outlook_signal(boardings_forecast_12m_df, boardings_forecast_24m_df),
        cost_recovery_signal(farebox_history_forecast_df),
    ]
    scenario_card = scenario_signal(scenario_summary_df, scenario_detail_df)
    signal_cards.append(scenario_card)

    return {
        "leadership_view": leadership_planning_view(signal_cards, scenario_card),
        "signals": signal_cards,
        "watch_areas": watch_areas(master_df, business_forecast_df, farebox_history_forecast_df),
    }
