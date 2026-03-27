# NLP Assignment Report: Probabilistic Earley Parser

<div align="center">
  <b>Author:</b> Jatin Agrawal &nbsp;|&nbsp; <b>Roll No:</b> 2023114014 <br>
  <b>GitHub Repository:</b> <a href="https://github.com/J10Official/Earley-Parser">Link to Code</a>
</div>

---

## 1. Earley Algorithm Execution Trace

**Context:** Simulating the Earley algorithm's behavior on the sentence *"time flies like an arrow"* using the baseline grammar.

### Final Parsing Chart & Abstract Syntax Trees
*Completed non-terminals are highlighted with an asterisk (`*`).*

```text
EARLEY CHART
========================================================================
-- Chart[0] (before reading any word) -----------------------
[0,0] S -> . NP VP
[0,0] NP -> . N
[0,0] NP -> . Det N
[0,0] NP -> . N N
[0,0] N -> . time
[0,0] N -> . flies
[0,0] N -> . arrow
[0,0] Det -> . a
[0,0] Det -> . an
-- Chart[1] (after reading 'time') --------------------------
* [0,1] N -> time .
* [0,1] NP -> N .
[0,1] NP -> N . N
[0,1] S -> NP . VP
[1,1] N -> . time
[1,1] N -> . flies
[1,1] N -> . arrow
[1,1] VP -> . V NP
[1,1] VP -> . V ADVP
[1,1] V -> . flies
[1,1] V -> . like
-- Chart[2] (after reading 'flies') -------------------------
* [1,2] N -> flies .
* [1,2] V -> flies .
* [0,2] NP -> N N .
[1,2] VP -> V . NP
[1,2] VP -> V . ADVP
[0,2] S -> NP . VP
[2,2] NP -> . N
[2,2] NP -> . Det N
[2,2] NP -> . N N
[2,2] ADVP -> . ADV NP
[2,2] VP -> . V NP
[2,2] VP -> . V ADVP
[2,2] N -> . time
[2,2] N -> . flies
[2,2] N -> . arrow
[2,2] Det -> . a
[2,2] Det -> . an
[2,2] ADV -> . like
[2,2] V -> . flies
[2,2] V -> . like
-- Chart[3] (after reading 'like') --------------------------
* [2,3] ADV -> like .
* [2,3] V -> like .
[2,3] ADVP -> ADV . NP
[2,3] VP -> V . NP
[2,3] VP -> V . ADVP
[3,3] NP -> . N
[3,3] NP -> . Det N
[3,3] NP -> . N N
[3,3] ADVP -> . ADV NP
[3,3] N -> . time
[3,3] N -> . flies
[3,3] N -> . arrow
[3,3] Det -> . a
[3,3] Det -> . an
[3,3] ADV -> . like
-- Chart[4] (after reading 'an') ----------------------------
* [3,4] Det -> an .
[3,4] NP -> Det . N
[4,4] N -> . time
[4,4] N -> . flies
[4,4] N -> . arrow
-- Chart[5] (after reading 'arrow') -------------------------
* [4,5] N -> arrow .
* [3,5] NP -> Det N .
* [2,5] ADVP -> ADV NP .
* [2,5] VP -> V NP .
* [1,5] VP -> V ADVP .
* [0,5] S -> NP VP .
========================================================================
PARSE TREES
========================================================================
-- Tree 1 (Verb Phrase "flies") ------------------------------
Probability : 0.0044800000
Cost (-log2): 7.8022855523
(S
  (NP (N time))
  (VP (V flies)
    (ADVP (ADV like)
      (NP (Det an) (N arrow)))))

-- Tree 2 (Noun Phrase "time flies") -------------------------
Probability : 0.0009600000
Cost (-log2): 10.0246779737
(S
  (NP (N time) (N flies))
  (VP (V like)
    (NP (Det an) (N arrow))))
```

---

## 2. Tree Probability & Cost Analysis

**Context:** Computing the individual probabilities and base-2 logarithmic costs of the valid parse trees emitted by the parser. 

The overall probability of a structural derivation is the product of its constituent rule probabilities. The corresponding cost is evaluated as $-\log_2(P)$.

###  Tree 1: Noun Phrase Interpretation (*"time flies"*)
**Derivation:** `[time flies]NP [like [an arrow]NP]VP`

$$ P(T_1) = P(S 	o NP\ VP) \times P(NP 	o N\ N) \times P(N 	o \text{time}) \times \dots $$
$$ P(T_1) = 1.0 \times 0.25 \times 0.4 \times 0.2 \times 0.6 \times 0.5 \times 0.4 \times 1.0 \times 0.4 = \mathbf{0.00096} $$

$$ \text{Cost} = -\log_2(0.00096) \approx \mathbf{10.02468} $$

###  Tree 2: Verb Phrase Interpretation (*"flies"*)
**Derivation:** `[time]NP [flies [like [an arrow]NP]ADVP]VP`

$$ P(T_2) = P(S 	o NP\ VP) \times P(NP 	o N) \times P(N 	o \text{time}) \times \dots $$
$$ P(T_2) = 1.0 \times 0.35 \times 0.4 \times 0.4 \times 0.5 \times 1.0 \times 1.0 \times 0.4 \times 1.0 \times 0.4 = \mathbf{0.00448} $$

$$ \text{Cost} = -\log_2(0.00448) \approx \mathbf{7.80229} $$

> **Conclusion:** Tree 2 is significantly more probable (approx. **4.67x**) under the provided grammar, structurally reflecting the preferred idiom "time flies like an arrow" yielding a minimized bit-encoding cost.

---

## 3. Designing Ambiguity: Grammar Construction

**Context:** Formulating a custom grammar to deliberately yield ambiguous structural analyses for the sentence: *"the man shot the soldier with a gun"*.

### Prepositional Phrase Attachment Grammar
To capture the classic PP-attachment structural ambiguity (i.e., whether the *man* used the gun to shoot, or the *soldier* was bearing the gun), we introduced equal-probability branches ($0.5$) where applicable:

```ebnf
1.0 S NP VP
0.5 NP DT N
0.5 NP DT N PP
0.5 VP V NP
0.5 VP V NP PP
1.0 PP P NP
0.5 DT the
0.5 DT a
0.25 N man
0.25 N soldier
0.25 N gun
1.0 V shot
1.0 P with
```

### Resulting Analyses
The parser accurately identifies and emits two distinct valid trees. Both resolve to identical probabilities ($P = 0.000122$), structurally confirming the intrinsic attachment ambiguity.

```text
EARLEY CHART
========================================================================
-- Chart[0] (before reading any word) -----------------------
... (Omitted full tree output for brevity, but analyses were found properly up to Chart[8])

========================================================================
PARSE TREES
========================================================================
-- Tree 1 ----------------------------------------------------
Probability : 0.0001220711
Cost (-log2): 13.000000
(S
  (NP (DT the) (N man))
  (VP (V shot)
    (NP (DT the) (N soldier))
    (PP (P with)
      (NP (DT a) (N gun)))))

-- Tree 2 ----------------------------------------------------
Probability : 0.0001220711
Cost (-log2): 13.000000
(S
  (NP (DT the) (N man))
  (VP (V shot)
    (NP (DT the) (N soldier)
      (PP (P with)
        (NP (DT a) (N gun))))))
```

---

## 4. Architectural Implementation & Algorithmic Efficiency

**Context:** Justifying the parser's adherence to dynamic programming constraints, execution correctness, and theoretical complexity boundaries.

###  Guaranteeing Correctness
Every mapped state represented computationally encapsulating a state pointer manages two keys: a `'cost'` metric (the optimal minimum negative base-2 logarithm cost) and `'backs'` (dynamically accumulating array of corresponding backpointers).

* **Viterbi Cost Optimization:** During structural discovery, each localized path's cost is tracked. If an identical grammatical state is synthesized by a provably less expensive computational path, the `'cost'` parameter is securely overwritten. This rigorously guarantees that the internal engine dynamically asserts the Viterbi mathematical minimum.
* **Exhaustive State Tracking:** Backpointers are continuously bundled to the `'backs'` trajectory registry solely upon encountering novel compositional derivations, isolated entirely from the Viterbi bounds. Extricating tree map recording from mathematical minimums equips the algorithmic post-phase engine with the absolute ability to exhaustively plot out every uniquely valid syntactic geometry without overwriting valid permutations.

###  Complexity & Performance Profile
At the protocol level, operations are bounded precisely within polynomial memory barriers—specifically $O(n^2)$ array domains—and a ceiling execution window factoring to $O(n^3)$:

* **Spatial Complexity — $O(n^2)$:**  
  Memory mapping structures arrayed in $n+1$ procedural sequences maintain keys shaped as `(rule_idx, dot, origin)`. As the base vocabulary dictionary $G$ remains invariant, structural instances `rule_idx` and `dot` remain mathematically capped. The `origin` index traces values purely up to size $j$. Consequently, array collections limit out safely at $O(|G| \cdot n)$ instances, establishing an absolute $O(n^2)$ overall space configuration.
  
* **Temporal Complexity — $O(n^3)$:**  
  Linear state operators, formally identified as *Predict* and *Scan*, compute safely at intervals $O(|G|)$ and $O(1)$. The algorithmic apex natively revolves around *Complete* routines. Expanding an iteration index `j` bridging from offset `i` implicitly mandates iterating backwards inside array sector `i`. Given states inside limit linearly to $O(|G| \cdot n)$ across matrix-squared $O(n^2)$ possible origin bounds `(i, j)`, the cumulative upper-bound procedural time caps neatly at $O(n^3)$.

* **Native Python State Deduplication ($O(1)$) :**  
  Grid sequence sectors deploy universally standard hash interfaces internally mapped as (`dict`). Routine pointer checks (`key not in index_map`) paired with state appends structurally evaluate matching $O(1)$ amortized loads. The capability to validate configuration keys virtually instantaneously strictly neutralizes duplicate recursive state queuing, protecting definitively against infinite combinatorial cycles.
