# Rebuild in Real Time

**Manchester City's midfield, 2026–27 — an in-season evidence study.**

In one transfer window Manchester City sold Rodri to Barcelona and signed three central midfielders
to replace him — Enzo Fernández, Elliot Anderson and Ayyoub Bouaddi — under a new manager, Enzo
Maresca, whose system does not use the single pivot the squad was built around. Four league games
later the verdict was already being written.

**This project does not argue with that verdict. It asks how much football has to be played before
anyone can responsibly reach it.** A prediction is locked before any 2026–27 City data is examined,
the season is then tracked matchweek by matchweek, and the study ends with a general result: for
each performance metric, how many matches of evidence are needed before signal exceeds noise.

---

## The design

The integrity of the whole thing rests on a holdout. In order:

| Step | When | What |
| --- | --- | --- |
| **Freeze** | Week 1 | Snapshot the season to date. Write unmodelled predictions in [`PREREGISTRATION.md`](PREREGISTRATION.md). Commit, never edit. |
| **Predict blind** | Week 9 | Build the prior from **pre-City data only** — Forest, Chelsea, Lille, and Maresca's own teams. City's 2026–27 rows stay sealed. |
| **Reveal** | Week 10 | Unseal. Compare predicted against observed, context-adjusted. |
| **Update** | Week 12 | Bayesian updating matchweek by matchweek; watch the credible intervals contract. |
| **Answer** | Week 14 | Split-half reliability across the full population: how many matches each metric needs. |

Because the prior uses only pre-City data, it does not matter that the season was already underway
when the study began. The holdout does the work the calendar cannot.

---

## A note on transfer fees

Reported fees for the three signings total roughly £327m, but that figure is an upper bound rather
than a fact: Bouaddi's reported £86m is £81.3m fixed plus £4.3m in conditional add-ons that may
never be paid, clubs do not publish fees, outlets disagree with each other, and the amortised
accounting figure differs from the headline again.

Fees are therefore cited with that caveat and never load-bearing. Every claim this study makes
rests on structural facts instead — one pivot left, three midfielders arrived, the manager changed,
and the shape went from a single pivot to a double pivot with two eights. Those hold whatever the
accounts eventually say. See `data/transfers_2026.csv` for each fee with its primary source.

---

## Data architecture

The two sources are deliberately split by how fragile they are.

**FBref — historical bulk, pulled once, committed.** `soccerdata`'s FBref reader is a
`BaseSeleniumReader`: it drives an undetected Chrome instance and ships a `solve_captcha()` method,
because FBref sits behind bot protection. That is fine for a one-off local pull of four seasons
across the Big 5 leagues plus the Championship. It is a poor thing to depend on every Tuesday.

**Understat — the weekly tracking spine.** `Understat`, `ClubElo`, `Sofascore` and `ESPN` are
`BaseRequestsReader`s: plain HTTP, no browser. Understat carries per-match player data with xG,
which is what the tracking model actually consumes. This is what the scheduled job pulls.

The consequence: **the automated weekly job never touches the browser-dependent source.** If FBref
changes or breaks in December, the historical cache is already committed and the weekly spine is
unaffected.

> **Known snag.** `soccerdata`'s HTTP layer uses `tls_requests`, which downloads a native TLS
> library from GitHub on first run. In locked-down environments that download can fail with
> `OSError: Failed to download the required TLS library`. Warm the cache on a machine with open
> egress, or vendor the library into the CI image.

---

## Layout

```
src/
  fetch.py         # historical (FBref, local) and weekly (Understat, CI) pulls
  features.py      # per-90, possession, league strength, game state, red cards
  roles.py         # PCA + clustering → role taxonomy
  track.py         # prior → posterior updating
data/
  raw/             # committed. snapshot_YYYY-MM-DD/ and weekly/
  db/              # SQLite, built from raw
notebooks/         # exploration only — nothing load-bearing lives here
reports/figures/   # every figure generated from code, never by hand
tests/
```

## Running it

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# week 1 only — the frozen baseline, which cannot be recreated later
python -m src.fetch snapshot --season 2526

# one-off, local, needs Chrome — four seasons of Big 5 + Championship
python -m src.fetch historical --seasons 2223 2324 2425 2526

# the weekly spine — no browser, safe in CI
python -m src.fetch weekly --season 2526

python -m pytest tests/ -q
```

## Status

Week 1 of 18. The charter and schedule are tracked separately; this repo is the work itself.

## Sources

Data via [soccerdata](https://github.com/probberechts/soccerdata) (FBref, Understat, Club Elo).
