"""Generate Shreve Vol II week notebooks matching graduate_probability.ipynb style."""
import json
import importlib.util
import sys
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from baxter_rennie_enrichment import (
    BAXTER_RENNIE_URL,
    ENRICHMENT,
    br_cells_for_week,
    further_reading_br,
    merge_parts_table,
)

OUT = Path(__file__).resolve().parent.parent / "notebooks" / "shreve"
SHREVE_URL = (
    "https://cms.dm.uba.ar/academico/materias/2docuat2016/"
    "analisis_cuantitativo_en_finanzas/Steve_ShreveStochastic_Calculus_for_Finance_II.pdf"
)

SETUP_MD = """---
## Setup — run this first

We use NumPy for simulation, SciPy for exact distributions, and Matplotlib for plots."""

SETUP_CODE = """# If anything is missing, uncomment and run once:
# !pip install numpy scipy matplotlib

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from scipy.special import erf

np.random.seed(42)
plt.rcParams["figure.figsize"] = (9, 5)
plt.rcParams["axes.grid"] = True

print("Ready. NumPy", np.__version__, "| SciPy", stats.__version__)"""

HOW_TO_USE = """## How to use this notebook

1. **Read** each markdown cell, then **run** the code beneath it (`Shift+Enter`).
2. **Change parameters** and re-run — stochastic calculus is about *relationships*, not memorized formulas.
3. Sections end with **"Your turn"** exercises. The **problem set** at the end has **click-to-reveal solutions**.
4. **Shreve** (*Stochastic Calculus for Finance II*) — rigorous measure-theoretic treatment; see chapter pointers in each section.
5. **Baxter & Rennie** (*Financial Calculus*) — market intuition, replication, and worked examples; see spotlight sections."""


def _source(text: str) -> list:
    """nbformat source: list of lines with trailing newlines."""
    lines = text.split("\n")
    return [line + "\n" for line in lines[:-1]] + ([lines[-1] + "\n"] if lines[-1] else [])


def md(text: str) -> dict:
    return {"cell_type": "markdown", "metadata": {}, "source": _source(text)}


def code(text: str) -> dict:
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": _source(text),
    }


def intro(title: str, week: int, topic: str, chapters: str, parts_table: str) -> dict:
    text = f"""# {title}

**Week {week}** — {topic}

This notebook teaches **{topic.lower()}** in the style of our graduate probability notebook: definitions from **Shreve**, intuition and examples from **Baxter & Rennie**, then **verified with Python**.

## What you will learn

{parts_table}

{HOW_TO_USE}

**References:**
- **Shreve** Vol II — {chapters} — [PDF]({SHREVE_URL})
- **Baxter & Rennie**, *Financial Calculus* — [PDF]({BAXTER_RENNIE_URL})

Let's begin."""
    return md(text)


def problem_section(problems: list[str], solutions: str) -> list[dict]:
    cells = [
        md("---\n# Problem Set\n\n**Try each problem before revealing the solution.**"),
        md("## Problems\n\n" + "\n\n".join(f"{i}. {p}" for i, p in enumerate(problems, 1))),
        md(
            f"<details>\n<summary><strong>Reveal solutions</strong></summary>\n\n{solutions}\n\n</details>"
        ),
    ]
    return cells


NOTEBOOKS = {}

# ── Week 1 ──────────────────────────────────────────────────────────
NOTEBOOKS["week01_probability_review_stochastic_processes.ipynb"] = {
    "meta": (1, "Probability Review & Stochastic Processes", "Ch. 1–2"),
    "parts_table": """| Part | Topic | Shreve |
|------|-------|--------|
| 1 | **Random variables & vectors** | Ch. 1.1–1.2 |
| 2 | **Expectation, variance, conditioning** | Ch. 1.3 |
| 3 | **Filtrations & adapted processes** | Ch. 2.1 |
| 4 | **Martingales (discrete preview)** | Ch. 2.3 |
| 5 | **Brownian motion as a random path** | Ch. 1.4, Ch. 3 preview |""",
    "cells": [
        md("""---
# Part 1 — Random Variables and Random Vectors

A **random variable** \\(X\\) is a measurable function \\(X: \\Omega \\to \\mathbb{R}\\). A **random vector** \\((X_1,\\ldots,X_d)\\) assigns a vector to each outcome.

For continuous \\(X\\) with PDF \\(f\\):
$$E[X] = \\int_{-\\infty}^{\\infty} x f(x)\\,dx, \\quad \\text{Var}(X) = E[X^2] - (E[X])^2$$

**Shreve Ch. 1.1–1.2:** random variables, distributions, and joint distributions on \\(\\mathbb{R}^d\\)."""),
        code("""# Joint normal vector — marginals and correlation
rho = 0.6
cov = np.array([[1.0, rho], [rho, 1.0]])
rng = np.random.default_rng(0)
samples = rng.multivariate_normal([0, 0], cov, size=50_000)

print(f"E[X1] ≈ {samples[:, 0].mean():.4f}, E[X2] ≈ {samples[:, 1].mean():.4f}")
print(f"Var(X1) ≈ {samples[:, 0].var():.4f}, Var(X2) ≈ {samples[:, 1].var():.4f}")
print(f"Cov(X1,X2) ≈ {np.cov(samples, rowvar=False)[0, 1]:.4f} (theory ρ={rho})")"""),
        md("""---
# Part 2 — Conditional Expectation

**Definition:** \\(E[X \\mid \\mathcal{G}]\\) is the unique \\(\\mathcal{G}\\)-measurable r.v. with \\(E[X \\mathbf{1}_A] = E[E[X|\\mathcal{G}] \\mathbf{1}_A]\\) for all \\(A \\in \\mathcal{G}\\).

**Tower property:** \\(E[E[X \\mid \\mathcal{G}]] = E[X]\\).

**Shreve Ch. 1.3:** conditional expectation as the best predictor in \\(L^2\\)."""),
        code("""# Tower property: E[Y] = E[E[Y|X]]
rng = np.random.default_rng(1)
X = rng.uniform(0, 1, 100_000)
Y = rng.normal(X, 0.1)  # Y | X ~ N(X, 0.1)

E_Y = Y.mean()
E_E_Y_given_X = X.mean()  # E[Y|X] = X for this construction
print(f"E[Y]           = {E_Y:.4f}")
print(f"E[E[Y|X]] = E[X] = {E_E_Y_given_X:.4f}")"""),
        md("""---
# Part 3 — Filtrations and Stochastic Processes

A **filtration** \\(\\{\\mathcal{F}_t\\}_{t \\geq 0}\\) is an increasing family of \\(\\sigma\\)-algebras: \\(\\mathcal{F}_s \\subseteq \\mathcal{F}_t\\) for \\(s \\leq t\\).

A **stochastic process** \\(\\{X_t\\}\\) is **adapted** if \\(X_t\\) is \\(\\mathcal{F}_t\\)-measurable for each \\(t\\).

**Shreve Ch. 2.1:** information grows over time; trading strategies must be adapted (you cannot use future prices)."""),
        code("""# Random walk S_n — natural filtration F_n = sigma(S_0,...,S_n)
n_steps = 200
rng = np.random.default_rng(2)
increments = rng.choice([-1, 1], size=n_steps)
S = np.concatenate([[0], np.cumsum(increments)])

fig, ax = plt.subplots()
ax.plot(S, lw=1.5)
ax.set_xlabel("time n")
ax.set_ylabel("S_n")
ax.set_title("Symmetric random walk (adapted to its own filtration)")
plt.show()"""),
        md("""---
# Part 4 — Martingales (Preview)

\\(M_t\\) is a **martingale** w.r.t. \\(\\{\\mathcal{F}_t\\}\\) if \\(E[|M_t|] < \\infty\\) and \\(E[M_t \\mid \\mathcal{F}_s] = M_s\\) for \\(s \\leq t\\).

Fair games: expected future wealth equals current wealth given all history.

**Shreve Ch. 2.3:** martingale definition; symmetric random walk is a martingale."""),
        code("""# Verify E[S_n] = 0 for symmetric random walk
rng = np.random.default_rng(3)
n_sims, n = 100_000, 50
walks = rng.choice([-1, 1], size=(n_sims, n))
S_n = walks.sum(axis=1)
print(f"E[S_{n}] simulated = {S_n.mean():.4f} (theory 0)")
print(f"Var(S_{n}) simulated = {S_n.var():.4f} (theory {n})")"""),
        md("""---
# Part 5 — Paths in \\(C[0,T]\\) (Brownian Preview)

Brownian motion \\(W_t\\) lives on **path space** \\(C[0,T]\\) — continuous functions on \\([0,T]\\).

**Shreve Ch. 1.4:** probability on \\(C[0,T]\\); Ch. 3 constructs \\(W\\) from random walks."""),
        code("""# Scaled random walk → Brownian motion (Donsker preview)
def brownian_from_rw(T=1.0, n=500, n_paths=5, seed=4):
    rng = np.random.default_rng(seed)
    dt = T / n
    fig, ax = plt.subplots()
    for _ in range(n_paths):
        dW = rng.choice([-1, 1], size=n) / np.sqrt(n)
        W = np.concatenate([[0], np.cumsum(dW)])
        t = np.linspace(0, T, n + 1)
        ax.plot(t, W, alpha=0.8)
    ax.set_title(f"Scaled random walk → W_t (n={n})")
    ax.set_xlabel("t")
    ax.set_ylabel("W_t")
    plt.show()

brownian_from_rw(n=2000)"""),
        md("**Your turn:** Increase `n` in the scaled random walk. How does the path roughness change?"),
    ],
    "problems": [
        "For \\(X \\sim N(0,1)\\), \\(Y = X^2\\), find \\(E[Y]\\) and \\(\\text{Var}(Y)\\).",
        "Prove the tower property for discrete \\(\\mathcal{G} = \\sigma(X)\\) using definition of conditional expectation.",
        "Show that if \\(M_n\\) is a martingale then \\(E[M_n] = E[M_0]\\) for all \\(n\\).",
        "For a symmetric random walk \\(S_n\\), verify \\(E[S_n^2] = n\\) by induction.",
    ],
    "solutions": """**1.** \\(E[Y] = E[X^2] = 1\\). \\(E[Y^2] = E[X^4] = 3\\), so \\(\\text{Var}(Y) = 2\\).

**2.** \\(E[E[X|\\sigma(X)]] = E[X]\\) by definition of conditional expectation with \\(A = \\Omega\\).

**3.** \\(E[M_n] = E[E[M_n|\\mathcal{F}_0]] = E[M_0]\\) by martingale property at \\(t=0\\).

**4.** \\(E[S_{n+1}^2] = E[(S_n + D)^2] = E[S_n^2] + 2E[S_n D] + E[D^2] = n + 0 + 1 = n+1\\).""",
    "reading_ch": "1–2",
}

# ── Week 2 ──────────────────────────────────────────────────────────
NOTEBOOKS["week02_random_walk_brownian_motion.ipynb"] = {
    "meta": (2, "Random Walk & Brownian Motion", "Ch. 3"),
    "parts_table": """| Part | Topic | Shreve |
|------|-------|--------|
| 1 | **Symmetric random walk** | Ch. 3.2 |
| 2 | **Quadratic variation of \\(W\\)** | Ch. 3.2 |
| 3 | **Donsker's theorem / construction** | Ch. 3.3 |
| 4 | **Covariance & Gaussian paths** | Ch. 3.2 |
| — | **Problem set** | Ch. 3 exercises |""",
    "cells": [
        md("""---
# Part 1 — Symmetric Random Walk

\\(S_0 = 0\\), \\(S_n = \\sum_{i=1}^n X_i\\) with \\(P(X_i = \\pm 1) = 1/2\\).

Properties: \\(E[S_n] = 0\\), \\(\\text{Var}(S_n) = n\\), increments independent.

**Shreve Ch. 3.2:** random walk as discrete Brownian motion."""),
        code("""rng = np.random.default_rng(10)
n_paths, n = 100, 500
walks = rng.choice([-1, 1], size=(n_paths, n))
paths = np.cumsum(walks, axis=1)

fig, ax = plt.subplots()
for p in paths[:30]:
    ax.plot(p, alpha=0.5)
ax.set_title("Symmetric random walk paths")
plt.show()

# Distribution of S_n
n = 100
S_n = rng.choice([-1, 1], size=(200_000, n)).sum(axis=1)
print(f"S_{n}: mean={S_n.mean():.3f}, var={S_n.var():.1f} (theory 0, {n})")"""),
        md("""---
# Part 2 — Quadratic Variation

For Brownian motion \\(W_t\\), **quadratic variation** on \\([0,T]\\):
$$[W, W]_T = \\lim_{n\\to\\infty} \\sum_{i=1}^n (W_{t_i} - W_{t_{i-1}})^2 = T$$

For smooth functions, quadratic variation is 0; for \\(W\\), it is \\(T\\). This is why \\((dW)^2 = dt\\) in Itô calculus.

**Shreve Ch. 3.2:** \\(W\\) has non-zero quadratic variation."""),
        code("""def quadratic_variation_demo(T=1.0, n_list=(10, 100, 1000, 10000), seed=11):
    rng = np.random.default_rng(seed)
    print("Quadratic variation of Brownian motion on [0,T]")
    for n in n_list:
        dt = T / n
        dW = rng.normal(0, np.sqrt(dt), size=n)
        W = np.cumsum(dW)
        qv = np.sum(dW**2)
        print(f"  n={n:5d}: QV = {qv:.4f} (theory T={T})")

quadratic_variation_demo()"""),
        md("""---
# Part 3 — Construction via Scaled Random Walk

**Donsker's theorem:** \\(W_t^{(n)} = \\frac{1}{\\sqrt{n}} S_{\\lfloor nt \\rfloor}\\) converges in distribution to \\(W_t\\) as \\(n \\to \\infty\\).

**Shreve Ch. 3.3:** rigorous construction of Brownian motion."""),
        code("""def donsker_path(T=1.0, n=5000, seed=12):
    rng = np.random.default_rng(seed)
    dt = T / n
    dW = rng.choice([-1, 1], size=n) / np.sqrt(n)
    W_rw = np.concatenate([[0], np.cumsum(dW)])
    dW_bm = rng.normal(0, np.sqrt(dt), size=n)
    W_bm = np.concatenate([[0], np.cumsum(dW_bm)])
    t = np.linspace(0, T, n + 1)
    fig, ax = plt.subplots()
    ax.plot(t, W_rw, label="scaled RW", alpha=0.8)
    ax.plot(t, W_bm, label="Brownian", alpha=0.8)
    ax.legend()
    ax.set_title("Scaled random walk vs simulated Brownian motion")
    plt.show()

donsker_path()"""),
        md("""---
# Part 4 — Covariance Structure

Brownian motion satisfies:
- \\(W_0 = 0\\)
- \\(W_t - W_s \\sim N(0, t-s)\\) for \\(t > s\\)
- \\(E[W_t W_s] = \\min(t, s)\\)

**Shreve Ch. 3.2:** characterizing \\(W\\) by independent Gaussian increments."""),
        code("""rng = np.random.default_rng(13)
T, n = 1.0, 1000
dt = T / n
dW = rng.normal(0, np.sqrt(dt), size=n)
W = np.concatenate([[0], np.cumsum(dW)])
t = np.linspace(0, T, n + 1)

# Check E[W_t W_s] = min(t,s) at sample times
idx = [0, n//4, n//2, 3*n//4, n]
times = t[idx]
Ws = W[idx]
print("Covariance matrix (simulated vs theory min(t,s)):")
cov_sim = np.cov(Ws)
cov_th = np.minimum.outer(times, times)
print("Simulated:", np.round(cov_sim, 4))
print("Theory:   ", np.round(cov_th, 4))"""),
        md("**Your turn:** Simulate \\(W_t\\) at \\(t=1\\) many times. Plot the histogram and overlay \\(N(0,1)\\)."),
    ],
    "problems": [
        "For symmetric RW \\(S_n\\), find \\(E[S_n^4]\\) (hint: use \\(S_{n+1} = S_n + X_{n+1}\\)).",
        "Show \\(E[W_t W_s] = \\min(t,s)\\) for Brownian motion using independent increments.",
        "Explain why \\(\\sum (\\Delta W_i)^2 \\to T\\) but \\(\\sum |\\Delta W_i| \\to \\infty\\) as mesh goes to 0.",
        "If \\(W_t^{(n)}\\) is scaled RW, what is \\(\\text{Var}(W_t^{(n)})\\)?",
    ],
    "solutions": """**1.** \\(E[S_{n+1}^4] = E[(S_n+X)^4]\\); cross terms vanish; yields \\(E[S_n^4] = 3n^2 + n\\).

**2.** Write \\(W_t = W_s + (W_t - W_s)\\); cross term \\(E[W_s(W_t-W_s)] = W_s E[W_t-W_s] = 0\\); so \\(E[W_t W_s] = E[W_s^2] = s\\) for \\(t>s\\).

**3.** QV: each squared increment has mean \\(dt\\), sum → \\(T\\). Total variation: \\(E[|\\Delta W|] \\sim \\sqrt{dt}\\), sum \\(\\sim n\\sqrt{dt} = T/\\sqrt{dt} \\to \\infty\\).

**4.** \\(\\text{Var}(W_t^{(n)}) = t\\) (each step variance \\(1/n\\), \\(nt\\) steps).""",
    "reading_ch": "3",
}

# ── Week 3 ──────────────────────────────────────────────────────────
NOTEBOOKS["week03_markov_reflection_passage_times.ipynb"] = {
    "meta": (3, "Markov Property, Reflection & Passage Times", "Ch. 3"),
    "parts_table": """| Part | Topic | Shreve |
|------|-------|--------|
| 1 | **Markov property** | Ch. 3.3 |
| 2 | **Reflection principle** | Ch. 3.3.6 |
| 3 | **First passage times** | Ch. 3.3.6 |
| 4 | **Maximum of Brownian motion** | Ch. 3.3.6 |
| — | **Problem set** | Ch. 3 |""",
    "cells": [
        md("""---
# Part 1 — Markov Property

\\(W_t\\) is **Markov:** \\(P(W_t \\in B \\mid \\mathcal{F}_s) = P(W_t \\in B \\mid W_s)\\) for \\(t > s\\).

Future depends only on present, not full history. Equivalently: \\(W_t - W_s\\) is independent of \\(\\mathcal{F}_s\\).

**Shreve Ch. 3.3:** Markov property of Brownian motion."""),
        code("""# Markov check: W_t - W_s independent of W_s
rng = np.random.default_rng(20)
n = 200_000
s, t = 0.3, 1.0
Ws = rng.normal(0, np.sqrt(s), size=n)
increment = rng.normal(0, np.sqrt(t - s), size=n)
Wt = Ws + increment

# Correlation between W_s and (W_t - W_s) should be ~0
corr = np.corrcoef(Ws, Wt - Ws)[0, 1]
print(f"Corr(W_s, W_t - W_s) = {corr:.4f} (theory 0)")"""),
        md("""---
# Part 2 — Reflection Principle

If path hits level \\(a > 0\\) before time \\(T\\), reflect the path after first hitting \\(a\\). Reflection preserves increments distribution.

**Key result:** \\(P(\\max_{0 \\leq t \\leq T} W_t \\geq a) = 2 P(W_T \\geq a)\\) for \\(a > 0\\).

**Shreve Ch. 3.3.6:** reflection principle."""),
        code("""# Reflection principle: P(max W_t >= a) vs 2*P(W_T >= a)
rng = np.random.default_rng(21)
T, a = 1.0, 0.5
n_sims, n_steps = 50_000, 500
dt = T / n_steps

max_W = np.zeros(n_sims)
W_T = np.zeros(n_sims)
for i in range(n_sims):
    dW = rng.normal(0, np.sqrt(dt), size=n_steps)
    W = np.cumsum(dW)
    max_W[i] = np.max(W)
    W_T[i] = W[-1]

p_max = (max_W >= a).mean()
p_tail = 2 * (W_T >= a).mean()
print(f"P(max W >= {a})     = {p_max:.4f}")
print(f"2 * P(W_T >= {a})   = {p_tail:.4f}")
print(f"Theory 2*P(W_T>=a)  = {2*(1-stats.norm.cdf(a/np.sqrt(T))):.4f}")"""),
        md("""---
# Part 3 — First Passage Times

**First passage time** to level \\(a > 0\\): \\(\\tau_a = \\inf\\{t \\geq 0 : W_t = a\\}\\).

Distribution: \\(P(\\tau_a \\leq t) = 2 P(W_t \\geq a) = 2\\left(1 - \\Phi(a/\\sqrt{t})\\right)\\).

PDF: \\(f_{\\tau_a}(t) = \\frac{a}{\\sqrt{2\\pi t^3}} e^{-a^2/(2t)}\\) (inverse Gaussian / Lévy).

**Shreve Ch. 3.3.6:** passage time distribution."""),
        code("""def first_passage_sim(a=1.0, T=2.0, n_steps=1000, n_sims=20_000, seed=22):
    rng = np.random.default_rng(seed)
    dt = T / n_steps
    tau = np.full(n_sims, T)  # default: not hit by T
    for i in range(n_sims):
        dW = rng.normal(0, np.sqrt(dt), size=n_steps)
        W = np.cumsum(dW)
        hit = np.where(W >= a)[0]
        if len(hit) > 0:
            tau[i] = hit[0] * dt
    return tau

a = 1.0
tau = first_passage_sim(a=a)
print(f"P(tau_a <= 1) sim = {(tau <= 1).mean():.4f}")
print(f"Theory            = {2*(1-stats.norm.cdf(a/1.0)):.4f}")

fig, ax = plt.subplots()
ax.hist(tau[tau < 2], bins=50, density=True, alpha=0.6, label="simulated")
t_plot = np.linspace(0.01, 2, 200)
pdf = a / np.sqrt(2 * np.pi * t_plot**3) * np.exp(-a**2 / (2 * t_plot))
ax.plot(t_plot, pdf, "r-", lw=2, label="theory")
ax.set_title(f"First passage time to a={a}")
ax.legend()
plt.show()"""),
        md("""---
# Part 4 — Maximum of Brownian Motion

\\(M_T = \\max_{0 \\leq t \\leq T} W_t\\) has PDF \\(f(x) = \\frac{2}{\\sqrt{2\\pi T}} e^{-x^2/(2T)}\\) for \\(x \\geq 0\\) (half-normal).

**Shreve Ch. 3.3.6:** distribution of maximum via reflection."""),
        code("""rng = np.random.default_rng(23)
T = 1.0
n_sims, n_steps = 30_000, 500
dt = T / n_steps
max_W = np.array([
    np.max(np.cumsum(rng.normal(0, np.sqrt(dt), n_steps)))
    for _ in range(n_sims)
])

fig, ax = plt.subplots()
ax.hist(max_W, bins=50, density=True, alpha=0.6)
x = np.linspace(0, 3, 100)
pdf = 2 / np.sqrt(2 * np.pi * T) * np.exp(-x**2 / (2 * T))
ax.plot(x, pdf, "r-", lw=2)
ax.set_title("Distribution of max W_t on [0,T]")
plt.show()"""),
        md("**Your turn:** Use reflection to derive \\(P(\\tau_a \\leq t)\\) in terms of \\(W_t\\)."),
    ],
    "problems": [
        "Prove \\(P(\\max_{0\\leq t\\leq T} W_t \\geq a) = 2P(W_T \\geq a)\\) using reflection.",
        "Find \\(E[\\tau_a]\\) for first passage to \\(a>0\\) (it is infinite!).",
        "For \\(a<0\\), relate \\(P(\\min W_t \\leq a)\\) to a normal tail.",
        "Show the Markov property implies \\(W_{t_3} - W_{t_2}\\) is independent of \\(W_{t_1}\\) for \\(t_1 < t_2 < t_3\\).",
    ],
    "solutions": """**1.** Reflect paths that hit \\(a\\) before \\(T\\); bijection gives equal mass above \\(a\\) at \\(T\\) from paths that hit \\(a\\) and paths that end above \\(a\\).

**2.** \\(E[\\tau_a] = \\infty\\) (BM hits every level but expected time is infinite).

**3.** By symmetry: \\(P(\\min W_t \\leq -a) = 2P(W_T \\leq -a)\\).

**4.** Increment \\(W_{t_3}-W_{t_2}\\) independent of \\(\\mathcal{F}_{t_2}\\), which contains \\(W_{t_1}\\).""",
    "reading_ch": "3",
}

# ── Week 4 ──────────────────────────────────────────────────────────
NOTEBOOKS["week04_stochastic_calculus_integrands.ipynb"] = {
    "meta": (4, "Stochastic Calculus — Integrands", "Ch. 4"),
    "parts_table": """| Part | Topic | Shreve |
|------|-------|--------|
| 1 | **Simple processes & Itô integral** | Ch. 4.1–4.2 |
| 2 | **Itô isometry** | Ch. 4.2 |
| 3 | **Quadratic variation of \\(W\\)** | Ch. 4.2 |
| 4 | **\\(L^2\\) integrands** | Ch. 4.3 |
| — | **Problem set** | Ch. 4 |""",
    "cells": [
        md("""---
# Part 1 — Simple Integrands and the Itô Integral

A **simple process** \\(H_t = \\sum_i H_i \\mathbf{1}_{(t_i, t_{i+1}]}(t)\\) is piecewise constant on intervals.

**Itô integral:**
$$\\int_0^T H_t\\, dW_t = \\sum_i H_i (W_{t_{i+1}} - W_{t_i})$$

Evaluated at **left endpoints** — this is the key difference from Stratonovich.

**Shreve Ch. 4.1–4.2:** construction for simple integrands."""),
        code("""def ito_integral_simple(H_values, T=1.0, seed=30):
    rng = np.random.default_rng(seed)
    n = len(H_values)
    dt = T / n
    dW = rng.normal(0, np.sqrt(dt), size=n)
    integral = np.sum(H_values * dW)
    return integral

H = np.ones(1000)
ints = [ito_integral_simple(H, seed=s) for s in range(500)]
print(f"∫₀¹ 1 dW_t: mean={np.mean(ints):.4f}, var={np.var(ints):.4f} (theory 0, 1)")"""),
        md("""---
# Part 2 — Itô Isometry

For simple \\(H\\):
$$E\\left[\\left(\\int_0^T H_t\\, dW_t\\right)^2\\right] = E\\left[\\int_0^T H_t^2\\, dt\\right]$$

**Shreve Ch. 4.2:** Itô isometry extends integral to \\(L^2\\) integrands."""),
        code("""# Itô isometry: Var(∫ H dW) = E[∫ H² dt]
rng = np.random.default_rng(31)
T, n = 1.0, 500
dt = T / n
n_sims = 10_000
H = rng.uniform(0, 1, size=n)  # random simple integrand

integrals = np.array([
    np.sum(H * rng.normal(0, np.sqrt(dt), size=n))
    for _ in range(n_sims)
])
var_sim = integrals.var()
theory = np.sum(H**2) * dt
print(f"Var(∫H dW) sim = {var_sim:.4f}, E[∫H²dt] = {theory:.4f}")"""),
        md("""---
# Part 3 — Quadratic Variation of Integrals

For \\(I_t = \\int_0^t H_s\\, dW_s\\), \\([I, I]_t = \\int_0^t H_s^2\\, ds\\).

Combined with \\(W\\): \\(W_t^2 - t\\) is a martingale (preview of Itô's lemma).

**Shreve Ch. 4.2:** quadratic variation of Itô integrals."""),
        code("""# W_t² - t has zero mean (martingale)
rng = np.random.default_rng(32)
T, n_steps, n_sims = 1.0, 500, 20_000
dt = T / n_steps
means = []
for _ in range(n_sims):
    dW = rng.normal(0, np.sqrt(dt), size=n_steps)
    W = np.cumsum(dW)
    W_T = W[-1]
    means.append(W_T**2 - T)
print(f"E[W_T² - T] = {np.mean(means):.4f} (theory 0)")"""),
        md("""---
# Part 4 — Extending to \\(L^2\\) Integrands

Process \\(H\\) is in \\(\\mathcal{L}^2\\) if \\(E[\\int_0^T H_t^2 dt] < \\infty\\). Approximate by simple processes; integral defined via Itô isometry limit.

**Shreve Ch. 4.3:** closure of simple integrands in \\(L^2\\)."""),
        code("""# ∫₀¹ W_t dW_t via discrete approximation (left endpoints)
def ito_integral_W(seed=33):
    rng = np.random.default_rng(seed)
    T, n = 1.0, 2000
    dt = T / n
    dW = rng.normal(0, np.sqrt(dt), size=n)
    W = np.concatenate([[0], np.cumsum(dW)])
    # H_t = W_{t_i} on (t_i, t_{i+1}]
    integral = np.sum(W[:-1] * dW)
    return integral

ints = [ito_integral_W(seed=s) for s in range(5000)]
# Itô: ∫ W dW = (W_T² - T)/2
print(f"∫ W dW: mean={np.mean(ints):.4f}, var={np.var(ints):.4f}")
print("Itô lemma predicts E[∫ W dW] = 0")"""),
        md("**Your turn:** Compare left-endpoint vs midpoint (Stratonovich) for \\(\\int W\\, dW\\). Which gives zero mean?"),
    ],
    "problems": [
        "For constant \\(H_t = c\\), show \\(E[\\int_0^T c\\, dW_t] = 0\\) and \\(\\text{Var} = c^2 T\\).",
        "Prove Itô isometry for a simple process with non-random \\(H_i\\).",
        "Show \\(M_t = W_t^2 - t\\) is a martingale (compute \\(E[W_{t+\\Delta}^2 \\mid W_t]\\)).",
        "Why must we use left endpoints in the Itô integral definition?",
    ],
    "solutions": """**1.** Integral is \\(c W_T\\), mean 0, var \\(c^2 T\\).

**2.** Expand square of sum; cross terms have zero expectation by independent increments.

**3.** \\(E[W_{t+\\Delta}^2] = W_t^2 + \\Delta\\), so \\(E[W_{t+\\Delta}^2 - (t+\\Delta) \\mid W_t] = W_t^2 - t\\).

**4.** Left endpoints make increment \\(W_{t_{i+1}}-W_{t_i}\\) independent of \\(H_{t_i}\\); midpoint would correlate \\(H\\) with future increment.""",
    "reading_ch": "4",
}

# ── Week 5 ──────────────────────────────────────────────────────────
NOTEBOOKS["week05_ito_lemma_applications.ipynb"] = {
    "meta": (5, "Itô's Lemma and Applications", "Ch. 4"),
    "parts_table": """| Part | Topic | Shreve |
|------|-------|--------|
| 1 | **Itô's lemma (1D)** | Ch. 4.4 |
| 2 | **\\(dW_t^2 = 2W_t dW_t + dt\\)** | Ch. 4.4 |
| 3 | **Geometric Brownian motion** | Ch. 4.4 |
| 4 | **Log-price dynamics** | Ch. 4.4 |
| — | **Problem set** | Ch. 4 |""",
    "cells": [
        md("""---
# Part 1 — Itô's Lemma

For smooth \\(f(t,x)\\) and \\(X_t\\) satisfying \\(dX_t = \\mu_t\\, dt + \\sigma_t\\, dW_t\\):

$$df(t, X_t) = \\frac{\\partial f}{\\partial t} dt + \\frac{\\partial f}{\\partial x} dX_t + \\frac{1}{2}\\frac{\\partial^2 f}{\\partial x^2} (dX_t)^2$$

With \\((dW)^2 = dt\\), \\((dt)^2 = 0\\), \\(dW\\, dt = 0\\).

**Shreve Ch. 4.4:** Itô's lemma — the chain rule of stochastic calculus."""),
        code("""# Verify Itô for f(W) = W²: df = 2W dW + dt
rng = np.random.default_rng(40)
T, n = 1.0, 2000
dt = T / n
dW = rng.normal(0, np.sqrt(dt), size=n)
W = np.concatenate([[0], np.cumsum(dW)])

f = W**2
df_actual = f[1:] - f[:-1]
df_ito = 2 * W[:-1] * dW + dt

print(f"Mean df (actual): {df_actual.mean():.6f}")
print(f"Mean df (Itô):    {df_ito.mean():.6f} (theory dt={dt})")
print(f"Corr(actual, Itô): {np.corrcoef(df_actual, df_ito)[0,1]:.4f}")"""),
        md("""---
# Part 2 — Application: \\(W_t^2 - t\\) Martingale

Itô on \\(f(W) = W^2\\): \\(d(W^2) = 2W\\, dW + dt\\), so \\(d(W^2 - t) = 2W\\, dW\\) — pure martingale part.

**Shreve Ch. 4.4:** building martingales via Itô's lemma."""),
        code("""rng = np.random.default_rng(41)
T, n_steps = 1.0, 1000
dt = T / n_steps
n_paths = 50
fig, ax = plt.subplots()
for _ in range(n_paths):
    dW = rng.normal(0, np.sqrt(dt), size=n_steps)
    W = np.concatenate([[0], np.cumsum(dW)])
    t = np.linspace(0, T, n_steps + 1)
    ax.plot(t, W**2 - t, alpha=0.7)
ax.axhline(0, color="k", lw=1)
ax.set_title("W_t² - t (martingale paths)")
plt.show()"""),
        md("""---
# Part 3 — Geometric Brownian Motion

Stock model: \\(dS_t = \\mu S_t\\, dt + \\sigma S_t\\, dW_t\\).

Itô on \\(\\log S\\): \\(d\\log S_t = (\\mu - \\sigma^2/2) dt + \\sigma\\, dW_t\\).

Solution: \\(S_t = S_0 \\exp\\big((\\mu - \\sigma^2/2)t + \\sigma W_t\\big)\\).

**Shreve Ch. 4.4:** GBM as application of Itô's lemma."""),
        code("""def simulate_gbm(S0, mu, sigma, T, n_steps, seed=42):
    rng = np.random.default_rng(seed)
    dt = T / n_steps
    dW = rng.normal(0, np.sqrt(dt), size=n_steps)
    log_S = np.log(S0) + (mu - sigma**2/2)*dt + sigma*dW
    S = np.exp(np.concatenate([[np.log(S0)], np.log(S0) + np.cumsum(
        (mu - sigma**2/2)*dt + sigma*dW)]))
    return S

S0, mu, sigma, T = 100, 0.08, 0.2, 1.0
paths = [simulate_gbm(S0, mu, sigma, T, 252, seed=s) for s in range(20)]
fig, ax = plt.subplots()
for p in paths:
    ax.plot(p, alpha=0.7)
ax.set_title(f"GBM paths: μ={mu}, σ={sigma}")
plt.show()
print(f"E[S_T] theory = {S0*np.exp(mu*T):.2f}")"""),
        md("""---
# Part 4 — Exponential Martingale

\\(M_t = \\exp(\\sigma W_t - \\frac{1}{2}\\sigma^2 t)\\) satisfies \\(dM_t = \\sigma M_t\\, dW_t\\) — a martingale.

**Shreve Ch. 4.4:** exponential martingale (Radon-Nikodym preview)."""),
        code("""rng = np.random.default_rng(43)
sigma, T, n_steps = 0.3, 1.0, 1000
dt = T / n_steps
n_sims = 10_000
M_T = []
for _ in range(n_sims):
    dW = rng.normal(0, np.sqrt(dt), size=n_steps)
    W_T = np.sum(dW)
    M_T.append(np.exp(sigma * W_T - 0.5 * sigma**2 * T))
print(f"E[M_T] sim = {np.mean(M_T):.4f} (theory 1.0 martingale)")"""),
        md("**Your turn:** Apply Itô to \\(f(S) = S^2\\) when \\(dS = \\mu S\\, dt + \\sigma S\\, dW\\)."),
    ],
    "problems": [
        "Apply Itô's lemma to \\(f(x) = e^x\\) with \\(dX = \\mu dt + \\sigma dW\\).",
        "Derive \\(d(S_t^2)\\) for GBM.",
        "Show \\(Y_t = e^{\\sigma W_t - \\frac{1}{2}\\sigma^2 t}\\) is a martingale.",
        "For \\(f(t,W_t) = t W_t\\), compute \\(df\\) using Itô's lemma.",
    ],
    "solutions": """**1.** \\(df = e^X(\\mu + \\frac{1}{2}\\sigma^2) dt + \\sigma e^X dW\\).

**2.** \\(d(S^2) = 2S dS + (dS)^2 = (2\\mu + \\sigma^2)S^2 dt + 2\\sigma S^2 dW\\).

**3.** Itô on log gives \\(d\\log Y = \\sigma dW\\), so \\(Y\\) is stochastic exponential of \\(\\sigma W\\).

**4.** \\(df = W_t dt + t dW_t\\).""",
    "reading_ch": "4",
}

# ── Week 6 ──────────────────────────────────────────────────────────
NOTEBOOKS["week06_black_scholes_merton.ipynb"] = {
    "meta": (6, "Black-Scholes-Merton Model", "Ch. 4"),
    "parts_table": """| Part | Topic | Shreve |
|------|-------|--------|
| 1 | **BSM PDE** | Ch. 4.5 |
| 2 | **European call formula** | Ch. 4.5 |
| 3 | **Delta hedging** | Ch. 4.5 |
| 4 | **Put-call parity** | Ch. 4.5 |
| — | **Problem set** | Ch. 4 |""",
    "cells": [
        md("""---
# Part 1 — The BSM Partial Differential Equation

Under risk-neutral measure: \\(dS_t = r S_t\\, dt + \\sigma S_t\\, dW_t\\).

For derivative \\(V(t,S)\\), Itô + self-financing portfolio gives:

$$\\frac{\\partial V}{\\partial t} + rS\\frac{\\partial V}{\\partial S} + \\frac{1}{2}\\sigma^2 S^2 \\frac{\\partial^2 V}{\\partial S^2} = rV$$

**Shreve Ch. 4.5:** derivation of BSM PDE via hedging."""),
        code("""def black_scholes_call(S, K, T, r, sigma):
    d1 = (np.log(S/K) + (r + 0.5*sigma**2)*T) / (sigma*np.sqrt(T))
    d2 = d1 - sigma*np.sqrt(T)
    return S*stats.norm.cdf(d1) - K*np.exp(-r*T)*stats.norm.cdf(d2)

S, K, T, r, sigma = 100, 100, 1.0, 0.05, 0.2
C = black_scholes_call(S, K, T, r, sigma)
print(f"BS call price C = {C:.4f}")"""),
        md("""---
# Part 2 — European Call Closed Form

$$C = S_0 \\Phi(d_1) - K e^{-rT} \\Phi(d_2)$$

where \\(d_1 = \\frac{\\ln(S_0/K) + (r + \\sigma^2/2)T}{\\sigma\\sqrt{T}}\\), \\(d_2 = d_1 - \\sigma\\sqrt{T}\\).

**Shreve Ch. 4.5:** solving PDE / risk-neutral expectation."""),
        code("""# Monte Carlo under risk-neutral measure
rng = np.random.default_rng(50)
S0, K, T, r, sigma = 100, 100, 1.0, 0.05, 0.2
n = 500_000
Z = rng.standard_normal(n)
S_T = S0 * np.exp((r - 0.5*sigma**2)*T + sigma*np.sqrt(T)*Z)
payoff = np.maximum(S_T - K, 0)
mc_price = np.exp(-r*T) * payoff.mean()
bs_price = black_scholes_call(S0, K, T, r, sigma)
print(f"MC price     = {mc_price:.4f}")
print(f"BS formula   = {bs_price:.4f}")"""),
        md("""---
# Part 3 — Delta Hedging

\\(\\Delta = \\frac{\\partial C}{\\partial S} = \\Phi(d_1)\\). Hold \\(\\Delta\\) shares + bond to replicate call.

**Shreve Ch. 4.5:** delta-hedging argument for PDE."""),
        code("""def bs_delta(S, K, T, r, sigma):
    d1 = (np.log(S/K) + (r + 0.5*sigma**2)*T) / (sigma*np.sqrt(T))
    return stats.norm.cdf(d1)

# Simple delta hedge simulation
rng = np.random.default_rng(51)
n_steps = 252
dt = T / n_steps
S_path = [S0]
for _ in range(n_steps):
    dW = rng.normal(0, np.sqrt(dt))
    S_path.append(S_path[-1] * np.exp((r-0.5*sigma**2)*dt + sigma*dW))
S_path = np.array(S_path)
deltas = [bs_delta(s, K, T - i*dt, r, sigma) for i, s in enumerate(S_path)]
print(f"Delta at S0: {deltas[0]:.4f}")
print(f"Delta at end: {deltas[-1]:.4f} (should → 0 or 1)")"""),
        md("""---
# Part 4 — Put-Call Parity

$$C - P = S_0 - K e^{-rT}$$

No arbitrage relationship between European call and put.

**Shreve Ch. 4.5:** put-call parity."""),
        code("""def black_scholes_put(S, K, T, r, sigma):
    d1 = (np.log(S/K) + (r + 0.5*sigma**2)*T) / (sigma*np.sqrt(T))
    d2 = d1 - sigma*np.sqrt(T)
    return K*np.exp(-r*T)*stats.norm.cdf(-d2) - S*stats.norm.cdf(-d1)

C = black_scholes_call(S0, K, T, r, sigma)
P = black_scholes_put(S0, K, T, r, sigma)
parity = C - P - (S0 - K*np.exp(-r*T))
print(f"C - P           = {C-P:.4f}")
print(f"S - Ke^{-rT}    = {S0 - K*np.exp(-r*T):.4f}")
print(f"Parity residual = {parity:.6f}")"""),
        md("**Your turn:** Plot call price vs \\(S_0\\) and overlay intrinsic value \\(\\max(S-K,0)\\)."),
    ],
    "problems": [
        "Derive the BSM PDE for \\(V(t,S)\\) using Itô and a delta-hedged portfolio.",
        "Verify put-call parity from the BS formulas.",
        "What is \\(\\Delta\\) for a deep ITM call as \\(T \\to 0\\)?",
        "Compute \\(\\Gamma = \\partial^2 C / \\partial S^2\\) and interpret.",
    ],
    "solutions": """**1.** Portfolio \\(\\Pi = V - \\Delta S\\); apply Itô, choose \\(\\Delta = \\partial V/\\partial S\\) to kill \\(dW\\), bond position \\(r\\Pi\\).

**2.** Algebra using \\(\\Phi(-x) = 1 - \\Phi(x)\\).

**3.** \\(\\Delta \\to 1\\) for \\(S > K\\).

**4.** \\(\\Gamma = \\Phi'(d_1)/(S\\sigma\\sqrt{T})\\); sensitivity of delta to spot.""",
    "reading_ch": "4",
}

# ── Week 7 ──────────────────────────────────────────────────────────
NOTEBOOKS["week07_multivariable_stochastic_calculus.ipynb"] = {
    "meta": (7, "Multivariable Stochastic Calculus", "Ch. 4"),
    "parts_table": """| Part | Topic | Shreve |
|------|-------|--------|
| 1 | **Multi-dimensional Brownian motion** | Ch. 4.6 |
| 2 | **Itô lemma in \\(n\\) dimensions** | Ch. 4.6 |
| 3 | **Correlation & covariance** | Ch. 4.6 |
| 4 | **Two-asset model** | Ch. 4.6 |
| — | **Problem set** | Ch. 4 |""",
    "cells": [
        md("""---
# Part 1 — Multidimensional Brownian Motion

\\(W_t = (W_t^{(1)}, \\ldots, W_t^{(d)})\\) with independent components, \\(E[W_t^{(i)} W_t^{(j)}] = \\min(t,s)\\, \\delta_{ij}\\).

**Shreve Ch. 4.6:** vector Brownian motion."""),
        code("""rng = np.random.default_rng(60)
T, n = 1.0, 1000
dt = T / n
dW = rng.normal(0, np.sqrt(dt), size=(n, 2))
W = np.cumsum(dW, axis=0)
corr = np.corrcoef(W[:, 0], W[:, 1])[0, 1]
print(f"Corr(W¹, W²) at T = {corr:.4f} (theory 0)")"""),
        md("""---
# Part 2 — Itô's Lemma (Several Variables)

For \\(f(t, X_t^{(1)}, \\ldots, X_t^{(n)})\\) with \\(dX^{(i)} = \\mu_i dt + \\sum_j \\sigma_{ij} dW^{(j)}\\):

$$df = \\frac{\\partial f}{\\partial t}dt + \\sum_i \\frac{\\partial f}{\\partial x_i} dX^{(i)} + \\frac{1}{2}\\sum_{i,j}\\frac{\\partial^2 f}{\\partial x_i \\partial x_j} d[X^{(i)}, X^{(j)}]$$

**Shreve Ch. 4.6:** multi-dimensional Itô."""),
        code("""# f(W1, W2) = W1 * W2: df = W2 dW1 + W1 dW2 (no dt term)
rng = np.random.default_rng(61)
dt = 1/1000
dW1 = rng.normal(0, np.sqrt(dt), 1000)
dW2 = rng.normal(0, np.sqrt(dt), 1000)
W1 = np.cumsum(dW1)
W2 = np.cumsum(dW2)
f = W1 * W2
df = f[1:] - f[:-1]
df_ito = W2[:-1]*dW1 + W1[:-1]*dW2
print(f"Corr(df, Itô approx) = {np.corrcoef(df, df_ito)[0,1]:.4f}")"""),
        md("""---
# Part 3 — Correlated Brownian Motions

Build \\(B_1 = W_1\\), \\(B_2 = \\rho W_1 + \\sqrt{1-\\rho^2} W_2\\) from independent \\(W_1, W_2\\).

**Shreve Ch. 4.6:** correlation structure."""),
        code("""rho = 0.7
rng = np.random.default_rng(62)
n = 200_000
Z1 = rng.standard_normal(n)
Z2 = rng.standard_normal(n)
B1 = Z1
B2 = rho*Z1 + np.sqrt(1-rho**2)*Z2
print(f"Corr(B1,B2) = {np.corrcoef(B1,B2)[0,1]:.4f} (ρ={rho})")"""),
        md("""---
# Part 4 — Two Correlated Stocks

\\(dS_1 = \\mu_1 S_1 dt + \\sigma_1 S_1 dB_1\\), \\(dS_2 = \\mu_2 S_2 dt + \\sigma_2 S_2 dB_2\\) with correlated \\(B_1, B_2\\).

**Shreve Ch. 4.6:** multi-asset GBM (preview of Ch. 5)."""),
        code("""def simulate_two_stocks(S01, S02, mu1, mu2, sig1, sig2, rho, T, n, seed=63):
    rng = np.random.default_rng(seed)
    dt = T / n
    Z1 = rng.standard_normal(n)
    Z2 = rng.standard_normal(n)
    dB1 = np.sqrt(dt) * Z1
    dB2 = np.sqrt(dt) * (rho*Z1 + np.sqrt(1-rho**2)*Z2)
    S1 = S01 * np.exp(np.cumsum((mu1-0.5*sig1**2)*dt + sig1*dB1))
    S2 = S02 * np.exp(np.cumsum((mu2-0.5*sig2**2)*dt + sig2*dB2))
    return S1, S2

S1, S2 = simulate_two_stocks(100, 100, 0.08, 0.06, 0.2, 0.25, 0.6, 1, 252)
print(f"Return corr = {np.corrcoef(np.diff(np.log(S1)), np.diff(np.log(S2)))[0,1]:.4f}")"""),
        md("**Your turn:** Derive \\(d(S_1 S_2)\\) for correlated GBMs using multi-dimensional Itô."),
    ],
    "problems": [
        "Write Itô's lemma for \\(f(W_t^{(1)}, W_t^{(2)}) = W^{(1)} W^{(2)}\\).",
        "How do you construct Brownian motions with correlation matrix \\(\\Sigma\\)?",
        "For two stocks with correlation \\(\\rho\\), find \\(d(S_1 S_2)\\).",
        "State the multidimensional Itô formula for \\(n\\) processes.",
    ],
    "solutions": """**1.** \\(df = W^{(2)} dW^{(1)} + W^{(1)} dW^{(2)}\\) (no \\(dt\\) since independent).

**2.** Cholesky: \\(\\Sigma = L L^\\top\\), \\(B = L Z\\) for standard normal \\(Z\\).

**3.** Product rule + \\((dS_1)(dS_2) = \\rho \\sigma_1 \\sigma_2 S_1 S_2 dt\\).

**4.** See Shreve Ch. 4.6 Eq. with \\(d[X^{(i)},X^{(j)}]\\) terms.""",
    "reading_ch": "4",
}

# ── Week 8 — Midterm Review ─────────────────────────────────────────
NOTEBOOKS["week08_midterm_review.ipynb"] = {
    "meta": (8, "Midterm Review", "Ch. 1–4"),
    "parts_table": """| Part | Topic | Shreve |
|------|-------|--------|
| 1 | **Brownian motion facts** | Ch. 3 |
| 2 | **Itô integral & isometry** | Ch. 4.1–4.3 |
| 3 | **Itô's lemma & GBM** | Ch. 4.4 |
| 4 | **BSM & delta hedging** | Ch. 4.5 |
| — | **Midterm problem set** | Ch. 1–4 |""",
    "cells": [
        md("""---
# Part 1 — Brownian Motion Checklist

- \\(W_0 = 0\\), continuous paths, independent increments
- \\(W_t - W_s \\sim N(0, t-s)\\)
- \\(E[W_t W_s] = \\min(t,s)\\)
- Markov property, reflection principle
- \\(P(\\max_{0\\leq t\\leq T} W_t \\geq a) = 2P(W_T \\geq a)\\)

**Shreve Ch. 3**"""),
        code("""# Quick BM verification suite
rng = np.random.default_rng(80)
T, n = 1.0, 1000
dt = T/n
dW = rng.normal(0, np.sqrt(dt), size=(50_000, n))
W_T = dW.sum(axis=1)
print(f"E[W_T] = {W_T.mean():.4f}, Var = {W_T.var():.4f} (0, 1)")
print(f"QV mean = {(dW**2).sum(axis=1).mean():.4f} (1)")"""),
        md("""---
# Part 2 — Itô Integral Essentials

- Simple integrands: \\(\\int H\\, dW = \\sum H_i \\Delta W_i\\) (left endpoints)
- Itô isometry: \\(E[(\\int H\\, dW)^2] = E[\\int H^2 dt]\\)
- \\(W_t^2 - t\\) is a martingale

**Shreve Ch. 4.1–4.3**"""),
        code("""# ∫₀¹ 1 dW ~ N(0,1)
rng = np.random.default_rng(81)
ints = rng.normal(0, 1, 100_000)  # exact distribution
print(f"P(int > 1) sim = {(ints>1).mean():.4f}, theory = {1-stats.norm.cdf(1):.4f}")"""),
        md("""---
# Part 3 — Itô's Lemma & GBM

$$df = \\frac{\\partial f}{\\partial t}dt + \\frac{\\partial f}{\\partial x}dX + \\frac{1}{2}\\frac{\\partial^2 f}{\\partial x^2}(dX)^2$$

GBM: \\(S_t = S_0 \\exp((\\mu-\\sigma^2/2)t + \\sigma W_t)\\).

**Shreve Ch. 4.4**"""),
        code("""# GBM mean: E[S_T] = S_0 e^{μT}
S0, mu, sigma, T = 100, 0.1, 0.2, 1
rng = np.random.default_rng(82)
Z = rng.standard_normal(100_000)
S_T = S0 * np.exp((mu-0.5*sigma**2)*T + sigma*np.sqrt(T)*Z)
print(f"E[S_T] sim = {S_T.mean():.2f}, theory = {S0*np.exp(mu*T):.2f}")"""),
        md("""---
# Part 4 — BSM Summary

PDE: \\(\\frac{\\partial V}{\\partial t} + rS\\frac{\\partial V}{\\partial S} + \\frac{1}{2}\\sigma^2 S^2 \\frac{\\partial^2 V}{\\partial S^2} = rV\\)

Call: \\(C = S\\Phi(d_1) - Ke^{-rT}\\Phi(d_2)\\). Delta = \\(\\Phi(d_1)\\).

**Shreve Ch. 4.5**"""),
        md("**Your turn:** Without looking, write the definition of martingale and derive BSM PDE outline."),
    ],
    "problems": [
        "State Markov property of \\(W_t\\) and prove \\(E[W_t W_s] = \\min(t,s)\\).",
        "Compute \\(E[\\int_0^T W_t\\, dW_t]\\) using Itô's lemma on \\(W^2\\).",
        "Derive \\(d(\\log S_t)\\) for GBM and solve for \\(S_t\\).",
        "A call has \\(S=100, K=100, T=1, r=0.05, \\sigma=0.2\\). Find \\(C\\), \\(\\Delta\\), and verify put-call parity.",
        "Using reflection, find \\(P(\\tau_1 \\leq 1)\\) for first passage to level 1.",
    ],
    "solutions": """**1.** Markov: future independent of past given present. For \\(t>s\\): \\(E[W_t W_s]=E[W_s^2]=s\\).

**2.** \\(W_T^2 = 2\\int W dW + T\\), so \\(E[\\int W dW] = 0\\).

**3.** \\(d\\log S = (\\mu-\\sigma^2/2)dt + \\sigma dW\\); integrate to get log-normal solution.

**4.** \\(C \\approx 10.45\\), \\(\\Delta \\approx 0.64\\); parity: \\(C-P = S-Ke^{-rT}\\).

**5.** \\(P(\\tau_1 \\leq 1) = 2P(W_1 \\geq 1) = 2(1-\\Phi(1)) \\approx 0.317\\).""",
    "reading_ch": "1–4",
}

# ── Week 9 ──────────────────────────────────────────────────────────
NOTEBOOKS["week09_risk_neutral_girsanov.ipynb"] = {
    "meta": (9, "Risk-Neutral Measure & Girsanov", "Ch. 5"),
    "parts_table": """| Part | Topic | Shreve |
|------|-------|--------|
| 1 | **Change of measure** | Ch. 5.1 |
| 2 | **Radon-Nikodym derivative** | Ch. 5.1 |
| 3 | **Girsanov theorem** | Ch. 5.2 |
| 4 | **Risk-neutral pricing** | Ch. 5.2 |
| — | **Problem set** | Ch. 5 |""",
    "cells": [
        md("""---
# Part 1 — Change of Probability Measure

Under \\(P\\), stock may have drift \\(\\mu\\). Under equivalent \\(Q\\), discounted price is martingale: \\(d(e^{-rt}S_t) = e^{-rt}\\sigma S_t\\, dW_t^Q\\).

**Shreve Ch. 5.1:** motivation for risk-neutral measure."""),
        code("""# Under P: E[S_T] = S_0 e^{μT}; under Q: E^Q[e^{-rT} S_T] = S_0
S0, mu, r, sigma, T = 100, 0.12, 0.05, 0.2, 1.0
rng = np.random.default_rng(90)
n = 200_000
# P measure
Z = rng.standard_normal(n)
S_T_P = S0 * np.exp((mu-0.5*sigma**2)*T + sigma*np.sqrt(T)*Z)
# Q measure: drift r instead of mu
S_T_Q = S0 * np.exp((r-0.5*sigma**2)*T + sigma*np.sqrt(T)*Z)
print(f"E[S_T] under P     = {S_T_P.mean():.2f} (S0 e^μT = {S0*np.exp(mu*T):.2f})")
print(f"E[e^{-rT}S_T] under Q = {np.exp(-r*T)*S_T_Q.mean():.2f} (S0 = {S0})")"""),
        md("""---
# Part 2 — Radon-Nikodym Derivative

$$\\frac{dQ}{dP} = Z_T = \\exp\\left(-\\theta W_T - \\frac{1}{2}\\theta^2 T\\right), \\quad \\theta = \\frac{\\mu - r}{\\sigma}$$

\\(Z_t\\) is a \\(P\\)-martingale with \\(E[Z_T] = 1\\).

**Shreve Ch. 5.1:** exponential martingale as density."""),
        code("""theta = (mu - r) / sigma
rng = np.random.default_rng(91)
Z_T = []
for _ in range(10_000):
    W_T = rng.normal(0, np.sqrt(T))
    Z_T.append(np.exp(-theta*W_T - 0.5*theta**2*T))
print(f"E[Z_T] sim = {np.mean(Z_T):.4f} (theory 1)")"""),
        md("""---
# Part 3 — Girsanov Theorem

Under \\(Q\\), define \\(W_t^Q = W_t + \\theta t\\). Then \\(W^Q\\) is Brownian motion under \\(Q\\).

Transforms drift: \\(\\mu S\\, dt + \\sigma S\\, dW \\Rightarrow r S\\, dt + \\sigma S\\, dW^Q\\).

**Shreve Ch. 5.2:** Girsanov theorem."""),
        code("""# Girsanov: W^Q = W + θt has same law under Q as W under P
rng = np.random.default_rng(92)
n = 100_000
W_T = rng.normal(0, np.sqrt(T), size=n)
W_Q_T = W_T + theta * T
print(f"W_T under P:  mean={W_T.mean():.4f}, var={W_T.var():.4f}")
print(f"W^Q_T under Q: mean={W_Q_T.mean():.4f}, var={W_Q_T.var():.4f}")
print(f"θT = {theta*T:.4f}")"""),
        md("""---
# Part 4 — Risk-Neutral Pricing

Derivative price: \\(V_0 = E^Q[e^{-rT} g(S_T)]\\).

Same expectation under \\(Q\\) gives BSM without real-world drift \\(\\mu\\).

**Shreve Ch. 5.2:** pricing by risk-neutral expectation."""),
        code("""K = 100
payoff = np.maximum(S_T_Q - K, 0)
price = np.exp(-r*T) * payoff.mean()
# BS reference
d1 = (np.log(S0/K)+(r+0.5*sigma**2)*T)/(sigma*np.sqrt(T))
d2 = d1 - sigma*np.sqrt(T)
bs = S0*stats.norm.cdf(d1) - K*np.exp(-r*T)*stats.norm.cdf(d2)
print(f"Risk-neutral MC = {price:.4f}, BS = {bs:.4f}")"""),
        md("**Your turn:** Why does option price not depend on \\(\\mu\\)?"),
    ],
    "problems": [
        "Define equivalent probability measures \\(P\\) and \\(Q\\).",
        "Show \\(Z_t = \\exp(-\\theta W_t - \\frac{1}{2}\\theta^2 t)\\) is a \\(P\\)-martingale.",
        "Apply Girsanov to transform GBM drift from \\(\\mu\\) to \\(r\\).",
        "Price a digital call (payoff \\(1_{S_T > K}\\)) under \\(Q\\).",
    ],
    "solutions": """**1.** \\(Q(A)=0 \\iff P(A)=0\\); same null sets; \\(Q(\\Omega)=1\\).

**2.** Itô on \\(\\log Z_t\\) gives \\(d\\log Z = -\\theta dW - \\frac{1}{2}\\theta^2 dt\\), so \\(dZ = -\\theta Z dW\\) (martingale).

**3.** \\(dW^Q = dW + \\theta dt\\), \\(\\theta=(\\mu-r)/\\sigma\\); substitute into \\(dS\\).

**4.** \\(V_0 = e^{-rT} Q(S_T > K) = e^{-rT}\\Phi(d_2)\\).""",
    "reading_ch": "5",
}

# ── Week 10 ─────────────────────────────────────────────────────────
NOTEBOOKS["week10_multidimensional_stock_model.ipynb"] = {
    "meta": (10, "Multidimensional Stock Model", "Ch. 5"),
    "parts_table": """| Part | Topic | Shreve |
|------|-------|--------|
| 1 | **Multi-asset GBM** | Ch. 5.3 |
| 2 | **Correlation & Cholesky** | Ch. 5.3 |
| 3 | **Portfolio of options** | Ch. 5.3 |
| 4 | **Diversification** | Ch. 5.3 |
| — | **Problem set** | Ch. 5 |""",
    "cells": [
        md("""---
# Part 1 — Multi-Asset GBM

\\(dS_i = r S_i\\, dt + \\sigma_i S_i\\, dB_i\\) under \\(Q\\), with correlated Brownian drivers.

Discounted prices \\(e^{-rt}S_t\\) are martingales under \\(Q\\).

**Shreve Ch. 5.3:** multidimensional stock model."""),
        code("""def multi_gbm(S0, sigmas, rho_matrix, r, T, n_steps, seed=100):
    m = len(S0)
    rng = np.random.default_rng(seed)
    dt = T / n_steps
    L = np.linalg.cholesky(rho_matrix)
    S = np.array(S0, dtype=float)
    paths = [S.copy()]
    for _ in range(n_steps):
        Z = rng.standard_normal(m)
        dB = np.sqrt(dt) * (L @ Z)
        S = S * np.exp((r - 0.5*np.array(sigmas)**2)*dt + np.array(sigmas)*dB)
        paths.append(S.copy())
    return np.array(paths)

S0 = [100, 50, 80]
sigmas = [0.2, 0.3, 0.25]
rho = np.array([[1, 0.5, 0.3], [0.5, 1, 0.4], [0.3, 0.4, 1]])
paths = multi_gbm(S0, sigmas, rho, 0.05, 1.0, 252)
print(f"Final prices: {paths[-1]}")"""),
        md("""---
# Part 2 — Correlation via Cholesky

Correlation matrix \\(\\rho\\) → Cholesky \\(L\\) with \\(\\rho = LL^\\top\\). Independent \\(Z\\) → \\(B = LZ\\).

**Shreve Ch. 5.3:** constructing correlated BM."""),
        code("""rho2 = np.array([[1, 0.6], [0.6, 1]])
L = np.linalg.cholesky(rho2)
rng = np.random.default_rng(101)
Z = rng.standard_normal((100_000, 2))
B = (L @ Z.T).T
print(f"Target ρ=0.6, simulated = {np.corrcoef(B[:,0], B[:,1])[0,1]:.4f}")"""),
        md("""---
# Part 3 — Basket / Exchange Options

Price \\(e^{-rT} E^Q[(S_1(T) + S_2(T) - K)^+]\\) by Monte Carlo.

**Shreve Ch. 5.3:** multi-asset derivatives."""),
        code("""rng = np.random.default_rng(102)
n = 300_000
T, r, K = 1.0, 0.05, 150
S1_T = paths[-1, 0]  # reuse single path endpoint — resim for MC
# proper MC
dt = T/252
L = np.linalg.cholesky(rho2)
payoffs = []
for _ in range(n):
    Z = rng.standard_normal(2)
    dB = np.sqrt(T) * (L @ Z)
    S1 = 100*np.exp((r-0.5*0.2**2)*T + 0.2*dB[0])
    S2 = 50*np.exp((r-0.5*0.3**2)*T + 0.3*dB[1])
    payoffs.append(max(S1+S2-K, 0))
basket_price = np.exp(-r*T) * np.mean(payoffs)
print(f"Basket call (S1+S2-K)+ price ≈ {basket_price:.2f}")"""),
        md("""---
# Part 4 — Diversification Effect

Portfolio variance \\(\\sigma_p^2 = w^\\top \\Sigma w\\) with covariance \\(\\Sigma_{ij} = \\rho_{ij}\\sigma_i\\sigma_j\\).

Lower average correlation → lower portfolio vol for fixed weights.

**Shreve Ch. 5.3:** correlation risk."""),
        code("""w = np.array([0.4, 0.3, 0.3])
cov = np.outer(sigmas, sigmas) * rho
port_var = w @ cov @ w
port_vol = np.sqrt(port_var)
avg_vol = np.mean(sigmas)
print(f"Portfolio vol = {port_vol:.4f}, avg asset vol = {avg_vol:.4f}")
print(f"Diversification ratio = {avg_vol/port_vol:.2f}")"""),
        md("**Your turn:** How does basket option price change as \\(\\rho_{12}\\) increases?"),
    ],
    "problems": [
        "Write the multidimensional GBM under \\(Q\\) with correlation matrix \\(\\rho\\).",
        "Price a spread option on \\(S_1 - S_2\\) by simulation.",
        "Show discounted \\(S_i\\) are martingales under \\(Q\\).",
        "Find portfolio weights minimizing variance for two assets.",
    ],
    "solutions": """**1.** \\(dS_i = rS_i dt + \\sigma_i S_i \\sum_j L_{ij} dW_j\\) with \\(LL^\\top=\\rho\\).

**2.** MC: \\(e^{-rT} E[(S_1-S_2-K)^+]\\); correlation affects spread distribution.

**3.** \\(d(e^{-rt}S_i) = e^{-rt}\\sigma_i S_i dB_i^Q\\) — no drift under \\(Q\\).

**4.** \\(w^* = \\Sigma^{-1}1 / (1^\\top\\Sigma^{-1}1)\\) for min-var portfolio.""",
    "reading_ch": "5",
}

# ── Week 11 ─────────────────────────────────────────────────────────
NOTEBOOKS["week11_pdes_and_sdes.ipynb"] = {
    "meta": (11, "PDEs and SDEs", "Ch. 6"),
    "parts_table": """| Part | Topic | Shreve |
|------|-------|--------|
| 1 | **SDE formulation** | Ch. 6.1 |
| 2 | **Feynman-Kac formula** | Ch. 6.2 |
| 3 | **BSM PDE ↔ expectation** | Ch. 6.2 |
| 4 | **Euler-Maruyama simulation** | Ch. 6.1 |
| — | **Problem set** | Ch. 6 |""",
    "cells": [
        md("""---
# Part 1 — Stochastic Differential Equations

General SDE: \\(dX_t = \\mu(t,X_t)\\, dt + \\sigma(t,X_t)\\, dW_t\\).

**Strong solution:** pathwise uniqueness. **Weak solution:** distribution uniqueness.

**Shreve Ch. 6.1:** SDEs and existence."""),
        code("""# Ornstein-Uhlenbeck: dX = -κX dt + σ dW
def simulate_ou(x0, kappa, sigma, T, n, seed=110):
    rng = np.random.default_rng(seed)
    dt = T/n
    X = x0
    path = [X]
    for _ in range(n):
        dW = rng.normal(0, np.sqrt(dt))
        X = X + (-kappa*X)*dt + sigma*dW
        path.append(X)
    return np.array(path)

path = simulate_ou(1.0, 2.0, 0.3, 5.0, 1000)
plt.plot(path)
plt.title("Ornstein-Uhlenbeck path")
plt.show()"""),
        md("""---
# Part 2 — Feynman-Kac Formula

If \\(V(t,x) = E^Q[e^{-r(T-t)} g(X_T) \\mid X_t=x]\\) and SDE for \\(X\\), then \\(V\\) solves:

$$\\frac{\\partial V}{\\partial t} + \\mu\\frac{\\partial V}{\\partial x} + \\frac{1}{2}\\sigma^2\\frac{\\partial^2 V}{\\partial x^2} - rV = 0$$

**Shreve Ch. 6.2:** bridge between PDE and expectation."""),
        code("""# Feynman-Kac: E[g(W_T)] solves heat equation with terminal g
# For g(x)=x^2: V(0,0) = E[W_T^2] = T
T = 2.0
rng = np.random.default_rng(111)
W_T_sq = rng.normal(0, np.sqrt(T), 100_000)**2
print(f"E[W_T²] MC = {W_T_sq.mean():.4f}, PDE terminal = T = {T}")"""),
        md("""---
# Part 3 — BSM as Feynman-Kac

Call price = \\(E^Q[e^{-rT}(S_T-K)^+]\\) solves BSM PDE with \\(V(T,S)=\\max(S-K,0)\\).

**Shreve Ch. 6.2:** BSM PDE from Feynman-Kac."""),
        code("""# PDE finite difference (simple) vs MC
S0, K, T, r, sig = 100, 100, 1, 0.05, 0.2
# MC already done in week 6
rng = np.random.default_rng(112)
Z = rng.standard_normal(500_000)
S_T = S0*np.exp((r-0.5*sig**2)*T + sig*np.sqrt(T)*Z)
mc = np.exp(-r*T)*np.maximum(S_T-K,0).mean()
print(f"Feynman-Kac (MC) call price = {mc:.4f}")"""),
        md("""---
# Part 4 — Euler-Maruyama Scheme

\\(X_{n+1} = X_n + \\mu\\Delta t + \\sigma\\sqrt{\\Delta t}\\, Z_n\\).

Discretizes SDE for simulation and PDE via Monte Carlo.

**Shreve Ch. 6.1:** numerical SDE methods."""),
        code("""def euler_maruyama(mu_fn, sig_fn, x0, T, n, seed=113):
    rng = np.random.default_rng(seed)
    dt = T/n
    X = x0
    for _ in range(n):
        dW = rng.normal(0, np.sqrt(dt))
        X = X + mu_fn(X)*dt + sig_fn(X)*dW
    return X

# GBM terminal
em = [euler_maruyama(lambda x: r*x, lambda x: sig*x, S0, T, 1000, seed=s)
      for s in range(10_000)]
print(f"EM E[S_T] = {np.mean(em):.2f}, theory = {S0*np.exp(r*T):.2f}")"""),
        md("**Your turn:** Discretization error of Euler-Maruyama for GBM as \\(\\Delta t\\) decreases."),
    ],
    "problems": [
        "State Feynman-Kac formula linking PDE to expectation.",
        "Write OU SDE and its stationary distribution.",
        "Derive BSM PDE from Feynman-Kac for \\(V=E^Q[e^{-rT}(S_T-K)^+]\\).",
        "What is the order of strong error for Euler-Maruyama?",
    ],
    "solutions": """**1.** \\(V(t,x)=E[e^{-r(T-t)}g(X_T)|X_t=x]\\) solves \\(V_t + \\mu V_x + \\frac{1}{2}\\sigma^2 V_{xx} - rV=0\\).

**2.** \\(dX=-\\kappa X dt + \\sigma dW\\); stationary \\(N(0, \\sigma^2/(2\\kappa))\\).

**3.** \\(X=S\\): \\(\\mu=rS\\), \\(\\sigma=\\sigma S\\) gives BSM PDE.

**4.** Strong order \\(O(\\sqrt{\\Delta t})\\) typically for EM.""",
    "reading_ch": "6",
}

# ── Week 12 ─────────────────────────────────────────────────────────
NOTEBOOKS["week12_poisson_jump_diffusion.ipynb"] = {
    "meta": (12, "Poisson Processes & Jump Diffusion", "Ch. 11"),
    "parts_table": """| Part | Topic | Shreve |
|------|-------|--------|
| 1 | **Poisson process** | Ch. 11.1 |
| 2 | **Compound Poisson** | Ch. 11.2 |
| 3 | **Jump-diffusion model** | Ch. 11.3 |
| 4 | **Merton jump model** | Ch. 11.3 |
| — | **Problem set** | Ch. 11 |""",
    "cells": [
        md("""---
# Part 1 — Poisson Process

\\(N_t\\) with \\(N_0=0\\), independent increments, \\(N_t - N_s \\sim \\text{Poisson}(\\lambda(t-s))\\).

Inter-arrival times are \\(\\text{Exp}(\\lambda)\\).

**Shreve Ch. 11.1:** counting processes."""),
        code("""def simulate_poisson(lam, T, seed=120):
    rng = np.random.default_rng(seed)
    t, N = 0.0, 0
    times = [0]
    counts = [0]
    while t < T:
        dt = rng.exponential(1/lam)
        t += dt
        if t < T:
            N += 1
            times.append(t)
            counts.append(N)
    times.append(T)
    counts.append(N)
    return np.array(times), np.array(counts)

lam, T = 3.0, 5.0
times, counts = simulate_poisson(lam, T)
plt.step(times, counts, where="post")
plt.title(f"Poisson process λ={lam}")
plt.show()
print(f"N_T mean = {counts[-1]}, theory λT = {lam*T}")"""),
        md("""---
# Part 2 — Compound Poisson

\\(J_t = \\sum_{i=1}^{N_t} Y_i\\) with jump sizes \\(Y_i\\) i.i.d.

Used for cumulative random jumps.

**Shreve Ch. 11.2:** compound Poisson process."""),
        code("""rng = np.random.default_rng(121)
lam, T = 2.0, 3.0
n_jumps = rng.poisson(lam*T)
jump_sizes = rng.normal(0, 0.5, n_jumps)
J_T = jump_sizes.sum()
print(f"Compound Poisson J_T: mean sim over many runs...")
means = []
for s in range(5000):
    nj = rng.poisson(lam*T)
    means.append(rng.normal(0, 0.5, nj).sum())
print(f"E[J_T] = {np.mean(means):.4f} (theory 0)")"""),
        md("""---
# Part 3 — Jump-Diffusion SDE

\\(dS_t = \\mu S_t\\, dt + \\sigma S_t\\, dW_t + S_t\\, dJ_t\\)

Combines continuous diffusion with jumps.

**Shreve Ch. 11.3:** jump-diffusion models."""),
        code("""def simulate_merton_jump(S0, mu, sigma, lam, jump_mu, jump_sig, T, n, seed=122):
    rng = np.random.default_rng(seed)
    dt = T/n
    S = S0
    for _ in range(n):
        dW = rng.normal(0, np.sqrt(dt))
        # Poisson jump in interval
        nj = rng.poisson(lam*dt)
        jump = sum(rng.normal(jump_mu, jump_sig, nj)) if nj > 0 else 0
        S = S * np.exp((mu-0.5*sigma**2)*dt + sigma*dW + jump)
    return S

paths = [simulate_merton_jump(100, 0.08, 0.15, 2.0, -0.1, 0.2, 1, 252, seed=s)
         for s in range(20)]
for p in paths:
    plt.plot(p, alpha=0.7)
plt.title("Merton jump-diffusion paths")
plt.show()"""),
        md("""---
# Part 4 — Merton Model & Fat Tails

Jumps create **heavier tails** than pure GBM — better fit to short-term options.

**Shreve Ch. 11.3:** Merton (1976) jump-diffusion."""),
        code("""# Compare return distributions: GBM vs jump
rng = np.random.default_rng(123)
n = 50_000
gbm_rets = rng.normal(0.05/252, 0.2/np.sqrt(252), n)
jump_rets = []
for _ in range(n):
    r = rng.normal(0.05/252, 0.2/np.sqrt(252))
    if rng.random() < 2*1/252:
        r += rng.normal(-0.1, 0.2)
    jump_rets.append(r)
fig, ax = plt.subplots()
ax.hist(gbm_rets, bins=80, density=True, alpha=0.5, label="GBM")
ax.hist(jump_rets, bins=80, density=True, alpha=0.5, label="Jump")
ax.legend()
ax.set_title("Daily returns: GBM vs jump-diffusion")
plt.show()"""),
        md("**Your turn:** How does jump intensity \\(\\lambda\\) affect option implied volatility skew?"),
    ],
    "problems": [
        "Show inter-arrival times of Poisson(\\(\\lambda\\)) are Exp(\\(\\lambda\\)).",
        "For compound Poisson with \\(E[Y]=0\\), show \\(E[J_t]=0\\).",
        "Write log-return SDE for Merton model.",
        "Why do jumps matter for short-dated options?",
    ],
    "solutions": """**1.** \\(P(T_1>t)=P(N_t=0)=e^{-\\lambda t}\\) → Exp(\\(\\lambda\\)).

**2.** \\(E[J_t]=E[N_t]E[Y]=\\lambda t \\cdot 0=0\\).

**3.** \\(d\\log S = (\\mu-\\sigma^2/2)dt + \\sigma dW + d(\\sum Y_i)\\).

**4.** Short maturity: jump risk dominates diffusion; skew from asymmetric jumps.""",
    "reading_ch": "11",
}

# ── Week 13 ─────────────────────────────────────────────────────────
NOTEBOOKS["week13_exotic_options.ipynb"] = {
    "meta": (13, "Exotic Options", "Ch. 7"),
    "parts_table": """| Part | Topic | Shreve |
|------|-------|--------|
| 1 | **Barrier options** | Ch. 7.1 |
| 2 | **Asian options** | Ch. 7.2 |
| 3 | **Lookback options** | Ch. 7.3 |
| 4 | **Path-dependent payoffs** | Ch. 7 |
| — | **Problem set** | Ch. 7 |""",
    "cells": [
        md("""---
# Part 1 — Barrier Options

**Down-and-out call:** pays \\((S_T-K)^+\\) only if \\(S_t > B\\) for all \\(t \\leq T\\).

Cheaper than vanilla — knockout reduces value.

**Shreve Ch. 7.1:** barrier options via reflection / PDE."""),
        code("""def simulate_barrier_call(S0, K, B, r, sigma, T, n_steps, seed=130):
    rng = np.random.default_rng(seed)
    dt = T/n_steps
    S = S0
    alive = True
    for _ in range(n_steps):
        dW = rng.normal(0, np.sqrt(dt))
        S = S * np.exp((r-0.5*sigma**2)*dt + sigma*dW)
        if S <= B:
            alive = False
            break
    payoff = max(S-K, 0) if alive else 0
    return payoff

S0, K, B = 100, 100, 80
payoffs = [simulate_barrier_call(S0, K, B, 0.05, 0.2, 1, 252, seed=s)
           for s in range(50_000)]
barrier_price = np.exp(-0.05)*np.mean(payoffs)
print(f"Down-and-out call (B=80) ≈ {barrier_price:.4f}")"""),
        md("""---
# Part 2 — Asian Options

Payoff depends on **average** price: \\((\\bar{S} - K)^+\\) where \\(\\bar{S} = \\frac{1}{n}\\sum S_{t_i}\\).

Path-dependent; no closed form for arithmetic average under GBM.

**Shreve Ch. 7.2:** Asian options — MC pricing."""),
        code("""def asian_call_mc(S0, K, r, sigma, T, n_steps, n_sims=50_000, seed=131):
    rng = np.random.default_rng(seed)
    dt = T/n_steps
    prices = []
    for _ in range(n_sims):
        S = S0
        path = []
        for _ in range(n_steps):
            dW = rng.normal(0, np.sqrt(dt))
            S = S*np.exp((r-0.5*sigma**2)*dt + sigma*dW)
            path.append(S)
        avg_S = np.mean(path)
        prices.append(max(avg_S-K, 0))
    return np.exp(-r*T)*np.mean(prices)

asian = asian_call_mc(100, 100, 0.05, 0.2, 1, 252)
print(f"Asian call price ≈ {asian:.4f}")"""),
        md("""---
# Part 3 — Lookback Options

**Floating strike lookback call:** payoff \\(S_T - S_{\\min}\\).

Benefit from lowest price over horizon.

**Shreve Ch. 7.3:** lookback options."""),
        code("""def lookback_call_mc(S0, r, sigma, T, n_steps, n_sims=30_000, seed=132):
    rng = np.random.default_rng(seed)
    dt = T/n_steps
    payoffs = []
    for _ in range(n_sims):
        S = S0
        S_min = S0
        for _ in range(n_steps):
            dW = rng.normal(0, np.sqrt(dt))
            S = S*np.exp((r-0.5*sigma**2)*dt + sigma*dW)
            S_min = min(S_min, S)
        payoffs.append(S - S_min)
    return np.exp(-r*T)*np.mean(payoffs)

lookback = lookback_call_mc(100, 0.05, 0.2, 1, 252)
print(f"Lookback call ≈ {lookback:.4f}")"""),
        md("""---
# Part 4 — Path Dependence & MC

Exotics require **full path simulation** — Feynman-Kac on augmented state or direct MC under \\(Q\\).

**Shreve Ch. 7:** general path-dependent derivatives."""),
        code("""# Vanilla vs Asian vs Barrier comparison
vanilla_mc = np.exp(-0.05)*np.mean([
    max(100*np.exp((0.05-0.5*0.2**2)*1 + 0.2*np.sqrt(1)*np.random.default_rng(s).standard_normal()), 100)-100
    for s in range(50_000)])
print(f"Vanilla call  ≈ {vanilla_mc:.4f}")
print(f"Asian call    ≈ {asian:.4f}")
print(f"Barrier call  ≈ {barrier_price:.4f}")
print(f"Lookback call ≈ {lookback:.4f}")"""),
        md("**Your turn:** Why is Asian call cheaper than vanilla for ATM options?"),
    ],
    "problems": [
        "Define down-and-in put and its relationship to down-and-out put.",
        "Price arithmetic Asian call by MC with 95% CI.",
        "How does barrier level \\(B\\) affect down-and-out call price?",
        "Compare lookback vs vanilla call at \\(S_0=100\\).",
    ],
    "solutions": """**1.** Down-and-in pays if barrier hit; in+out ≈ vanilla by parity on barrier segment.

**2.** MC with \\(n\\) paths, CI \\(\\hat{V} \\pm 1.96\\, \\hat{\\sigma}/\\sqrt{n}\\).

**3.** Lower \\(B\\) (closer to \\(S_0\\)) → higher knockout prob → lower price.

**4.** Lookback > vanilla: guaranteed positive payoff \\(S_T - S_{\\min} \\geq 0\\).""",
    "reading_ch": "7",
}

# ── Week 14 — Review ────────────────────────────────────────────────
NOTEBOOKS["week14_review_catchup.ipynb"] = {
    "meta": (14, "Review & Catch-up", "Ch. 1–7, 11"),
    "parts_table": """| Part | Topic | Shreve |
|------|-------|--------|
| 1 | **Course map** | All chapters |
| 2 | **BM → Itô → BSM pipeline** | Ch. 3–4 |
| 3 | **Risk-neutral & multi-asset** | Ch. 5 |
| 4 | **SDEs, jumps, exotics** | Ch. 6, 7, 11 |
| — | **Comprehensive problem set** | Full course |""",
    "cells": [
        md("""---
# Part 1 — Course Map

| Week | Topic | Shreve |
|------|-------|--------|
| 1–2 | Probability, RW, BM | Ch. 1–3 |
| 3 | Markov, reflection, passage | Ch. 3 |
| 4–7 | Itô calculus, BSM, multi-D | Ch. 4 |
| 9–10 | Risk-neutral, Girsanov | Ch. 5 |
| 11 | PDEs & SDEs | Ch. 6 |
| 12 | Jumps | Ch. 11 |
| 13 | Exotics | Ch. 7 |

**Shreve Vol II** — [PDF link]({SHREVE_URL})""".replace("{SHREVE_URL}", SHREVE_URL)),
        md("""---
# Part 2 — Core Pipeline

1. Build \\(W_t\\) (Ch. 3)
2. Define \\(\\int H\\, dW\\) (Ch. 4.1–4.3)
3. Itô's lemma → GBM (Ch. 4.4)
4. Hedge → BSM PDE (Ch. 4.5)
5. Girsanov → risk-neutral pricing (Ch. 5)"""),
        code("""# End-to-end: BM → GBM → call price
rng = np.random.default_rng(140)
S0, K, r, sig, T = 100, 100, 0.05, 0.2, 1.0
Z = rng.standard_normal(200_000)
S_T = S0*np.exp((r-0.5*sig**2)*T + sig*np.sqrt(T)*Z)
price = np.exp(-r*T)*np.maximum(S_T-K,0).mean()
print(f"Pipeline MC call = {price:.4f}")"""),
        md("""---
# Part 3 — Key Formulas Cheat Sheet

- **Itô:** \\(df = f_t dt + f_x dX + \\frac{1}{2}f_{xx}(dX)^2\\)
- **GBM:** \\(S_t = S_0 e^{(\\mu-\\sigma^2/2)t + \\sigma W_t}\\)
- **BSM:** \\(C = S\\Phi(d_1) - Ke^{-rT}\\Phi(d_2)\\)
- **Girsanov:** \\(dW^Q = dW + \\theta dt\\), \\(\\theta=(\\mu-r)/\\sigma\\)
- **Feynman-Kac:** \\(V_t + \\mu V_x + \\frac{1}{2}\\sigma^2 V_{xx} - rV = 0\\)"""),
        md("""---
# Part 4 — What's Next?

- **Volatility surfaces** and local/stochastic vol
- **Interest rate models** (Ch. 10 in Shreve)
- **Numerical methods** (finite difference, FFT)
- **Shreve Vol I** for discrete-time completeness"""),
        md("**Your turn:** Pick one week notebook, rerun all simulations, and write a one-page summary."),
    ],
    "problems": [
        "Outline the proof of Itô's lemma in 5 steps.",
        "Explain risk-neutral pricing without using the word 'arbitrage'.",
        "Compare pricing European, Asian, and barrier calls — which needs path info?",
        "When would you use jump-diffusion instead of BSM?",
        "State Girsanov theorem and one application.",
    ],
    "solutions": """**1.** Taylor expand \\(f(t+dt, X+dx)\\); keep \\(dt\\), \\(dx\\), \\(dx^2\\); substitute \\(dx=\\mu dt+\\sigma dW\\), \\(dx^2=\\sigma^2 dt\\).

**2.** Price = discounted expected payoff under measure where asset grows at \\(r\\).

**3.** European: terminal \\(S_T\\) only; Asian/barrier/lookback need full path.

**4.** Short-dated options, crash risk, empirical skew/smile.

**5.** Change drift of BM; remove excess stock drift for derivative pricing.""",
    "reading_ch": "1–7, 11",
}


def build_notebook(spec: dict, filename: str) -> dict:
    week, topic, chapters = spec["meta"]
    br_data = ENRICHMENT.get(filename, {})
    parts_table = spec["parts_table"]
    if br_data.get("br_rows"):
        parts_table = merge_parts_table(parts_table, br_data["br_rows"])
    cells = [
        intro(f"Shreve Week {week:02d} — {topic}", week, topic, chapters, parts_table),
        md(SETUP_MD),
        code(SETUP_CODE),
    ]
    cells.extend(spec["cells"])
    cells.extend(br_cells_for_week(filename, md, code))
    cells.extend(problem_section(spec["problems"], spec["solutions"]))
    cells.append(md(further_reading_br(spec["reading_ch"], SHREVE_URL, filename)))
    return {
        "cells": cells,
        "metadata": {
            "kernelspec": {"display_name": "quant", "language": "python", "name": "python3"},
            "language_info": {
                "codemirror_mode": {"name": "ipython", "version": 3},
                "file_extension": ".py",
                "mimetype": "text/x-python",
                "name": "python",
                "nbconvert_exporter": "python",
                "pygments_lexer": "ipython3",
                "version": "3.12.13",
            },
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }


def save_all():
    OUT.mkdir(parents=True, exist_ok=True)
    for name, spec in NOTEBOOKS.items():
        path = OUT / name
        with open(path, "w", encoding="utf-8") as f:
            json.dump(build_notebook(spec, name), f, indent=2, ensure_ascii=False)
        print(f"  wrote {path.name}")


if __name__ == "__main__":
    save_all()
    print(f"Done — {len(NOTEBOOKS)} notebooks in {OUT}")
    # Normalize LaTeX delimiters for KaTeX ($...$ / $$...$$)
    import importlib.util

    fix_path = Path(__file__).parent / "fix_notebook_latex_for_katex.py"
    spec = importlib.util.spec_from_file_location("fix_latex", fix_path)
    fix_mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(fix_mod)
    fix_mod.main()
