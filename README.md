# Transit Rideshare Analytics Pipeline

### An end-to-end analytics pipeline built with synthetic transit rideshare data to analyze ridership, revenue, operating costs, farebox recovery, forecasting, and fare scenario impacts.

## Project Overview

### This project simulates a public transit rideshare and vanpool analytics workflow using fully synthetic data. It was developed as a portfolio-safe version of a realistic transit business problem and demonstrates the full analytics lifecycle from synthetic data generation to forecasting and scenario analysis.

### The project is designed to answer how a transit agency can evaluate service performance, monitor financial sustainability, and assess the impact of pricing decisions over time.

## Business Problem

### A transit agency wants to assess the performance and long-term sustainability of its rideshare service. Although service demand may recover over time, leadership still needs to understand:

    - how ridership has changed over time
    - how revenue compares with operating cost
    - how farebox recovery has evolved
    - which cost components most affect performance
    - how future demand and financial performance may change
    - how fare changes may improve or weaken outcomes under different assumptions

This project approaches the problem as both an analytics and decision-support use case.

## Project Goals
    - Generate realistic synthetic monthly transit operations and cost data
    - Build a clean ETL and analytics pipeline
    - Create a master KPI dataset for reporting and modeling
    - Perform descriptive and diagnostic analysis of ridership, revenue, and cost trends
    - Forecast future boardings, revenue, and farebox recovery
    - Evaluate pricing and cost-pressure scenarios to support planning decisions

## Data Note

### All data in this repository is synthetic and generated for portfolio purposes. No confidential, proprietary, or client-provided transit agency data is included.

### The synthetic data was designed to preserve a realistic business structure, including:
    - disruption and recovery patterns
    - monthly seasonality
    - revenue linked to ridership and fare assumptions
    - cost variation across fuel, maintenance, and insurance
    - long-term stabilization effects relevant to planning and forecasting

## Project Architecture

### The project follows a layered analytics pipeline:

### Synthetic Raw Data  
    - Monthly Spine  
    - Master KPI Dataset  
    - Modeling Dataset  
    - Descriptive and Diagnostic Analytics  
    - Forecasting  
  - Scenario Analysis

## Repository Structure


transit-rideshare-analytics/
├── data/
│   ├── raw/
│   ├── processed/
│   └── scenarios/
├── notebooks/
├── src/
├── sql/
├── docs/
├── dashboards/
└── outputs/

## Pipeline Components

### 1. Synthetic Data Generation

### Synthetic monthly source data is generated for:
	•	operations and boardings
	•	fuel costs
	•	maintenance costs
	•	insurance costs

### 2. ETL and Data Modeling

### The ETL layer creates:
	•	rs_monthly_spine.csv for a complete monthly timeline
	•	rs_monthly_master.csv as the main KPI dataset
	•	rs_modeling_dataset.csv as the forecasting-ready dataset

### 3. Validation

### Validation checks confirm:
	•	expected row counts
	•	required fields
	•	absence of nulls in key columns
	•	uniqueness of monthly records
	•	cost calculation consistency

### 4. Descriptive and Diagnostic Analytics

### The descriptive layer analyzes:
	•	monthly boardings
	•	revenue versus total cost
	•	farebox recovery trends
	•	cost component behavior
	•	period comparisons across disruption, recovery, and stabilization

### 5. Forecasting

### The forecasting layer uses time-series modeling to project:
	•	monthly boardings
	•	short-term business outlook
	•	projected revenue
	•	projected farebox recovery

### The project includes both a 12-month operational forecast and a 24-month planning outlook.

### 6. Scenario Analysis

### Scenario analysis tests how alternative assumptions affect business outcomes, including:
	•	base case
	•	moderate fare increase
	•	higher fare increase
	•	fare increase with added cost pressure

## Core KPIs

### Key metrics used throughout the project include:
	•	Boardings
	•	Revenue
	•	Total Cost
	•	Farebox Recovery
	•	Cost per Boarding
	•	Cost per Service Hour
	•	Revenue per Boarding

## Tools Used
	•	Python
	•	pandas
	•	matplotlib
	•	statsmodels
	•	Jupyter Notebook
	•	SQL
	•	Git / GitHub

## Key Outputs

### The project produces analytics-ready and modeling-ready outputs such as:
	•	rs_monthly_master.csv
	•	rs_modeling_dataset.csv
	•	boardings_forecast_12m.csv
	•	boardings_forecast_24m.csv
	•	business_forecast_12m.csv
	•	scenario_analysis_output.csv
	•	scenario_summary.csv

### Key Insights
	•	Ridership declines sharply during the disruption period and recovers gradually over time.
	•	Revenue generally follows ridership, while operating cost behaves more steadily.
	•	Farebox recovery improves during recovery years but begins to level off in later periods.
	•	Maintenance costs are more volatile than insurance costs and can create financial pressure.
	•	Fare increase scenarios improve farebox recovery under current assumptions, but stronger financial outcomes may come with ridership tradeoffs.
	•	Cost pressure can weaken the benefits of fare changes, highlighting the importance of both pricing and cost management.

## Why This Project Matters

### This project demonstrates how an analytics workflow can move beyond reporting and support actual planning decisions. It combines data engineering, KPI development, forecasting, and scenario analysis in a single end-to-end portfolio project.

## Future Improvements

### Possible extensions include:
	•	vehicle-level or route-level simulation
	•	more advanced cost forecasting
	•	alternative elasticity assumptions
	•	dashboard development in Power BI or Tableau
	•	sensitivity analysis across multiple planning scenarios
