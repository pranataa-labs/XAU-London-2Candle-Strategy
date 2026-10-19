# indie:lang_version = 5
from indie import indicator, color, plot, param

@indicator('Trading Sessions (Tokyo, London, New York)', overlay_main_pane=True)
@param.int('tz_offset', default=7, min=-12, max=14, title='Timezone Offset (WIB = 7)')
@param.bool('show_tokyo', default=True, title='Tokyo Session (07:00 - 14:30 WIB)')
@param.bool('show_london', default=True, title='London Session (14:30 - 22:30 WIB)')
@param.bool('show_ny', default=True, title='New York Session (20:30 - 03:00 WIB)')
@plot.background(title='Tokyo (Asia) Session', color=color.YELLOW(0.07))
@plot.background(title='London Session', color=color.BLUE(0.08))
@plot.background(title='New York Session', color=color.RED(0.08))
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

    # 1. Sesi Tokyo / Asia (07:00 s/d 14:30 WIB)
    tokyo_start = 7 * 60          # 07:00 = 420 menit
    tokyo_end = 14 * 60 + 30      # 14:30 = 870 menit
    in_tokyo = (cur_m >= tokyo_start and cur_m < tokyo_end)

    # 2. Sesi London (14:30 s/d 22:30 WIB)
    london_start = 14 * 60 + 30   # 14:30 = 870 menit
    london_end = 22 * 60 + 30     # 22:30 = 1350 menit
    in_london = (cur_m >= london_start and cur_m < london_end)

    # 3. Sesi New York (20:30 s/d 03:00 WIB - melewati tengah malam)
    ny_start = 20 * 60 + 30       # 20:30 = 1230 menit
    ny_end = 3 * 60               # 03:00 = 180 menit
    in_ny = (cur_m >= ny_start or cur_m < ny_end)

    # Objek pewarnaan latar belakang per sesi
    bg_tokyo = plot.Background(color=color.YELLOW(0.07)) if (show_tokyo and in_tokyo) else plot.Background()
    bg_london = plot.Background(color=color.BLUE(0.08)) if (show_london and in_london) else plot.Background()
    bg_ny = plot.Background(color=color.RED(0.08)) if (show_ny and in_ny) else plot.Background()

    return bg_tokyo, bg_london, bg_ny
