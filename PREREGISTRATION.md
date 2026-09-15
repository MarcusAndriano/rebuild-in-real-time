# Pre-registration

**Written:** 2026-09-__  ·  **Matchweek at time of writing:** __  ·  **Author:** Marcus Riddick-Andriano

This file is written before any modelling and is **never edited after it is committed**. If a
prediction here turns out badly wrong, that is the result, not an embarrassment. In week 15 the
model gets graded against these numbers, and so do the confident takes published in September.

Git history is the timestamp. If you change your mind later, add a new dated section at the
bottom — do not touch what is above it.

---

## 1. What I believe right now, in words

Two or three sentences, no hedging. What do you actually think about this rebuild, before you have
run a single line of analysis?

> _(write it here)_

---

## 2. Numeric predictions

Fill in a point estimate and a range you would be genuinely surprised to fall outside. Per 90,
Premier League only, as of the final matchweek before 17 January 2027.

Leave a row blank rather than guessing at something you have no view on — a blank is honest, a
made-up number pollutes the comparison.

### Enzo Fernández

| Metric | Low | Point estimate | High |
| --- | --- | --- | --- |
| Minutes played (total, PL) | | | |
| Progressive passes / 90 | | | |
| Shot-creating actions / 90 | | | |
| xG + xA / 90 | | | |
| Pass completion % | | | |
| Tackles + interceptions / 90 | | | |

### Elliot Anderson

| Metric | Low | Point estimate | High |
| --- | --- | --- | --- |
| Minutes played (total, PL) | | | |
| Progressive passes / 90 | | | |
| Shot-creating actions / 90 | | | |
| xG + xA / 90 | | | |
| Pass completion % | | | |
| Tackles + interceptions / 90 | | | |

### Ayyoub Bouaddi

| Metric | Low | Point estimate | High |
| --- | --- | --- | --- |
| Minutes played (total, PL) | | | |
| Progressive passes / 90 | | | |
| Shot-creating actions / 90 | | | |
| xG + xA / 90 | | | |
| Pass completion % | | | |
| Tackles + interceptions / 90 | | | |

---

## 3. Structural predictions

Yes / no / don't know. These are cheap to write and surprisingly hard to get right.

- [ ] Anderson plays more minutes in the deeper of the two pivot roles than Fernández does.
- [ ] Bouaddi starts fewer than 10 Premier League matches before 17 January.
- [ ] City's possession share is higher under Maresca than in Guardiola's final season.
- [ ] At least one of the three is being openly questioned in the press by January.
- [ ] City are top of the league on 17 January 2027.

---

## 4. What would change my mind

Name in advance what evidence would make you conclude the rebuild is **not** working. Deciding this
now is the single thing that stops you rationalising whatever happens.

> _(write it here)_

---

## 5. Declared conflicts

State them plainly. They do not undermine the study; concealing them would.

- I support Manchester City. I will watch most of these matches as a fan before I ever see the
  data, and I cannot un-see them.
- The holdout discipline is therefore procedural, not psychological: City's 2026–27 rows stay out
  of every notebook until week 10, and this file is the record of what I thought beforehand.

---

## 6. Method commitments

Locked now so they cannot be chosen later to suit a result.

- **Metric list** for role discovery: committed separately in `docs/metric_list.md` by week 7,
  before any clustering is run.
- **Population:** Big 5 league midfielders, four seasons, minimum 450 minutes in a season.
- **Adjustments applied before any comparison:** per-90, possession adjustment for defensive
  actions, opponent strength, game state, and minutes played a man up or down.
- **Primary outcome:** per-metric stabilisation point — matches required before split-half
  reliability exceeds 0.70.
- **The verdict is scoped to what the stabilisation table supports.** If a metric has not
  stabilised by January, no claim is made about it. "Not enough games yet" is a permitted and
  expected conclusion.
