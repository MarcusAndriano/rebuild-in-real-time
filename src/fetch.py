"""Data acquisition for Rebuild in Real Time.

Two entry points, split by how fragile the underlying source is.

``historical``
    FBref, via a browser. FBref sits behind bot protection, so soccerdata's
    FBref reader drives an undetected Chrome instance. Run this locally, once,
    and commit what it writes. Do not put it in CI.

``weekly``
    Understat, over plain HTTP. This is what the scheduled job runs every
    Tuesday. No browser, no Chrome version to drift, nothing to break at 3am.

Both write to ``data/raw/`` and both are idempotent: a file that already exists
is left alone unless ``--force`` is passed. That matters more than it sounds —
it means you can re-run either command without corrupting the archive you are
relying on being immutable.
"""

from __future__ import annotations

import argparse
import logging
import sys
from datetime import date
from pathlib import Path

import pandas as pd

LOG = logging.getLogger("fetch")

REPO_ROOT = Path(__file__).resolve().parent.parent
RAW = REPO_ROOT / "data" / "raw"

BIG5 = [
    "ENG-Premier League",
    "ESP-La Liga",
    "ITA-Serie A",
    "GER-Bundesliga",
    "FRA-Ligue 1",
]

# Maresca's Leicester promotion season is in the Championship, and it is one of
# the three independent readings of his system. Without it the system profile
# rests on Chelsea alone.
MARESCA_EXTRA = ["ENG-Championship"]

FBREF_STAT_TYPES = [
    "standard",
    "passing",
    "passing_types",
    "defense",
    "possession",
    "playing_time",
    "misc",
]


def _rel(path: Path) -> str:
    """Path relative to the repo root, for logging.

    Falls back to the absolute path rather than raising: a logging call must
    never be the thing that kills a twenty-minute pull.
    """
    try:
        return str(path.relative_to(REPO_ROOT))
    except ValueError:
        return str(path)


def _write(df: pd.DataFrame, path: Path, force: bool = False) -> bool:
    """Write a dataframe to parquet. Returns True if written, False if skipped.

    The index is reset into columns first. Understat and FBref both return
    multi-indexed frames, and an index that is not materialised as data is an
    index you have lost by the time you re-read the archive in January.
    """
    if path.exists() and not force:
        LOG.info("skip (exists): %s", _rel(path))
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    df.reset_index().to_parquet(path, index=False)
    LOG.info("wrote %-58s %6d rows", _rel(path), len(df))
    return True


def fetch_historical(seasons: list[str], force: bool = False) -> None:
    """Bulk FBref pull. Local only — needs Chrome."""
    import soccerdata as sd

    leagues = BIG5 + MARESCA_EXTRA
    out = RAW / "fbref"

    for season in seasons:
        for league in leagues:
            # Championship only matters for the season Maresca was there.
            if league == "ENG-Championship" and season != "2324":
                continue

            slug = league.split("-")[0].lower()
            try:
                fb = sd.FBref(leagues=league, seasons=season)
            except Exception as exc:  # noqa: BLE001
                LOG.error("could not open FBref for %s %s: %s", league, season, exc)
                LOG.error("FBref needs a working Chrome. This command is local-only.")
                raise

            for stat in FBREF_STAT_TYPES:
                path = out / season / f"{slug}_player_{stat}.parquet"
                if path.exists() and not force:
                    LOG.info("skip (exists): %s", _rel(path))
                    continue
                try:
                    df = fb.read_player_season_stats(stat_type=stat)
                except Exception as exc:  # noqa: BLE001
                    # One missing stat type in one league-season should not kill
                    # a pull that takes twenty minutes.
                    LOG.warning("failed %s %s %s: %s", league, season, stat, exc)
                    continue
                _write(df, path, force=force)

            # Team-level style vectors — possession share, pressures, etc.
            path = out / season / f"{slug}_team_standard.parquet"
            if not path.exists() or force:
                try:
                    _write(fb.read_team_season_stats(stat_type="standard"), path, force)
                except Exception as exc:  # noqa: BLE001
                    LOG.warning("failed team stats %s %s: %s", league, season, exc)


def fetch_weekly(season: str, force: bool = False) -> None:
    """Understat pull — per-match player data with xG. Safe in CI."""
    import soccerdata as sd

    stamp = date.today().isoformat()
    out = RAW / "weekly" / stamp
    us = sd.Understat(leagues="ENG-Premier League", seasons=season)

    wrote = 0
    wrote += _write(us.read_schedule(), out / "schedule.parquet", force)

    # read_player_match_stats is the spine of the whole study: one row per
    # player per match is what the tracking model consumes. Everything else
    # here is context around it.
    for name, call in [
        ("player_match", us.read_player_match_stats),
        ("team_match", us.read_team_match_stats),
        ("player_season", us.read_player_season_stats),
        ("shots", us.read_shot_events),
    ]:
        try:
            wrote += _write(call(), out / f"{name}.parquet", force)
        except Exception as exc:  # noqa: BLE001
            LOG.warning("%s unavailable: %s", name, exc)

    if wrote == 0:
        # A silent no-op run is the failure mode that would actually hurt this
        # project — you would not notice until January, and the gap would be
        # unrecoverable. Exit non-zero so the Action goes red.
        LOG.error("nothing written — treat this as a failed run, not a quiet one")
        raise SystemExit(1)

    LOG.info("weekly pull complete: %s (%d files)", _rel(out), wrote)


def fetch_snapshot(season: str, force: bool = False) -> None:
    """Week 1 only: the frozen baseline, written to a dated folder.

    This is the one you cannot recreate later. Once more matchweeks are played,
    the season-to-date view of four matchweeks is gone for good.
    """
    import soccerdata as sd

    stamp = date.today().isoformat()
    out = RAW / f"snapshot_{stamp}"
    us = sd.Understat(leagues="ENG-Premier League", seasons=season)

    for name, call in [
        ("schedule", us.read_schedule),
        ("player_match", us.read_player_match_stats),
        ("team_match", us.read_team_match_stats),
        ("player_season", us.read_player_season_stats),
        ("shots", us.read_shot_events),
    ]:
        try:
            _write(call(), out / f"{name}.parquet", force)
        except Exception as exc:  # noqa: BLE001
            LOG.warning("%s unavailable: %s", name, exc)

    LOG.info("snapshot frozen at %s — commit this and do not regenerate it", out.name)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="python -m src.fetch", description=__doc__)
    parser.add_argument("-v", "--verbose", action="store_true")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_hist = sub.add_parser("historical", help="FBref bulk pull (local, needs Chrome)")
    p_hist.add_argument("--seasons", nargs="+", default=["2223", "2324", "2425", "2526"])
    p_hist.add_argument("--force", action="store_true")

    p_week = sub.add_parser("weekly", help="Understat pull (CI-safe)")
    p_week.add_argument("--season", default="2526")
    p_week.add_argument("--force", action="store_true")

    p_snap = sub.add_parser("snapshot", help="week 1 frozen baseline")
    p_snap.add_argument("--season", default="2526")
    p_snap.add_argument("--force", action="store_true")

    args = parser.parse_args(argv)
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(levelname)-7s %(message)s",
    )

    if args.cmd == "historical":
        fetch_historical(args.seasons, args.force)
    elif args.cmd == "weekly":
        fetch_weekly(args.season, args.force)
    elif args.cmd == "snapshot":
        fetch_snapshot(args.season, args.force)
    return 0


if __name__ == "__main__":
    sys.exit(main())
