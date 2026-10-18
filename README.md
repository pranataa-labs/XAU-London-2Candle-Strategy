# ⚡ XAU/USD London Open 2-Candle Strategy
### Quantitative Intraday Volatility & Trend-Aligned Model (14.00 & 14.15 WIB)

<div align="left">

![Asset](https://img.shields.io/badge/Asset-XAU%2FUSD%20(Gold)-ffd700?style=for-the-badge)
![Timeframe](https://img.shields.io/badge/Timeframe-M15-blue?style=for-the-badge)
![Win Rate](https://img.shields.io/badge/Win%20Rate-54.8%25-2ca02c?style=for-the-badge)
![Profit Factor](https://img.shields.io/badge/Profit%20Factor-2.42-success?style=for-the-badge)
![Risk:Reward](https://img.shields.io/badge/R%3AR-1%3A2.0-orange?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)

</div>

> **Model Overview:**  
> Model kuantitatif trading harian XAU/USD berbasis rentang acuan 2-candle pembukaan sesi London (14.00 & 14.15 WIB) searah tren Sesi Asia dengan rasio Risk to Reward 1:2.

### 📊 Ringkasan Kinerja Utama (Key Performance Metrics - 50 Entri)

| Parameter Metrik | Hasil Kuantitatif (50 Sesi) |
| :--- | :--- |
| **Total Sesi Diuji** | **50 Hari Perdagangan** |
| **Order Terpicu (*Fill*)** | **42 Trade** (Rasio eksekusi 84.0%) |
| **Order Unfilled** | **8 Hari** (16.0%) |
| **Menang / Kalah** | **23 Win / 19 Loss** |
| **Win Rate** | **54.8%** (naik ke **60.0%** pada $\Delta Asia \ge \$10$) |
| **Risk to Reward (R:R)** | **1 : 2.0** (+2.0 R / -1.0 R) |
| **Net Profit** | **+27.00 R** (Gross Profit: +46.0 R / Loss: -19.0 R) |
| **Profit Factor (PF)** | **2.42** |
| **Max Drawdown** | **-4.00 R** |
| **Waktu Pemasangan Order** | **Pukul 14.30 WIB** |

---

## 1. Parameter Model

- **Aset**: XAU/USD (Emas / Gold Futures `GC=F`)
- **Timeframe**: M15 (15 Menit)
- **Candle Acuan**:
  - Candle 1: 14.00 – 14.15 WIB
  - Candle 2: 14.15 – 14.30 WIB
- **Batas Rentang**:
  - $High_{ref} = \max(High_{14.00}, High_{14.15})$
  - $Low_{ref} = \min(Low_{14.00}, Low_{14.15})$
  - $Range = High_{ref} - Low_{ref}$
- **Filter Tren Sesi Asia (07.00 – 14.00 WIB)**:
  - $\Delta Asia = Close_{13.45} - Open_{07.00}$
  - $\Delta Asia \ge 0 \rightarrow$ Bullish $\rightarrow$ Pasang **BUY LIMIT** di $Low_{ref}$
  - $\Delta Asia < 0 \rightarrow$ Bearish $\rightarrow$ Pasang **SELL LIMIT** di $High_{ref}$
- **Manajemen Risiko**:
  - Stop Loss (SL) = 0.5 × Range
  - Take Profit (TP) = 1.0 × Range (Batas sebaliknya)
  - Risk to Reward = 1 : 2.0 (Win = +2.0 R, Loss = -1.0 R)
- **Masa Berlaku Order**:
  - Pemasangan: Pukul 14.30 WIB
  - Penutupan: Pukul 22.00 WIB (Tutup posisi aktif di harga pasar, batalkan order jika belum terpicu)

---

## 2. Hasil Backtest Kuantitatif (50 Entri)

Evaluasi pada 50 sesi perdagangan data historis M15:

| Parameter Metrik | Hasil Backtest |
| :--- | :--- |
| **Total Sesi Diuji** | 50 Hari Perdagangan |
| **Order Terpicu (*Fill*)** | 42 Trade (Rasio eksekusi 84.0%) |
| **Order Unfilled** | 8 Hari (16.0%) |
| **Menang / Kalah** | 23 Win / 19 Loss |
| **Win Rate** | **54.8%** |
| **Risk to Reward** | **1 : 2.0** |
| **Net Profit** | **+27.00 R** |
| **Profit Factor** | **2.42** |
| **Max Drawdown** | **-4.00 R** |

### Performa Berdasarkan Arah Posisi

| Posisi | Kondisi Asia | Total Sesi | Terpicu | Win / Loss | Win Rate | Net PnL | Profit Factor |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **BUY** | Bullish ($\Delta \ge 0$) | 28 | 23 | 13 W / 10 L | 56.5% | **+16.00 R** | 2.60 |
| **SELL** | Bearish ($\Delta < 0$) | 22 | 19 | 10 W / 9 L | 52.6% | **+11.00 R** | 2.22 |

### Filter Kekuatan Pergerakan Asia ($\Delta Asia$)

| Ambang Batas Delta Asia | Total Trade | Win / Loss | Win Rate | Net PnL | Profit Factor |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Semua ($\Delta \ge \$0$)** | 42 | 23 W / 19 L | 54.8% | +27.00 R | 2.42 |
| **$\Delta \ge \$5$** | 38 | 22 W / 16 L | 57.9% | +28.00 R | 2.75 |
| **$\Delta \ge \$10$** | 35 | 21 W / 14 L | **60.0%** | **+28.00 R** | **3.00** |

---

## 3. Struktur Berkas Repositori

```text
xau-london-2candle-strategy/
├── analisis_strategi_2candle_1400_1415.ipynb  # Notebook analisis komprehensif & grafik
├── xau_2candle_signal.py                      # Skrip CLI kalkulator sinyal harian
├── run_signal.bat                             # Peluncur 1-klik Windows
├── gold_15m_cache.csv                         # Data cache lokal M15
├── README.md                                  # Dokumentasi model
└── .gitignore                                 # Konfigurasi filter git
```

---

## 4. Panduan Eksekusi Harian (SOP)

1. **Pukul 14.25 WIB**:
   - Jalankan `run_signal.bat` atau `python xau_2candle_signal.py`.
   - Program menghitung $\Delta Asia$ dan menentukan jenis order (BUY LIMIT atau SELL LIMIT).
2. **Pukul 14.30 WIB**:
   - Pasang Limit Order pada level harga yang ditampilkan terminal.
   - Tetapkan Stop Loss (SL) dan Take Profit (TP) sesuai angka output program.
3. **Pukul 22.00 WIB**:
   - Tutup transaksi jika posisi masih berjalan.
   - Batalkan pending order jika belum tersentuh (*unfilled*).
