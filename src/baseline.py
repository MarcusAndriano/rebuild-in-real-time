"""Pre-City baselines for the three signings — calibration for the pre-registration.

This is deliberately allowed under the holdout. The prior is supposed to be
built from what these players did BEFORE they signed; the only thing sealed is
their Manchester City 2026-27 rows. So: Fernández at Chelsea, Anderson at
Forest, Bouaddi at Lille.

    python -m src.baseline

Prints per-90 numbers for each, so the pre-registration is an informed prior
rather than a guess at an unfamiliar scale.

If a name does not match, pass --search to see what the source actually calls
them — accents and spellings vary between sources, which is itself a data
problem you will have to solve properly in week 4.
"""

from __future__ import annotations

import argparse
import logging
import warnings

import pandas as pd

LOG = logging.getLogger("baseline")

# league, season, and the substring to match on. Seasons before the City move.
SUBJECTS = [
    ("Enzo Fernández", "ENG-Premier League", "2526", "Chelsea"),
    ("Enzo Fernández", "ENG-Premier League", "2425", "Chelsea"),
    ("Elliot Anderson", "ENG-Premier League", "2526", "Nottingham Forest"),
    ("Elliot Anderson", "ENG-Premier League", "2425", "Nottingham Forest"),
    ("Bouaddi", "FRA-Ligue 1", "2526", "Lille"),
    ("Bouaddi", "FRA-Ligue 1", "2425", "Lille"),
]

# Understat per-season columns we care about, and whether to show them per 90.
PER90 = ["xg", "xa", "xg_chain", "xg_buildup", "key_passes", "shots"]


def _load(league: str, season: str) -> pd.DataFrame:
    import soccerdata as sd

    us = sd.Understat(leagues=league, seasons=season)
    return us.read_player_season_stats().reset_index()


def _per90(row: pd.Series) -> dict:
    mins = row.get("minutes", 0) or 0
    out = {"minutes": int(mins), "games": int(row.get("games", 0) or 0)}
    if mins < 1:
        return out
    for col in PER90:
        if col in row and pd.notna(row[col]):
            out[f"{col}/90"] = round(float(row[col]) * 90.0 / mins, 3)
    return out


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="python -m src.baseline", description=__doc__)
    parser.add_argument("--search", help="print every player name containing this string")
    parser.add_argument("--league", default="ENG-Premier League")
    parser.add_argument("--season", default="2526")
    args = parser.parse_args(argv)

    logging.basicConfig(level=logging.INFO, format="%(levelname)-7s %(message)s")
    warnings.filterwarnings("ignore")

    if args.search:
        df = _load(args.league, args.season)
        name_col = "player" if "player" in df.columns else df.columns[0]
        hits = df[df[name_col].astype(str).str.contains(args.search, case=False, na=False)]
        if hits.empty:
            print(f"no name in {args.league} {args.season} contains {args.search!r}")
        else:
            print(hits[[name_col, "team", "minutes"]].to_string(index=False))
        return 0

    cache: dict[tuple[str, str], pd.DataFrame] = {}

    for name, league, season, club in SUBJECTS:
        key = (league, season)
        if key not in cache:
            try:
                cache[key] = _load(league, season)
            except Exception as exc:  # noqa: BLE001
                LOG.warning("could not load %s %s: %s", league, season, exc)
                cache[key] = pd.DataFrame()
        df = cache[key]
        if df.empty:
            continue

        name_col = "player" if "player" in df.columns else df.columns[0]
        hits = df[df[name_col].astype(str).str.contains(name.split()[-1], case=False, na=False)]

        print(f"\n=== {name} — {club}, {season} ({league}) ===")
        if hits.empty:
            print("  not found. try:  python -m src.baseline --search "
                  f"{name.split()[-1]} --league '{league}' --season {season}")
            continue
        for _, row in hits.iterrows():
            stats = _per90(row)
            print(f"  {row[name_col]} ({row.get('team', '?')})")
            for k, v in stats.items():
                print(f"      {k:<18} {v}")

    print(
        "\nUse these to set the scale for your pre-registration. They are what the "
        "\nplayers did before City — which is exactly what the week-9 prior is built "
        "\nfrom, so looking at them now is allowed and intended."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
