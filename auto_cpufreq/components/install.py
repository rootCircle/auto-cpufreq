import auto_cpufreq.core as core
import os

def install():
    if os.getenv("PKG_MARKER") == "SNAP":
        core.root_check()
        core.running_daemon_check()
        core.gnome_power_detect_snap()
        core.tlp_service_detect_snap()
        core.bluetooth_notif_snap()
        core.gov_check()
        core.run("snapctl set daemon=enabled", shell=True)
        core.run("snapctl start --enable auto-cpufreq", shell=True)
        core.deploy_complete_msg()
    else:
        core.root_check()
        core.running_daemon_check()
        core.gov_check()
        core.deploy_daemon()
        core.deploy_completecore._msg()