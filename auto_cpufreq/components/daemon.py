import auto_cpufreq.core as core
import os

def monitor():
    core.config_info_dialog()
    core.root_check()
    core.file_stats()
    if os.getenv("PKG_MARKER") == "SNAP" and core.dcheck == "enabled":
        core.gnome_power_detect_snap()
        core.tlp_service_detect_snap()
        while True:
            core.footer()
            core.gov_check()
            core.cpufreqctl()
            core.distro_info()
            core.sysinfo()
            core.set_autofreq()
            core.countdown(2)
            
    elif os.getenv("PKG_MARKER") != "SNAP":
        core.gnome_power_detect()
        core.tlp_service_detect()
        while True:
            core.footer()
            core.gov_check()
            core.cpufreqctl()
            core.distro_info()
            core.sysinfo()
            core.set_autofreq()
            core.countdown(2)
    else:
        pass
    #"daemon_not_found" is not defined
        #daemon_not_found()