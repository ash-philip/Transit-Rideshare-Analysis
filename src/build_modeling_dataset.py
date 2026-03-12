from pathlib import Path
import pandas as pd


def load_master_dataset(project_root: Path) -> pd.DataFrame:
    """
    Load the processed monthly master dataset.
    """
    file_path = project_root / "data" / "processed" / "rs_monthly_master.csv"
    df = pd.read_csv(file_path)
    return df


def build_modeling_dataset(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create a modeling-ready dataset with lag and rolling features.
    """
    modeling_df = df.copy()

    # Create a proper datetime field for sorting.
    modeling_df["date"] = pd.to_datetime(modeling_df["year_month"] + "-01")
    modeling_df = modeling_df.sort_values("date").reset_index(drop=True)

    # Lag features for boardings.
    modeling_df["lag_1_boardings"] = modeling_df["boardings"].shift(1)
    modeling_df["lag_12_boardings"] = modeling_df["boardings"].shift(12)

    # Rolling features.
    modeling_df["rolling_3m_boardings"] = modeling_df["boardings"].rolling(window=3).mean()
    modeling_df["rolling_3m_revenue"] = modeling_df["revenue"].rolling(window=3).mean()

    # Keep a clean set of columns for modeling.
    modeling_df = modeling_df[
        [
            "year_month",
            "date",
            "year",
            "month",
            "boardings",
            "service_hours",
            "revenue",
            "total_cost",
            "farebox_recovery",
            "lag_1_boardings",
            "lag_12_boardings",
            "rolling_3m_boardings",
            "rolling_3m_revenue",
        ]
    ]

    return modeling_df


def save_modeling_dataset(modeling_df: pd.DataFrame, project_root: Path) -> None:
    """
    Save the modeling dataset to data/processed.
    """
    output_file = project_root / "data" / "processed" / "rs_modeling_dataset.csv"
    modeling_df.to_csv(output_file, index=False)

    print(f"Modeling dataset created: {output_file}")
    print(f"Rows: {len(modeling_df)}")
    print(f"Columns: {len(modeling_df.columns)}")


def main() -> None:
    project_root = Path(__file__).resolve().parents[1]
    df = load_master_dataset(project_root)
    modeling_df = build_modeling_dataset(df)
    save_modeling_dataset(modeling_df, project_root)


if __name__ == "__main__":
    main()