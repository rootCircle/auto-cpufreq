import auto_cpufreq.core as core
import time
import os
import sys

def live():
    core.root_check()
    core.config_info_dialog()
    print('\nNote: You can quit live mode by pressing "ctrl+c"')
    time.sleep(1)
    if os.getenv("PKG_MARKER") == "SNAP":
        core.gnome_power_detect_snap()
        core.tlp_service_detect_snap()
    else:
        core.gnome_power_detect_install()
        core.gnome_power_stop_live()
        core.tlp_service_detect()
    while True:
        try:
            core.running_daemon_check()
            core.footer()
            core.gov_check()
            core.cpufreqctl()
            core.distro_info()
            core.sysinfo()
            core.set_autofreq()
            core.countdown(2)
        except KeyboardInterrupt:
            core.gnome_power_start_live()
            print("")
            sys.exit()