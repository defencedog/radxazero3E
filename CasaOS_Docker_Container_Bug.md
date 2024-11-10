# OCI_Runtime | Proxy Binding Error while installing containers in CasaOS

## Bug
This bug I observed in all Armbian variants Ubuntu Jammy, Noble & Debian Bookworm

Bug changes but mostly it is like this 
> Error response from daemon: failed to create task for container: failed to create shim task: OCI runtime create failed: runc did not terminate successfully: exit status 134: unknown

Sometimes it changes to something more gibbersish but in the end CasaOS fails to initiate container at `proxy binding` step. Container do install 100%. The output of `sudo docker ps -a` display the container state as `created` not `started` This bug occurs after you have create 4 to 5 containers. This user experienced exactly [same issue](https://forums.docker.com/t/docker-error-response-from-daemon-failed-to-create-task-for-container-failed-to-create-shim-task-oci-runtime-create-failed-runc-did-not-terminate-successfully-exit-status-134-unknown/136097)

> The problem still exists today. I have now reinstalled the OS and Docker several times and tested the setup with different containers. After all that time I assume that there is actually a problem with the resources, because I can deploy between 5 and 6 containers at a time, depending on the images. One more run command and I get the aforementioned error.
> 
> My problem is that I have no idea which resource might be the limiting one. Using htop I can see that all CPUs are idling at about 0% to 1%. When I request a website from the docker, one of the four CPUs goes up to 25%, the others are still around 1%. Also, the memory is constantly between 900 and 1000 MB, but there are 8 GB available

Some user insisted its a memory leak / resources [problem](https://github.com/getsentry/self-hosted/issues/1438#issuecomment-1119860236) Then I tried to edit `/etc/security/limits.conf` as explained in [RHEL tutorial](https://access.redhat.com/solutions/22105) but didn't succeed 
## Solution 1 
If the output of `sysctl kernel.threads-max` is lower than 2000 increase it by editing `sudo nano /etc/sysctl.conf`
```
kernel.threads-max = 2055 # at EOF
```
I got this value from Armbian `noble` image running on same CPU RK3566 on OPi3b v2.1. Reboot afterwards
## Solution 2
Finally I used some old debian packages. It must be noted in official [Docker documentation](https://docs.docker.com/engine/install/ubuntu/) these legacy packages are meant to be removed but in my case I have to reinstall these! Issued the following command & it skipped some packages but did install some other legacy packages. After this my existing CasaOS containers were completely removed. I installed new ones with no error
```
for pkg in docker.io docker-doc docker-compose docker-compose-v2 podman-docker containerd runc golang-github-containernetworking-plugin-dnsname; do sudo apt-get reinstall $pkg; done
```
**Note** `golang-github-containernetworking-plugin-dnsname` is important for internal DNS name resolution especially if you wanr to run `paperless-ngx` stack [issue](https://github.com/paperless-ngx/paperless-ngx/discussions/7377#discussioncomment-10226382)
After a reboot `hold` these packages to avoid update
```
sudo apt-mark hold docker-* python3-compose* python3-docker* runc crun podman* containerd containernetworking-*
```
To view previous held packages `apt-mark showhold`
To un-hold held packages `sudo apt-mark unhold $(apt-mark showhold)`

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
