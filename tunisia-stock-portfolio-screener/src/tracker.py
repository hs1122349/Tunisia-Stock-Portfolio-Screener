"""Log daily TUNINDEX snapshots over time and compute simple returns.

The repo ships with one real snapshot row. Run run_log_snapshot.py again on
a later date to add a new row, and compute_return will work once two or
more rows exist.
"""
from __future__ import annotations

import os

import pandas as pd


LOG_COLUMNS = ["date", "tunindex_close", "source"]


def append_snapshot(log_path: str, date: str, tunindex_close: float, source: str = "ilboursa.com") -> pd.DataFrame:
    """Add one row to the snapshot log, creating the file if needed."""
    new_row = pd.DataFrame([{"date": date, "tunindex_close": tunindex_close, "source": source}])
    if os.path.exists(log_path):
        existing = pd.read_csv(log_path)
        combined = pd.concat([existing, new_row], ignore_index=True)
    else:
        combined = new_row
    combined = combined.drop_duplicates(subset="date", keep="last").sort_values("date")
    combined.to_csv(log_path, index=False)
    return combined


def compute_return(log: pd.DataFrame) -> pd.DataFrame:
    """Add a percent-change column once the log has two or more rows."""
    log = log.sort_values("date").reset_index(drop=True)
    log["pct_change"] = log["tunindex_close"].pct_change() * 100
    return log
