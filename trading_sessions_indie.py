# indie:lang_version = 5
from indie import indicator, color, plot, param

@indicator('Trading Sessions (Tokyo, London, New York)', overlay_main_pane=True)
@param.int('tz_offset', default=7, min=-12, max=14, title='Timezone Offset (WIB = 7)')
@param.bool('show_tokyo', default=True, title='Sesi Tokyo (07:00 - 14:30 WIB)')
@param.bool('show_london', default=True, title='Sesi London (14:30 - 22:30 WIB)')
@param.bool('show_ny', default=True, title='Sesi New York (20:30 - 03:00 WIB)')
@plot.background(title='Session Highlight')
def Main(self, tz_offset, show_tokyo, show_london, show_ny):
    # Konversi timestamp POSIX (float) ke waktu lokal
    raw_time = self.time[0]
    sec = (raw_time / 1000.0) if raw_time > 10000000000.0 else raw_time
    local_sec = int(sec + tz_offset * 3600.0)
    date_key = float(int(local_sec / 86400))
    sec_in_day = local_sec - int(date_key) * 86400
    hour = int(sec_in_day / 3600)
    minute = int((sec_in_day - hour * 3600) / 60)
    cur_m = hour * 60 + minute

    # 1. Sesi Tokyo / Asia (07:00 - 14:30 WIB = 420 - 870 menit)
    in_tokyo = (show_tokyo and (cur_m >= 420 and cur_m < 870))

    # 2. Sesi London (14:30 - 22:30 WIB = 870 - 1350 menit)
    in_london = (show_london and (cur_m >= 870 and cur_m < 1350))

    # 3. Sesi New York (20:30 - 03:00 WIB = 1230 menit s/d 180 menit)
    in_ny = (show_ny and (cur_m >= 1230 or cur_m < 180))

    # Penentuan satu warna latar belakang per bar tanpa tumpang tindih
    if in_london and in_ny:
        # Overlap London & New York (20:30 - 22:30 WIB)
        bg = color.PURPLE(0.14)
    elif in_ny:
        # Sesi New York murni (22:30 - 03:00 WIB)
        bg = color.RED(0.12)
    elif in_london:
        # Sesi London murni (14:30 - 20:30 WIB)
        bg = color.BLUE(0.12)
    elif in_tokyo:
        # Sesi Tokyo murni (07:00 - 14:30 WIB)
        bg = color.YELLOW(0.10)
    else:
        # Di luar sesi trading (transparan bersih)
        bg = color.TRANSPARENT

    return plot.Background(color=bg)
