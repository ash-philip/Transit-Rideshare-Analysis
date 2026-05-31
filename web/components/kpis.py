import streamlit as st


def metric_card(value: str, label: str, delta: str | None = None) -> None:
    delta_html = f"<div class='kpi-delta'>{delta}</div>" if delta else ""
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-value">{value}</div>
            <div class="kpi-label">{label}</div>
            {delta_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def metric_row(metrics: list[dict[str, str]]) -> None:
    columns = st.columns(len(metrics))
    for column, metric in zip(columns, metrics):
        with column:
            metric_card(metric["value"], metric["label"], metric.get("delta"))


def info_card(card: dict[str, str]) -> None:
    tone = card.get("tone", "neutral")
    st.markdown(
        f"""
        <div class="info-card info-card-{tone}">
            <div class="info-card-label">{card["title"]}</div>
            <div class="info-card-status">{card["status"]}</div>
            <div class="info-card-summary">{card["summary"]}</div>
            <div class="info-card-detail">{card["detail"]}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def info_card_row(cards: list[dict[str, str]]) -> None:
    columns = st.columns(len(cards))
    for column, card in zip(columns, cards):
        with column:
            info_card(card)
