import streamlit as st

from components import charts
from components.kpis import info_card_row, metric_row
from components.layout import (
    load_css,
    page_header,
    section_text,
    section_title,
    sidebar_navigation,
    spacer,
    takeaway,
)
from services.data_loader import load_command_center_data
from services.metrics import (
    executive_kpis,
    forecast_outlook,
    latest_program_metrics,
    performance_snapshot,
    program_health_status,
    scenario_recommendation,
)


CHART_CONFIG = {"displayModeBar": False, "responsive": True}


st.set_page_config(
    page_title="Rideshare Command Center",
    page_icon="📈",
    layout="wide",
)


def render_executive_overview(master_df, business_forecast_df, scenario_summary_df) -> None:
    section_title("Executive Overview")
    section_text(
        """
        This view summarizes the current rideshare operating picture for leadership: demand, financial recovery,
        near-term forecast posture, and scenario tradeoffs. Forecasts and scenarios are planning tools based on
        current assumptions, not guaranteed outcomes.
        """
    )

    metric_row(executive_kpis(master_df))
    spacer()

    info_card_row(
        [
            program_health_status(master_df),
            forecast_outlook(business_forecast_df),
            scenario_recommendation(scenario_summary_df),
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


def render_program_health(master_df) -> None:
    section_title("Program Health")
    section_text(
        """
        Service demand declined sharply during the disruption period and then recovered gradually over time.
        Revenue moved in the same direction, but total operating cost remained more stable, creating sustained
        pressure on cost recovery during lower-demand periods.
        """
    )

    metric_row(latest_program_metrics(master_df))
    spacer()

    c1, c2 = st.columns(2)
    with c1:
        st.plotly_chart(charts.monthly_boardings(master_df), use_container_width=True, config=CHART_CONFIG)
    with c2:
        st.plotly_chart(charts.revenue_vs_total_cost(master_df), use_container_width=True, config=CHART_CONFIG)

    st.plotly_chart(charts.farebox_recovery(master_df), use_container_width=True, config=CHART_CONFIG)
    takeaway(
        """
        Ridership recovery was meaningful, but financial recovery was slower and less consistent because operating
        cost remained comparatively stable throughout the recovery period.
        """
    )


def render_forecast_center(business_forecast_df, farebox_history_forecast_df) -> None:
    section_title("Forecast Center")
    section_text(
        """
        The baseline forecast suggests that ridership remains relatively stable over the next 12 months. However,
        farebox recovery continues to fluctuate seasonally rather than improve in a straight line, which indicates
        that recent progress may be leveling off rather than accelerating.
        """
    )
    section_text(
        """
        For planning purposes, this shifts the challenge from short-term recovery to long-term sustainability.
        A stable outlook is encouraging, but it does not eliminate the need to test how future pricing or cost changes
        could alter the agency's financial position.
        """
    )

    c1, c2 = st.columns(2)
    with c1:
        st.plotly_chart(
            charts.forecast_boardings(business_forecast_df),
            use_container_width=True,
            config=CHART_CONFIG,
        )
    with c2:
        st.plotly_chart(
            charts.historical_forecast_farebox(farebox_history_forecast_df),
            use_container_width=True,
            config=CHART_CONFIG,
        )

    takeaway(
        """
        The baseline outlook is stable, but not fully resolved. Future gains remain sensitive to pricing assumptions
        and ongoing operating cost pressure.
        """
    )


def render_scenario_simulator(scenario_summary_df) -> None:
    section_title("Scenario Simulator")
    section_text(
        """
        Scenario analysis tests how alternative fare and cost assumptions affect ridership and cost recovery.
        Under the current assumptions, higher fares improve farebox recovery, but they also reduce boardings.
        These outputs should be interpreted as planning scenarios, not guaranteed predictions.
        """
    )
    section_text(
        """
        The current simulator view uses precomputed scenario outputs so the dashboard remains stable and easy to audit.
        Future iterations can add interactive controls while preserving this baseline scenario logic.
        """
    )

    c1, c2 = st.columns(2)
    with c1:
        st.plotly_chart(
            charts.scenario_farebox_recovery(scenario_summary_df),
            use_container_width=True,
            config=CHART_CONFIG,
        )
    with c2:
        st.plotly_chart(
            charts.scenario_boardings(scenario_summary_df),
            use_container_width=True,
            config=CHART_CONFIG,
        )

    takeaway(
        """
        Higher fare increases produce the strongest recovery under current assumptions, but a moderate fare increase
        may offer a more balanced path by improving cost recovery while limiting ridership loss.
        """
    )


def render_recommendations() -> None:
    section_title("Recommendations")
    section_text(
        """
        The rideshare service appears to have recovered meaningfully, but the analysis suggests that recent gains may
        be difficult to sustain without targeted action. Forecasting and scenario analysis indicate that future
        performance will depend not only on continued demand, but also on how pricing and operating cost pressure are
        managed together.
        """
    )
    section_text(
        """
        In practice, the agency's challenge is no longer simply restoring service performance. It is determining which
        decisions can improve long-term financial sustainability without undermining ridership and service value.
        """
    )
    spacer()

    section_title("Methodology")
    left, right = st.columns([2, 1])
    with left:
        section_text(
            """
            This project was built as a full analytics pipeline using synthetic transit data designed to preserve
            realistic service, cost, and recovery patterns without using confidential or proprietary agency data.
            The workflow combines data generation, ETL, KPI development, forecasting, and scenario analysis to support
            a more decision-oriented view of transit performance.
            """
        )
    with right:
        st.markdown(
            """
            <div class="method-box">
                <div class="method-title">Methods Used</div>
                <ul>
                    <li>Synthetic monthly data generation</li>
                    <li>ETL and monthly spine creation</li>
                    <li>KPI engineering</li>
                    <li>Descriptive and diagnostic analysis</li>
                    <li>Time-series forecasting</li>
                    <li>Scenario analysis using fare and cost assumptions</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )

    spacer()
    section_title("Project Links")
    section_text("Explore the repository, documentation, and project assets below.")
    st.markdown(
        """
        <div class="links-box">
            <a href="https://github.com/ash-philip/Transit-Rideshare-Analysis" target="_blank">GitHub Repository</a>
        </div>
        """,
        unsafe_allow_html=True,
    )


def main() -> None:
    load_css()
    page_header()
    section = sidebar_navigation()
    spacer()

    (
        master_df,
        business_forecast_df,
        farebox_history_forecast_df,
        scenario_summary_df,
    ) = load_command_center_data()

    if section == "Executive Overview":
        render_executive_overview(master_df, business_forecast_df, scenario_summary_df)
    elif section == "Program Health":
        render_program_health(master_df)
    elif section == "Forecast Center":
        render_forecast_center(business_forecast_df, farebox_history_forecast_df)
    elif section == "Scenario Simulator":
        render_scenario_simulator(scenario_summary_df)
    elif section == "Recommendations":
        render_recommendations()


if __name__ == "__main__":
    main()
