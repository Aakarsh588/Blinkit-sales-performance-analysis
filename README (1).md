# What Actually Drives Grocery Sales? A Statistically-Backed Answer

**A retail analytics case study — SQL, Excel, Power BI, and hypothesis testing on 8,523 real grocery transactions**

---

## Brief

A grocery retail chain wants to know what actually moves the needle on per-transaction sales: **where** you sell (outlet type, size, location tier) or **what** you sell (item category)? Most retailers default to optimizing store format and location — this analysis tests that assumption against real data, using statistical significance rather than eyeballed averages, and finds the conventional wisdom doesn't hold up.

**Dataset:** 8,523 real item-outlet grocery transactions across 10 outlets, 4 regions, and 16 item categories. Publicly sourced, genuinely messy — inconsistent categorical labels, missing values, and duplicate-prone fields, reflecting real-world data quality rather than a pre-cleaned teaching set.

**Tools used:** SQL (SQLite) for querying and cleaning · Excel (Pivot Tables, XLOOKUP, SUMIFS) for exploratory analysis · Power BI for an interactive relationship-modeled dashboard · Python/SciPy for hypothesis testing.

---

## Insight

**Step 1 — the obvious hypothesis, tested first.** Retailers commonly assume store format drives revenue. Grouping average Sales by each outlet-level factor:

| Factor | Highest avg. | Lowest avg. | Spread |
|---|---|---|---|
| Outlet Type | 141.68 (Supermarket Type2) | 139.80 (Supermarket Type3) | 1.88 |
| Outlet Size | 142.04 (High) | 139.88 (Medium) | 2.16 |
| Outlet Location Tier | 141.17 (Tier 2) | 140.87 (Tier 1) | 0.30 |

All three spreads are small — under 3 points on a ~140 average. Rather than eyeball that as "basically no difference" (a common but unrigorous analyst shortcut), this analysis ran actual two-sample t-tests to check.

**Step 2 — statistical testing, not assumption.**

| Comparison | t-statistic | p-value | Verdict |
|---|---|---|---|
| Outlet Size: High vs. Medium | 1.191 | 0.234 | Not significant |
| Outlet Size: High vs. Small | 0.182 | 0.855 | Not significant |

Neither result approaches the conventional 0.05 significance threshold. **In plain terms: if store size truly had zero effect on per-transaction sales, you'd still see gaps this large roughly 23–86% of the time by pure chance.** That's not rare enough to call these differences real. The same held for Outlet Type and Location Tier.

**Step 3 — the factor that actually matters.** Grouping by `Item Type` instead:

- Highest: **Household** (149.42) · Lowest: **Baking Goods** (126.38) · **Spread: 23.04**

That's more than **10x** the spread seen across any outlet-level factor — a difference too large to need a formal test to take seriously, and confirmed against the small-spread comparisons above as the genuine signal in this dataset.

---

## Idea

**Recommendation: stop optimizing outlet format and location for revenue-per-transaction — it isn't where the signal is. Redirect that effort toward category-level merchandising and inventory strategy**, where a statistically confirmed, order-of-magnitude-larger effect actually exists. A "High" size store is not meaningfully outperforming a "Medium" one on a per-sale basis; a store's Household and Dairy assortment depth is where real transaction-value differences originate.

---

## Results

An interactive Power BI dashboard was built on a proper relational data model — three tables (`Sales`, `Outlet_Managers`, `Item_Categories`) joined via defined relationships, not manually flattened — allowing live filtering by region without rewriting any queries. The dashboard includes KPI summary cards (Average Revenue, Total Revenue), a transaction-count breakdown by item category, an average-revenue-per-item-type chart, and a region slicer for live cross-filtering:

![Interactive Power BI dashboard: KPI cards, revenue by item type, transaction counts, and a region slicer](assets/dashboard.png)

**Full pipeline, start to finish:**
1. Cleaned inconsistent categorical data in SQL (e.g., `Item Fat Content` collapsed from 5 raw variants — `Regular`, `Low Fat`, `low fat`, `LF`, `reg` — down to 2 clean categories via `CASE WHEN`)
2. Built multi-table SQL joins and window-function rankings to explore performance by outlet, manager, and region
3. Cross-validated every aggregate result across three independent tools (pandas, SQL, Excel) before trusting it
4. Ran formal two-sample t-tests to separate real effects from noise — rather than asserting a "winner" from a small spread
5. Modeled a relational Power BI dashboard with live cross-filtering, replacing manual Excel lookups with proper table relationships
6. Iterated the dashboard through several design passes — KPI cards, a consistent theme, sorted and labeled charts, and a working region slicer — to move from a functional prototype to a presentable, portfolio-ready deliverable

*Analysis conducted with Claude as an active technical collaborator — used for query debugging, statistical validation, and structured critique of each finding, with every result independently cross-checked against ground truth before being trusted.*

---

## Files in this repository
- `blinkit_analysis.py` — full analysis code: pandas exploration, SQL queries (joins, window functions, multi-CTE chains), and data cleaning, exactly as written and run
- `blinkit_grocery.csv` — source dataset
- `assets/dashboard.png` — Power BI dashboard screenshot
