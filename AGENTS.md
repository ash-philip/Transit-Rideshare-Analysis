# AGENTS.md

## Project Goal

This repository is being productized into a polished Streamlit-based **Rideshare Command Center**: a SaaS-style analytics product for senior leadership, the Rideshare team, IT, and Operations.

The product should help users monitor program health, understand ridership and financial trends, review forecasts, and explore fare increase and sustainability scenarios. Treat outputs as decision-support analytics, not operational guarantees.

## Repository Structure

- `web/` contains the Streamlit application and UI assets.
- `web/app.py` is the current Streamlit app entry point.
- `web/assets/` contains existing exported dashboard images. Prefer replacing these with live Plotly charts when implementing dashboard features.
- `web/styles.css` contains app styling.
- `src/` contains reusable Python scripts for synthetic data generation, monthly dataset builds, modeling preparation, validation, forecasting, and scenario analysis.
- `data/raw/` contains synthetic source CSVs.
- `data/processed/` contains precomputed analytics outputs used by the app.
- `notebooks/` contains exploratory and development notebooks.
- `outputs/` contains generated charts and artifacts.
- `sql/` contains schema, staging, mart, and modeling SQL.
- `docs/` and `dashboards/` contain project documentation and notes.

## Data Source Expectations

- Prefer loading precomputed CSV files from `data/processed/`.
- Keep the app designed so data loading can later migrate to live data, a database, or an API.
- Avoid hardcoded absolute paths. Resolve paths from the repository root or the current file location.
- Do not change generated data files in `data/processed/`, `data/raw/`, or `outputs/` unless the task specifically asks for data regeneration or output updates.
- Add lightweight validation around loaded data when practical: required columns, parseable dates, expected metric fields, and null checks for dashboard-critical columns.
- App runtime should favor stable precomputed outputs over running expensive forecasting, synthetic generation, or pipeline logic inside Streamlit.

## Coding Style

- Keep changes focused, reviewable, and aligned with existing project patterns.
- Prefer small functions with clear names over large inline blocks in `web/app.py`.
- Use `pathlib.Path` for filesystem paths.
- Use pandas for tabular transformations.
- Keep formatting and naming consistent with the existing Python code.
- Avoid broad refactors without approval.
- Do not rewrite notebooks unless explicitly asked.
- Avoid adding new dependencies unless the task clearly requires them.
- Preserve synthetic-data safety and avoid implying the data is real agency data.

## UI Style

- Build toward a SaaS-style Command Center rather than a portfolio narrative page.
- Prioritize clear information hierarchy, fast scanning, and professional leadership-facing language.
- Keep leadership-facing text clear, cautious, and professional.
- Avoid overstating certainty. Use language like "suggests", "indicates", "under current assumptions", and "planning scenario".
- Make pages useful for different audiences:
  - Leadership: executive health, financial sustainability, forecast outlook, recommended planning posture.
  - Rideshare team: ridership, service, farebox recovery, scenario tradeoffs.
  - IT: data freshness, validation status, pipeline readiness.
  - Operations: service hours, active vehicles, cost pressure, boardings trends.
- Keep UI controls and labels concise. Avoid long explanatory text inside the app when a chart, KPI, or short note can carry the message.

## Charting Approach

- Use Plotly for interactive charts.
- Prefer live charts from processed CSVs over static images from `web/assets/`.
- Standard chart sources:
  - `rs_monthly_master.csv` for historical boardings, revenue, costs, farebox recovery, cost per boarding, service metrics, and cost components.
  - `business_forecast_12m.csv` for 12-month operational forecasts.
  - `boardings_forecast_12m.csv` and `boardings_forecast_24m.csv` for forecast confidence intervals and horizon comparisons.
  - `farebox_recovery_history_forecast.csv` for historical plus forecast farebox recovery.
  - `scenario_analysis_output.csv` for monthly scenario paths.
  - `scenario_summary.csv` for scenario comparison cards and charts.
- Use consistent formatting for currency, percentages, and whole-number ridership metrics.
- Include confidence intervals where available.
- Keep color choices consistent and accessible.

## Scenario Simulator Rules

- Frame simulator outputs as planning scenarios, not guaranteed predictions.
- Make assumptions visible: fare change, ridership elasticity, cost pressure, and forecast horizon.
- Prefer using precomputed baseline forecast data as the starting point.
- Keep scenario calculations deterministic and easy to inspect.
- Clearly show tradeoffs:
  - boardings impact
  - revenue impact
  - total cost impact
  - farebox recovery impact
  - change from baseline
- Avoid presenting a single "correct" answer. If recommending a scenario, explain it as a balanced planning posture under current assumptions.
- Do not run model fitting inside the simulator unless explicitly requested.

## Testing And Validation

- When changing app logic, run the Streamlit app or at minimum run Python syntax/import checks where practical.
- Validate data-loading changes against the current files in `data/processed/`.
- When changing pipeline scripts, run the affected script and relevant validation checks.
- Keep validation rules adaptable as the dataset grows. Avoid brittle assumptions such as fixed row counts unless the task specifically requires them.
- For UI changes, verify that core pages render and that charts receive the expected columns.
- Do not update generated outputs solely to make tests pass unless the task includes regeneration.

## Change Management Rules

- Modify only files required for the task.
- Keep changes focused and reviewable.
- Do not make broad refactors without approval.
- Do not rewrite notebooks unless asked.
- Do not change generated data files unless specifically requested.
- Preserve existing user work and avoid reverting unrelated changes.
- Prefer incremental productization:
  1. Separate data loading, metrics, charts, and layout helpers.
  2. Add focused pages or tabs.
  3. Replace static dashboard images with live Plotly charts.
  4. Move notebook logic into reusable modules only when requested or clearly in scope.
  5. Keep the app CSV-first while preserving a path to future live data migration.
