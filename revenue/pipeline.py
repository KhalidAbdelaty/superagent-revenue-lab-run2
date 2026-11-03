"""Daily revenue report built from payment events."""
import pandas as pd


def load_events(path):
    """Read payment events; amounts are integer cents."""
    return pd.read_csv(path, parse_dates=["occurred_at", "received_at"])


def daily_revenue(events):
    """Return one row per UTC day with total revenue in cents.

    A payment webhook may deliver the same event more than once, so only the
    first delivery of each ``event_id`` is counted.
    """
    events = events.drop_duplicates(subset=["event_id"], keep="first")
    days = events["occurred_at"].dt.strftime("%Y-%m-%d")
    report = (
        events.assign(day=days)
        .groupby("day", as_index=False)["amount_cents"]
        .sum()
        .rename(columns={"amount_cents": "revenue_cents"})
    )
    return report
