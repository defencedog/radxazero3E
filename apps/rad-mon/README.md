# rad-mon / opi-mon: Hardware Telemetry Utility for Rockchip RK3566

[![Hardware](https://img.shields.io/badge/Hardware-Radxa%20ZERO%203%20%2F%20Orange%20Pi%203B-blue.svg)](https://radxa.com/products/zeros/zero3e)
[![SoC](https://img.shields.io/badge/SoC-Rockchip%20RK3566-orange.svg)](https://www.rock-chips.com/)
[![NPU](https://img.shields.io/badge/NPU-RKNN%201%20TOPS-green.svg)](https://github.com/rockchip-linux/rknpu2)
[![GPU](https://img.shields.io/badge/GPU-Mali--G52%202EE-purple.svg)](https://gitlab.freedesktop.org/panfrost)
[![Display](https://img.shields.io/badge/Display-Mobile%20Optimized%20%3C38%20cols-brightgreen.svg)]()

A lightweight, real-time hardware telemetry dashboard crafted specifically for Rockchip RK3566 Single Board Computers (**Radxa ZERO 3W / 3E** and **Orange Pi 3B**).

Designed with a strict **37-column width** constraint, `rad-mon` fits mobile SSH clients (Termux, JuiceSSH, ConnectBot) in vertical portrait orientation without text wrapping, line jitter, or horizontal scrolling.

---

## Live Dashboard Preview

```text
 Radxa ZERO 3 (RK3566)
 23:12:28 · Up: 6d 3h · Load: 4.01
─────────────────────────────────────
 CPU  66% [██████░░░░] 68.1°C  1.80GHz
 NPU   9% [░░░░░░░░░░]  900MHz  1 TOPS
 GPU   0% [░░░░░░░░░░] 63.8°C   200MHz
 VPU   6% [░░░░░░░░░░] 2 Codec  RKMPP
 FAN  60% [██████░░░░] 153/255  PWM
 RAM  25% [██░░░░░░░░] 0.9/3.6G 2783M free
 SWP   0% [░░░░░░░░░░] 0.0/1.8G 1857M free
─────────────────────────────────────
 [Ctrl+C] Exit  ·  Refresh: 1s
```

---

## Monitored Hardware Subsystems

| Metric | Source / Sysfs Path | Details |
|---|---|---|
| **CPU** | `/proc/stat`, `/proc/loadavg` | Real-time percentage delta, 1-min load avg, scaling governor frequency (`cpufreq`), and SoC temperature (`thermal_zone0`). |
| **NPU** | `/sys/kernel/debug/rknpu/load` | Neural Processing Unit compute load %, operating clock (`fde40000.npu`), and 1 TOPS operational status. |
| **GPU** | `/sys/devices/platform/fde60000.gpu/` | ARM Mali-G52 2EE GPU compute utilization %, operating frequency (200–800 MHz), and thermal zone (`thermal_zone1`). |
| **VPU** | `/proc/mpp_service/load` | Rockchip Media Process Platform (MPP) hardware video encoder/decoder load % and active codec device tags (e.g. `RVEP`, `VDPU`, `2 Codec`). |
| **FAN** | `/sys/class/pwm/pwmchip*/` or `hwmon/` | Cooling fan PWM percentage (0–100%), raw 8-bit scale duty (`0–255`), and dynamic multi-channel detection. |
| **RAM** | `/proc/meminfo` | Memory utilization percentage, human-readable used/total capacity (`0.9/3.6G`), and available free MB. |
| **SWP** | `/proc/meminfo` | Swap space consumption %, active swap capacity, and available free swap MB. |

---

## Quick Start & Installation

### Option 1: Direct Execution
Clone or copy `rad-mon.sh` and run it directly:
```bash
chmod +x rad-mon.sh
./rad-mon.sh
```

### Option 2: System-Wide Installation
Install `rad-mon` globally into `/usr/local/bin/` with convenience symlinks (`rad-mon` and `opi-mon`):
```bash
sudo ./install.sh
```

Once installed, simply run from any terminal:
```bash
rad-mon
# or
opi-mon
```

### CLI Command Options
```bash
# Default live refresh loop (1 second interval)
rad-mon

# Custom refresh interval in seconds (e.g. 2 seconds)
rad-mon 2

# Single-shot execution (useful for motd, SSH login banners, or shell scripts)
rad-mon --once
# or
rad-mon -1
```

---

## PWM Cooling Fan & Custom Pinout Configuration

Because single-board computer cases, expansion boards, and custom fan mounts connect to different physical pins on the **40-pin GPIO header**, `rad-mon` incorporates flexible PWM detection logic.

### 1. How Fan Speed is Detected
`rad-mon` uses a multi-tier detection cascade:
1. **Direct PWM Sysfs Channel:** Auto-discovers any active exported channel under `/sys/class/pwm/pwmchip*/pwm*/` (measuring `duty_cycle`, `period`, and `enable`).
2. **Kernel `pwm-fan` Driver:** Checks `/sys/devices/platform/pwm-fan/hwmon/hwmon*/pwm1` (used on Orange Pi 3B).
3. **Environment Override:** Inspects `$PWM_PATH` if specified by the user.
4. **Service Journal Fallback:** Reads recent duty reports from `fan_control.service` / `pwm-fan.service`.

---

### 2. GPIO Pinout & PWM Controller Mapping

Depending on which header pin you wire your fan's PWM control wire to, different Rockchip PWM controllers and Device Tree Overlays are used:

| Physical Pin | BCM / GPIO | PWM Channel | Platform Controller | Sysfs Channel | Device Tree Overlay |
|:---:|:---:|:---:|:---:|:---:|:---:|
| **Pin 7** | GPIO0_C0 | `pwm15_m1` | `fe700030.pwm` | `pwmchip2` | `rk3568-pwm15-m1.dtbo` |
| **Pin 11** | GPIO0_C4 | `pwm14_m0` | `fe700020.pwm` | `pwmchip1` | `rk3568-pwm14-m0.dtbo` *(Default on Radxa Zero 3)* |
| **Pin 13** | GPIO0_C2 | `pwm13_m1` | `fe6f0030.pwm` | `pwmchipX` | `rk3568-pwm13-m1.dtbo` |
| **Pin 15** | GPIO0_C3 | `pwm12_m1` | `fe6f0020.pwm` | `pwmchipX` | `rk3568-pwm12-m1.dtbo` |
| **Pin 32** | GPIO0_B7 | `pwm11_m1` | `fe6e0030.pwm` | `pwmchip0` | `rk3568-pwm11-m1.dtbo` *(Default on Orange Pi 3B)* |
| **Pin 33** | GPIO0_B6 | `pwm9_m0`  | `fe6d0010.pwm` | `pwmchipX` | `rk3568-pwm9-m0.dtbo` |

> 📖 **Comprehensive PWM Setup Guide:**  
> For complete step-by-step instructions on activating device tree overlays, calculating PWM frequencies in nanoseconds, and wiring transistor/MOSFET fan circuits, refer to:  
> **[Orange Pi 3B & Radxa Zero 3E PWM Configuration Tutorial](https://github.com/defencedog/orangepi3b_v2.1/blob/main/tutorials/OPi3b_Radxa3E_PWM.md)**

---

### 3. Using a Custom PWM Channel with `rad-mon`

If your cooling fan is connected to a different pin (for example, **Pin 7** using `pwmchip2`), you can override the auto-detection path using the `PWM_PATH` environment variable:

```bash
# Run rad-mon using a specific exported PWM channel:
PWM_PATH=/sys/class/pwm/pwmchip2/pwm0 rad-mon

# Or export it permanently in your shell profile (~/.bashrc or /etc/environment):
export PWM_PATH="/sys/class/pwm/pwmchip2/pwm0"
```

---

### 4. Thermal Fan Control Daemon (`fan_control.sh`)

To automatically control fan speeds based on CPU temperatures, a reference daemon script (`fan_control.sh`) and systemd service (`fan_control.service`) are provided in this directory.

#### Configuration:
Edit `fan_control.sh` to match your PWM chip and channel if using an alternative pin:
```bash
# Defaults to pwmchip1 / pwm0 (Pin 11 / pwm14-m0 on Radxa Zero 3)
PWM_CHIP=1
PWM_CHANNEL=0
```

#### Install and Enable Fan Service:
```bash
sudo cp fan_control.sh /usr/local/bin/fan_control.sh
sudo chmod +x /usr/local/bin/fan_control.sh
sudo cp fan_control.service /etc/systemd/system/fan_control.service
sudo systemctl daemon-reload
sudo systemctl enable --now fan_control.service
```

#### Temperature Thresholds:
- **< 60°C:** Fan **OFF** (0% RPM, completely silent)
- **60°C – 64°C:** **40%** speed (`duty_cycle=20000 ns`)
- **64°C – 67°C:** **60%** speed (`duty_cycle=30000 ns`)
- **> 67°C:** **80%** speed (`duty_cycle=40000 ns`)

---

## File Structure

```text
rad-mon/
├── rad-mon.sh             # Core telemetry monitor script (executable)
├── install.sh             # System installation script (/usr/local/bin/)
├── fan_control.sh         # Reference thermal-governed PWM fan control loop
├── fan_control.service    # Systemd unit for automatic fan daemon
└── README.md              # Complete hardware reference & pinout documentation
```

---

## License

Released under the [MIT License](LICENSE).  
Hardware documentation & tutorials courtesy of [defencedog](https://github.com/defencedog).
