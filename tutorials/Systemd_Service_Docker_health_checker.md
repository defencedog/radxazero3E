# Recurring service to auto restart any nonfunctional container

**First x2 methods of invoking podman are deprecated & must not be used. I have observed `out  of memory` errors & containers stuck in `Stopping` conditions if `systemd` or `init.d` services are involved** 

I am using `podman version 4.9.3`

> https://github.com/containers/podman/issues/24268
>
> Officially deprecated `podman generate systemd` as referenced here https://www.tutorialworks.com/podman-systemd/

## Via init.d

Because of SBC's reduced RAM or weak CPU complex containers may not properly initiate at a reboot. So one can check status of each container & restart it if it is not healthy. To auto-check it [at boot time](https://askubuntu.com/a/335253/110979):
```
sudo nano /etc/init.d/ukhan_docker
sudo chmod +x /etc/init.d/ukhan_docker
sudo chown root:root /etc/init.d/ukhan_docker
sudo update-rc.d ukhan_docker defaults
sudo update-rc.d ukhan_docker enable
sudo reboot
```
File contents

```
#!/bin/bash

### BEGIN INIT INFO
# Provides:          ukhan_docker
# Required-Start:    $all
# Required-Stop:
# Default-Start:     2 3 4 5
# Default-Stop:
# Short-Description: radxa3E CasaOS
### END INIT INFO

container_id_list=$(docker ps -a -q -f "status=exited" -f "status=created")
for container_id in $container_id_list; do
    docker restart "${container_id}"
    # Set result based on exit code
    [[ $? -eq 0 ]] && result="SUCCESS" || result="FAILED"
    echo "Restart of container ${container_id} - ${result}"
    sleep 30
done
```
At next reboot check status `sudo service ukhan_docker status`
```
● ukhan_docker.service - LSB: radxa3E CasaOS
     Loaded: loaded (/etc/init.d/ukhan_docker; generated)
     Active: activating (start) since Wed 2024-11-06 03:35:50 +03; 1min 22s ago
       Docs: man:systemd-sysv-generator(8)
  Cntrl PID: 867 (ukhan_docker)
      Tasks: 9 (limit: 81)
     Memory: 37.6M (peak: 49.7M)
        CPU: 10.950s
     CGroup: /system.slice/ukhan_docker.service
             ├─ 867 /bin/bash /etc/init.d/ukhan_docker start
             ├─1531 /usr/bin/conmon --api-version 1 -c 4d3d6b547ff683096f216dae7ff1fffa04ad0b5b0cc0171b9f46fba9680c34ae -u 4d3d6b547ff683096f216dae7ff1fffa04ad0b5b0cc0171b9f46fba9680c34ae -r /usr/bin/crun -b >
             ├─2406 /usr/bin/conmon --api-version 1 -c 6d0d101e768d181db0a1cdcc90f39d75a36cd109ca8ef51af5f98d64a9eea385 -u 6d0d101e768d181db0a1cdcc90f39d75a36cd109ca8ef51af5f98d64a9eea385 -r /usr/bin/crun -b >
             ├─2737 /usr/bin/conmon --api-version 1 -c 20523390e63bd2fe122fb8b76a1f2a1e40792df1e9c68ed3506cc86051ce1563 -u 20523390e63bd2fe122fb8b76a1f2a1e40792df1e9c68ed3506cc86051ce1563 -r /usr/bin/crun -b >
             ├─3075 /usr/bin/conmon --api-version 1 -c 4b787454f674d6ef83b07ea5a2c66ea0f3d1334a7a87e62707cec9c16a6e3738 -u 4b787454f674d6ef83b07ea5a2c66ea0f3d1334a7a87e62707cec9c16a6e3738 -r /usr/bin/crun -b >
             ├─3427 /usr/bin/conmon --api-version 1 -c c35a34debfb81923255dde20cb427201e0d168fac8a2911013fef6e501aea9e2 -u c35a34debfb81923255dde20cb427201e0d168fac8a2911013fef6e501aea9e2 -r /usr/bin/crun -b >
             ├─4330 /usr/bin/conmon --api-version 1 -c 1acd65f0d0c6d0ff71f6d53c04422a072860b5668a013195157f742d3838317d -u 1acd65f0d0c6d0ff71f6d53c04422a072860b5668a013195157f742d3838317d -r /usr/bin/crun -b >
             ├─4815 /usr/bin/conmon --api-version 1 -c e042deaf65cb20b1d5a118353730e32b9f064d5504fc4709642c5746370d0a33 -u e042deaf65cb20b1d5a118353730e32b9f064d5504fc4709642c5746370d0a33 -r /usr/bin/crun -b >
             └─4819 sleep 10

Nov 06 03:37:06 radxa-zero3 jellyfin[1531]: [03:37:06] [INF] [1] Emby.Server.Implementations.ApplicationHost: Core startup complete
Nov 06 03:37:06 radxa-zero3 jellyfin[1531]: [03:37:06] [INF] [1] Main: Startup complete 0:01:01.4648889
Nov 06 03:37:06 radxa-zero3 jellyfin[1531]: [ls.io-init] done.
Nov 06 03:37:07 radxa-zero3 ukhan_docker[4636]: Emulate Docker CLI using podman. Create /etc/containers/nodocker to quiet msg.
Nov 06 03:37:08 radxa-zero3 podman[4636]: 2024-11-06 03:37:08.120088762 +0300 +03 m=+0.212706203 container restart e042deaf65cb20b1d5a118353730e32b9f064d5504fc4709642c5746370d0a33 (image=docker.io/linuxserver>
Nov 06 03:37:09 radxa-zero3 podman[4636]: 2024-11-06 03:37:09.673745309 +0300 +03 m=+1.766362459 container init e042deaf65cb20b1d5a118353730e32b9f064d5504fc4709642c5746370d0a33 (image=docker.io/linuxserver/ca>
Nov 06 03:37:09 radxa-zero3 podman[4636]: 2024-11-06 03:37:09.701051832 +0300 +03 m=+1.793668981 container start e042deaf65cb20b1d5a118353730e32b9f064d5504fc4709642c5746370d0a33 (image=docker.io/linuxserver/c>
Nov 06 03:37:09 radxa-zero3 ukhan_docker[4636]: e042deaf65cb
Nov 06 03:37:09 radxa-zero3 ukhan_docker[867]: Restart of container e042deaf65cb - SUCCESS
Nov 06 03:37:11 radxa-zero3 calibre-web[4815]: [mod-init] Running Docker Modification Logic
```


## Via systemd
All x3 files are to be located in `/etc/systemd/system/` & following commands needs `sudo`

### Main Script
> https://stackoverflow.com/questions/79157218/bash-loop-to-get-docker-container-names-start-them-if-not-running

```
nano ukhan_docker.sh
chmod +x ukhan_docker.sh
```
_ukhan_docker.sh_
```
#!/bin/bash

container_id_list=$(docker ps -a -q -f "status=exited" -f "status=created")
for container_id in $container_id_list; do
    docker restart "${container_id}"
    # Set result based on exit code
    [[ $? -eq 0 ]] && result="SUCCESS" || result="FAILED"
    echo "Restart of container ${container_id} - ${result}"
    sleep 60
done
```
### Timer Script
> https://unix.stackexchange.com/a/294200/29032
> 
> https://www.freedesktop.org/software/systemd/man/latest/systemd.timer.html
```
nano ukhan_docker.timer
systemd-analyze verify ukhan_docker.timer #check for any syntax mistake
```
_ukhan_docker.timer_
```
[Unit]
Description=UKhan Docker Recurrence Checker

[Timer]
OnBootSec=3min
OnUnitActiveSec=15min
#  unit started 3 minutes after boot and then every 15 minutes after that first time

[Install]
WantedBy=timers.target
```
### Service Script
```
nano ukhan_docker.service
chmod +x ukhan_docker.service
```
_ukhan_docker.service_
```
[Unit]
Description = uKhan Docker State checker
After = network.target

[Service]
Type=exec
ExecStart=/etc/systemd/system/ukhan_docker.sh
TimeoutStartSec=600 #assuming you have x10 containers

[Install]
WantedBy=default.target
```
### Initiation
To see all files are setup ok
```
systemctl daemon-reload
systemctl enable ukhan_docker.timer
systemctl start ukhan_docker.timer
systemctl status ukhan_docker.timer #will show timer name
systemctl list-timers
journalctl -f --unit ukhan_docker.timer
systemctl status ukhan_docker.service #will show service proper start / exit
journalctl -f --unit ukhan_docker.service
```
## Via crontab
Create bash script & place it in any location

_ukhan_docker.sh_
```
#!/bin/bash

container_id_list=$(docker ps -a -q -f "status=exited" -f "status=created")
for container_id in $container_id_list; do
    docker restart "${container_id}"
    # Set result based on exit code
    [[ $? -eq 0 ]] && result="SUCCESS" || result="FAILED"
    echo "Restart of container ${container_id} - ${result}"
    sleep 60
done
```

Launch `sudo crontab -e` & add line `@reboot /etc/systemd/system/ukhan_docker.sh` (match your location)
