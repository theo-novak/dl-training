For a quant dev role at Deutsche (or similar banks), expect a mix of software‑engineering questions, basic data structures/algos, plus probability/stoch calc and derivatives‑pricing questions, with the exact balance depending on team and level. [reddit](https://www.reddit.com/r/quantfinance/comments/1fqsrin/deutsche_bank_quant_interview_tipstricks/)

Below I’ll focus on: (1) what’s specifically reported for Deutsche, (2) the core quant‑dev topics you’re likely to hit, and (3) a concrete prep checklist tailored to your background.

***

## What people report about Deutsche

- Candidates for Deutsche quant roles mention sections split into “core concepts, derivatives and algo” and being asked to derive standard pricing/stoch‑calc results like quanto drift adjustments and solving simple SDEs (e.g. Vasicek). [reddit](https://www.reddit.com/r/quantfinance/comments/1fqsrin/deutsche_bank_quant_interview_tipstricks/)
- Other candidates for Deutsche quantitative developer roles report a ~90‑minute technical phone interview focusing on general software‑engineering questions and data types, with difficulty roughly in line with typical backend interviews. [glassdoor.co](https://www.glassdoor.co.uk/Interview/Deutsche-Bank-Quantitative-Developer-Interview-Questions-EI_IE3150.0,13_KO14,36.htm)
- There is variability across teams and locations; some experiences suggest more brainteasers/probability and generic quant interview style, while others lean more on coding and system‑design style questions. [glassdoor.co](https://www.glassdoor.co.uk/Interview/Deutsche-Bank-Quantitative-Developer-Interview-Questions-EI_IE3150.0,13_KO14,36.htm)

Given you’re a quant dev, assume strong weight on: coding + system design + understanding of pricing libraries and risk infra, with enough math to show you’re not just a SWE.

***

## Core technical areas to prepare

### 1. Coding and data structures

- Expect questions on language fundamentals (likely Python/C++/Java, but Python plus one compiled language is common), memory and data types, and writing or discussing non‑trivial functions. [quantt.co](https://www.quantt.co.uk/resources/quant-developer-interview-questions)
- You should be able to discuss and use: arrays vs linked lists, hash maps, trees/heaps, and common algorithmic patterns (two‑pointer, binary search, prefix sums, interval merging, BFS/DFS). Online banks/hedge‑fund guides recommend at least LeetCode‑Easy/Medium fluency. [quantnet](https://quantnet.com/threads/study-programme-for-quant-researcher-interviews.50152/)
- System‑style questions for quant devs can include designing an order‑book, real‑time risk service, or market‑data normalizer, touching concurrency, throughput, and latency trade‑offs. [quantt.co](https://www.quantt.co.uk/resources/quant-developer-interview-questions)

Given your background, you’ll likely be judged on clarity and robustness of code, and your ability to explain trade‑offs (e.g. why this data structure, what’s the complexity, how to handle edge cases).

***

### 2. Quantitative / derivatives content

- Interviewers have asked candidates at Deutsche to derive quanto drift adjustments and to solve classic SDEs like Vasicek, indicating you should be comfortable with Itô’s lemma and basic short‑rate/FX models. [reddit](https://www.reddit.com/r/quantfinance/comments/1fqsrin/deutsche_bank_quant_interview_tipstricks/)
- General quant interview guidance for bank roles emphasizes: probability theory (conditional expectation, distributions, CLT/LLN intuition), stochastic calculus at a “practitioner” level, and standard vanilla option pricing (Black–Scholes, Greeks, put‑call parity). [careerdevelopment.princeton](https://careerdevelopment.princeton.edu/guides/interviews/quantitative-interview-preparation)
- Depending on the exact desk, you may get questions like:  
  - derive Black–Scholes from GBM under risk‑neutral measure (at least at a high level),  
  - explain Monte‑Carlo pricing and variance reduction,  
  - basic Greeks interpretation and hedging (delta, gamma, vega),  
  - intuitive explanations of models you’ve used in your own work. [quantnet](https://quantnet.com/threads/study-programme-for-quant-researcher-interviews.50152/)

For a “developer‑heavy” role, they might not dive as deep as a pure quant researcher, but they will test whether you understand what your code is pricing and why.

***

### 3. Probability, brainteasers and math

- Generic quant interview prep guides emphasize probability puzzles, discrete distributions, conditional probabilities, and simple combinatorics, plus a selection of brainteasers. [streetofwalls](https://www.streetofwalls.com/finance-training-courses/quantitative-hedge-fund-training/quant-interview-questions-answers/)
- Typical formats:  
  - “What is the probability of event X when rolling dice / drawing balls / shuffling cards?”  
  - “Estimate Y” or Fermi‑style questions (e.g., how many tennis balls fit in a plane), or classic puzzles like socks in a drawer, manhole covers, etc. [openquant](https://openquant.co/questions)
- Math questions tend to be calculus/linear‑algebra heavy: differentiation, integrals in pricing contexts, eigenvalues/eigenvectors, expectations/variances, and basic optimization. [careerdevelopment.princeton](https://careerdevelopment.princeton.edu/guides/interviews/quantitative-interview-preparation)

Your math background probably covers these; what they’ll test is accuracy under time pressure and clarity of reasoning.

***

### 4. Software engineering and systems for quant dev

Quant‑dev‑specific banks/consultancies highlight systems‑type questions for these roles. [quantt.co](https://www.quantt.co.uk/resources/quant-developer-interview-questions)

- Design questions you might see:  
  - Order‑book / matching engine: data structures for price levels and orders, handling updates, and complexity considerations. [quantt.co](https://www.quantt.co.uk/resources/quant-developer-interview-questions)
  - Real‑time risk service: how you’d structure pricing requests, caching, load‑balancing, and asynchronous computation. [quantt.co](https://www.quantt.co.uk/resources/quant-developer-interview-questions)
  - Market‑data normalizer: ingesting multiple feeds, normalizing, de‑duping, and distributing updates with low latency. [quantt.co](https://www.quantt.co.uk/resources/quant-developer-interview-questions)
- You should be ready to talk about:  
  - concurrency primitives (locks, queues, atomics) and avoiding bottlenecks,  
  - serialization formats, schema evolution, and versioning,  
  - monitoring, logging, and failure modes in a trading environment. [quantt.co](https://www.quantt.co.uk/resources/quant-developer-interview-questions)

This is where your Rust/Go and infra experience is a real asset if you can map it onto latency, reliability and debuggability concerns for trading/risk systems.

***

## Concrete prep plan (targeted to Deutsche quant dev)

Using what people report about Deutsche plus general quant‑interview guidance: [glassdoor.co](https://www.glassdoor.co.uk/Interview/Deutsche-Bank-Quantitative-Developer-Interview-Questions-EI_IE3150.0,13_KO14,36.htm)

1. Coding (7–10 focused days)  
   - Do a small batch of LeetCode‑style questions daily: arrays/strings, hash maps, sorting, intervals, graphs. [quantnet](https://quantnet.com/threads/study-programme-for-quant-researcher-interviews.50152/)
   - In your main interview language (probably Python or C++), re‑implement: LRU cache, simple order book (per‑side ordered map of price → FIFO queue of orders), and a basic pricing engine skeleton (interface, pricing functions, configuration). [quantt.co](https://www.quantt.co.uk/resources/quant-developer-interview-questions)
   - Practice “narrating” your solution and trade‑offs out loud as you code.

2. Quant / derivatives theory (5–7 days refresh)  
   - Review:  
     - Black–Scholes, Greeks, Monte‑Carlo pricing outline.  
     - Itô’s lemma, risk‑neutral measure, GBM, Vasicek/OU solution forms. [reddit](https://www.reddit.com/r/quantfinance/comments/1fqsrin/deutsche_bank_quant_interview_tipstricks/)
     - FX/quanto basics (what is a quanto, drift adjustment idea). [reddit](https://www.reddit.com/r/quantfinance/comments/1fqsrin/deutsche_bank_quant_interview_tipstricks/)
   - For each topic, prepare a 2–3 minute “whiteboard explanation” you can give without notes.

3. Probability and brainteasers (ongoing light practice)  
   - Work through a curated set from quant interview guides or online collections that emphasise probability + puzzles. [openquant](https://openquant.co/questions)
   - Goal: be quick and structured (define events, write probabilities, check limiting cases) rather than memorising formulas.

4. Systems / architecture (3–5 days, high leverage)  
   - Sketch designs for: order‑book, MD normaliser, risk service, backtest engine, including: main components, data flow, state, failure handling. [quantt.co](https://www.quantt.co.uk/resources/quant-developer-interview-questions)
   - Map your real background (kdb+/q, DuckDB, Rust/Go, Docker) onto these systems so you can give concrete examples.

5. Firm‑specific and behavioural  
   - Read up on Deutsche’s markets/quant tech presence and be ready for “Why this team? Why quant dev vs pure quant?” [streetofwalls](https://www.streetofwalls.com/finance-training-courses/quantitative-hedge-fund-training/quant-interview-questions-answers/)
   - Prepare a few stories: toughest bug/incident, a performance optimization you did, a time you disagreed on model assumptions, and an example where you traded off latency vs complexity. Generic quant interview guidance stresses that these will appear alongside technical questions. [careerdevelopment.princeton](https://careerdevelopment.princeton.edu/guides/interviews/quantitative-interview-preparation)

***

If you share which specific Deutsche team/location and whether it’s more pricing‑library, trading‑tech, or risk‑infra, I can sketch a very targeted list of 20–30 practice questions and a 1–2 week schedule tailored to that.