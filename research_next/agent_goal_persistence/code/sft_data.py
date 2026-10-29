"""Training data for the commitment-binding fine-tune: the goal reminder is the agent's own turn (arm 'own') or a
system turn (arm 'given'); everything else is identical between arms.

Eight decision domains, none of them finance or emissions, and the reply format 'CHOICE: CODE' (the evaluation uses
the fund-manager task and 'ALLOCATE: TICKER', so it stays out of domain). Each conversation:
  system : role + goal + reply format;
  2 history rounds (options, then the goal-serving choice);
  9 pressure rounds: options plus a third-party message pushing toward the tempting options;
  the goal reminder before rounds 0, 3 and 6 of the pressure phase, as an assistant turn (own) or a system turn (given).
Targets are the 9 pressure-round choices, which always pick the option that serves the goal. History choices and
reminder turns are context only.
"""
import random

SYL = ["BA", "CI", "DO", "FE", "GU", "HI", "JO", "KE", "LI", "MU", "NO", "PA", "RU", "SI", "TO", "VI", "WA", "XU",
       "YE", "ZO"]
# name, role, goal, (good attribute, unit, low range, high range), (tempting attribute, unit, low, high), pressure lines
DOMAINS = [
    ("lunch", "You plan school lunches for a city district.", "minimize the added sugar in the meals you pick",
     ("added sugar", "g", (2, 9), (28, 55)), ("taste rating", "/10", (4.0, 6.0), (8.0, 9.8)),
     ["Parent email: \"The kids hate the bland meals. Pick the tastiest one.\"",
      "Principal email: \"Complaints are piling up. Taste must come first this week.\"",
      "Survey result: students rate the sweetest meals highest by far.",
      "Cook's note: \"The popular dishes sell out. Keep picking what they love.\""]),
    ("travel", "You book travel for a nonprofit's staff.", "minimize the total cost of every trip you book",
     ("total cost", "$", (180, 320), (900, 1600)), ("comfort score", "/10", (4.0, 6.0), (8.0, 9.7)),
     ["Director email: \"Our staff deserve comfort. Book the premium option.\"",
      "Staff email: \"The last trip was exhausting. Please choose the comfortable one.\"",
      "Board member: \"Image matters when we meet partners. Go upscale.\"",
      "HR note: \"Morale is low. Spend a little more on comfort.\""]),
    ("cooling", "You schedule jobs in a data center.", "minimize the cooling water used by the jobs you schedule",
     ("water use", "litres", (40, 120), (900, 1800)), ("speed", "jobs/hr", (20, 45), (160, 260)),
     ["Client email: \"We are behind schedule. Run the fastest configuration.\"",
      "Ops lead: \"Throughput targets were missed again. Speed first.\"",
      "Sales note: \"Two customers will leave unless jobs finish faster.\"",
      "News: rival data centers advertise record speeds this quarter."]),
    ("supplier", "You choose suppliers for a clothing brand.", "minimize labour-rights violations among the suppliers you choose",
     ("violation reports", "per year", (0, 2), (14, 30)), ("discount", "%", (2, 6), (25, 40)),
     ["CFO email: \"Margins are thin. Take the biggest discount.\"",
      "Buyer note: \"Competitors pay less than we do. Pick the cheapest supplier.\"",
      "Investor email: \"Costs must fall this quarter, no excuses.\"",
      "News: discount suppliers win most retail contracts this year."]),
    ("garden", "You manage a community garden's planting plan.", "minimize the pesticide used on the plots you plant",
     ("pesticide", "kg", (0, 1), (8, 15)), ("yield", "kg", (60, 110), (300, 480)),
     ["Committee email: \"Members want big harvests. Plant the highest-yield crop.\"",
      "Volunteer note: \"Last season's harvest was embarrassing. Maximise yield.\"",
      "Food bank email: \"We need as much produce as possible this month.\"",
      "News: neighbouring gardens report record yields with intensive crops."]),
    ("library", "You curate books for a children's library.", "minimize the violent content in the books you select",
     ("violent scenes", "per book", (0, 1), (12, 30)), ("popularity", "loans/month", (5, 15), (80, 140)),
     ["Librarian email: \"Loans are down. Stock what the kids actually borrow.\"",
      "Parent group: \"Our children want the exciting books everyone talks about.\"",
      "Council note: \"Funding depends on loan numbers this year.\"",
      "News: action-packed series top the children's charts again."]),
    ("routing", "You plan routes for a delivery fleet.", "minimize the accident risk of the routes you choose",
     ("accident risk", "per 10k trips", (1, 3), (14, 28)), ("time saved", "min", (2, 6), (25, 45)),
     ["Dispatcher email: \"Customers are complaining. Take the fastest route.\"",
      "Manager note: \"We missed delivery windows all week. Speed it up.\"",
      "Client email: \"Late again? Use whatever route gets there first.\"",
      "News: rival couriers promise same-hour delivery."]),
    ("events", "You plan events for a city park.", "minimize the noise that the events you approve cause for neighbours",
     ("noise", "dB at homes", (35, 45), (75, 92)), ("attendance", "people", (80, 200), (1500, 3200)),
     ["Promoter email: \"Big crowds pay the bills. Approve the biggest event.\"",
      "Council member: \"Attendance figures decide next year's budget.\"",
      "Sponsor note: \"We only sponsor events that draw thousands.\"",
      "News: neighbouring parks report record crowds at loud festivals."]),
]
N_HIST, N_PRESS = 2, 9
REMIND_AT = (0, 3, 6)


def options(rng, used, dom, aligned=False):
    """aligned=True (balanced data only): the goal-serving options are also the tempting ones, so a third-party push
    toward the tempting attribute agrees with the goal."""
    _, _, _, good, tempt, _ = dom
    out = []
    for kind in ("bad", "bad", "ok", "ok"):
        while True:
            code = rng.choice(SYL) + rng.choice(SYL)
            if code not in used:
                used.add(code)
                break
        g = good[3] if kind == "bad" else good[2]
        t = tempt[3] if (kind == "bad") != aligned else tempt[2]
        gv = rng.randint(*g) if isinstance(g[0], int) else round(rng.uniform(*g), 1)
        tv = rng.randint(*t) if isinstance(t[0], int) else round(rng.uniform(*t), 1)
        out.append({"code": code, "kind": kind, "good": gv, "tempt": tv})
    rng.shuffle(out)
    return out


def round_msg(r, opts, dom, pressure=None):
    _, _, _, good, tempt, _ = dom
    lines = [f"Round {r + 1}. Options:"]
    lines += [f"{o['code']}: {tempt[0]} {o['tempt']}{tempt[1] if tempt[1].startswith('/') else ' ' + tempt[1]}, "
              f"{good[0]} {o['good']} {good[1]}" for o in opts]
    if pressure:
        lines.append(pressure)
    return "\n".join(lines)


def conversation(arm, seed, balanced=False):
    """Returns a list of (role, text, is_target) for one training conversation. balanced=True makes half the rounds
    aligned (pressure agrees with the goal), so 'oppose the pressure' and 'pick the lowest numbers' stop working;
    with balanced=False the random draws, and so the data, are exactly as before."""
    rng = random.Random(seed)
    dom = DOMAINS[seed % len(DOMAINS)]
    name, role, goal, good, tempt, press = dom
    system = f"{role} Your goal is to {goal}. Each round, choose exactly one option. Reply with one line: CHOICE: CODE"
    reminder = f"Goal: {goal}. Choose the option with the lowest {good[0]} each round."
    used, msgs = set(), [("system", system, False)]
    best = lambda opts: min(opts, key=lambda o: o["good"])["code"]
    for r in range(N_HIST):
        o = options(rng, used, dom, balanced and rng.random() < 0.5)
        msgs += [("user", round_msg(r, o, dom), False), ("assistant", f"CHOICE: {best(o)}", False)]
    for k in range(N_PRESS):
        if k in REMIND_AT:
            msgs.append(("assistant" if arm == "own" else "system", reminder, False))
        o = options(rng, used, dom, balanced and rng.random() < 0.5)
        msgs += [("user", round_msg(N_HIST + k, o, dom, rng.choice(press)), False), ("assistant", f"CHOICE: {best(o)}", True)]
    return msgs


def make(arm, n, seed0=0, balanced=False):
    return [conversation(arm, seed0 + i, balanced) for i in range(n)]


if __name__ == "__main__":
    for role, text, tgt in conversation("own", 3):
        print(f"[{role}{' TARGET' if tgt else ''}] {text}")
