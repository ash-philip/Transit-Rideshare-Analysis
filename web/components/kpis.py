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


def metric_row(metrics: list[dict[str, str]], columns_per_row: int | None = None) -> None:
    row_size = columns_per_row or len(metrics)
    for start in range(0, len(metrics), row_size):
        row_metrics = metrics[start:start + row_size]
        columns = st.columns(len(row_metrics))
        for column, metric in zip(columns, row_metrics):
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


def signal_card(card: dict[str, str]) -> None:
    tone = card.get("tone", "neutral")
    st.markdown(
        f"""
        <div class="signal-card signal-card-{tone}">
            <div>
                <div class="signal-card-label">{card["title"]}</div>
                <div class="signal-card-status">{card["status"]}</div>
            </div>
            <div class="signal-card-summary">{card["summary"]}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def planning_input_grid(items: list[dict[str, str]]) -> None:
    item_html = "".join(
        f"""
        <div class="planning-input-item">
            <div class="planning-input-label">{item["label"]}</div>
            <div class="planning-input-value">{item["value"]}</div>
        </div>
        """
        for item in items
    )
    st.markdown(
        f"""
        <div class="planning-input-grid">
            {item_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def planning_signal_card(card: dict[str, object]) -> None:
    tone = card.get("tone", "neutral")
    metrics = card.get("metrics", [])
    metric_html = "".join(
        f"""
        <div class="signal-metric">
            <span>{metric["label"]}</span>
            <strong>{metric["value"]}</strong>
        </div>
        """
        for metric in metrics
    )
    st.markdown(
        f"""
        <div class="planning-signal-card signal-card-{tone}">
            <div class="planning-signal-topline">
                <div class="info-card-label">{card["title"]}</div>
                <div class="planning-signal-status">{card["status"]}</div>
            </div>
            <div class="signal-metric-grid">
                {metric_html}
            </div>
            <div class="planning-signal-summary">{card["summary"]}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def planning_signal_grid(cards: list[dict[str, object]], columns_per_row: int = 2) -> None:
    for start in range(0, len(cards), columns_per_row):
        row_cards = cards[start:start + columns_per_row]
        columns = st.columns(len(row_cards))
        for column, card in zip(columns, row_cards):
            with column:
                planning_signal_card(card)


def watch_area_grid(items: list[dict[str, str]]) -> None:
    item_html = "".join(
        f"""
        <div class="watch-area-item">
            <span>{item["label"]}</span>
            <strong>{item["value"]}</strong>
            <small>{item["status"]}</small>
        </div>
        """
        for item in items
    )
    st.markdown(
        f"""
        <div class="watch-area-grid">
            {item_html}
        </div>
        """,
        unsafe_allow_html=True,
    )
