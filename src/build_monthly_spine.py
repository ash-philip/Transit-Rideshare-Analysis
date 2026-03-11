from pathlib import Path
import pandas as pd


START_DATE = "2020-01-01"
END_DATE = "2026-12-01"


def create_monthly_spine() -> pd.DataFrame:
    """
    Create a complete monthly spine from START_DATE to END_DATE.
    """
    months = pd.date_range(start=START_DATE, end=END_DATE, freq="MS")
    spine = pd.DataFrame({"date": months})
    spine["year_month"] = spine["date"].dt.strftime("%Y-%m")
    return spine[["year_month"]]


def save_spine(spine_df: pd.DataFrame) -> None:
    """
    Save the monthly spine to data/processed.
    """
    project_root = Path(__file__).resolve().parents[1]
    processed_path = project_root / "data" / "processed"
    processed_path.mkdir(parents=True, exist_ok=True)

    output_file = processed_path / "rs_monthly_spine.csv"
    spine_df.to_csv(output_file, index=False)

    print(f"Monthly spine created: {output_file}")


def main() -> None:
    spine_df = create_monthly_spine()
    save_spine(spine_df)


if __name__ == "__main__":
    main()
