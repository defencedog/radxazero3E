# Recurring service to auto restart any nonfunctional container

All x3 files are to be located in `/etc/systemd/system/` & following commands needs `sudo`

## Main Script
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
    sleep 30
done
```
## Timer Script
> https://stackoverflow.com/a/50539088/1162750
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
OnStartupSec=120
OnCalendar=*-*-* *:*:05
# After boot delay 120sec & restart .service after every 5min

[Install]
WantedBy=timers.target
```
## Service Script
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

[Install]
WantedBy=default.target
```
## Initiation
To see all files are setup ok
```
systemctl daemon-reload
systemctl enable ukhan_docker.timer
systemctl start ukhan_docker.timer
systemctl status ukhan_docker.timer #will show timer name
systemctl status ukhan_docker.service #will show service proper start / exit
```
