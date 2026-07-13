"""Unit tests for the snapshot tracker. Uses a temp file, no real data needed.

Run with: pytest tests/
"""
import os

import pandas as pd
import pytest

from src.tracker import append_snapshot, compute_return


def test_append_snapshot_creates_file(tmp_path):
    log_path = os.path.join(tmp_path, "log.csv")
    log = append_snapshot(log_path, "2026-07-13", 19835.16)
    assert os.path.exists(log_path)
    assert len(log) == 1


def test_append_snapshot_adds_second_row(tmp_path):
    log_path = os.path.join(tmp_path, "log.csv")
    append_snapshot(log_path, "2026-07-13", 19835.16)
    log = append_snapshot(log_path, "2026-07-14", 19900.0)
    assert len(log) == 2


def test_append_snapshot_overwrites_same_date(tmp_path):
    log_path = os.path.join(tmp_path, "log.csv")
    append_snapshot(log_path, "2026-07-13", 19835.16)
    log = append_snapshot(log_path, "2026-07-13", 19900.0)
    assert len(log) == 1
    assert log["tunindex_close"].iloc[0] == pytest.approx(19900.0)


def test_compute_return_first_row_is_nan():
    log = pd.DataFrame({"date": ["2026-07-13"], "tunindex_close": [19835.16], "source": ["ilboursa.com"]})
    result = compute_return(log)
    assert pd.isna(result["pct_change"].iloc[0])


def test_compute_return_second_row():
    log = pd.DataFrame({
        "date": ["2026-07-13", "2026-07-14"],
        "tunindex_close": [100.0, 110.0],
        "source": ["ilboursa.com", "ilboursa.com"],
    })
    result = compute_return(log)
    assert result["pct_change"].iloc[1] == pytest.approx(10.0)
