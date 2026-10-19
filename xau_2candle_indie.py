# indie:lang_version = 5
from math import nan
from indie import indicator, color, line_style, plot, param, MutSeriesF

@indicator('XAU London 2-Candle Trend Strategy', overlay_main_pane=True)
@param.int('tz_offset', default=7, min=-12, max=14, title='Timezone Offset (WIB = 7)')
@param.float('sl_ratio', default=1.0, min=0.1, max=3.0, title='SL Multiplier (1.0 = 100% Range)')
@param.float('buffer_usd', default=1.0, min=0.0, max=10.0, title='SL Buffer USD (Peredam Wick/Spread)')
@param.float('rr_ratio', default=2.0, min=0.5, max=5.0, title='Risk-Reward Ratio (RR 1:2.0)')
@param.bool('show_ref_box', default=True, title='Show Reference Range (14:00-14:15)')
@plot.line(title='Entry Level', color=color.YELLOW, line_width=2)
@plot.line(title='Stop Loss (SL)', color=color.RED, line_width=2)
@plot.line(title='Take Profit (TP)', color=color.GREEN, line_width=2)
@plot.line(title='Ref High (14:00-14:15)', color=color.GRAY, line_style=line_style.DASHED, line_width=1)
@plot.line(title='Ref Low (14:00-14:15)', color=color.GRAY, line_style=line_style.DASHED, line_width=1)
def Main(self, tz_offset, sl_ratio, buffer_usd, rr_ratio, show_ref_box):
    # Inisialisasi mutable state series
    day_s = MutSeriesF.new(0.0)
    asia_open_s = MutSeriesF.new(0.0)
    asia_close_s = MutSeriesF.new(0.0)
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

    # Penanganan bar pertama vs bar kelanjutan
    if self.bar_index == 0:
        day_s[0] = date_key
        asia_open_s[0] = 0.0
        asia_close_s[0] = 0.0
        is_bull_s[0] = 1.0
        h_ref_s[0] = 0.0
        l_ref_s[0] = 0.0
        ready_s[0] = 0.0
    else:
        # Reset otomatis setiap pergantian hari kalender
        if date_key != day_s[1]:
            day_s[0] = date_key
            asia_open_s[0] = 0.0
            asia_close_s[0] = 0.0
            is_bull_s[0] = 1.0
            h_ref_s[0] = 0.0
            l_ref_s[0] = 0.0
            ready_s[0] = 0.0
        else:
            day_s[0] = day_s[1]
            asia_open_s[0] = asia_open_s[1]
            asia_close_s[0] = asia_close_s[1]
            is_bull_s[0] = is_bull_s[1]
            h_ref_s[0] = h_ref_s[1]
            l_ref_s[0] = l_ref_s[1]
            ready_s[0] = ready_s[1]

    # 1. Sesi Asia (07:00 s/d 13:59 WIB)
    if hour >= 7 and hour < 14:
        if asia_open_s[0] == 0.0:
            asia_open_s[0] = self.open[0]
        asia_close_s[0] = self.close[0]
        delta_asia = asia_close_s[0] - asia_open_s[0]
        is_bull_s[0] = 1.0 if delta_asia >= 0.0 else 0.0

    # 2. Pembentukan Rentang Acuan London 2-Candle (14:00 & 14:15 WIB pada M15)
    if hour == 14 and minute < 30:
        if h_ref_s[0] == 0.0:
            h_ref_s[0] = self.high[0]
            l_ref_s[0] = self.low[0]
        else:
            if self.high[0] > h_ref_s[0]:
                h_ref_s[0] = self.high[0]
            if self.low[0] < l_ref_s[0]:
                l_ref_s[0] = self.low[0]

    # 3. Kunci status kesiapan eksekusi mulai 14:30 WIB
    if (hour == 14 and minute >= 30) or (hour >= 15 and hour < 22):
        if h_ref_s[0] > 0.0 and l_ref_s[0] > 0.0:
            ready_s[0] = 1.0

    # Penentuan jendela aktif perdagangan (14:30 - 22:00 WIB)
    in_trade_window = (ready_s[0] == 1.0) and ((hour == 14 and minute >= 30) or (hour >= 15 and hour < 22))
    in_ref_formation = (hour == 14 and minute < 30) and (h_ref_s[0] > 0.0)

    # Inisialisasi level harga
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
            # SL diperlebar: rasio rentang ditambah buffer USD peredam wick
            sl_dist = (sl_ratio * rng) + buffer_usd
            # TP diperlebar mengikuti rasio Risk-to-Reward (default RR 1:2.0)
            tp_dist = rr_ratio * sl_dist

            if is_bull_s[0] == 1.0:
                # Sesi Asia Naik -> BUY LIMIT di Low Acuan
                entry_val = l
                sl_val = l - sl_dist
                tp_val = l + tp_dist
            else:
                # Sesi Asia Turun -> SELL LIMIT di High Acuan
                entry_val = h
                sl_val = h + sl_dist
                tp_val = h - tp_dist

            if show_ref_box:
                ref_h_val = h
                ref_l_val = l
    elif in_ref_formation and show_ref_box:
        ref_h_val = h_ref_s[0]
        ref_l_val = l_ref_s[0]

    return entry_val, sl_val, tp_val, ref_h_val, ref_l_val
