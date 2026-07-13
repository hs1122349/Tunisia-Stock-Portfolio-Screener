"""Append a new TUNINDEX snapshot to the running log.

Run this on any day you check ilboursa.com, and pass the closing value by
hand. The log starts with the one real snapshot already in this repo.

Usage:
    python run_log_snapshot.py 2026-07-14 19900.50
"""
import sys

from src.tracker import append_snapshot, compute_return

LOG_PATH = "data/portfolio_log.csv"


def main():
    if len(sys.argv) != 3:
        print("usage: python run_log_snapshot.py YYYY-MM-DD TUNINDEX_CLOSE")
        sys.exit(1)

    date, close = sys.argv[1], float(sys.argv[2])
    log = append_snapshot(LOG_PATH, date, close)
    log = compute_return(log)
    print(log.to_string(index=False))


if __name__ == "__main__":
    main()
