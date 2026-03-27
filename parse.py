"""
Probabilistic Earley Parser
Usage:  python parse.py grammar.gr sentences.sen

Outputs the exact format requested:
- Parse tree (Lisp-style S-expression)
- Log2 cost (negative log base 2)
- "NONE" if no parse is found
"""

import sys
from grammar import load_grammar
from earley import earley, all_trees, tree_cost, tree_to_str


def main():
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit("Error: expected exactly two arguments: grammar.gr sentences.sen")

    grammar_file = sys.argv[1]
    sentences_file = sys.argv[2]

    # Load PCFG
    rules, by_lhs, nts, rule_map = load_grammar(grammar_file)
    
    # Auto-detect root symbol
    start_sym = 'ROOT' if 'ROOT' in by_lhs else ('S' if 'S' in by_lhs else list(by_lhs.keys())[0])

    # Read sentences
    with open(sentences_file) as fh:
        sentences = [line.split() for line in fh if line.strip()]

    # Parse and Output
    for words in sentences:
        chart = earley(words, rules, by_lhs, nts, start=start_sym)
        n = len(words)

        # Look for completed start symbols covering the entire sentence
        complete_roots = [
            (ridx, len(rules[ridx][2]), 0)
            for ridx in by_lhs.get(start_sym, [])
            if (ridx, len(rules[ridx][2]), 0) in chart[n]
        ]

        if not complete_roots:
            print("NONE")
            continue

        valid_parses = []
        seen = set()

        # Enumerate trees
        for root_key in complete_roots:
            for tree in all_trees(root_key, n, chart, rules, words):
                ts = tree_to_str(tree)
                # Ensure no duplicates from alternative paths generating exact same structure
                if ts not in seen:
                    seen.add(ts)
                    tc = tree_cost(tree, rule_map)
                    valid_parses.append((tc, ts))
        
        # Sort by cost ascending (best trees first)
        valid_parses.sort(key=lambda x: x[0])

        # Print outputs
        for cost, ts in valid_parses:
            print(ts)
            print(cost)

if __name__ == '__main__':
    main()