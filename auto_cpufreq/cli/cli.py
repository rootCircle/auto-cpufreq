#!/usr/bin/env python3
#
# auto-cpufreq - Automatic CPU speed & power optimizer for Linux
#
# Blog post: https://foolcontrol.org/?p=3124

# core import
import sys
import time
from click import UsageError
from subprocess import call, run

from auto_cpufreq.core import *
from auto_cpufreq.power_helper import *
import auto_cpufreq.cli.cli

import auto_cpufreq.components.daemon
import auto_cpufreq.components.debug
import auto_cpufreq.components.donate
import auto_cpufreq.components.force
import auto_cpufreq.components.get_state
import auto_cpufreq.components.install
import auto_cpufreq.components.live
import auto_cpufreq.components.log
import auto_cpufreq.components.monitor
import auto_cpufreq.components.remove
import auto_cpufreq.components.stats
import auto_cpufreq.components.update
import auto_cpufreq.components.version

# cli
@click.command()
@click.option("--monitor", is_flag=True, help="Monitor and see suggestions for CPU optimizations")
@click.option("--live", is_flag=True, help="Monitor and make (temp.) suggested CPU optimizations")
@click.option("--install", is_flag=True, help="Install daemon for (permanent) automatic CPU optimizations")
@click.option("--update", is_flag=False, help="Update daemon and package for (permanent) automatic CPU optimizations", flag_value="--update")
@click.option("--remove", is_flag=True, help="Remove daemon for (permanent) automatic CPU optimizations")

@click.option("--stats", is_flag=True, help="View live stats of CPU optimizations made by daemon")
@click.option("--force", is_flag=False, help="Force use of either \"powersave\" or \"performance\" governors. Setting to \"reset\" will go back to normal mode")
@click.option("--get-state", is_flag=True, hidden=True)
@click.option(
    "--config",
    is_flag=False,
    default="/etc/auto-cpufreq.conf",
    help="Use config file at defined path",
)
@click.option("--debug", is_flag=True, help="Show debug info (include when submitting bugs)")
@click.option("--version", is_flag=True, help="Show currently installed version")
@click.option("--donate", is_flag=True, help="Support the project")
@click.option("--log", is_flag=True, hidden=True)
@click.option("--daemon", is_flag=True, hidden=True)
def main(config, daemon, debug, update, install, remove, live, log, monitor, stats, version, donate, force, get_state):

    # display info if config file is used
    def config_info_dialog():
        if get_config(config) and hasattr(get_config, "using_cfg_file"):
            print("\nUsing settings defined in " + config + " file")

    # set governor override unless None or invalid
    if force is not None:
        not_running_daemon_check()
        root_check() # Calling root_check before set_override as it will require sudo access
        set_override(force) # Calling set override, only if force has some values

    if len(sys.argv) == 1:
 
        print("\n" + "-" * 32 + " auto-cpufreq " + "-" * 33 + "\n")
        print("Automatic CPU speed & power optimizer for Linux")
 
        print("\nExample usage:\nauto-cpufreq --monitor")
        print("\n-----\n")

        run(["auto-cpufreq", "--help"])
        footer()
    else:
        if daemon:
            auto_cpufreq.components.daemon.daemon()
        elif monitor:
            auto_cpufreq.components.monitor.monitor()
        elif live:
            auto_cpufreq.components.live.live()
        elif stats:
            auto_cpufreq.components.stats.stats()
        elif log:
            deprecated_log_msg()
        elif get_state:
            not_running_daemon_check()
            override = get_override()
            print(override)
        elif debug:
            auto_cpufreq.components.debug.debug()
        elif version:
            auto_cpufreq.components.version.version()
        elif donate:
            auto_cpufreq.components.donate.donate()
        elif install:
            auto_cpufreq.components.install.install()
        elif remove:
            if os.getenv("PKG_MARKER") == "SNAP":
                root_check()
                run("snapctl set daemon=disabled", shell=True)
                run("snapctl stop --disable auto-cpufreq", shell=True)
                if auto_cpufreq_stats_path.exists():
                    if auto_cpufreq_stats_file is not None:
                        auto_cpufreq_stats_file.close()

                    auto_cpufreq_stats_path.unlink()
                # ToDo: 
                # {the following snippet also used in --update, update it there too(if required)}
                # * undo bluetooth boot disable
                gnome_power_rm_reminder_snap()
                remove_complete_msg()
            else:
                root_check()
                remove_daemon()
                remove_complete_msg()
        elif update:
            root_check()
            custom_dir = "/opt/auto-cpufreq/source"
            for arg in sys.argv:
                if arg.startswith("--update="):
                    custom_dir = arg.split("=")[1]
                    sys.argv.remove(arg)
                    
            if "--update" in sys.argv:
                update = True
                sys.argv.remove("--update")
                if len(sys.argv) == 2:
                    custom_dir = sys.argv[1] 
                    
            if os.getenv("PKG_MARKER") == "SNAP":
                print("Detected auto-cpufreq was installed using snap")
                # refresh snap directly using this command
                # path wont work in this case

                print("Please update using snap package manager, i.e: `sudo snap refresh auto-cpufreq`.")
                #check for AUR 
            elif subprocess.run(["bash", "-c", "command -v pacman >/dev/null 2>&1"]).returncode == 0 and subprocess.run(["bash", "-c", "pacman -Q auto-cpufreq >/dev/null 2>&1"]).returncode == 0:
                print("Arch-based distribution with AUR support detected. Please refresh auto-cpufreq using your AUR helper.")
            else:
                verify_update()
                ans = input("Do you want to update auto-cpufreq to the latest release? [Y/n]: ").strip().lower()
                if not os.path.exists(custom_dir):
                    os.makedirs(custom_dir)
                if os.path.exists(os.path.join(custom_dir, "auto-cpufreq")):
                    shutil.rmtree(os.path.join(custom_dir, "auto-cpufreq"))
                if ans in ['', 'y', 'yes']:
                    remove_daemon()
                    remove_complete_msg()
                    new_update(custom_dir)
                    print("enabling daemon")
                    run(["auto-cpufreq", "--install"])
                    print("auto-cpufreq is installed with the latest version")
                    run(["auto-cpufreq", "--version"])
                else:
                    print("Aborted")

if __name__ == "__main__":
    main()
