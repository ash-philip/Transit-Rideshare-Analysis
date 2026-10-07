import pandas as pd


def _pct_change(current: float, previous: float) -> float:
    if previous == 0:
        return 0.0
    return (current - previous) / previous


def format_count(value: float) -> str:
    return f"{value:,.0f}"


def format_currency(value: float) -> str:
    sign = "-" if value < 0 else ""
    return f"{sign}${abs(value):,.0f}"


def format_currency_millions(value: float) -> str:
    return f"${value / 1_000_000:.2f}M"


def format_percent(value: float) -> str:
    return f"{value:.2%}"


def format_currency_unit(value: float) -> str:
    sign = "-" if value < 0 else ""
    return f"{sign}${abs(value):.2f}"


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


def program_health_kpis(master_df: pd.DataFrame) -> list[dict[str, str]]:
    history = master_df.sort_values("date").reset_index(drop=True)
    latest = history.iloc[-1]
    previous = history.iloc[-2] if len(history) > 1 else latest

    return [
        {
            "label": "Boardings",
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
            "delta": f"{format_delta_percent(_pct_change(latest['total_cost'], previous['total_cost']))} MoM",
        },
        {
            "label": "Farebox Recovery",
            "value": format_percent(latest["farebox_recovery"]),
            "delta": f"{format_delta_points(latest['farebox_recovery'] - previous['farebox_recovery'])} MoM",
        },
        {
            "label": "Cost per Boarding",
            "value": format_currency_unit(latest["cost_per_boarding"]),
            "delta": f"{format_delta_percent(_pct_change(latest['cost_per_boarding'], previous['cost_per_boarding']))} MoM",
        },
        {
            "label": "Revenue per Boarding",
            "value": format_currency_unit(latest["revenue_per_boarding"]),
            "delta": f"{format_delta_percent(_pct_change(latest['revenue_per_boarding'], previous['revenue_per_boarding']))} MoM",
        },
        {
            "label": "Service Hours",
            "value": format_count(latest["service_hours"]),
            "delta": f"{format_delta_percent(_pct_change(latest['service_hours'], previous['service_hours']))} MoM",
        },
        {
            "label": "Active Vehicles",
            "value": format_count(latest["active_vehicles"]),
            "delta": f"{format_delta_percent(_pct_change(latest['active_vehicles'], previous['active_vehicles']))} MoM",
        },
        {
            "label": "Avg Passengers / Vehicle",
            "value": format_count(latest["avg_passengers_per_vehicle"]),
            "delta": f"{format_delta_percent(_pct_change(latest['avg_passengers_per_vehicle'], previous['avg_passengers_per_vehicle']))} MoM",
        },
    ]


def program_health_signals(master_df: pd.DataFrame) -> list[dict[str, str]]:
    history = master_df.sort_values("date").reset_index(drop=True)
    latest = history.iloc[-1]
    previous = history.iloc[-2] if len(history) > 1 else latest
    recent = history.tail(min(6, len(history)))
    prior = history.iloc[-12] if len(history) >= 12 else history.iloc[0]

    boardings_mom = _pct_change(latest["boardings"], previous["boardings"])
    boardings_long = _pct_change(latest["boardings"], prior["boardings"])
    cost_per_boarding_mom = _pct_change(latest["cost_per_boarding"], previous["cost_per_boarding"])
    recovery_delta = latest["farebox_recovery"] - previous["farebox_recovery"]
    utilization_mom = _pct_change(
        latest["avg_passengers_per_vehicle"],
        previous["avg_passengers_per_vehicle"],
    )

    ridership_status = "Improving" if boardings_mom >= 0 else "Softening"
    ridership_tone = "positive" if boardings_mom >= 0 else "watch"

    cost_status = "Pressure rising" if cost_per_boarding_mom > 0 else "Pressure easing"
    cost_tone = "risk" if cost_per_boarding_mom > 0 else "positive"

    recovery_status = "Recovery up" if recovery_delta >= 0 else "Recovery down"
    recovery_tone = "positive" if recovery_delta >= 0 else "watch"

    utilization_status = "Utilization up" if utilization_mom >= 0 else "Utilization down"
    utilization_tone = "positive" if utilization_mom >= 0 else "watch"

    return [
        {
            "title": "Ridership Trend",
            "status": ridership_status,
            "tone": ridership_tone,
            "summary": f"Latest boardings moved {format_delta_percent(boardings_mom)} month over month.",
            "detail": f"Compared with the prior reference month, boardings are {format_delta_percent(boardings_long)}.",
        },
        {
            "title": "Cost Pressure",
            "status": cost_status,
            "tone": cost_tone,
            "summary": f"Cost per boarding moved {format_delta_percent(cost_per_boarding_mom)} month over month.",
            "detail": (
                f"The recent six-month average cost per boarding is "
                f"{format_currency_unit(recent['cost_per_boarding'].mean())}."
            ),
        },
        {
            "title": "Recovery Trend",
            "status": recovery_status,
            "tone": recovery_tone,
            "summary": f"Farebox recovery moved {format_delta_points(recovery_delta)} month over month.",
            "detail": f"Latest recovery is {format_percent(latest['farebox_recovery'])}.",
        },
        {
            "title": "Utilization Signal",
            "status": utilization_status,
            "tone": utilization_tone,
            "summary": (
                f"Passengers per vehicle moved {format_delta_percent(utilization_mom)} month over month."
            ),
            "detail": (
                f"Latest average passengers per vehicle is "
                f"{format_count(latest['avg_passengers_per_vehicle'])}."
            ),
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
            f"The current planning baseline averages {format_count(avg_boardings)} monthly boardings "
            f"and {format_percent(avg_recovery)} farebox recovery."
        ),
        "detail": (
            f"Average monthly revenue is estimated at {format_currency(avg_revenue)} against "
            f"{format_currency(avg_cost)} in total cost under current assumptions."
        ),
    }


def scenario_planning_signal(scenario_summary_df: pd.DataFrame) -> dict[str, str]:
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
        posture = "Scenario planning signal"

    if not base.empty:
        base_row = base.iloc[0]
        boardings_delta = selected["scenario_boardings"] - base_row["scenario_boardings"]
        recovery_delta = selected["scenario_farebox_recovery"] - base_row["scenario_farebox_recovery"]
        detail = (
            f"Compared with the base case, this planning case changes average boardings by "
            f"{format_count(boardings_delta)} and farebox recovery by {format_delta_points(recovery_delta)}."
        )
    else:
        detail = "Base case comparison is unavailable in the current scenario summary."

    return {
        "title": "Scenario Planning Signal",
        "status": posture,
        "tone": "watch",
        "summary": (
            f"{label} is shown as a comparison case with "
            f"{format_percent(selected['scenario_farebox_recovery'])} average farebox recovery."
        ),
        "detail": (
            f"{detail} This is not a final recommendation; it is a directional input for leadership discussion."
        ),
    }


def scenario_decision_kpis(adjusted_scenario_df: pd.DataFrame) -> list[dict[str, str]]:
    avg_boardings = adjusted_scenario_df["selected_boardings"].mean()
    avg_revenue = adjusted_scenario_df["selected_revenue"].mean()
    avg_cost = adjusted_scenario_df["selected_total_cost"].mean()
    avg_recovery = adjusted_scenario_df["selected_farebox_recovery"].mean()

    return [
        {"label": "Projected Avg Boardings", "value": format_count(avg_boardings)},
        {"label": "Projected Avg Revenue", "value": format_currency(avg_revenue)},
        {"label": "Projected Avg Cost", "value": format_currency(avg_cost)},
        {"label": "Projected Farebox Recovery", "value": format_percent(avg_recovery)},
    ]


def scenario_simulator_signal(
    adjusted_scenario_df: pd.DataFrame,
    scenario_name: str,
    target_recovery: float,
) -> dict[str, str]:
    normalized_target = target_recovery / 100 if target_recovery > 1 else target_recovery
    avg_recovery = adjusted_scenario_df["selected_farebox_recovery"].mean()
    avg_gap = adjusted_scenario_df["recovery_gap"].mean()
    months_below_target = int((~adjusted_scenario_df["target_status"]).sum())
    months_above_target = len(adjusted_scenario_df) - months_below_target
    gap_direction = "above" if avg_gap >= 0 else "below"
    gap_text = (
        f"Average monthly revenue is {format_currency(abs(avg_gap))} "
        f"{gap_direction} the revenue needed to meet the target."
    )

    if avg_recovery >= normalized_target and months_below_target == 0:
        status = "Average recovery meets target"
        tone = "positive"
        target_context = "Average recovery meets the selected planning target, and all months meet the monthly threshold."
    elif avg_recovery >= normalized_target:
        status = "Average recovery meets target"
        tone = "watch"
        target_context = (
            "Average recovery meets the selected planning target, though some months remain below the monthly threshold."
        )
    else:
        status = "Average recovery below target"
        tone = "risk"
        if months_above_target > 0:
            target_context = (
                "Average recovery is below the selected planning target. Some months exceed the threshold, "
                "but the selected case remains below target on average."
            )
        else:
            target_context = (
                "Average recovery is below the selected planning target, and no months meet the monthly threshold."
            )

    return {
        "title": "Scenario Signal",
        "status": status,
        "tone": tone,
        "summary": (
            f"{scenario_name} averages {format_percent(avg_recovery)} recovery versus a "
            f"{format_percent(normalized_target)} planning target. {target_context} "
            f"Monthly threshold performance: {months_below_target} of {len(adjusted_scenario_df)} months are below target. "
            f"{gap_text}"
        ),
    }


def forecast_center_kpis(
    view: str,
    business_forecast_df: pd.DataFrame,
    boardings_forecast_12m_df: pd.DataFrame,
    boardings_forecast_24m_df: pd.DataFrame,
    farebox_history_forecast_df: pd.DataFrame,
) -> list[dict[str, str]]:
    business = business_forecast_df.sort_values("date").reset_index(drop=True)
    demand_12m = boardings_forecast_12m_df.sort_values("date").reset_index(drop=True)
    demand_24m = boardings_forecast_24m_df.sort_values("date").reset_index(drop=True)
    recovery = farebox_history_forecast_df.sort_values("date").reset_index(drop=True)

    if view == "12-Month Planning View":
        return [
            {"label": "Avg Monthly Boardings", "value": format_count(business["forecast_boardings"].mean())},
            {"label": "Avg Monthly Revenue", "value": format_currency(business["forecast_revenue"].mean())},
            {"label": "Avg Monthly Cost", "value": format_currency(business["forecast_total_cost"].mean())},
            {"label": "Avg Farebox Recovery", "value": format_percent(business["forecast_farebox_recovery"].mean())},
        ]

    if view == "24-Month Demand Outlook":
        final_month = demand_24m.iloc[-1]
        return [
            {"label": "Forecast Horizon", "value": f"{len(demand_24m)} months"},
            {"label": "Avg Monthly Boardings", "value": format_count(demand_24m["forecast_boardings"].mean())},
            {"label": "Final Month Boardings", "value": format_count(final_month["forecast_boardings"])},
            {
                "label": "Final Month Range",
                "value": f"{format_count(final_month['lower_ci'])}-{format_count(final_month['upper_ci'])}",
            },
        ]

    if view == "Farebox Recovery Outlook":
        historical = recovery.loc[recovery["series_type"] == "Historical"]
        forecast = recovery.loc[recovery["series_type"] == "Forecast"]
        latest_historical = historical.iloc[-1] if not historical.empty else recovery.iloc[0]
        avg_forecast = forecast["farebox_recovery_value"].mean() if not forecast.empty else recovery["farebox_recovery_value"].mean()
        final_forecast = forecast.iloc[-1] if not forecast.empty else recovery.iloc[-1]
        return [
            {"label": "Latest Historical Recovery", "value": format_percent(latest_historical["farebox_recovery_value"])},
            {"label": "Avg Forecast Recovery", "value": format_percent(avg_forecast)},
            {"label": "Final Forecast Recovery", "value": format_percent(final_forecast["farebox_recovery_value"])},
        ]

    avg_fare = business["projected_avg_fare"].mean()
    first_period = business["date"].iloc[0].strftime("%b %Y")
    final_period = business["date"].iloc[-1].strftime("%b %Y")
    return [
        {"label": "Primary Planning Horizon", "value": f"{len(demand_12m)} months"},
        {"label": "Longer Demand Horizon", "value": f"{len(demand_24m)} months"},
        {"label": "Forecast Period", "value": f"{first_period}-{final_period}"},
        {"label": "Avg Fare Assumption", "value": format_currency_unit(avg_fare)},
    ]


def forecast_center_signal(
    view: str,
    business_forecast_df: pd.DataFrame,
    boardings_forecast_12m_df: pd.DataFrame,
    boardings_forecast_24m_df: pd.DataFrame,
    farebox_history_forecast_df: pd.DataFrame,
) -> dict[str, str]:
    business = business_forecast_df.sort_values("date").reset_index(drop=True)
    demand_12m = boardings_forecast_12m_df.sort_values("date").reset_index(drop=True)
    demand_24m = boardings_forecast_24m_df.sort_values("date").reset_index(drop=True)
    recovery = farebox_history_forecast_df.sort_values("date").reset_index(drop=True)

    if view == "12-Month Planning View":
        avg_recovery = business["forecast_farebox_recovery"].mean()
        avg_revenue = business["forecast_revenue"].mean()
        avg_cost = business["forecast_total_cost"].mean()
        status = "Recovery watch" if avg_recovery < 1 else "Recovery stable"
        tone = "watch" if avg_recovery < 1 else "positive"
        return {
            "title": "Planning Signal",
            "status": status,
            "tone": tone,
            "summary": (
                f"Average forecast revenue is {format_currency(avg_revenue)} against "
                f"{format_currency(avg_cost)} in average monthly cost."
            ),
        }

    if view == "24-Month Demand Outlook":
        first_boardings = demand_24m["forecast_boardings"].iloc[0]
        final_boardings = demand_24m["forecast_boardings"].iloc[-1]
        demand_delta = _pct_change(final_boardings, first_boardings)
        status = "Demand growth signal" if demand_delta >= 0 else "Demand softness signal"
        tone = "positive" if demand_delta >= 0 else "watch"
        return {
            "title": "What to Watch",
            "status": status,
            "tone": tone,
            "summary": f"Final-month demand is {format_delta_percent(demand_delta)} versus the first forecast month.",
        }

    if view == "Farebox Recovery Outlook":
        forecast = recovery.loc[recovery["series_type"] == "Forecast"]
        if forecast.empty:
            forecast = recovery
        recovery_delta = forecast["farebox_recovery_value"].iloc[-1] - forecast["farebox_recovery_value"].iloc[0]
        status = "Recovery improving" if recovery_delta >= 0 else "Recovery pressure"
        tone = "positive" if recovery_delta >= 0 else "watch"
        return {
            "title": "Planning Signal",
            "status": status,
            "tone": tone,
            "summary": f"Forecast recovery moves {format_delta_points(recovery_delta)} across the planning window.",
        }

    first_period = business["date"].iloc[0].strftime("%b %Y")
    final_period = business["date"].iloc[-1].strftime("%b %Y")
    return {
        "title": "Input Check",
        "status": "Precomputed planning inputs",
        "tone": "neutral",
        "summary": f"Business forecast covers {first_period}-{final_period}; demand outlook includes {len(demand_24m)} months.",
    }


def planning_input_summary(
    business_forecast_df: pd.DataFrame,
    boardings_forecast_12m_df: pd.DataFrame,
    boardings_forecast_24m_df: pd.DataFrame,
) -> list[dict[str, str]]:
    business = business_forecast_df.sort_values("date").reset_index(drop=True)
    demand_12m = boardings_forecast_12m_df.sort_values("date").reset_index(drop=True)
    demand_24m = boardings_forecast_24m_df.sort_values("date").reset_index(drop=True)
    first_period = business["date"].iloc[0].strftime("%b %Y")
    final_period = business["date"].iloc[-1].strftime("%b %Y")
    avg_fare = business["projected_avg_fare"].mean()
    first_fare = business["projected_avg_fare"].iloc[0]
    final_fare = business["projected_avg_fare"].iloc[-1]
    avg_cost = business["forecast_total_cost"].mean()

    return [
        {"label": "Primary Horizon", "value": f"{len(demand_12m)} months"},
        {"label": "Longer Demand Horizon", "value": f"{len(demand_24m)} months"},
        {"label": "Forecast Period", "value": f"{first_period}-{final_period}"},
        {"label": "Average Fare Assumption", "value": format_currency_unit(avg_fare)},
        {"label": "Fare Range", "value": f"{format_currency_unit(first_fare)}-{format_currency_unit(final_fare)}"},
        {"label": "Average Monthly Cost Input", "value": format_currency(avg_cost)},
        {"label": "Data Source", "value": "Precomputed processed CSVs"},
    ]
