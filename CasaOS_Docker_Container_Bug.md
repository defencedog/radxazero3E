# `OCI runtime` | `crun` errors at containers startup in CasaOS

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
Finally I used some old debian packages. It must be noted in official [Docker documentation](https://docs.docker.com/engine/install/ubuntu/) these legacy packages are meant to be removed but in my case I have to reinstall these! Issued the following command & it skipped some packages but did install some other legacy packages. **After this my existing CasaOS containers were completely removed.** I installed new ones with no error
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

## Solution 3
I recently updated Casa-OS after about x6 months of stable system run. Again this `OCI-runtime` / `crun` errors are happening. Considering same `podman` version as well as same Ubuntu `Noble` release it seems others also have this issue

> https://askubuntu.com/questions/1517387/container-is-stuck-in-state-stopping-cannot-clear-it

I have installed a great docker management CLI utility `ctop` by running `sudo ctop -a` it showed me all containers managed by `podman` but it was **incomplete** list. This helped me but I didnt want to loose by containers & respective data

> https://unix.stackexchange.com/a/739025/29032

So I issued in the terminal (but **didn't press yes**) `sudo podman system reset` & it showed x2 old containers that were invisible in Casa-OS webui, `ctop` or `podman ps -a`! I removed those x2 entries one by one via `sudo podman rm <container_id>` & reboot system. Everything stable for now.

The other issue I discovered relates to `systemd` & startup of containers at boot. This is dicsussed here:

> https://github.com/defencedog/radxazero3E/blob/main/Systemd_Service_Docker_health_checker.md

