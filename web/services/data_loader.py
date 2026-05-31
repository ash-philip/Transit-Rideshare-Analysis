from pathlib import Path

import pandas as pd
import streamlit as st


BASE_DIR = Path(__file__).resolve().parents[1]
PROJECT_ROOT = BASE_DIR.parent
DATA_DIR = PROJECT_ROOT / "data" / "processed"


def _read_processed_csv(filename: str) -> pd.DataFrame:
    file_path = DATA_DIR / filename
    if not file_path.exists():
        st.error(
            f"Required data file is missing: `{file_path.relative_to(PROJECT_ROOT)}`. "
            "Run the data pipeline or restore the processed CSV before loading this dashboard."
        )
        st.stop()

    try:
        return pd.read_csv(file_path)
    except Exception as exc:
        st.error(
            f"Could not load `{file_path.relative_to(PROJECT_ROOT)}`. "
            f"Details: {exc}"
        )
        st.stop()


def _parse_date_column(df: pd.DataFrame, source_name: str, column: str = "date") -> pd.DataFrame:
    if column not in df.columns:
        st.error(f"`{source_name}` is missing required `{column}` column.")
        st.stop()

    try:
        df[column] = pd.to_datetime(df[column])
    except Exception as exc:
        st.error(f"`{source_name}` has an invalid `{column}` column. Details: {exc}")
        st.stop()

    return df


def load_master_data() -> pd.DataFrame:
    df = _read_processed_csv("rs_monthly_master.csv")
    if "year_month" not in df.columns:
        st.error("`rs_monthly_master.csv` is missing required `year_month` column.")
        st.stop()

    try:
        df["date"] = pd.to_datetime(df["year_month"] + "-01")
    except Exception as exc:
        st.error(f"`rs_monthly_master.csv` has invalid `year_month` values. Details: {exc}")
        st.stop()

    return df


def load_business_forecast() -> pd.DataFrame:
    df = _read_processed_csv("business_forecast_12m.csv")
    return _parse_date_column(df, "business_forecast_12m.csv")


def load_farebox_history_forecast() -> pd.DataFrame:
    df = _read_processed_csv("farebox_recovery_history_forecast.csv")
    return _parse_date_column(df, "farebox_recovery_history_forecast.csv")


def load_scenario_summary() -> pd.DataFrame:
    return _read_processed_csv("scenario_summary.csv")


def load_command_center_data() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    return (
        load_master_data(),
        load_business_forecast(),
        load_farebox_history_forecast(),
        load_scenario_summary(),
    )
