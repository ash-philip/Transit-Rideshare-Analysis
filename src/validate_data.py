from pathlib import Path
import pandas as pd


def load_master_dataset(project_root: Path) -> pd.DataFrame:
    """
    Load the processed monthly master dataset.
    """
    file_path = project_root / "data" / "processed" / "rs_monthly_master.csv"
    return pd.read_csv(file_path)


def run_validation_checks(df: pd.DataFrame) -> None:
    """
    Run simple validation checks on the master dataset.
    """
    print("Running validation checks...\n")

    # 1. Row count
    expected_rows = 84
    actual_rows = len(df)
    print(f"Row count check: {actual_rows} rows")
    assert actual_rows == expected_rows, f"Expected {expected_rows} rows, found {actual_rows}"

    # 2. Required columns
    required_columns = [
        "year_month",
        "boardings",
        "service_hours",
        "revenue",
        "fuel_cost",
        "maintenance_cost",
        "insurance_cost",
        "total_cost",
        "farebox_recovery",
        "cost_per_boarding",
        "cost_per_service_hour",
        "revenue_per_boarding",
    ]
    missing_columns = [col for col in required_columns if col not in df.columns]
    print(f"Required column check: {len(missing_columns)} missing")
    assert not missing_columns, f"Missing columns: {missing_columns}"

    # 3. Null check on core fields
    core_fields = [
        "year_month",
        "boardings",
        "service_hours",
        "revenue",
        "total_cost",
    ]
    null_counts = df[core_fields].isnull().sum()
    print("Null check on core fields:")
    print(null_counts)
    assert null_counts.sum() == 0, "Null values found in core fields"

    # 4. Uniqueness of year_month
    unique_months = df["year_month"].nunique()
    print(f"\nUnique month check: {unique_months} unique months")
    assert unique_months == len(df), "Duplicate year_month values found"

    # 5. Cost logic check
    recalculated_total_cost = (
        df["fuel_cost"] + df["maintenance_cost"] + df["insurance_cost"]
    ).round(2)

    mismatched_costs = (df["total_cost"].round(2) != recalculated_total_cost).sum()
    print(f"Total cost formula check: {mismatched_costs} mismatched rows")
    assert mismatched_costs == 0, "total_cost does not match component sum"

    # 6. Positive values check
    print("\nPositive value checks:")
    assert (df["boardings"] > 0).all(), "Non-positive boardings found"
    assert (df["service_hours"] > 0).all(), "Non-positive service_hours found"
    assert (df["revenue"] > 0).all(), "Non-positive revenue found"
    assert (df["total_cost"] > 0).all(), "Non-positive total_cost found"
    print("All positive value checks passed")

    print("\nAll validation checks passed successfully.")


def main() -> None:
    project_root = Path(__file__).resolve().parents[1]
    master_df = load_master_dataset(project_root)
    run_validation_checks(master_df)


if __name__ == "__main__":
    main()
