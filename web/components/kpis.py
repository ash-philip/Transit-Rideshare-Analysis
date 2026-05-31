import streamlit as st


def metric_card(value: str, label: str) -> None:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-value">{value}</div>
            <div class="kpi-label">{label}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def metric_row(metrics: list[dict[str, str]]) -> None:
    columns = st.columns(len(metrics))
    for column, metric in zip(columns, metrics):
        with column:
            metric_card(metric["value"], metric["label"])
