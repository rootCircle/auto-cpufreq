import auto_cpufreq.core as core
import os

def stats():
    core.not_running_daemon_check()
    core.config_info_dialog()
    print('\nNote: You can quit stats mode by pressing "ctrl+c"')
    if os.getenv("PKG_MARKER") == "SNAP":
        core.gnome_power_detect_snap()
        core.tlp_service_detect_snap()
    else:
        core.gnome_power_detect()
        core.tlp_service_detect()
    core.read_stats()