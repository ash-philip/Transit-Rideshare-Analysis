import pandas as pd


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
