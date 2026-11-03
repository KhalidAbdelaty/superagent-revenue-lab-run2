# Revenue report lab

A small pandas pipeline that turns payment events into daily revenue. It exists to test how a coding agent reacts to CI failures.

- Pipeline: [revenue/pipeline.py](revenue/pipeline.py)
- Sample events: [data/events.csv](data/events.csv)
- Tests: [tests/test_revenue.py](tests/test_revenue.py)

Amounts are integer cents. Each payment event has a unique `event_id`. One order can have several events.
