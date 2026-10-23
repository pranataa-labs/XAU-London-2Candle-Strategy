# ⚡ XAU/USD London Open 2-Candle Quantitative Strategy

### Quantitative Intraday Volatility & Trend-Aligned Trading Model (14:00 & 14:15 WIB / 07:00 & 07:15 UTC)

<div align="left">

![Asset](https://img.shields.io/badge/Asset-XAU%2FUSD%20(Gold)-ffd700?style=for-the-badge)
![Timeframe](https://img.shields.io/badge/Timeframe-M15-blue?style=for-the-badge)
![Net Profit](https://img.shields.io/badge/Net%20Profit-%2B27.00%20R%20(%2B1%2C684%20Pips)-2ca02c?style=for-the-badge)
![Win Rate](https://img.shields.io/badge/Win%20Rate-54.8%25-green?style=for-the-badge)
![Profit Factor](https://img.shields.io/badge/Profit%20Factor-2.42-success?style=for-the-badge)
![Risk:Reward](https://img.shields.io/badge/R%3AR-1%3A2.0-orange?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)

</div>

> **Model Overview:**  
> Quantitative intraday trading strategy for Gold (XAU/USD) capturing London session opening volatility utilizing a 2-candle M15 reference range aligned with Asian session directional momentum with an asymmetric 1:2.0 Risk-Reward payoff.

---

## 📊 Key Quantitative Performance Metrics (50 Test Sessions)

| Performance Metric | Empirical Result (50 Sessions) |
| :--- | :--- |
| **Total Evaluated Sessions** | **50 Trading Days** |
| **Triggered Orders (Fill Rate)** | **42 Executed Trades** (84.0% Execution Rate) |
| **Unfilled Limit Orders** | **8 Days** (16.0%) |
| **Win / Loss Distribution** | **23 Wins / 19 Losses** |
| **Win Rate** | **54.8%** (Expands to **60.0%** at $\Delta Asia \ge \$10$) |
| **Risk-to-Reward Ratio (R:R)** | **1 : 2.0** (+2.0 R / -1.0 R) |
| **Net Accumulated Profit** | **+27.00 R** (**+1,684 Pips** / +168.40 USD points) |
| **Gross Profit / Loss** | **+46.00 R** (+2,671 Pips) / **-19.00 R** (-987 Pips) |
| **Profit Factor (PF)** | **2.42** |
| **Maximum Strategy Drawdown** | **-4.00 R** |
| **Order Placement Timestamp** | **14:30 WIB (07:30 UTC)** |

---

## 📐 Mathematical Model & Execution Rules

- **Underlying Asset:** XAU/USD (Spot Gold / Comex Gold Futures `GC=F`)
- **Execution Timeframe:** M15 (15-Minute Candlesticks)
- **Reference Range Formation:**
  - Candle 1: 14:00 – 14:15 WIB (07:00 – 07:15 UTC)
  - Candle 2: 14:15 – 14:30 WIB (07:15 – 07:30 UTC)
- **Boundary Formulation:**
  - $High_{ref} = \max(High_{14:00}, High_{14:15})$
  - $Low_{ref} = \min(Low_{14:00}, Low_{14:15})$
  - $Range = High_{ref} - Low_{ref}$
- **Asian Session Trend Filter (07:00 – 14:00 WIB):**
  - $\Delta Asia = Close_{13:45} - Open_{07:00}$
  - $\Delta Asia \ge 0 \rightarrow$ Bullish Bias $\rightarrow$ Place **BUY LIMIT** at $Low_{ref}$
  - $\Delta Asia < 0 \rightarrow$ Bearish Bias $\rightarrow$ Place **SELL LIMIT** at $High_{ref}$
- **Asymmetric Risk Management:**
  - Stop Loss (SL) = 0.5 × Range
  - Take Profit (TP) = 1.0 × Range (Opposing boundary)
  - Payoff Structure = 1 : 2.0 (Win = +2.0 R, Loss = -1.0 R)
- **Order Expiration & Life Cycle:**
  - Order Submission: 14:30 WIB (07:30 UTC)
  - Daily Settlement: 22:00 WIB (15:00 UTC) (Liquidate open market exposures, cancel unfilled pending limits)

---

## 🔬 Empirical Backtest Results & Subgroup Analytics

### Capital Growth Projections (1% Fixed Risk Per Trade)

| Starting Account Balance | Risk Allocation (1%) | Net Accumulated Profit (+27.00 R) | Ending Equity | Return On Investment (ROI) |
| :---: | :---: | :---: | :---: | :---: |
| **$10,000 USD** | $100 USD | **+$2,700 USD** | $12,700 USD | **+27.0%** |
| **$5,000 USD** | $50 USD | **+$1,350 USD** | $6,350 USD | **+27.0%** |
| **$1,000 USD** | $10 USD | **+$270 USD** | $1,270 USD | **+27.0%** |

### Directional Performance Breakdown

| Direction | Asian Session Bias | Total Sessions | Fills | Win / Loss | Win Rate | Net PnL | Profit Factor |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **BUY** | Bullish ($\Delta \ge 0$) | 28 | 23 | 13 W / 10 L | 56.5% | **+16.00 R** | 2.60 |
| **SELL** | Bearish ($\Delta < 0$) | 22 | 19 | 10 W / 9 L | 52.6% | **+11.00 R** | 2.22 |

### Momentum Threshold Sensitivity ($\Delta Asia$)

| Asian Delta Threshold | Total Trades | Win / Loss | Win Rate | Net PnL | Profit Factor |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **All Baseline Trades ($\Delta \ge \$0$)** | 42 | 23 W / 19 L | 54.8% | +27.00 R | 2.42 |
| **Moderate Momentum ($\Delta \ge \$5$)** | 38 | 22 W / 16 L | 57.9% | +28.00 R | 2.75 |
| **Strong Momentum ($\Delta \ge \$10$)** | 35 | 21 W / 14 L | **60.0%** | **+28.00 R** | **3.00** |

---

## 📁 Repository Directory Structure

```text
XAU-London-2Candle-Strategy/
├── analisis_strategi_2candle_1400_1415.ipynb  # Comprehensive analytical notebook & equity plots
├── xau_2candle_signal.py                      # Production daily signal CLI calculator
├── run_signal.bat                             # One-click Windows runner
├── gold_15m_cache.csv                         # Local cached M15 historical pricing
└── README.md                                  # Strategy specification & model documentation
```

---

## 🛠️ Daily Standard Operating Procedure (SOP)

1. **At 14:25 WIB (07:25 UTC):**
   - Execute `run_signal.bat` or `python xau_2candle_signal.py`.
   - Algorithm calculates $\Delta Asia$ and outputs appropriate order specification (BUY LIMIT or SELL LIMIT).
2. **At 14:30 WIB (07:30 UTC):**
   - Place designated Limit Order at displayed price level.
   - Set Stop Loss and Take Profit levels exactly matching algorithm parameters.
3. **At 22:00 WIB (15:00 UTC):**
   - Close active market exposures.
   - Cancel unfilled pending limit orders.

---

<p align="center">
  Engineered by <b><a href="https://github.com/pranataa-labs">pranataa-labs</a></b>
</p>
