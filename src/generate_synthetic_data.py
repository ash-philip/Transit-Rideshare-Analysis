from pathlib import Path
import numpy as np
import pandas as pd


# ----------------------------
# Configuration
# ----------------------------
START_DATE = "2020-01-01"
END_DATE = "2026-12-01"
RANDOM_SEED = 42


# ----------------------------
# Helpers
# ----------------------------
def create_month_index() -> pd.DataFrame:
    """
    Create a monthly date index from START_DATE to END_DATE.
    """
    months = pd.date_range(start=START_DATE, end=END_DATE, freq="MS")
    df = pd.DataFrame({"date": months})
    df["year_month"] = df["date"].dt.strftime("%Y-%m")
    df["month_num"] = df["date"].dt.month
    df["year"] = df["date"].dt.year
    df["t"] = np.arange(len(df))
    return df


def generate_operations_data(months_df: pd.DataFrame) -> pd.DataFrame:
    """
    Generate synthetic monthly operations data:
    - boardings
    - service_hours
    - revenue
    - active_vehicles
    - avg_passengers_per_vehicle
    - avg_fare_per_boarding

    This version is tuned so that:
    - demand drops sharply during the disruption period
    - ridership gradually recovers
    - recovery stabilizes in later years
    - farebox recovery improves, but does not rise too aggressively
    """
    rng = np.random.default_rng(RANDOM_SEED)
    df = months_df.copy()

    # Seasonality in ridership demand
    seasonality = 1 + 0.10 * np.sin(2 * np.pi * df["month_num"] / 12)

    # Disruption and recovery pattern
    shock_factor = []
    for date in df["date"]:
        if date < pd.Timestamp("2020-04-01"):
            shock_factor.append(1.00)
        elif date <= pd.Timestamp("2020-12-01"):
            shock_factor.append(0.45)
        elif date <= pd.Timestamp("2021-12-01"):
            shock_factor.append(0.62)
        elif date <= pd.Timestamp("2022-12-01"):
            shock_factor.append(0.75)
        elif date <= pd.Timestamp("2023-12-01"):
            shock_factor.append(0.87)
        elif date <= pd.Timestamp("2024-12-01"):
            shock_factor.append(0.94)
        else:
            shock_factor.append(0.97)

    df["shock_factor"] = shock_factor

    # Mild growth only until stabilization
    growth_factor = []
    for date in df["date"]:
        if date <= pd.Timestamp("2023-12-01"):
            growth_factor.append(1 + (df.loc[df["date"] == date, "t"].iloc[0] * 0.0018))
        else:
            growth_factor.append(1.07)

    df["growth_factor"] = growth_factor

    # Boardings: recover and then stabilize
    base_boardings = 7600
    noise_boardings = rng.normal(0, 275, len(df))
    df["boardings"] = (
        base_boardings
        * seasonality
        * df["shock_factor"]
        * df["growth_factor"]
        + noise_boardings
    ).round().clip(lower=1800)

    # Service hours: smoother than boardings and less sensitive to demand swings
    service_noise = rng.normal(0, 35, len(df))
    df["service_hours"] = (
        1280
        * (0.94 + 0.06 * seasonality)
        * (0.78 + 0.22 * df["shock_factor"])
        * (1 + df["t"] * 0.0012)
        + service_noise
    ).round().clip(lower=700)

    # Active vehicles: modest recovery and then flat
    vehicle_noise = rng.normal(0, 1.0, len(df))
    df["active_vehicles"] = (
        40
        * (0.82 + 0.18 * df["shock_factor"])
        * (1 + np.minimum(df["t"], 48) * 0.0008)
        + vehicle_noise
    ).round().clip(lower=24)

    # Average fare per boarding:
    # slower long-term growth so revenue does not outpace cost too aggressively
    fare_noise = rng.normal(0, 0.05, len(df))
    df["avg_fare_per_boarding"] = (
        4.10 + (np.minimum(df["t"], 36) * 0.0025) + fare_noise
    ).round(2).clip(lower=3.75, upper=4.65)

    # Revenue follows boardings and fare, with slight noise
    revenue_noise = rng.normal(1.0, 0.025, len(df))
    df["revenue"] = (
        df["boardings"] * df["avg_fare_per_boarding"] * revenue_noise
    ).round(2)

    # Average passengers per vehicle
    df["avg_passengers_per_vehicle"] = (
        df["boardings"] / df["active_vehicles"]
    ).round(2)

    return df[
        [
            "year_month",
            "boardings",
            "service_hours",
            "revenue",
            "active_vehicles",
            "avg_passengers_per_vehicle",
            "avg_fare_per_boarding",
        ]
    ]


def generate_fuel_data(months_df: pd.DataFrame, operations_df: pd.DataFrame) -> pd.DataFrame:
    """
    Generate synthetic monthly fuel costs based on service hours and a fuel price index.

    This version adds slightly more long-run fuel pressure.
    """
    rng = np.random.default_rng(RANDOM_SEED + 1)
    df = months_df[["year_month", "t", "month_num"]].copy()

    merged = df.merge(
        operations_df[["year_month", "service_hours"]],
        on="year_month",
        how="left"
    )

    seasonal_fuel = 1 + 0.05 * np.cos(2 * np.pi * merged["month_num"] / 12)

    fuel_price_index = (
        1.00
        + 0.08 * np.sin(2 * np.pi * merged["t"] / 18)
        + 0.0015 * merged["t"]
        + rng.normal(0, 0.025, len(merged))
    )
    fuel_price_index = np.clip(fuel_price_index, 0.88, 1.32)

    merged["fuel_price_index"] = fuel_price_index.round(3)

    merged["fuel_cost"] = (
        merged["service_hours"] * 9.8 * seasonal_fuel * merged["fuel_price_index"]
        + rng.normal(0, 220, len(merged))
    ).round(2).clip(lower=4000)

    return merged[["year_month", "fuel_cost", "fuel_price_index"]]


def generate_maintenance_data(months_df: pd.DataFrame, operations_df: pd.DataFrame) -> pd.DataFrame:
    """
    Generate synthetic monthly maintenance costs with occasional spikes.

    This version adds more long-run maintenance pressure so total cost
    grows more realistically as the fleet ages and service stabilizes.
    """
    rng = np.random.default_rng(RANDOM_SEED + 2)
    df = months_df[["year_month", "t"]].copy()

    merged = df.merge(
        operations_df[["year_month", "service_hours", "active_vehicles"]],
        on="year_month",
        how="left"
    )

    base_cost = 8600 + (merged["t"] * 12)
    variable_cost = merged["service_hours"] * 2.9
    fleet_component = merged["active_vehicles"] * 58

    spike_flags = rng.choice([0, 1], size=len(merged), p=[0.86, 0.14])
    spike_amount = spike_flags * rng.uniform(2800, 7200, size=len(merged))

    merged["maintenance_event_count"] = (
        2 + spike_flags + rng.integers(0, 3, size=len(merged))
    )

    merged["maintenance_cost"] = (
        base_cost
        + variable_cost
        + fleet_component
        + spike_amount
        + rng.normal(0, 550, len(merged))
    ).round(2).clip(lower=5500)

    return merged[["year_month", "maintenance_cost", "maintenance_event_count"]]


def generate_insurance_data(months_df: pd.DataFrame) -> pd.DataFrame:
    """
    Generate smooth monthly insurance costs with slightly stronger annual increases.
    """
    rng = np.random.default_rng(RANDOM_SEED + 3)
    df = months_df[["year_month", "t"]].copy()

    df["insurance_cost"] = (
        6200
        + (df["t"] * 24)
        + rng.normal(0, 110, len(df))
    ).round(2).clip(lower=5500)

    return df[["year_month", "insurance_cost"]]


def save_outputs(
    operations_df: pd.DataFrame,
    fuel_df: pd.DataFrame,
    maintenance_df: pd.DataFrame,
    insurance_df: pd.DataFrame
) -> None:
    """
    Save all generated datasets to data/raw.
    """
    project_root = Path(__file__).resolve().parents[1]
    raw_path = project_root / "data" / "raw"
    raw_path.mkdir(parents=True, exist_ok=True)

    operations_df.to_csv(raw_path / "synthetic_monthly_operations.csv", index=False)
    fuel_df.to_csv(raw_path / "synthetic_fuel_costs.csv", index=False)
    maintenance_df.to_csv(raw_path / "synthetic_maintenance_costs.csv", index=False)
    insurance_df.to_csv(raw_path / "synthetic_insurance_costs.csv", index=False)

    print("Synthetic raw data files created in data/raw/")
    print("- synthetic_monthly_operations.csv")
    print("- synthetic_fuel_costs.csv")
    print("- synthetic_maintenance_costs.csv")
    print("- synthetic_insurance_costs.csv")


def main() -> None:
    months_df = create_month_index()
    operations_df = generate_operations_data(months_df)
    fuel_df = generate_fuel_data(months_df, operations_df)
    maintenance_df = generate_maintenance_data(months_df, operations_df)
    insurance_df = generate_insurance_data(months_df)

    save_outputs(operations_df, fuel_df, maintenance_df, insurance_df)


if __name__ == "__main__":
    main()
