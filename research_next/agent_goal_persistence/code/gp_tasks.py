"""GARDEN tasks and prompts (rules in ../GARDEN.md). Six rule pairs: every item has two binary features F1 and F2.
Rule "F1" labels an item X if F1 is true, else Y; rule "F2" the same with F2. Ambiguous items (F1 == F2) get the same
label under both rules (zero evidence between them); diagnostic items (F1 != F2) are labelled by the target rule B;
queries are conflict items (F1 != F2), where the two rules give different labels.
make_prompts() builds every prompt deterministically from a seed, identically for every model.
"""
import hashlib
import json
import random

LABELS = (" dax", " wug")   # nonce labels; the readout is each label's first token after "Label:"


def _numbers():
    return [(str(n), n % 2 == 0, n > 50) for n in range(1, 100)]            # F1 even, F2 greater than 50


ANIMALS = "dog cat horse rabbit tiger lion bear wolf mouse snake eagle duck goat sheep frog camel zebra monkey otter " \
          "fox deer whale shark parrot pigeon".split()
OBJECTS = "chair table lamp book cup spoon window door pencil bottle shoe clock candle basket mirror pillow hammer " \
          "wallet button jacket kettle ladder rocket carpet blanket".split()


def _animal_plural():
    out = []
    for w in ANIMALS:
        pl = {"mouse": "mice", "sheep": "sheep", "fox": "foxes", "deer": "deer", "wolf": "wolves"}.get(w, w + "s")
        if pl == w:
            continue
        out += [(w, True, False), (pl, True, True)]
    for w in OBJECTS:
        pl = {"shoe": "shoes", "candle": "candles"}.get(w, w + "s")
        out += [(w, False, False), (pl, False, True)]
    return out                                                              # F1 animal, F2 plural


FOOD_V = "apple apricot avocado almond egg eggplant olive onion orange oat oyster artichoke asparagus endive udon " \
         "edamame anchovy omelette okra icecream".split()
FOOD_C = "bread cheese banana carrot potato tomato pasta rice butter cherry grape lemon mango peach pizza salad " \
         "sausage steak noodle cookie pancake waffle muffin yogurt walnut".split()
THING_V = "anchor elbow engine island igloo ink oven owl umbrella uniform envelope elevator arrow axe iron ocean " \
          "eagle antenna ankle easel".split()
THING_C = "table house chair rope desk ladder hammer pillow window pencil carpet bottle candle basket mirror " \
          "wallet button jacket rocket kettle blanket cable bucket fence tunnel".split()


def _vowel_food():
    return ([(w, True, True) for w in FOOD_V] + [(w, False, True) for w in FOOD_C] +
            [(w, True, False) for w in THING_V] + [(w, False, False) for w in THING_C])   # F1 starts with a vowel, F2 food


POS = "great wonderful lovely excellent superb delightful fantastic pleasant".split()
NEG = "awful terrible horrible dreadful disgusting miserable unpleasant poor".split()
FOODN = "soup bread pasta cake salad pizza curry stew pie sandwich".split()
PLACEN = "museum beach hotel park station library airport garden theater market".split()


def _sentiment_food():
    out = []
    for a in POS + NEG:
        for n in FOODN + PLACEN:
            out.append((f"The {n} was {a}.", a in POS, n in FOODN))         # F1 positive, F2 about food
    return out


COUNTRIES = "france spain italy germany japan china brazil canada mexico egypt kenya peru chile norway sweden " \
            "poland greece turkey india vietnam".split()
CITIES = "paris madrid rome berlin tokyo beijing lisbon toronto london cairo nairobi lima santiago oslo stockholm " \
         "warsaw athens istanbul mumbai hanoi".split()


def _country_caps():
    out = []
    for w in COUNTRIES:
        out += [(w.capitalize(), True, False), (w.upper(), True, True)]
    for w in CITIES:
        out += [(w.capitalize(), False, False), (w.upper(), False, True)]
    return out                                                              # F1 country, F2 written in capitals


COL_S = "red blue pink gold teal gray navy rose jade lime plum rust ruby sand wine".split()
COL_L = "purple orange yellow violet maroon indigo scarlet crimson magenta turquoise lavender silver bronze " \
        "emerald amber".split()
OBJ_S = "cat door lamp rope desk fish book cup hat bike coin fork kite nail ship".split()
OBJ_L = "window pencil carpet bottle ladder rocket candle basket mirror pillow hammer wallet button jacket kettle".split()


def _color_short():
    return ([(w, True, True) for w in COL_S] + [(w, True, False) for w in COL_L] +
            [(w, False, True) for w in OBJ_S] + [(w, False, False) for w in OBJ_L])   # F1 colour word, F2 at most 4 letters


TASKS = {"num_even_gt50": _numbers(), "animal_plural": _animal_plural(), "vowel_food": _vowel_food(),
         "sentiment_food": _sentiment_food(), "country_caps": _country_caps(), "color_short": _color_short()}
FILLER_FROM = {"num_even_gt50": "color_short", "animal_plural": "country_caps", "vowel_food": "sentiment_food",
               "sentiment_food": "vowel_food", "country_caps": "animal_plural", "color_short": "num_even_gt50"}

# cells: (name, n_ambiguous_including_4_anchors, m_diagnostic, order, filler_count)
CELLS = [("calib", 16, 0, "shuffle", 0)]
CELLS += [(f"base_m{m}", 4, m, "shuffle", 0) for m in (1, 2, 4, 8, 16, 32, 64)]
for rho, rn in ((8, "1/8"), (4, "1/4"), (2, "1/2")):
    for k in (8, 16, 32, 64, 128):
        CELLS.append((f"share{rho}_k{k}", k - k // rho, k // rho, "shuffle", 0))
for n in (4, 16, 64):
    for m in (2, 4, 8):
        for pos in ("last", "first"):
            CELLS.append((f"gp_n{n}_m{m}_{pos}", n, m, pos, 0))
for f in (12, 60):
    CELLS.append((f"filler{f}_m4_last", 4, 4, "last", f))


def _fmt(item, label):
    return f"Input: {item}\nLabel:{label}\n"


def make_prompts(draws=20, seed=4400):
    """Yields dicts, one per prompt. Counterbalanced over target rule B (F1 or F2) and label map (X = feature true or
    false). Ambiguous items are balanced (half F1=F2=True, half both False); diagnostics balanced over the two kinds;
    the query is a conflict item not used in the prompt."""
    rng = random.Random(seed)
    for task, items in TASKS.items():
        amb = [it for it in items if it[1] == it[2]]
        con = [it for it in items if it[1] != it[2]]
        fill = TASKS[FILLER_FROM[task]]
        for bfeat in (1, 2):
            for lmap in (0, 1):
                lab = lambda truth: LABELS[0] if truth == (lmap == 0) else LABELS[1]   # label for a feature value
                for cell, n, m, order, nfill in CELLS:
                    for d in range(draws):
                        q = rng.choice(con)
                        pool_amb = [it for it in amb if it[0] != q[0]]
                        pool_con = [it for it in con if it[0] != q[0]]
                        ambs = [x for i in range(n) for x in [rng.choice([a for a in pool_amb if a[1] == (i % 2 == 0)])]]
                        diags = [x for i in range(m) for x in
                                 [rng.choice([c for c in pool_con if c[bfeat] == (i % 2 == 0)])]]
                        ex_amb = [_fmt(a[0], lab(a[1])) for a in ambs]          # F1 == F2, so either feature
                        ex_diag = [_fmt(c[0], lab(c[bfeat])) for c in diags]
                        ex_fill = [_fmt(f[0], LABELS[i % 2]) for i, f in enumerate(rng.sample(fill, min(nfill, len(fill))))]
                        while len(ex_fill) < nfill:
                            ex_fill.append(_fmt(rng.choice(fill)[0], LABELS[len(ex_fill) % 2]))
                        anchors, rest = ex_amb[:4], ex_amb[4:] + ex_fill
                        rng.shuffle(anchors), rng.shuffle(rest), rng.shuffle(ex_diag)
                        if order == "shuffle":
                            body = anchors + rest + ex_diag
                            rng.shuffle(body)
                        elif order == "last":
                            body = anchors + rest + ex_diag
                        else:
                            body = ex_diag + anchors + rest
                        prompt = "".join(body) + f"Input: {q[0]}\nLabel:"
                        yield {"task": task, "bfeat": bfeat, "lmap": lmap, "cell": cell, "n": n, "m": m, "order": order,
                               "nfill": nfill, "draw": d, "query": q[0], "label_B": lab(q[bfeat]),
                               "label_A": lab(q[3 - bfeat]), "prompt": prompt}


def prompts_hash(draws=20, seed=4400):
    h = hashlib.sha256()
    n = 0
    for p in make_prompts(draws, seed):
        h.update(json.dumps(p, sort_keys=True).encode())
        n += 1
    return h.hexdigest(), n


if __name__ == "__main__":
    print(prompts_hash())
