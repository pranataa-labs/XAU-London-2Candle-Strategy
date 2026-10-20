# indie:lang_version = 5
from math import nan
from indie import indicator, color, line_style, plot, param, MutSeriesF

@indicator('XAU London Strategy & Sessions', overlay_main_pane=True)
# --- Parameter Strategi & Waktu ---
@param.int('tz_offset', default=7, min=-12, max=14, title='Timezone Offset (WIB = 7)')
@param.float('sl_ratio', default=1.0, min=0.1, max=3.0, title='SL Multiplier (1.0 = 100% Range)')
@param.float('buffer_usd', default=1.0, min=0.0, max=10.0, title='SL Buffer USD (Peredam Wick/Spread)')
@param.float('rr_ratio', default=2.0, min=0.5, max=5.0, title='Risk-Reward Ratio (RR 1:2.0)')
@param.bool('show_ref_box', default=True, title='Show Reference Range (14:00-14:15)')
# --- Parameter Sesi Pasar ---
@param.bool('show_tokyo', default=True, title='Tokyo Session (07:00 - 14:30 WIB)')
@param.bool('show_london', default=True, title='London Session (14:30 - 22:30 WIB)')
@param.bool('show_ny', default=True, title='New York Session (20:30 - 03:00 WIB)')
# --- Plot Garis Level Strategi ---
@plot.line(title='Entry Level', color=color.YELLOW, line_width=2)
@plot.line(title='Stop Loss (SL)', color=color.RED, line_width=2)
@plot.line(title='Take Profit (TP)', color=color.GREEN, line_width=2)
@plot.line(title='Ref High (14:00-14:15)', color=color.GRAY, line_style=line_style.DASHED, line_width=1)
@plot.line(title='Ref Low (14:00-14:15)', color=color.GRAY, line_style=line_style.DASHED, line_width=1)
# --- Plot Latar Belakang Sesi ---
@plot.background(title='Session Highlight')
def Main(self, tz_offset, sl_ratio, buffer_usd, rr_ratio, show_ref_box, show_tokyo, show_london, show_ny):
    # Inisialisasi mutable state series strategi
    day_s = MutSeriesF.new(0.0)
    c_open_s = MutSeriesF.new(0.0)
    c_close_s = MutSeriesF.new(0.0)
    is_bull_s = MutSeriesF.new(1.0)
    h_ref_s = MutSeriesF.new(0.0)
    l_ref_s = MutSeriesF.new(0.0)
    ready_s = MutSeriesF.new(0.0)

    # Konversi timestamp POSIX (float) ke waktu lokal
    raw_time = self.time[0]
    sec = (raw_time / 1000.0) if raw_time > 10000000000.0 else raw_time
    local_sec = int(sec + tz_offset * 3600.0)
    date_key = float(int(local_sec / 86400))
    sec_in_day = local_sec - int(date_key) * 86400
    hour = int(sec_in_day / 3600)
    minute = int((sec_in_day - hour * 3600) / 60)
    cur_m = hour * 60 + minute

    # ==========================================
    # 1. LOGIKA SESI TRADING
    # ==========================================
    # Tokyo: 07:00 - 14:30 WIB (420 - 870 menit)
    in_tokyo = (show_tokyo and (cur_m >= 420 and cur_m < 870))

    # London: 14:30 - 22:30 WIB (870 - 1350 menit)
    in_london = (show_london and (cur_m >= 870 and cur_m < 1350))

    # New York: 20:30 - 03:00 WIB (1230 menit s/d 180 menit hari berikutnya)
    in_ny = (show_ny and (cur_m >= 1230 or cur_m < 180))

    if in_london and in_ny:
        bg = color.PURPLE(0.14)
    elif in_ny:
        bg = color.RED(0.12)
    elif in_london:
        bg = color.BLUE(0.12)
    elif in_tokyo:
        bg = color.YELLOW(0.10)
    else:
        bg = color.TRANSPARENT

    bg_session = plot.Background(color=bg)

    # ==========================================
    # 2. LOGIKA STRATEGI 2-CANDLE LONDON
    # ==========================================
    if self.bar_index == 0:
        day_s[0] = date_key
        c_open_s[0] = 0.0
        c_close_s[0] = 0.0
        is_bull_s[0] = 1.0
        h_ref_s[0] = 0.0
        l_ref_s[0] = 0.0
        ready_s[0] = 0.0
    else:
        # Reset otomatis setiap hari kalender baru
        if date_key != day_s[1]:
            day_s[0] = date_key
            c_open_s[0] = 0.0
            c_close_s[0] = 0.0
            is_bull_s[0] = 1.0
            h_ref_s[0] = 0.0
            l_ref_s[0] = 0.0
            ready_s[0] = 0.0
        else:
            day_s[0] = day_s[1]
            c_open_s[0] = c_open_s[1]
            c_close_s[0] = c_close_s[1]
            is_bull_s[0] = is_bull_s[1]
            h_ref_s[0] = h_ref_s[1]
            l_ref_s[0] = l_ref_s[1]
            ready_s[0] = ready_s[1]

    # Pembentukan Rentang 2-Candle London (14:00 & 14:15 WIB pada M15)
    if hour == 14 and minute < 30:
        if h_ref_s[0] == 0.0:
            c_open_s[0] = self.open[0]
            h_ref_s[0] = self.high[0]
            l_ref_s[0] = self.low[0]
        else:
            if self.high[0] > h_ref_s[0]:
                h_ref_s[0] = self.high[0]
            if self.low[0] < l_ref_s[0]:
                l_ref_s[0] = self.low[0]

        c_close_s[0] = self.close[0]
        is_bull_s[0] = 1.0 if c_close_s[0] >= c_open_s[0] else 0.0

    # Kunci status eksekusi mulai 14:30 WIB
    if (hour == 14 and minute >= 30) or (hour >= 15 and hour < 22):
        if h_ref_s[0] > 0.0 and l_ref_s[0] > 0.0:
            ready_s[0] = 1.0

    in_trade_window = (ready_s[0] == 1.0) and ((hour == 14 and minute >= 30) or (hour >= 15 and hour < 22))
    in_ref_formation = (hour == 14 and minute < 30) and (h_ref_s[0] > 0.0)

    entry_val = nan
    sl_val = nan
    tp_val = nan
    ref_h_val = nan
    ref_l_val = nan

    if in_trade_window:
        h = h_ref_s[0]
        l = l_ref_s[0]
        rng = h - l
        if rng > 0.0:
            sl_dist = (sl_ratio * rng) + buffer_usd
            tp_dist = rr_ratio * sl_dist

            if is_bull_s[0] == 1.0:
                # 2 Candle Acuan Naik -> BUY LIMIT di Low Acuan
                entry_val = l
                sl_val = l - sl_dist
                tp_val = l + tp_dist
            else:
                # 2 Candle Acuan Turun -> SELL LIMIT di High Acuan
                entry_val = h
                sl_val = h + sl_dist
                tp_val = h - tp_dist

            if show_ref_box:
                ref_h_val = h
                ref_l_val = l
    elif in_ref_formation and show_ref_box:
        ref_h_val = h_ref_s[0]
        ref_l_val = l_ref_s[0]

    return entry_val, sl_val, tp_val, ref_h_val, ref_l_val, bg_session
