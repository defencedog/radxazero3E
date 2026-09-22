#!/bin/bash
# ==============================================================================
# PWM Fan Control Daemon for Radxa Zero 3 / Orange Pi 3B
# Controls fan duty cycle via sysfs PWM based on CPU thermal zone readings
# ==============================================================================

# Allow configuring PWM chip/channel (defaults to pwmchip1/pwm0 for Radxa Zero 3)
PWM_CHIP="${PWM_CHIP:-1}"
PWM_CHANNEL="${PWM_CHANNEL:-0}"
PWM_DIR="/sys/class/pwm/pwmchip${PWM_CHIP}"
CHANNEL_DIR="${PWM_DIR}/pwm${PWM_CHANNEL}"

sleep 5

# Export PWM channel if not already exported
if [ ! -d "${CHANNEL_DIR}" ]; then
    echo "${PWM_CHANNEL}" > "${PWM_DIR}/export" 2>/dev/null || true
    sleep 1
fi

# Configure 20 kHz PWM period (50000 ns)
echo 50000 > "${CHANNEL_DIR}/period" 2>/dev/null || true
echo normal > "${CHANNEL_DIR}/polarity" 2>/dev/null || true
echo 1 > "${CHANNEL_DIR}/enable" 2>/dev/null || true

# Initial spin-up to overcome fan inertia
duty_cycle=30000
min_duty_cycle=20000
echo $duty_cycle > "${CHANNEL_DIR}/duty_cycle"
sleep 1

while true; do
    # Read SoC temperature (milli-Celsius to Celsius)
    temp_raw=$(cat /sys/devices/virtual/thermal/thermal_zone0/temp 2>/dev/null || echo 0)
    temp=$((temp_raw / 1000))

    # Thermal curve
    if [ "$temp" -gt 67 ]; then
        duty_cycle=40000   # 80% speed
    elif [ "$temp" -gt 64 ]; then
        duty_cycle=30000   # 60% speed
    elif [ "$temp" -gt 60 ]; then
        duty_cycle=$min_duty_cycle # 40% speed
    else
        duty_cycle=0       # Fan OFF
    fi

    # Overcome motor stall when spinning up from 0
    if [ "$duty_cycle" -eq "$min_duty_cycle" ] && [ "$(cat "${CHANNEL_DIR}/duty_cycle" 2>/dev/null)" -eq 0 ]; then
        echo 30000 > "${CHANNEL_DIR}/duty_cycle"
        sleep 2
    fi

    echo "$duty_cycle" > "${CHANNEL_DIR}/duty_cycle" 2>/dev/null || true
    speed=$((duty_cycle * 100 / 50000))
    echo "Temp: ${temp}°C, Fan Speed: ${speed}%"
    sleep 2
done
