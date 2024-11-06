# OCI_Runtime | Proxy Binding Error while installing containers in CasaOS

This bug I observed in all Armbian variants Ubuntu Jammy, Noble & Debian Bookworm

Bug changes but mostly it is like this 
> Error response from daemon: failed to create task for container: failed to create shim task: OCI runtime create failed: runc did not terminate successfully: exit status 134: unknown

Sometimes it changes to something more gibbersish but in the end CasaOS fails to initiate container at `proxy binding` step. Container do install 100%. The output of `sudo docker ps -a` display the container state as `created` not `started` This bug occurs after you have create 4 to 5 containers. This user experienced exactly [same issue](https://forums.docker.com/t/docker-error-response-from-daemon-failed-to-create-task-for-container-failed-to-create-shim-task-oci-runtime-create-failed-runc-did-not-terminate-successfully-exit-status-134-unknown/136097)

> The problem still exists today. I have now reinstalled the OS and Docker several times and tested the setup with different containers. After all that time I assume that there is actually a problem with the resources, because I can deploy between 5 and 6 containers at a time, depending on the images. One more run command and I get the aforementioned error.
> 
> My problem is that I have no idea which resource might be the limiting one. Using htop I can see that all CPUs are idling at about 0% to 1%. When I request a website from the docker, one of the four CPUs goes up to 25%, the others are still around 1%. Also, the memory is constantly between 900 and 1000 MB, but there are 8 GB available

Some user insisted its a memory leak / resources [problem](https://github.com/getsentry/self-hosted/issues/1438#issuecomment-1119860236) Then I tried to edit `/etc/security/limits.conf` as explained in [RHEL tutorial](https://access.redhat.com/solutions/22105) but didn't succeed 

Finally I used some old debian packages. It must be noted in official [Docker documentation](https://docs.docker.com/engine/install/ubuntu/) these legacy packages are meant to be removed but in my case I have to reinstall these! Issued the following command & it skipped some packages but did install some other legacy packages. After this my existing CasaOS containers were completely removed. I installed new ones with no error
```
for pkg in docker.io docker-doc docker-compose docker-compose-v2 podman-docker containerd runc; do sudo apt-get reinstall $pkg; done
```
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
sudo service ukhan_docker enable
sudo reboot
```
File contents

```
#!/bin/bash

container_id_list=$(docker ps -a -q -f "status=exited" -f "status=created")
for container_id in $container_id_list; do
    docker restart "${container_id}"
    # Set result based on exit code
    [[ $? -eq 0 ]] && result="SUCCESS" || result="FAILED"
    echo "Restart of container ${container_id} - ${result}"
    sleep 10
done
```
Output
> Emulate Docker CLI using podman. Create /etc/containers/nodocker to quiet msg.
> 
> 6d0d101e768d
> 
> Restart of container 6d0d101e768d - SUCCESS
> 
> Emulate Docker CLI using podman. Create /etc/containers/nodocker to quiet msg.
> 
> 20523390e63b
> 
> Restart of container 20523390e63b - SUCCESS
