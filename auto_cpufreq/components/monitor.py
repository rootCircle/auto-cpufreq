import auto_cpufreq.core as core
import os
import time

def monitor():
    core.config_info_dialog()
    core.root_check()
    print('\nNote: You can quit monitor mode by pressing "ctrl+c"')
    if os.getenv("PKG_MARKER") == "SNAP":
        core.gnome_power_detect_snap()
        core.tlp_service_detect_snap()
    else:
        core.gnome_power_detect()
        core.tlp_service_detect()
    while True:
        time.sleep(1)
        core.running_daemon_check()
        core.footer()
        core.gov_check()
        core.cpufreqctl()
        core.distro_info()
        core.sysinfo()
        core.mon_autofreq()
        core.countdown(2)