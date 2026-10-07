from pathlib import Path

import pandas as pd
import streamlit as st


BASE_DIR = Path(__file__).resolve().parents[1]
PROJECT_ROOT = BASE_DIR.parent
DATA_DIR = PROJECT_ROOT / "data" / "processed"
SCENARIO_DETAIL_FILE = "scenario_analysis_output.csv"


def load_scenario_detail() -> pd.DataFrame:
    file_path = DATA_DIR / SCENARIO_DETAIL_FILE
    if not file_path.exists():
        st.warning(
            f"Required data file is missing: `{file_path.relative_to(PROJECT_ROOT)}`. "
            "Scenario detail views will be unavailable until the processed scenario output is restored."
        )
        return pd.DataFrame()

    try:
        df = pd.read_csv(file_path)
        df["date"] = pd.to_datetime(df["date"])
        return df
    except Exception as exc:
        st.warning(
            f"Could not load `{file_path.relative_to(PROJECT_ROOT)}`. "
            f"Details: {exc}"
        )
        return pd.DataFrame()


def apply_planning_assumptions(
    scenario_detail_df: pd.DataFrame,
    scenario_name: str,
    fare_adjustment_pct: float,
    demand_response: float,
    cost_pressure_pct: float,
    target_recovery: float,
) -> pd.DataFrame:
    scenario = (
        scenario_detail_df.loc[scenario_detail_df["scenario_name"] == scenario_name]
        .sort_values("date")
        .reset_index(drop=True)
        .copy()
    )

    if scenario.empty:
        return scenario

    normalized_target = target_recovery / 100 if target_recovery > 1 else target_recovery
    fare_factor = 1 + (fare_adjustment_pct / 100)
    cost_factor = 1 + (cost_pressure_pct / 100)
    demand_factor = max(0, 1 + (demand_response * (fare_adjustment_pct / 100)))

    scenario["selected_avg_fare"] = scenario["scenario_avg_fare"] * fare_factor
    scenario["selected_boardings"] = scenario["scenario_boardings"] * demand_factor
    scenario["selected_revenue"] = scenario["selected_boardings"] * scenario["selected_avg_fare"]
    scenario["selected_total_cost"] = scenario["scenario_total_cost"] * cost_factor
    scenario["selected_farebox_recovery"] = scenario["selected_revenue"] / scenario["selected_total_cost"]
    scenario["target_recovery"] = normalized_target
    scenario["recovery_gap"] = scenario["selected_revenue"] - (scenario["selected_total_cost"] * normalized_target)
    scenario["target_status"] = scenario["selected_farebox_recovery"] >= normalized_target
    return scenario


def scenario_options(scenario_detail_df: pd.DataFrame) -> list[str]:
    if scenario_detail_df.empty or "scenario_name" not in scenario_detail_df.columns:
        return []

    preferred_order = [
        "Base Case",
        "Moderate Fare Increase",
        "Higher Fare Increase",
        "Fare Increase + Cost Pressure",
    ]
    available = set(scenario_detail_df["scenario_name"].dropna().unique())
    ordered = [name for name in preferred_order if name in available]
    remaining = sorted(available.difference(ordered))
    return ordered + remaining
