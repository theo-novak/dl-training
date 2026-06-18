"""Baxter & Rennie reading map and enrichment cells per syllabus week."""

BAXTER_RENNIE_URL = (
    "https://cms.dm.uba.ar/academico/materias/2docuat2016/"
    "analisis_cuantitativo_en_finanzas/Baxter_Rennie_Financial_Calculus.pdf"
)

# Per-week: chapters, table rows (B&R column), optional extra cells, further-reading bullets
ENRICHMENT = {
    "week01_probability_review_stochastic_processes.ipynb": {
        "br_chapters": "Parable; Ch. 1; Ch. 2.1–2.2",
        "br_rows": [
            "| 1 | **Expectation vs arbitrage pricing** | Ch. 1.1–1.3 |",
            "| 2 | **Binomial branch model (preview)** | Ch. 2.1 |",
            "| 3 | **Filtrations & discrete martingales** | Ch. 2.2–2.3 |",
            "| 4 | **Overture to continuous models** | Ch. 2.4 |",
            "| 5 | **Brownian motion preview** | Ch. 3.1 |",
        ],
        "cells_md_code": [
            (
                """---
## Baxter & Rennie spotlight — The parable of the bookmaker

Before measure theory, Baxter & Rennie motivate pricing with a **bookmaker** who sets odds so no arbitrage exists. The same logic underlies derivative pricing:

- **Expectation pricing** (Ch. 1.1): fair price = expected payoff (needs a probability measure).
- **Arbitrage pricing** (Ch. 1.2): fair price = cost of a **replicating** strategy.

**Read:** *Financial Calculus*, Parable + Ch. 1.1–1.3. Compare Shreve's rigorous $(\\Omega, \\mathcal{F}, P)$ setup with B&R's market-first intuition.""",
                None,
            ),
            (
                """**B&R Example (Ch. 2.1):** A one-step branch — stock $S$ goes to $S_0 u$ or $S_0 d$ with probabilities $p$ and $1-p$. A claim paying $V_u$ or $V_d$ has **no-arbitrage price**

$$V_0 = e^{-r\\Delta t}\\big(p^* V_u + (1-p^*) V_d\\big)$$

where $p^*$ is the **risk-neutral probability** (not necessarily physical $p$).""",
                """# B&R Ch. 2.1 — one-step binomial risk-neutral price
S0, u, d, r, dt = 100, 1.1, 0.9, 0.05, 1/252
Vu, Vd = 10, 0  # e.g. digital or call-like payoff at step 1
p_star = (np.exp(r * dt) - d) / (u - d)
V0 = np.exp(-r * dt) * (p_star * Vu + (1 - p_star) * Vd)
print(f"Risk-neutral prob p* = {p_star:.4f}")
print(f"No-arbitrage claim price V0 = {V0:.4f}")""",
            ),
        ],
        "further": """- **Baxter & Rennie**, *Financial Calculus*, Parable + Ch. 1–2.2 — [PDF]({url})
  - Ch. 1.1–1.3: expectation vs arbitrage (complements Shreve Ch. 1–2).
  - Ch. 2.1–2.2: binomial branch/tree — discrete martingales before Brownian motion.
  - **Appendix 2** (notation) and **Appendix 4** (glossary) are useful references.""",
    },
    "week02_random_walk_brownian_motion.ipynb": {
        "br_chapters": "Ch. 2.4; Ch. 3.1",
        "br_rows": [
            "| 1 | **From binomial tree to continuous time** | Ch. 2.4 |",
            "| 2 | **Continuous processes & Brownian motion** | Ch. 3.1 |",
            "| 3 | **Quadratic variation** | Ch. 3.1 |",
            "| 4 | **Log-normal stock as exponential BM** | Ch. 3.1 |",
            "| — | **Exercises** | App. 3 |",
        ],
        "cells_md_code": [
            (
                """---
## Baxter & Rennie spotlight — Overture to continuous models (Ch. 2.4)

B&R pass from the **binomial tree** (Ch. 2.2) to continuous time by shrinking $\\Delta t$ and rescaling increments — the same idea as Donsker's theorem in Shreve Ch. 3.3.

**Ch. 3.1** defines a **continuous process** as a random function of time and introduces **Brownian motion** $W_t$ as the fundamental building block with:

- $W_0 = 0$, continuous paths, independent increments, $W_t - W_s \\sim N(0, t-s)$.

**Read:** B&R Ch. 2.4 then 3.1 alongside Shreve Ch. 3.2.""",
                None,
            ),
            (
                """**B&R Example:** Stock with **log-normal** dynamics — if $\\log S_t = \\log S_0 + \\sigma W_t + (\\mu - \\frac{1}{2}\\sigma^2)t$, then $S_t$ is an exponential of Brownian motion (preview of GBM).""",
                """# B&R Ch. 3.1 — exponential of Brownian motion (log-normal)
rng = np.random.default_rng(20)
T, n, sigma, mu = 1.0, 2000, 0.2, 0.08
dt = T / n
dW = rng.normal(0, np.sqrt(dt), size=n)
log_S = np.log(100) + (mu - 0.5*sigma**2)*dt + sigma*dW
S = np.exp(np.concatenate([[np.log(100)], np.log(100) + np.cumsum(
    (mu - 0.5*sigma**2)*dt + sigma*dW)]))
plt.plot(S)
plt.title("B&R: exponential Brownian motion (log-normal stock)")
plt.ylabel("S_t")
plt.show()""",
            ),
        ],
        "further": """- **Baxter & Rennie**, Ch. 2.4 & 3.1 — [PDF]({url}): binomial-to-continuous limit; definition of $W_t$.
- B&R emphasize **visual** continuous paths before Itô calculus — good intuition before Shreve Ch. 4.""",
    },
    "week03_markov_reflection_passage_times.ipynb": {
        "br_chapters": "Ch. 3.1",
        "br_rows": [
            "| 1 | **Markov property of Brownian motion** | Ch. 3.1 |",
            "| 2 | **Transition densities** | Ch. 3.1 |",
            "| 3 | **First passage (via densities)** | Ch. 3.1 |",
            "| 4 | **Maximum of $W_t$** | Ch. 3.1 |",
            "| — | **Exercises** | App. 3 |",
        ],
        "cells_md_code": [
            (
                """---
## Baxter & Rennie spotlight — Properties of Brownian motion (Ch. 3.1)

B&R develop **continuous processes** with the **Markov property**: the future of $W_t$ depends only on the present value, not the path history — matching Shreve's reflection-principle setup.

They stress **quadratic variation** $[W]_t = t$ as the distinguishing feature of Brownian motion (smooth functions have zero QV).

**Read:** B&R Ch. 3.1 sections on Brownian motion before moving to stochastic calculus in Ch. 3.2.""",
                None,
            ),
        ],
        "further": """- **Baxter & Rennie**, Ch. 3.1 — [PDF]({url}): Markov property, quadratic variation, transition probabilities.
- Shreve Ch. 3.3.6 adds **reflection principle** detail; B&R builds the same intuition with less measure theory.""",
    },
    "week04_stochastic_calculus_integrands.ipynb": {
        "br_chapters": "Ch. 3.2",
        "br_rows": [
            "| 1 | **Stochastic integration** | Ch. 3.2 |",
            "| 2 | **Itô isometry** | Ch. 3.2 |",
            "| 3 | **Quadratic variation of integrals** | Ch. 3.2 |",
            "| 4 | **$\\int W\\, dW$** | Ch. 3.2 |",
            "| — | **Exercises** | App. 3 |",
        ],
        "cells_md_code": [
            (
                """---
## Baxter & Rennie spotlight — Stochastic calculus (Ch. 3.2)

B&R introduce the **Itô integral** $\\int H_t\\, dW_t$ for **previsible** integrands $H_t$ — functions adapted to the filtration whose value at $t$ depends only on history *strictly before* $t$ (left-continuous).

Key message: we cannot use ordinary calculus because $W_t$ is too rough ($dW_t^2 = dt$).

**Read:** B&R Ch. 3.2 with Shreve Ch. 4.1–4.3.""",
                None,
            ),
        ],
        "further": """- **Baxter & Rennie**, Ch. 3.2 — [PDF]({url}): construction of stochastic integrals, Itô isometry.
- B&R **Appendix 3** has worked answers for Ch. 3 exercises — check your integral calculations.""",
    },
    "week05_ito_lemma_applications.ipynb": {
        "br_chapters": "Ch. 3.3",
        "br_rows": [
            "| 1 | **Itô's lemma** | Ch. 3.3 |",
            "| 2 | **Itô vs Stratonovich** | Ch. 3.3 |",
            "| 3 | **GBM from Itô** | Ch. 3.3 |",
            "| 4 | **Exponential martingales** | Ch. 3.3 |",
            "| — | **Exercises** | App. 3 |",
        ],
        "cells_md_code": [
            (
                """---
## Baxter & Rennie spotlight — Itô calculus (Ch. 3.3)

B&R present **Itô's lemma** as the chain rule for functions of stochastic processes, emphasizing the extra $\\frac{1}{2} f'' (dX)^2$ term from nonzero quadratic variation.

They derive **geometric Brownian motion** by applying Itô to $\\log S_t$.

**Read:** B&R Ch. 3.3; compare notation with Shreve Ch. 4.4.""",
                None,
            ),
            (
                """**B&R drill:** For $f(x) = e^x$ and $dX_t = \\mu\\, dt + \\sigma\\, dW_t$, Itô gives $df = e^X(\\mu + \\frac{1}{2}\\sigma^2)\\, dt + \\sigma e^X\\, dW$.""",
                """# B&R Ch. 3.3 — Itô on exp(X)
rng = np.random.default_rng(40)
mu, sigma, T, n = 0.05, 0.3, 1.0, 5000
dt = T / n
dW = rng.normal(0, np.sqrt(dt), size=n)
X = np.cumsum(mu*dt + sigma*dW)
f = np.exp(X)
df = f[1:] - f[:-1]
df_ito = f[:-1] * (mu + 0.5*sigma**2)*dt + f[:-1]*sigma*dW
print(f"Corr(actual df, Itô): {np.corrcoef(df, df_ito)[0,1]:.4f}")""",
            ),
        ],
        "further": """- **Baxter & Rennie**, Ch. 3.3 — [PDF]({url}): Itô's lemma, GBM derivation.
- B&R worked examples use the same $(dW)^2 = dt$ rules as Shreve.""",
    },
    "week06_black_scholes_merton.ipynb": {
        "br_chapters": "Ch. 3.6–3.8",
        "br_rows": [
            "| 1 | **Replication & construction strategies** | Ch. 3.6 |",
            "| 2 | **Black–Scholes model** | Ch. 3.7 |",
            "| 3 | **Black–Scholes in action** | Ch. 3.8 |",
            "| 4 | **Hedging interpretation** | Ch. 3.7 |",
            "| — | **Exercises** | App. 3 |",
        ],
        "cells_md_code": [
            (
                """---
## Baxter & Rennie spotlight — Black–Scholes (Ch. 3.7–3.8)

B&R's flagship example: price a **European call** by

1. Assuming stock follows GBM under a risk-neutral measure.
2. Building a **self-financing** portfolio of stock + bond that replicates the payoff.
3. Obtaining the **Black–Scholes PDE** and closed-form formula.

**Ch. 3.8** walks through numerics and hedging — parallel to Shreve Ch. 4.5.

**Read:** B&R Ch. 3.6 (construction strategies) then 3.7–3.8.""",
                None,
            ),
            (
                """**B&R Example (Ch. 3.7):** European call — verify B&R's formula matches risk-neutral expectation $e^{-rT} E[(S_T-K)^+]$.""",
                """# B&R Ch. 3.7 — BS call: formula vs risk-neutral MC
def bs_call(S, K, T, r, sig):
    d1 = (np.log(S/K) + (r + 0.5*sig**2)*T) / (sig*np.sqrt(T))
    d2 = d1 - sig*np.sqrt(T)
    return S*stats.norm.cdf(d1) - K*np.exp(-r*T)*stats.norm.cdf(d2)

S0, K, T, r, sig = 100, 100, 1.0, 0.05, 0.2
rng = np.random.default_rng(50)
Z = rng.standard_normal(300_000)
ST = S0*np.exp((r-0.5*sig**2)*T + sig*np.sqrt(T)*Z)
mc = np.exp(-r*T)*np.maximum(ST-K, 0).mean()
print(f"B&R BS formula : {bs_call(S0,K,T,r,sig):.4f}")
print(f"Risk-neutral MC: {mc:.4f}")""",
            ),
        ],
        "further": """- **Baxter & Rennie**, Ch. 3.6–3.8 — [PDF]({url}): replication, BSM PDE, closed-form call, practical hedging.
- B&R Ch. 3.8 exercises: replicate a call with discrete rebalancing — compare to our delta hedge.""",
    },
    "week07_multivariable_stochastic_calculus.ipynb": {
        "br_chapters": "Ch. 6.1; Ch. 6.3",
        "br_rows": [
            "| 1 | **General stock model** | Ch. 6.1 |",
            "| 2 | **Multi-dimensional Itô** | Ch. 6.1 |",
            "| 3 | **Multiple stock models** | Ch. 6.3 |",
            "| 4 | **Correlation structure** | Ch. 6.3 |",
            "| — | **Exercises** | App. 3 |",
        ],
        "cells_md_code": [
            (
                """---
## Baxter & Rennie spotlight — Bigger models preview (Ch. 6.1, 6.3)

B&R extend to **vector** Brownian motion and a **general stock model** where each stock is driven by linear combinations of independent Brownian motions.

**Ch. 6.3** prices derivatives on several stocks — covariance matrix of log-returns enters exactly as in Shreve Ch. 4.6.

**Read:** B&R Ch. 6.1 and 6.3 (multi-stock section) with Shreve Ch. 4.6.""",
                None,
            ),
        ],
        "further": """- **Baxter & Rennie**, Ch. 6.1 & 6.3 — [PDF]({url}): general stock model, correlated assets.
- B&R Ch. 6.4 (numeraires) previews change-of-numeraire techniques used in multi-currency models.""",
    },
    "week08_midterm_review.ipynb": {
        "br_chapters": "Ch. 1–3",
        "br_rows": [
            "| 1 | **Arbitrage & expectation pricing** | Ch. 1 |",
            "| 2 | **Binomial → continuous** | Ch. 2–3.1 |",
            "| 3 | **Itô & GBM** | Ch. 3.2–3.3 |",
            "| 4 | **Black–Scholes** | Ch. 3.7 |",
            "| — | **Midterm exercises** | App. 3 |",
        ],
        "cells_md_code": [
            (
                """---
## Baxter & Rennie midterm map

| Topic | Shreve | Baxter & Rennie |
|-------|--------|-----------------|
| Pricing philosophy | Ch. 1–2 | Parable, Ch. 1.1–1.3 |
| Discrete martingales | Ch. 2 | Ch. 2.2–2.3 |
| Brownian motion | Ch. 3 | Ch. 3.1 |
| Itô calculus | Ch. 4.1–4.4 | Ch. 3.2–3.3 |
| BSM | Ch. 4.5 | Ch. 3.7–3.8 |

**Review:** B&R [PDF]({url}) Ch. 1–3 and **Appendix 3** (answers).""".replace("{url}", BAXTER_RENNIE_URL),
                None,
            ),
        ],
        "further": """- **Baxter & Rennie**, Ch. 1–3 — [PDF]({url}): full continuous-time core before interest rates.
- Work B&R **Appendix 3** exercises for Ch. 2–3 as midterm practice.""",
    },
    "week09_risk_neutral_girsanov.ipynb": {
        "br_chapters": "Ch. 3.4",
        "br_rows": [
            "| 1 | **Change of measure** | Ch. 3.4 |",
            "| 2 | **Cameron–Martin–Girsanov** | Ch. 3.4 |",
            "| 3 | **Radon–Nikodym derivative** | Ch. 3.4 |",
            "| 4 | **Risk-neutral stock dynamics** | Ch. 3.4 |",
            "| — | **Exercises** | App. 3 |",
        ],
        "cells_md_code": [
            (
                """---
## Baxter & Rennie spotlight — Change of measure (Ch. 3.4)

B&R's **Cameron–Martin–Girsanov (C-M-G) theorem** is the accessible entry to Girsanov:

Under a new measure $Q$, a Brownian motion with drift $\\mu$ becomes a Brownian motion with zero drift after subtracting $\\mu t$.

The **Radon–Nikodym derivative** $dQ/dP = \\exp(-\\theta W_T - \\frac{1}{2}\\theta^2 T)$ is an exponential martingale — the same object as Shreve Ch. 5.1.

**Read:** B&R Ch. 3.4 alongside Shreve Ch. 5.2.""",
                None,
            ),
            (
                """**B&R C-M-G:** With $\\theta = (\\mu - r)/\\sigma$, GBM drift $\\mu$ under $P$ becomes drift $r$ under $Q$.""",
                """# B&R Ch. 3.4 — C-G drift change
theta = (0.12 - 0.05) / 0.2
T = 1.0
rng = np.random.default_rng(90)
W_P = rng.normal(0, np.sqrt(T), 100_000)
W_Q = W_P + theta * T  # Brownian motion under Q
Z = np.exp(-theta*W_P - 0.5*theta**2*T)  # dQ/dP
print(f"E[Z] = {Z.mean():.4f} (should be 1)")
print(f"W^Q mean = {W_Q.mean():.4f}, var = {W_Q.var():.4f}")""",
            ),
        ],
        "further": """- **Baxter & Rennie**, Ch. 3.4 — [PDF]({url}): C-M-G theorem, risk-neutral measure.
- B&R present Girsanov before abstract multi-asset models — good narrative complement to Shreve.""",
    },
    "week10_multidimensional_stock_model.ipynb": {
        "br_chapters": "Ch. 6.1; Ch. 6.3",
        "br_rows": [
            "| 1 | **General stock model** | Ch. 6.1 |",
            "| 2 | **Log-normal models** | Ch. 6.2 |",
            "| 3 | **Multiple stock models** | Ch. 6.3 |",
            "| 4 | **Market price of risk** | Ch. 4.4 |",
            "| — | **Exercises** | App. 3 |",
        ],
        "cells_md_code": [
            (
                """---
## Baxter & Rennie spotlight — Multiple stocks (Ch. 6.3)

B&R write $n$ stocks as driven by $n$ Brownian motions with volatility matrix $\\sigma_{ij}$:

$$dS^i_t = S^i_t \\sum_j \\sigma_{ij}\\, dW^j_t$$

under the risk-neutral measure (drift $r S^i_t\\, dt$ added in physical measure).

**Ch. 4.4** introduces the **market price of risk** linking extra drifts to change of measure — connects to Shreve Ch. 5.3.

**Read:** B&R Ch. 6.1–6.3 and Ch. 4.4.""",
                None,
            ),
        ],
        "further": """- **Baxter & Rennie**, Ch. 6.1–6.3 & 4.4 — [PDF]({url}): multi-asset GBM, market price of risk.
- B&R Ch. 6.4 (numeraires): pick a numeraire asset to simplify multi-currency pricing.""",
    },
    "week11_pdes_and_sdes.ipynb": {
        "br_chapters": "Ch. 3.5–3.6",
        "br_rows": [
            "| 1 | **Martingale representation** | Ch. 3.5 |",
            "| 2 | **Construction strategies** | Ch. 3.6 |",
            "| 3 | **PDE from replication** | Ch. 3.7 |",
            "| 4 | **Feynman–Kac link** | Ch. 3.5–3.7 |",
            "| — | **Exercises** | App. 3 |",
        ],
        "cells_md_code": [
            (
                """---
## Baxter & Rennie spotlight — Martingale representation & replication (Ch. 3.5–3.6)

**Ch. 3.5 Martingale representation theorem:** every $Q$-martingale can be written as a stochastic integral $\\int H_t\\, dW_t$ — the mathematical backbone of **hedging**.

**Ch. 3.6 Construction strategies:** explicit recipe to build the hedging portfolio for a claim — the SDE/PDE duality Shreve develops in Ch. 6.

B&R derive the **BSM PDE** from replication, then identify it with the **discounted expectation** — the Feynman–Kac bridge.

**Read:** B&R Ch. 3.5–3.6 with Shreve Ch. 6.""",
                None,
            ),
        ],
        "further": """- **Baxter & Rennie**, Ch. 3.5–3.6 — [PDF]({url}): martingale representation, construction strategies.
- Compare B&R's replication argument for the PDE with Shreve's Feynman–Kac (Ch. 6).""",
    },
    "week12_poisson_jump_diffusion.ipynb": {
        "br_chapters": "Ch. 6 (extensions)",
        "br_rows": [
            "| 1 | **Limitations of diffusion** | Ch. 3.7 |",
            "| 2 | **Bigger models overview** | Ch. 6 |",
            "| 3 | **Log-normal extensions** | Ch. 6.2 |",
            "| — | **Jumps: Shreve Ch. 11** | Shreve |",
            "| — | **Exercises** | App. 3 |",
        ],
        "cells_md_code": [
            (
                """---
## Baxter & Rennie note — Beyond pure diffusion

Baxter & Rennie focus on **continuous** models (Ch. 3–6). Jump processes are covered rigorously in **Shreve Ch. 11**.

B&R **Ch. 6** ("Bigger models") discusses extensions: more assets, numeraires, and completeness — when continuous models suffice and when markets are incomplete.

**Read:** B&R Ch. 6 intro + Shreve Ch. 11.1 for Poisson processes.""",
                None,
            ),
        ],
        "further": """- **Shreve** Ch. 11 — jump processes (primary for this week).
- **Baxter & Rennie**, Ch. 6 — [PDF]({url}): model completeness, extensions; contrasts with jump incompleteness.""",
    },
    "week13_exotic_options.ipynb": {
        "br_chapters": "Ch. 4",
        "br_rows": [
            "| 1 | **Foreign exchange** | Ch. 4.1 |",
            "| 2 | **Equities & dividends** | Ch. 4.2 |",
            "| 3 | **Bonds** | Ch. 4.3 |",
            "| 4 | **Quantos** | Ch. 4.5 |",
            "| — | **Exercises** | App. 3 |",
        ],
        "cells_md_code": [
            (
                """---
## Baxter & Rennie spotlight — Pricing market securities (Ch. 4)

B&R apply the same **change-of-measure** machinery to:

- **FX options** (Ch. 4.1): two currencies, two drifts, one risk-neutral measure.
- **Dividends** (Ch. 4.2): adjust spot for yield.
- **Bonds** (Ch. 4.3): forward bond prices as martingales.
- **Quantos** (Ch. 4.5): payoff in wrong currency — exotic structure.

Path-dependent exotics (Asian, barrier) are natural **Monte Carlo** extensions of Shreve Ch. 7; B&R Ch. 4 gives cross-asset templates.

**Read:** B&R Ch. 4.1–4.3 and 4.5.""",
                None,
            ),
            (
                """**B&R Example (Ch. 4.1):** FX forward — under domestic risk-neutral measure, foreign bond discounted at foreign rate is a martingale when converted.""",
                """# B&R Ch. 4.1 — FX: domestic vs foreign growth rates
r_d, r_f, T = 0.05, 0.03, 1.0
# Forward F_0 = S_0 * exp((r_d - r_f) * T)
S0 = 1.20  # USD per EUR
F = S0 * np.exp((r_d - r_f) * T)
print(f"FX forward F_0 = {F:.4f} (USD per EUR)")""",
            ),
        ],
        "further": """- **Baxter & Rennie**, Ch. 4 — [PDF]({url}): FX, dividends, bonds, quantos.
- Shreve Ch. 7 exotics + B&R Ch. 4 cross-asset pricing = full practitioner toolkit.""",
    },
    "week14_review_catchup.ipynb": {
        "br_chapters": "Ch. 1–6; Appendix 1",
        "br_rows": [
            "| 1 | **Full B&R arc** | Ch. 1–6 |",
            "| 2 | **Interest rates preview** | Ch. 5 |",
            "| 3 | **Further reading list** | App. 1 |",
            "| 4 | **Notation & glossary** | App. 2–4 |",
            "| — | **Comprehensive exercises** | App. 3 |",
        ],
        "cells_md_code": [
            (
                """---
## Baxter & Rennie course map

| B&R | Topic | Shreve overlap |
|-----|-------|----------------|
| Ch. 1 | Arbitrage vs expectation | Vol II Ch. 1–2 |
| Ch. 2 | Binomial trees | Vol I Ch. 1–3 |
| Ch. 3 | Continuous, Itô, C-M-G, BSM | Vol II Ch. 3–4, 5 |
| Ch. 4 | FX, bonds, quantos | Vol II Ch. 5, 7 |
| Ch. 5 | Interest rates, HJM | Vol II Ch. 10 |
| Ch. 6 | Multi-asset, numeraires | Vol II Ch. 5 |

**Appendix 1** lists classic further reading; **Appendix 4** glossary matches course notation.

[B&R PDF]({url})""".replace("{url}", BAXTER_RENNIE_URL),
                None,
            ),
        ],
        "further": """- **Baxter & Rennie**, full text + **Appendix 1** (further reading) — [PDF]({url}).
- Next steps: B&R Ch. 5 (interest rates) and Shreve Vol II Ch. 10.""",
    },
}


def br_cells_for_week(filename: str, md_fn, code_fn):
    """Return list of cell dicts from ENRICHMENT."""
    data = ENRICHMENT.get(filename, {})
    out = []
    for item in data.get("cells_md_code", []):
        md_text, code_text = item
        out.append(md_fn(md_text))
        if code_text:
            out.append(code_fn(code_text))
    return out


def merge_parts_table(shreve_table: str, br_rows: list[str]) -> str:
    lines = shreve_table.strip().split("\n")
    if len(lines) < 2:
        return shreve_table
    header = lines[0].rstrip() + " Baxter & Rennie |"
    sep = lines[1].rstrip() + "-----------------|"
    new_lines = [header, sep]
    body = [line for line in lines[2:] if line.strip().startswith("|")]
    for i, row in enumerate(body):
        br_col = ""
        if i < len(br_rows):
            parts = [p.strip() for p in br_rows[i].split("|")]
            if len(parts) >= 4:
                br_col = parts[3]
        trimmed = row.rstrip()
        if trimmed.endswith("|"):
            trimmed = trimmed[:-1].rstrip()
        new_lines.append(f"{trimmed} | {br_col} |")
    return "\n".join(new_lines)


def further_reading_br(shreve_ch: str, shreve_url: str, filename: str) -> str:
    data = ENRICHMENT.get(filename, {})
    br_extra = data.get("further", "").format(url=BAXTER_RENNIE_URL)
    return f"""---
## Further reading

### Shreve
- **Shreve**, *Stochastic Calculus for Finance II*, Ch. {shreve_ch} — [Vol II PDF]({shreve_url})
- **Shreve**, *Stochastic Calculus for Finance I* — discrete-time foundations (Ch. 1–5).
- **Karatzas & Shreve**, *Brownian Motion and Stochastic Calculus* — rigorous continuous-time theory.

### Baxter & Rennie
{br_extra}

Whenever a theorem says a process "converges" or a formula "holds in expectation," you can **simulate it** here and see the numbers match."""
