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
    """
    rng = np.random.default_rng(RANDOM_SEED)
    df = months_df.copy()

    # Seasonal pattern for demand
    seasonality = 1 + 0.12 * np.sin(2 * np.pi * df["month_num"] / 12)

    # Disruption and recovery multipliers
    shock_factor = []
    for date in df["date"]:
        if date < pd.Timestamp("2020-04-01"):
            shock_factor.append(1.00)
        elif date <= pd.Timestamp("2020-12-01"):
            shock_factor.append(0.45)
        elif date <= pd.Timestamp("2021-12-01"):
            shock_factor.append(0.65)
        elif date <= pd.Timestamp("2022-12-01"):
            shock_factor.append(0.78)
        elif date <= pd.Timestamp("2023-12-01"):
            shock_factor.append(0.90)
        else:
            shock_factor.append(1.00)

    df["shock_factor"] = shock_factor

    # Long-term mild growth trend
    growth_factor = 1 + (df["t"] * 0.0025)

    # Boardings
    base_boardings = 7500
    noise_boardings = rng.normal(0, 350, len(df))
    df["boardings"] = (
        base_boardings
        * seasonality
        * df["shock_factor"]
        * growth_factor
        + noise_boardings
    ).round().clip(lower=1800)

    # Service hours: smoother and less volatile than boardings
    service_noise = rng.normal(0, 40, len(df))
    df["service_hours"] = (
        1250
        * (0.92 + 0.08 * seasonality)
        * (0.75 + 0.25 * df["shock_factor"])
        * (1 + df["t"] * 0.0015)
        + service_noise
    ).round().clip(lower=700)

    # Active vehicles
    vehicle_noise = rng.normal(0, 1.2, len(df))
    df["active_vehicles"] = (
        42
        * (0.80 + 0.20 * df["shock_factor"])
        * (1 + df["t"] * 0.001)
        + vehicle_noise
    ).round().clip(lower=25)

    # Average fare per boarding
    fare_noise = rng.normal(0, 0.08, len(df))
    df["avg_fare_per_boarding"] = (
        4.10 + (df["t"] * 0.01) + fare_noise
    ).round(2).clip(lower=3.50, upper=5.50)

    # Revenue
    revenue_noise = rng.normal(1.0, 0.03, len(df))
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
    """
    rng = np.random.default_rng(RANDOM_SEED + 1)
    df = months_df[["year_month", "t", "month_num"]].copy()
    merged = df.merge(
        operations_df[["year_month", "service_hours"]],
        on="year_month",
        how="left"
    )

    seasonal_fuel = 1 + 0.06 * np.cos(2 * np.pi * merged["month_num"] / 12)
    fuel_price_index = 1.00 + 0.10 * np.sin(2 * np.pi * merged["t"] / 18) + rng.normal(0, 0.03, len(merged))
    fuel_price_index = np.clip(fuel_price_index, 0.85, 1.35)

    merged["fuel_price_index"] = fuel_price_index.round(3)
    merged["fuel_cost"] = (
        merged["service_hours"] * 9.5 * seasonal_fuel * merged["fuel_price_index"]
        + rng.normal(0, 250, len(merged))
    ).round(2).clip(lower=4000)

    return merged[["year_month", "fuel_cost", "fuel_price_index"]]


def generate_maintenance_data(months_df: pd.DataFrame, operations_df: pd.DataFrame) -> pd.DataFrame:
    """
    Generate synthetic monthly maintenance costs with occasional spikes.
    """
    rng = np.random.default_rng(RANDOM_SEED + 2)
    df = months_df[["year_month"]].copy()
    merged = df.merge(
        operations_df[["year_month", "service_hours", "active_vehicles"]],
        on="year_month",
        how="left"
    )

    base_cost = 8500
    variable_cost = merged["service_hours"] * 2.8
    fleet_component = merged["active_vehicles"] * 55

    spike_flags = rng.choice([0, 1], size=len(merged), p=[0.88, 0.12])
    spike_amount = spike_flags * rng.uniform(2500, 7000, size=len(merged))

    merged["maintenance_event_count"] = (
        2 + spike_flags + rng.integers(0, 3, size=len(merged))
    )

    merged["maintenance_cost"] = (
        base_cost
        + variable_cost
        + fleet_component
        + spike_amount
        + rng.normal(0, 600, len(merged))
    ).round(2).clip(lower=5000)

    return merged[["year_month", "maintenance_cost", "maintenance_event_count"]]


def generate_insurance_data(months_df: pd.DataFrame) -> pd.DataFrame:
    """
    Generate smooth monthly insurance costs with slight annual increases.
    """
    rng = np.random.default_rng(RANDOM_SEED + 3)
    df = months_df[["year_month", "t"]].copy()

    df["insurance_cost"] = (
        6200
        + (df["t"] * 18)
        + rng.normal(0, 120, len(df))
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
