# Pre-registration

**Written:** 2026-09-15  ·  **Matchweek at time of writing:** 5  ·  **Author:** Marcus Riddick Andriano

This file is written before any modelling and is **never edited after it is committed**. If a
prediction here turns out badly wrong, that is the result, not an embarrassment. In week 15 the
model gets graded against these numbers, and so do the confident takes published in September.

Git history is the timestamp. If you change your mind later, add a new dated section at the
bottom — do not touch what is above it.

> **This is an informed prior, not a blind guess.** You are allowed — encouraged — to look up what
> these three players did *before* they signed for City: Fernández at Chelsea, Anderson at Forest,
> Bouaddi at Lille. That is exactly the evidence the week-9 model will use. The holdout forbids one
> thing and one thing only: looking at their **Manchester City 2026–27 rows**. Run
> `python -m src.baseline` to pull their pre-City seasons and calibrate against real numbers.

---

## 1. What I believe right now, in words

Two or three sentences, no hedging. What do you actually think about this rebuild, before you have run a single line of analysis?

> The risk isn't talent, it's that a new coach and an entirely new roster have zero shared history, so chemistry and identity will lag the talent level for a while no matter how good the individual pieces are. The team that "figures out who they are" fastest usually outperforms the one that's just more talented on paper.

---

## 2. Numeric predictions

Per 90, Premier League only, as of the final matchweek before 17 January 2027. Give a point
estimate and a range you would be genuinely surprised to fall outside.

Leave a row blank rather than guessing at something you have no view on — a blank is honest, a
made-up number pollutes the comparison.

The source column matters: **Understat** metrics are tracked automatically every week, **FBref**
metrics come from the manual monthly pull. Both get checked in week 10.

### Enzo Fernández

| Metric | Source | Low | Point estimate | High |
| --- | --- | --- | --- | --- |
| Minutes played (total, PL) | Understat |2,500|2,950|3,300|
| xGChain / 90 | Understat |0.55|0.72|0.90|
| xGBuildup / 90 | Understat |0.45|0.64|0.80|
| Key passes / 90 | Understat |0.75|0.97|1.15|
| xG + xA / 90 | Understat |0.30|0.40|0.52|
| Progressive passes / 90 | FBref |6.2|7.3|8.4|
| Pass completion % | FBref |84.5%|88.0%|89.0%|
| Tackles + interceptions / 90 | FBref |2.8|3.5|4.2|

### Elliot Anderson

| Metric | Source | Low | Point estimate | High |
| --- | --- | --- | --- | --- |
| Minutes played (total, PL) | Understat |2,400|2,750|3,150|
| xGChain / 90 | Understat |0.35|0.48|0.65|
| xGBuildup / 90 | Understat |0.27|0.38|0.52|
| Key passes / 90 | Understat |0.75|1.05|1.35|
| xG + xA / 90 | Understat |0.22|0.31|0.42|
| Progressive passes / 90 | FBref |7.5|8.8|10.0|
| Pass completion % | FBref |83.0%|86%|88.5%|
| Tackles + interceptions / 90 | FBref |4.0|5.0|6.0|

### Ayyoub Bouaddi

| Metric | Source | Low | Point estimate | High |
| --- | --- | --- | --- | --- |
| Minutes played (total, PL) | Understat |1,000|1,650|2,300|
| xGChain / 90 | Understat |0.25|0.38|0.52|
| xGBuildup / 90 | Understat |0.20|0.31|0.44|
| Key passes / 90 | Understat |0.45|0.70|0.95|
| xG + xA / 90 | Understat |0.12|0.19|0.28|
| Progressive passes / 90 | FBref |3.0|4.0|5.0|
| Pass completion % | FBref |87.0%|90.0%|91.5%|
| Tackles + interceptions / 90 | FBref |3.0|4.0|5.0|

**Note on xGBuildup.** It measures involvement in possessions that end in a shot, *excluding* the
shot and the final pass — so it captures deep build-up contribution specifically. That is close to
the job Maresca asks of his pivot, and it may end up the most informative metric here for Anderson
and Bouaddi. Worth thinking hardest about this row.

---

## 3. Structural predictions

Yes / no / don't know. Cheap to write, surprisingly hard to get right.

- [No] Anderson plays more minutes in the deeper of the two pivot roles than Fernández does.
- [No] Bouaddi starts fewer than 10 Premier League matches before 17 January.
- [Yes] City's possession share is higher under Maresca than in Guardiola's final season.
- [Yes] At least one of the three is being openly questioned in the press by January.
- [Yes] City are top of the league on 17 January 2027.

---

## 4. What would change my mind

Name in advance what evidence would make you conclude the rebuild is **not** working. Deciding this
now is the single thing that stops you rationalising whatever happens.

> Maresca's rebuild requires a sustained improvement in underlying possession/control and chance-creation metrics. If that is not shown and the Fernández–Anderson–Bouaddi midfield still lacks stable complementary roles, I will regard the rebuild as not working regardless of league position or trophies won this season. 

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
- **Data sources are fixed:** Understat weekly (automated), FBref monthly (manual). No metric
  enters the analysis that cannot be measured by one of them.
- **The verdict is scoped to what the stabilisation table supports.** If a metric has not
  stabilised by January, no claim is made about it. "Not enough games yet" is a permitted and
  expected conclusion.
