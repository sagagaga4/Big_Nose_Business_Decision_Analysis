# Strategic Business Analysis: Algorithmic Success vs. Sustainable Branding
<img width="2752" height="1536" alt="Algorithmic Success Versus Brand Dilution" src="https://github.com/user-attachments/assets/178fd88b-a05f-4b2a-9a4a-0f25d4fe66c8" />

## Project Overview
This project evaluates the business performance of independent artist "Big Nose" following a strategic pivot to Lofi/Instrumental music in 2021. By correlating financial data with audience engagement metrics, this analysis seeks to answer a critical business question: **Did the pivot create a sustainable brand, or merely generate passive algorithmic success?**

The analysis determines that while the pivot was financially lucrative, it resulted in significant brand dilution, characterizing the artist as a "Passive Algorithmic Success" rather than an "Upcoming Brand".

## Data Sources & Methodology
The analysis integrates two distinct datasets to correlate financial outcomes with user behavior:

1.  **Financial Data (DistroKid):** 5-year transaction history covering 120 songs and $1,985.95 in total revenue.
2.  **Engagement Data (Spotify for Artists):** Daily audience timelines, stream counts, and save rates for the trailing 12-month period.

**Techniques Used:**
* **ETL Process:** Cleaning and merging disparate data sources, handling reporting lags between financial and engagement reporting.
* **Segmentation:** Clustering the audience into four distinct behavioral groups.
* **Metric Engineering:** Calculating custom KPIs such as "Programmed vs. Active Ratio" and "Revenue Concentration Risk."

## Key Business Insights

### 1. Financial Risk: Extreme Revenue Concentration
The analysis identified a critical "Pareto Risk" within the revenue model.
* **Concentration:** The top 5 songs generate **83.3%** of total lifetime revenue.
* **Single Asset Dependency:** One track, "NANA," accounts for **42.5% ($845.22)** of all income.
* **Long Tail Failure:** The bottom 100 songs combined generate less revenue than the top two tracks.
* **Implication:** The business model is fragile; a loss of playlist support for a single asset would result in a ~45% revenue collapse.

### 2. Audience Analysis: The "Ghost Listener" Discrepancy
A massive divergence was found between distribution (Reach) and retention (Intent).
* **The Discrepancy:** While the artist reached **205,368** "Programmed Listeners" (via Smart Shuffle/Radio), only **733** were "Active Listeners".
* **Passive Consumption:** **93.9%** of the audience consumes the content passively via algorithms.
* **Engagement Rate:** The overall Save Rate is **0.42%** (832 saves on 196k streams), significantly below the industry benchmark of 3%-6%.

### 3. Case Study: The 2021 Lofi Pivot
Comparing pre-pivot (vocal) and post-pivot (instrumental) performance reveals a trade-off between cash flow and loyalty.
* **Revenue Impact:** The pivot increased the revenue ceiling per song by approximately **590%** (comparing top pre-pivot vs. post-pivot tracks).
* **Brand Impact:** Listener loyalty collapsed. [cite_start]Pre-pivot tracks maintained a **10.09%** Save Rate, whereas post-pivot hits dropped to **0.17%**.

## Customer Segmentation
The analysis classified the audience into four strategic segments:
1.  **Hit-Driven Listeners:** Focus exclusively on the Top 5 tracks; high churn risk.
2.  **Programmed Listeners:** The dominant segment (205k); passive consumers with zero brand affinity.
3.  **Active Fans:** A core group of 733 monthly users with high Lifetime Value (LTV) potential.
4.  **Previously Active:** A dormant segment of ~12,000 listeners available for retargeting.

## Strategic Recommendations

Based on the data, the following strategic roadmap was developed:

* **Short-Term (De-Risk Cash Flow):** Release a "sequel" track to the top performer ("NANA") with identical tempo (70-90 BPM) and instrumentation to leverage existing algorithmic affinity.
* **Mid-Term (Diversification):** Reallocate 10% of earnings to market the second-best performing track ("dust") to establish a secondary revenue pillar.
* **Long-Term (Retention):** Implement specific Call-to-Actions on Spotify Canvas assets to convert passive "Programmed" listeners into "Active" followers, targeting a Save Rate increase to 1.0%.

## Repository Structure

* `big_nose_analysis.py`: Main Python script for data processing and visualization.
* `Executive_Presentation.md`: Stakeholder presentation deck summarizing findings.
* `analysis_output/`: Contains generated visualizations (Earnings Trends, Correlation Plots) and processed CSV datasets.
