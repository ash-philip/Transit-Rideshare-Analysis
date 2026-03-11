from pathlib import Path
import numpy as np
import pandas as pd


def load_data(project_root: Path) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Load the monthly spine and all raw synthetic source files.
    """
    data_path = project_root / "data"

    spine_df = pd.read_csv(data_path / "processed" / "rs_monthly_spine.csv")
    operations_df = pd.read_csv(data_path / "raw" / "synthetic_monthly_operations.csv")
    fuel_df = pd.read_csv(data_path / "raw" / "synthetic_fuel_costs.csv")
    maintenance_df = pd.read_csv(data_path / "raw" / "synthetic_maintenance_costs.csv")
    insurance_df = pd.read_csv(data_path / "raw" / "synthetic_insurance_costs.csv")

    return spine_df, operations_df, fuel_df, maintenance_df, insurance_df


def build_master_dataset(
    spine_df: pd.DataFrame,
    operations_df: pd.DataFrame,
    fuel_df: pd.DataFrame,
    maintenance_df: pd.DataFrame,
    insurance_df: pd.DataFrame
) -> pd.DataFrame:
    """
    Join all source datasets to the monthly spine and engineer core KPI fields.
    """
    master_df = spine_df.copy()

    master_df = master_df.merge(operations_df, on="year_month", how="left")
    master_df = master_df.merge(fuel_df, on="year_month", how="left")
    master_df = master_df.merge(maintenance_df, on="year_month", how="left")
    master_df = master_df.merge(insurance_df, on="year_month", how="left")

    # Fill missing numeric values with 0 only if needed
    numeric_cols = master_df.select_dtypes(include=[np.number]).columns
    master_df[numeric_cols] = master_df[numeric_cols].fillna(0)

    # Core cost and revenue KPIs
    master_df["total_cost"] = (
        master_df["fuel_cost"]
        + master_df["maintenance_cost"]
        + master_df["insurance_cost"]
    ).round(2)

    master_df["farebox_recovery"] = np.where(
        master_df["total_cost"] > 0,
        (master_df["revenue"] / master_df["total_cost"]).round(4),
        np.nan
    )

    master_df["cost_per_boarding"] = np.where(
        master_df["boardings"] > 0,
        (master_df["total_cost"] / master_df["boardings"]).round(2),
        np.nan
    )

    master_df["cost_per_service_hour"] = np.where(
        master_df["service_hours"] > 0,
        (master_df["total_cost"] / master_df["service_hours"]).round(2),
        np.nan
    )

    master_df["revenue_per_boarding"] = np.where(
        master_df["boardings"] > 0,
        (master_df["revenue"] / master_df["boardings"]).round(2),
        np.nan
    )

    # Optional date features for later analytics/modeling
    master_df["year"] = master_df["year_month"].str.slice(0, 4).astype(int)
    master_df["month"] = master_df["year_month"].str.slice(5, 7).astype(int)

    # Reorder columns for readability
    ordered_cols = [
        "year_month",
        "year",
        "month",
        "boardings",
        "service_hours",
        "revenue",
        "active_vehicles",
        "avg_passengers_per_vehicle",
        "avg_fare_per_boarding",
        "fuel_cost",
        "fuel_price_index",
        "maintenance_cost",
        "maintenance_event_count",
        "insurance_cost",
        "total_cost",
        "farebox_recovery",
        "cost_per_boarding",
        "cost_per_service_hour",
        "revenue_per_boarding",
    ]

    master_df = master_df[ordered_cols]

    return master_df


def save_master_dataset(master_df: pd.DataFrame, project_root: Path) -> None:
    """
    Save the master dataset to data/processed.
    """
    processed_path = project_root / "data" / "processed"
    processed_path.mkdir(parents=True, exist_ok=True)

    output_file = processed_path / "rs_monthly_master.csv"
    master_df.to_csv(output_file, index=False)

    print(f"Master dataset created: {output_file}")
    print(f"Rows: {len(master_df)}")
    print(f"Columns: {len(master_df.columns)}")


def main() -> None:
    project_root = Path(__file__).resolve().parents[1]

    spine_df, operations_df, fuel_df, maintenance_df, insurance_df = load_data(project_root)

    master_df = build_master_dataset(
        spine_df=spine_df,
        operations_df=operations_df,
        fuel_df=fuel_df,
        maintenance_df=maintenance_df,
        insurance_df=insurance_df,
    )

    save_master_dataset(master_df, project_root)


if __name__ == "__main__":
    main()
