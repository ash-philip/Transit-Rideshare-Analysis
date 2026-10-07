import streamlit as st

from components import charts
from components.kpis import (
    info_card_row,
    metric_row,
    planning_input_grid,
    planning_signal_grid,
    signal_card,
    watch_area_grid,
)
from components.layout import (
    load_css,
    page_header,
    section_text,
    section_title,
    spacer,
    takeaway,
    view_selector,
)
from services.data_loader import load_command_center_data
from services.metrics import (
    executive_kpis,
    forecast_center_kpis,
    forecast_center_signal,
    forecast_outlook,
    planning_input_summary,
    program_health_kpis,
    program_health_signals,
    program_health_status,
    scenario_decision_kpis,
    scenario_planning_signal,
    scenario_simulator_signal,
)
from services.scenario_engine import (
    apply_planning_assumptions,
    load_scenario_detail,
    scenario_options,
)
from services.planning_signals import build_planning_signals


CHART_CONFIG = {"displayModeBar": False, "responsive": True}


PROGRAM_HEALTH_VIEWS = {
    "Ridership": {
        "title": "Ridership",
        "help": "Tracks monthly usage of the rideshare program and helps identify demand trends or seasonality.",
    },
    "Financial Performance": {
        "title": "Financial Performance",
        "help": "Compares fare revenue against total program cost to show sustainability pressure.",
    },
    "Farebox Recovery": {
        "title": "Farebox Recovery",
        "help": "Shows the share of total cost covered by fare revenue.",
    },
    "Cost Efficiency": {
        "title": "Cost Efficiency",
        "help": "Shows the estimated cost required to support each boarding.",
    },
    "Operations": {
        "title": "Operations",
        "help": "Shows whether operating supply and fleet activity are moving with demand.",
    },
}


FORECAST_CENTER_VIEWS = {
    "Demand Outlook": {
        "title": "Demand Outlook",
        "help": "Shows expected boardings direction and uncertainty for the selected planning horizon.",
    },
    "Farebox Recovery Outlook": {
        "title": "Farebox Recovery Outlook",
        "help": "Combines historical and forecasted farebox recovery to monitor cost-recovery direction.",
    },
    "Planning Inputs": {
        "title": "Planning Inputs",
        "help": "Summarizes the precomputed inputs behind the planning views without model detail or refitting in the app.",
    },
}


SCENARIO_CHART_VIEWS = {
    "Recovery vs Target": {
        "title": "Recovery vs Target",
        "help": "Compares estimated farebox recovery under selected assumptions against the planning threshold.",
    },
    "Revenue vs Cost": {
        "title": "Revenue vs Cost",
        "help": "Shows whether estimated revenue is keeping pace with total program cost in the selected case.",
    },
    "Boardings Impact": {
        "title": "Boardings Impact",
        "help": "Compares preset boardings with boardings after the selected fare and demand-response assumptions.",
    },
    "Scenario Comparison": {
        "title": "Scenario Comparison",
        "help": "Benchmarks the selected assumptions against the precomputed scenario recovery averages.",
    },
}


st.set_page_config(
    page_title="Rideshare Command Center",
    page_icon="📈",
    layout="wide",
)


def render_executive_overview(master_df, business_forecast_df, scenario_summary_df) -> None:
    section_title("Executive Overview")
    section_text(
        """
        Leadership view for current demand, financial recovery, near-term outlook, and scenario tradeoffs.
        """
    )
    st.markdown(
        """
        <div class="planning-note">
            Forecasts and scenarios are planning tools based on available processed data and stated assumptions.
            They should be reviewed alongside operational context before decisions are made.
        </div>
        """,
        unsafe_allow_html=True,
    )

    metric_row(executive_kpis(master_df))
    spacer()

    info_card_row(
        [
            program_health_status(master_df),
            forecast_outlook(business_forecast_df),
            scenario_planning_signal(scenario_summary_df),
        ]
    )
    spacer()

    section_title("Leadership Trends")
    c1, c2 = st.columns(2)
    with c1:
        st.plotly_chart(charts.monthly_boardings(master_df), use_container_width=True, config=CHART_CONFIG)
    with c2:
        st.plotly_chart(charts.revenue_vs_total_cost(master_df), use_container_width=True, config=CHART_CONFIG)

    st.plotly_chart(charts.farebox_recovery(master_df), use_container_width=True, config=CHART_CONFIG)


def program_health_chart(view: str, filtered_df):
    if view == "Ridership":
        return charts.monthly_boardings(filtered_df)
    if view == "Financial Performance":
        return charts.revenue_vs_total_cost(filtered_df)
    if view == "Farebox Recovery":
        return charts.farebox_recovery(filtered_df)
    if view == "Cost Efficiency":
        return charts.cost_per_boarding(filtered_df)
    return charts.service_hours_active_vehicles(filtered_df)


def forecast_center_chart(
    view: str,
    master_df,
    business_forecast_df,
    boardings_forecast_12m_df,
    boardings_forecast_24m_df,
    farebox_history_forecast_df,
):
    if view == "12-Month Planning View":
        return charts.boardings_forecast_with_interval(
            boardings_forecast_12m_df,
            "12-Month Boardings Planning View",
            historical_df=master_df,
        )
    if view == "24-Month Demand Outlook":
        return charts.boardings_forecast_with_interval(
            boardings_forecast_24m_df,
            "24-Month Boardings Demand Outlook",
            historical_df=master_df,
        )
    if view == "Farebox Recovery Outlook":
        return charts.historical_forecast_farebox(farebox_history_forecast_df)
    return charts.projected_avg_fare(business_forecast_df)


def scenario_simulator_chart(view: str, scenario_summary_df, adjusted_scenario_df, selected_scenario: str):
    if view == "Recovery vs Target":
        return charts.selected_scenario_recovery(adjusted_scenario_df)
    if view == "Revenue vs Cost":
        return charts.selected_scenario_revenue_cost(adjusted_scenario_df)
    if view == "Boardings Impact":
        return charts.selected_scenario_boardings(adjusted_scenario_df)
    return charts.scenario_comparison_summary(
        scenario_summary_df,
        adjusted_scenario_df,
        selected_scenario,
    )


def render_program_health(master_df) -> None:
    section_title("Program Health")
    section_text(
        """
        Diagnostic view for ridership, cost pressure, recovery, and operating utilization.
        """
    )

    history = master_df.sort_values("date").reset_index(drop=True)
    min_date = history["date"].min().date()
    max_date = history["date"].max().date()

    selected_range = st.date_input(
        "Date range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
    )

    if isinstance(selected_range, tuple) and len(selected_range) == 2:
        start_date, end_date = selected_range
    else:
        start_date, end_date = min_date, max_date

    filtered_df = history[
        (history["date"].dt.date >= start_date)
        & (history["date"].dt.date <= end_date)
    ].copy()

    if filtered_df.empty:
        st.warning("No program health data is available for the selected date range.")
        return

    metric_row(program_health_kpis(filtered_df), columns_per_row=3)
    spacer()

    section_title("Health Signals")
    info_card_row(program_health_signals(filtered_df))
    spacer()

    section_title("Health View")
    selector_col, chart_col = st.columns([1, 3.2], gap="large")
    with selector_col:
        selected_view = view_selector(
            "Health views",
            list(PROGRAM_HEALTH_VIEWS.keys()),
            key="program_health_view",
        )

    with chart_col:
        selected_meta = PROGRAM_HEALTH_VIEWS[selected_view]
        st.markdown(
            f"""
            <div class="chart-panel-heading">
                <div class="chart-panel-title">{selected_meta["title"]}</div>
                <div class="chart-panel-help">{selected_meta["help"]}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.plotly_chart(
            charts.set_chart_height(program_health_chart(selected_view, filtered_df), 520),
            use_container_width=True,
            config=CHART_CONFIG,
        )

    takeaway(
        """
        This page is diagnostic: signals highlight where ridership, cost, recovery, or utilization may need review.
        """
    )


def render_forecast_center(
    master_df,
    business_forecast_df,
    boardings_forecast_12m_df,
    boardings_forecast_24m_df,
    farebox_history_forecast_df,
) -> None:
    section_title("Forecast Center")
    section_text(
        """
        Forward-looking planning views for demand, revenue, cost, and farebox recovery.
        """
    )

    selector_col, chart_col = st.columns([1, 3.2], gap="large")
    with selector_col:
        selected_view = view_selector(
            "Forecast views",
            list(FORECAST_CENTER_VIEWS.keys()),
            key="forecast_center_view",
        )
        forecast_horizon = "12-Month"
        if selected_view == "Demand Outlook":
            st.markdown("<div class='view-selector-label'>Planning horizon</div>", unsafe_allow_html=True)
            forecast_horizon = st.radio(
                "Planning horizon",
                ["12-Month", "24-Month"],
                horizontal=True,
                key="forecast_horizon",
                label_visibility="collapsed",
            )

    with chart_col:
        selected_meta = FORECAST_CENTER_VIEWS[selected_view]
        metric_view = selected_view
        chart_title = selected_meta["title"]
        chart_help = selected_meta["help"]
        if selected_view == "Demand Outlook":
            metric_view = "12-Month Planning View" if forecast_horizon == "12-Month" else "24-Month Demand Outlook"
            chart_title = metric_view
            chart_help = (
                "Shows near-term boardings, revenue, cost, and recovery expectations using the 12-month business forecast."
                if forecast_horizon == "12-Month"
                else "Extends the demand planning window to show boardings direction and uncertainty over 24 months."
            )
        metric_row(
            forecast_center_kpis(
                metric_view,
                business_forecast_df,
                boardings_forecast_12m_df,
                boardings_forecast_24m_df,
                farebox_history_forecast_df,
            ),
            columns_per_row=4,
        )
        signal_card(
            forecast_center_signal(
                metric_view,
                business_forecast_df,
                boardings_forecast_12m_df,
                boardings_forecast_24m_df,
                farebox_history_forecast_df,
            )
        )
        st.markdown(
            f"""
            <div class="chart-panel-heading">
                <div class="chart-panel-title">{chart_title}</div>
                <div class="chart-panel-help">{chart_help}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if selected_view == "Planning Inputs":
            planning_input_grid(
                planning_input_summary(
                    business_forecast_df,
                    boardings_forecast_12m_df,
                    boardings_forecast_24m_df,
                )
            )
        else:
            st.plotly_chart(
                charts.set_chart_height(
                    forecast_center_chart(
                        metric_view,
                        master_df,
                        business_forecast_df,
                        boardings_forecast_12m_df,
                        boardings_forecast_24m_df,
                        farebox_history_forecast_df,
                    ),
                    520,
                ),
                use_container_width=True,
                config=CHART_CONFIG,
            )

    st.markdown(
        """
        <div class="dashboard-note">
            Forecasts are planning tools based on available processed data and model assumptions. They are not
            guaranteed outcomes and should be reviewed with operating context.
        </div>
        """,
        unsafe_allow_html=True,
    )

    takeaway(
        """
        Forecast Center uses precomputed outputs only; no models are refit inside the dashboard.
        """
    )


def render_scenario_simulator(scenario_summary_df, scenario_detail_df) -> None:
    section_title("Scenario Simulator")
    section_text(
        """
        Explore fare, demand response, cost pressure, and recovery targets as directional planning cases.
        """
    )

    if scenario_detail_df.empty:
        st.warning("Scenario simulator detail is unavailable because `scenario_analysis_output.csv` could not be loaded.")
        return

    scenario_horizon_months = int(scenario_detail_df.groupby("scenario_name")["date"].nunique().max())
    scenario_case_options = scenario_options(scenario_detail_df)
    if not scenario_case_options:
        st.warning("No scenario planning cases are available in the scenario detail output.")
        return

    controls_col, output_col = st.columns([0.9, 3.7], gap="large")
    with controls_col:
        st.markdown("<div class='control-panel-title'>Scenario controls</div>", unsafe_allow_html=True)
        selected_scenario = st.selectbox(
            "Planning case",
            scenario_case_options,
            index=0,
            help="Select a precomputed scenario as the starting point.",
        )
        fare_adjustment_pct = st.slider(
            "Fare adjustment",
            min_value=-10,
            max_value=25,
            value=0,
            step=1,
            format="%d%%",
            help="Applies an additional fare adjustment to the selected preset case.",
        )
        demand_response = st.slider(
            "Demand response",
            min_value=-1.00,
            max_value=0.00,
            value=-0.30,
            step=0.05,
            help="Estimated boarding response for each 1% fare change. More negative values assume stronger demand sensitivity.",
        )
        cost_pressure_pct = st.slider(
            "Cost pressure",
            min_value=-10,
            max_value=25,
            value=0,
            step=1,
            format="%d%%",
            help="Applies an additional cost change to the selected preset case.",
        )
        target_recovery_pct = st.slider(
            "Planning recovery threshold",
            min_value=70,
            max_value=115,
            value=90,
            step=1,
            format="%d%%",
            help="Adjustable planning threshold used for average recovery comparison and monthly threshold counts.",
        )
        st.markdown(
            """
            <div class="dashboard-note">
                Controls apply lightweight adjustments to precomputed scenario outputs. They do not refit models.
            </div>
            """,
            unsafe_allow_html=True,
        )
        if scenario_horizon_months < 24:
            st.markdown(
                f"""
                <div class="dashboard-note">
                    Scenario outputs currently cover the precomputed {scenario_horizon_months}-month scenario horizon.
                    24-month scenario outputs are not available for this simulator.
                </div>
                """,
                unsafe_allow_html=True,
            )

    adjusted_scenario_df = apply_planning_assumptions(
        scenario_detail_df,
        selected_scenario,
        fare_adjustment_pct,
        demand_response,
        cost_pressure_pct,
        target_recovery_pct / 100,
    )

    if adjusted_scenario_df.empty:
        st.warning("No scenario rows are available for the selected planning case.")
        return

    with output_col:
        st.markdown(
            f"""
            <div class="scenario-case-badge">
                <span>Selected planning case</span>
                <strong>{selected_scenario}</strong>
            </div>
            """,
            unsafe_allow_html=True,
        )
        metric_row(scenario_decision_kpis(adjusted_scenario_df), columns_per_row=4)
        signal_card(
            scenario_simulator_signal(
                adjusted_scenario_df,
                selected_scenario,
                target_recovery_pct / 100,
            )
        )

        selected_chart = st.radio(
            "Scenario chart",
            list(SCENARIO_CHART_VIEWS.keys()),
            horizontal=True,
            key="scenario_chart_view",
        )
        selected_chart_meta = SCENARIO_CHART_VIEWS[selected_chart]
        st.markdown(
            f"""
            <div class="chart-panel-heading">
                <div class="chart-panel-title">{selected_chart_meta["title"]}</div>
                <div class="chart-panel-help">{selected_chart_meta["help"]}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.plotly_chart(
            charts.set_chart_height(
                scenario_simulator_chart(
                    selected_chart,
                    scenario_summary_df,
                    adjusted_scenario_df,
                    selected_scenario,
                ),
                520,
            ),
            use_container_width=True,
            config=CHART_CONFIG,
        )

    takeaway(
        """
        Scenario outputs are estimated planning impacts based on selected assumptions, not final recommendations.
        """
    )


def render_planning_signals(
    master_df,
    business_forecast_df,
    boardings_forecast_12m_df,
    boardings_forecast_24m_df,
    farebox_history_forecast_df,
    scenario_summary_df,
    scenario_detail_df,
) -> None:
    section_title("Planning Signals")
    section_text(
        """
        Decision-support signal board based on program health, forecast outlook, and scenario comparison.
        """
    )

    planning_board = build_planning_signals(
        master_df,
        business_forecast_df,
        boardings_forecast_12m_df,
        boardings_forecast_24m_df,
        farebox_history_forecast_df,
        scenario_summary_df,
        scenario_detail_df,
    )

    section_title("Leadership Planning View")
    planning_input_grid(planning_board["leadership_view"])

    spacer()
    section_title("Signal Board")
    planning_signal_grid(planning_board["signals"])

    spacer()
    section_title("Watch Areas")
    watch_area_grid(planning_board["watch_areas"])

    st.markdown(
        """
        <div class="dashboard-note">
            Planning signals are based on available processed data and assumptions. They are decision-support prompts,
            not final recommendations.
        </div>
        """,
        unsafe_allow_html=True,
    )


def main() -> None:
    load_css()
    section = page_header()
    spacer()

    (
        master_df,
        business_forecast_df,
        boardings_forecast_12m_df,
        boardings_forecast_24m_df,
        farebox_history_forecast_df,
        scenario_summary_df,
    ) = load_command_center_data()
    scenario_detail_df = load_scenario_detail()

    if section == "Executive Overview":
        render_executive_overview(master_df, business_forecast_df, scenario_summary_df)
    elif section == "Program Health":
        render_program_health(master_df)
    elif section == "Forecast Center":
        render_forecast_center(
            master_df,
            business_forecast_df,
            boardings_forecast_12m_df,
            boardings_forecast_24m_df,
            farebox_history_forecast_df,
        )
    elif section == "Scenario Simulator":
        render_scenario_simulator(scenario_summary_df, scenario_detail_df)
    elif section == "Planning Signals":
        render_planning_signals(
            master_df,
            business_forecast_df,
            boardings_forecast_12m_df,
            boardings_forecast_24m_df,
            farebox_history_forecast_df,
            scenario_summary_df,
            scenario_detail_df,
        )


if __name__ == "__main__":
    main()
