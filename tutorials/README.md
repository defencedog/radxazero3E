# Radxa ZERO 3E Tutorials & Configuration Guides

A curated collection of system administration guides, GPIO hardware interfacing, Docker/CasaOS container management, and troubleshooting walkthroughs for the **Radxa ZERO 3E** (Rockchip RK3566).

---

## 🛠️ System Setup & Performance Tuning

| Tutorial | Description |
| :--- | :--- |
| [**First Start & Installation**](./First_Start_Install.md) | Comprehensive post-install checklist: Armbian configuration, package repositories, and essential service setup. |
| [**Manual Overclocking**](./Manual_Overclocking.md) | CPU scaling from 1.8 GHz up to 2.0 GHz, DVFS opp-table tweaks, and thermal stability checks. |
| [**Increasing Ramlog Size**](./Increase_ramlog_avoid_rsyslog_errors.md) | Preventing disk-fill and rsyslog failure loops by properly sizing `armbian-ramlog`. |

---

## 🐳 Docker, Containers & CasaOS Administration

| Tutorial | Description |
| :--- | :--- |
| [**CasaOS Container Crash Fix (Exit 134)**](./CasaOS_Docker_Container_Bug.md) | Fixing `runc` shim task initialization failures and container startup bugs in CasaOS. |
| [**Docker Health Checker Watchdog**](./Systemd_Service_Docker_health_checker.md) | Automated systemd timer and service script to restart unhealthy or dead containers. |
| [**Software RAID (mdadm) in CasaOS**](./RAID_via_mdadm_in_CasaOS.md) | Building and mounting multi-disk software RAID arrays for persistent container storage. |
| [**SIST2 Advanced SQLite Syntax**](./SIST2_Advance_SQLite_Syntax.md) | Advanced Full-Text Search (FTS) query syntax for the SIST2 lightweight document search engine. |

---

## ⚡ GPIO & Hardware Interfacing

| Tutorial | Description |
| :--- | :--- |
| [**Non-Root GPIO Access**](./Non-root_access_GPIO.md) | Udev rules and user permission setup for accessing 40-pin GPIO without `sudo`. |
| [**High-Power LED GPIO Switch**](./High_Power_Led_GPIO_Switch.md) | Driving high-current LEDs and loads using MOSFET / transistor switching circuits. |
| [**Hardware PWM Configuration**](./PWM_GPIO.md) | Activating hardware PWM channels for fan speed modulation and dimmers. |
