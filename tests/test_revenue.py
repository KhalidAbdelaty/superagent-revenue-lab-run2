from pathlib import Path

import pandas as pd

from revenue.pipeline import daily_revenue, load_events

DATA = Path(__file__).resolve().parents[1] / "data" / "events.csv"


def frame(rows):
    columns = ["event_id", "order_id", "occurred_at", "received_at", "amount_cents"]
    events = pd.DataFrame(rows, columns=columns)
    for column in ("occurred_at", "received_at"):
        events[column] = pd.to_datetime(events[column])
    return events


def test_daily_totals_match_known_values():
    report = daily_revenue(load_events(DATA))
    totals = dict(zip(report["day"], report["revenue_cents"]))
    assert totals == {"2026-10-28": 20398, "2026-10-29": 27550, "2026-10-30": 15100}


def test_events_on_the_same_order_are_all_counted():
    # Two real events (different event IDs) on one order: both count.
    events = frame([
        ("evt_a", "ord_1", "2026-10-28T10:00:00Z", "2026-10-28T10:00:01Z", 1000),
        ("evt_b", "ord_1", "2026-10-28T10:05:00Z", "2026-10-28T10:05:01Z", 250),
    ])
    report = daily_revenue(events)
    assert report["revenue_cents"].tolist() == [1250]


def test_replayed_event_is_counted_once():
    # The payment webhook delivered evt_r twice; received_at differs, event_id does not.
    events = frame([
        ("evt_r", "ord_9", "2026-10-30T09:00:00Z", "2026-10-30T09:00:01Z", 4000),
        ("evt_r", "ord_9", "2026-10-30T09:00:00Z", "2026-10-30T09:06:30Z", 4000),
    ])
    report = daily_revenue(events)
    assert report["revenue_cents"].tolist() == [4000]
