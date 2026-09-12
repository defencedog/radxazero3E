# LED toggle Radxa 3E

## Problem
I am running a Ubuntu system on my Radxa Zero 3E (single board computer)
Using its GPIO I am driving a 5V LED via an NPN transisitor. Everything works.
For switching it **on** I use `gpioset $(gpiofind PIN_36)=1` & for **off** `gpioset $(gpiofind PIN_36)=0`
My problem is I cannot run above commands as a single line like `sudo gpioset $(gpiofind PIN_36)=0` I must first move to root terminal via `sudo su` & then commands work perfectly. 
The other alternative is that I use x2 separate `sudo` one liners first for `gpiofind` & then for `gpioset`. Both Binaries are located in `/usr/bin`
## Hardware circuit
Check attachment. Simulated via Proto on Android. Check LED module documentation for **maximum amperage** & select base resistor R1 accordingly. For mine it was 20-30mA.
In simulation you can observe when GPIO is on (simulated via switch) LED I (current) is ~20mA

![Physical GPIO](https://i.imgur.com/P72a2eA.jpeg)

![PROTO simulation](https://i.imgur.com/hGTNgh4.jpeg)

## Software solution
```
mkdir ~/led && cd led
nano led_toggle.sh
chmod +x led_toggle.sh
sudo nano /etc/systemd/system/cam_led.timer
sudo nano /etc/systemd/system/cam_led.service
sudo systemctl daemon-reload 
sudo systemctl enable cam_led.timer
sudo systemctl start cam_led.tmer
```

*led_toggle.sh*
```
#!/bin/bash

PIN=$(gpiofind PIN_36)
gpioset $PIN=$1
```
*cam_led.timer*
```
[Unit]
Description=Timer to control LED on Radxa Zero 3E

[Timer]
OnCalendar=*-*-* 20:00:00
OnCalendar=*-*-* 06:22:00
Persistent=true

[Install]
WantedBy=timers.target
```
*cam_led.service*
```
[Unit]
Description=Control LED on Radxa Zero 3E

[Service]
Type=oneshot
ExecStart=/home/ukhan/led/led_toggle.sh 1
ExecStop=/home/ukhan/led/led_toggle.sh 0
```
