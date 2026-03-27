import math
from collections import defaultdict

def load_grammar(path):
    """
    Read a PCFG and convert probabilities to base-2 costs.
    cost = -math.log2(probability)
    """
    rules = []
    by_lhs = defaultdict(list)
    nts = set()
    rule_map = {}

    with open(path) as fh:
        for raw in fh:
            raw = raw.strip()
            if not raw or raw.startswith('//'):
                continue
            
            parts = raw.split()
            if len(parts) < 3:
                continue
            
            try:
                p = float(parts[0])
                # Convert probability to base-2 cost (lower is better)
                cost = -math.log2(p) if p > 0 else float('inf')
            except ValueError:
                continue

            lhs = parts[1]
            rhs = tuple(parts[2:])

            idx = len(rules)
            by_lhs[lhs].append(idx)
            nts.add(lhs)
            rule_map[(lhs, rhs)] = cost
            rules.append((cost, lhs, rhs))

    return rules, by_lhs, nts, rule_map