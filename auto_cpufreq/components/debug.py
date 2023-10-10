import auto_cpufreq.core as core

def debug():
    # ToDo: add status of GNOME Power Profile service status
    core.config_info_dialog()
    core.root_check()
    core.cpufreqctl()
    core.footer()
    core.distro_info()
    core.sysinfo()
    print("")
    core.app_version()
    print("")
    core.python_info()
    print("")
    core.device_info()
    if core.charging():
        print("Battery is: charging")
    else:
        print("Battery is: discharging")
    print("")
    core.app_res_use()
    core.display_load()
    core.get_current_gov()
    core.get_turbo()
    core.footer()