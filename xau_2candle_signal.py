"""
XAU/USD London Open 2-Candle Trend-Aligned Signal Generator
SOP: Eksekusi 14.25 - 14.30 WIB
Model: 2-Candle Reference Range (14.00 & 14.15 WIB) Searah Tren Sesi Asia
"""

import os
import sys
import datetime
import pandas as pd
import numpy as np
import yfinance as yf

# UTF-8 stdout
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

os.system('')

# ANSI Colors
GOLD = '\033[38;5;220m'
GREEN = '\033[1;32m'
CYAN = '\033[1;36m'
RED = '\033[1;31m'
GRAY = '\033[90m'
WHITE = '\033[1;37m'
RESET = '\033[0m'
BOLD = '\033[1m'

def fetch_data():
    local_cache = "gold_15m_cache.csv"
    df = None
    try:
        df = yf.download("GC=F", period="5d", interval="15m", progress=False)
        if isinstance(df.columns, pd.MultiIndex):
            df = df.xs("GC=F", level="Ticker", axis=1)
        df = df.dropna(subset=['High', 'Low', 'Close', 'Open'])
    except Exception:
        df = None

    if df is None or len(df) == 0:
        if os.path.exists(local_cache):
            df = pd.read_csv(local_cache, index_col=0, parse_dates=True)

    if df is None or len(df) == 0:
        return None

    if df.index.tz is None:
        df.index = df.index.tz_localize("UTC")
    df.index = df.index.tz_convert("Asia/Jakarta")
    df = df.dropna(subset=['High', 'Low', 'Close', 'Open'])
    return df

def generate_signal():
    df = fetch_data()
    if df is None:
        print(f"{RED}[ERROR] Gagal memuat data pasar.{RESET}")
        return

    now_wib = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=7)))
    today_date = now_wib.date()

    # Cari tanggal sesi perdagangan yang memiliki Sesi Asia
    dates_with_asia = []
    for d in sorted(list(set(df.index.date)), reverse=True):
        bars = df[(df.index.date == d) & (df.index.hour >= 7) & (df.index.hour < 14)]
        if len(bars) >= 10:
            dates_with_asia.append(d)

    if not dates_with_asia:
        print(f"{RED}[ERROR] Data Sesi Asia belum lengkap.{RESET}")
        return

    # Gunakan hari ini jika ada, atau gunakan sesi perdagangan terakhir
    dates_with_london = []
    for d in sorted(list(set(df.index.date)), reverse=True):
        bars = df[(df.index.date == d) & (df.index.hour == 14)]
        if len(bars) >= 2:
            dates_with_london.append(d)

    if not dates_with_london:
        print(f"{RED}[ERROR] Data lilin sesi London belum tersedia.{RESET}")
        return

    target_date = today_date if today_date in dates_with_london else dates_with_london[0]
    df_today = df[df.index.date == target_date]

    # Lilin Acuan 14.00 & 14.15 WIB
    c1400 = df_today[(df_today.index.hour == 14) & (df_today.index.minute == 0)]
    c1415 = df_today[(df_today.index.hour == 14) & (df_today.index.minute == 15)]

    if len(c1400) == 0 or len(c1415) == 0:
        print(f"{GRAY}[*] Menunggu pembentukan candle 14.00 dan 14.15 WIB selesai (pukul 14.30 WIB)...{RESET}")
        return

    c_open = float(c1400['Open'].iloc[0])
    c_close = float(c1415['Close'].iloc[0])
    london_delta = c_close - c_open
    is_bull = london_delta >= 0

    h_ref = max(float(c1400['High'].iloc[0]), float(c1415['High'].iloc[0]))
    l_ref = min(float(c1400['Low'].iloc[0]), float(c1415['Low'].iloc[0]))
    rng = h_ref - l_ref
    
    # 1. Setup Lebar (Wide - Default Anti-Wick Hunt): SL = 1.0 * Range + 1.0 USD Buffer
    sl_dist_wide = (1.0 * rng) + 1.0
    tp_dist_wide = 2.0 * sl_dist_wide

    # 2. Setup Ketat (Tight): SL = 0.5 * Range
    sl_dist_tight = 0.5 * rng
    tp_dist_tight = 1.0 * rng

    if is_bull:
        order_type = "BUY LIMIT"
        entry_px = l_ref
        sl_px = l_ref - sl_dist_wide
        tp_px = l_ref + tp_dist_wide
        direction_color = GREEN
    else:
        order_type = "SELL LIMIT"
        entry_px = h_ref
        sl_px = h_ref + sl_dist_wide
        tp_px = h_ref - tp_dist_wide
        direction_color = RED

    current_px = float(df_today.iloc[-1]['Close'])

    print(f"\n{GOLD}======================================================================{RESET}")
    print(f"{GOLD}        XAU/USD 2-CANDLE LONDON OPEN SIGNAL GENERATOR (M15)           {RESET}")
    print(f"{GOLD}======================================================================{RESET}")
    print(f" Tanggal Sesi     : {WHITE}{target_date.strftime('%Y-%m-%d (%A)')}{RESET}")
    print(f" Delta 2-Lilin    : {direction_color}{london_delta:+.2f} USD ({'BULLISH' if is_bull else 'BEARISH'}){RESET}")
    print(f" High Acuan       : {WHITE}${h_ref:.2f}{RESET}")
    print(f" Low Acuan        : {WHITE}${l_ref:.2f}{RESET}")
    print(f" Lebar Rentang    : {WHITE}${rng:.2f} USD{RESET}")
    print(f" Harga Saat Ini   : {WHITE}${current_px:.2f}{RESET}")
    print(f"{GOLD}----------------------------------------------------------------------{RESET}")
    print(f" INSTRUKSI ORDER  : {BOLD}{direction_color}{order_type}{RESET}")
    print(f" LEVEL ENTRY      : {BOLD}{WHITE}${entry_px:.2f}{RESET}")
    print(f" STOP LOSS (SL)   : {BOLD}{RED}${sl_px:.2f}{RESET}  (Jarak: ${sl_dist_wide:.2f} | 1.0x Range + $1 Buffer)")
    print(f" TAKE PROFIT (TP) : {BOLD}{GREEN}${tp_px:.2f}{RESET}  (Target: ${tp_dist_wide:.2f} | RR 1:2.0)")
    print(f" RISK TO REWARD   : {BOLD}{WHITE}1 : 2.0{RESET}")
    print(f" EXPIRE ORDER     : {GRAY}22.00 WIB (Tutup posisi / Batalkan jika unfilled){RESET}")
    print(f"{GOLD}----------------------------------------------------------------------{RESET}")
    print(f" {GRAY}Opsi Ketat (0.5x Range): SL = ${l_ref - sl_dist_tight if is_bull else h_ref + sl_dist_tight:.2f} | TP = ${l_ref + tp_dist_tight if is_bull else h_ref - tp_dist_tight:.2f}{RESET}")
    print(f"{GOLD}======================================================================{RESET}\n")

if __name__ == "__main__":
    generate_signal()
