# Immich Migration to New Instance
My source machine & destination machine has same Armbian OS except the former is *headless* & not overclocked to 2GHz 
```
OS: Armbian 25.5.2 noble aarch64
Host: Rockchip RK3566 OPi 3B
Kernel: 6.1.115-vendor-rk35xx
Uptime: 2 hours, 7 mins
Packages: 2582 (dpkg)
Shell: bash 5.2.21
Resolution: 1024x768
Terminal: /dev/pts/3
CPU: (4) @ 1.992GHz
Memory: 2112MiB / 3911MiB
```
```
OS: Armbian 25.5.2 noble aarch64
Host: Radxa ZERO 3
Kernel: 6.1.115-vendor-rk35xx
Uptime: 15 hours, 32 mins
Packages: 1104 (dpkg)
Shell: bash 5.2.21
Terminal: /dev/pts/0
CPU: (4) @ 1.800GHz
Memory: 1207MiB / 3724MiB
```
## From Radxa 3E to OPi3b (both RK3566)
Install docker `sudo apt install docker-ce docker-ce-cli docker-compose containerd.io docker-compose-plugin` if you want to install very latest version not available in default repos [follow this](https://gist.github.com/serafdev/2914392a6c0a3650cd4b047909544ce7)
## Container location
I arbitrarily choose *~/.local/share/containers*
`cd ~/.local/share/containers && mkdir immich && cd immich` Open a separate terminal to ssh to Radxa3E to get folder locations. Get *library* folder from Radxa3E to new OPi3b do not copy *postgres* folder `scp ukhan@192.168.1.55:/DATA/AppData/immich/library .` Now you must have *~/.local/share/containers/immich/library* Use `du -sh` on both machines to check folder size to know everything is in sync
## Important HWaccel Variables
Place the attached x3 *.yaml* & x1 *.env* file in  *~/.local/share/containers/immich*

In the *.env* file db password & username are kept default which makes standardise immich migration among different machines also the data & db location folders are kept within immich parent folder

The RKNPU is activated by an overlay which is not discussed here however Armbian by default has RKNPU drivers. You can [read here](https://itsfoss.com/monitor-npu-linux/) to know if your NPU is loaded & working

In **headless** machine you can install vendor *libmali* via install `libmali-bifrost-g52-g13p0-dummy-wayland-gbm_1.9-1_arm64.deb` however don't do it if running GNOME it will break wayland! So in OPI3b I have to comment out `/usr/lib/aarch64-linux-gnu/libmali.so.1:/usr/lib/aarch64-linux-gnu/libmali.so.1:ro` in *hwaccel.transcoding.yml* 

To utilise OpenCl do `sudo apt install clinfo ocl-icd-libopencl1` It will give you a file `mesa.icd` in */etc/OpenCL/vendors* & on *headless* you can get `mali.icd` because I installed `libmali-bifrost-g52-g13p0-dummy-wayland-gbm_1.9-1_arm64.deb` In [kisak-mesa ppa](https://launchpad.net/~kisak/+archive/ubuntu/turtle/?field.series_filter=noble) one can also install `mesa-opencl-icd` I have not tested it. The **headless** environment i.e `mali.icd` exposes more hardware capabilities so better setup immich in *headless* environment. This statement can be verified by running `clinfo` & comparing terminal output
For details check **RKMPP** subsection in [official docs](https://immich.app/docs/features/hardware-transcoding/)
## Initiating Containers & Migration
After you have placed all compose / environment files & copied *library* folder
```
cd ~/.local/share/containers/immich
docker compose pull             # Update to latest version of Immich (if desired)
docker compose create           # Create Docker containers for Immich apps without running them
docker start immich_postgres    # Start Postgres server
```
By default, Immich will keep the last 14 database dumps and create a new dump every day at 2:00 AM. Check for latest db backup done my immich
```
cd ~/.local/share/containers/immich
ls -t | head -n 1
```
In my case it was *immich-db-backup-1757124000053.sql.gz* Now restore it
```
gunzip --stdout "~/.local/share/containers/immich/backup/immich-db-backup-1757124000053.sql.gz" \
| sed "s/SELECT pg_catalog.set_config('search_path', '', false);/SELECT pg_catalog.set_config('search_path', 'public, pg_catalog', true);/g" \
| docker exec -i immich_postgres psql --dbname=postgres --username=<DB_USERNAME>  # Restore Backup
docker compose up -d            # Start remainder of Immich apps
```
## Bonus
In *headless* Radxa3E I was using CasaOS but I don't want to burden feeble RK3566 of OPi3b further because it is already running GNOME so use `ctop` for container logging/start/stop...
```
cd /usr/local/bin
sudo wget -O ctop "https://github.com/bcicen/ctop/releases/download/v0.7.7/ctop-0.7.7-linux-arm64"
sudo chmod +x ctop
cd ~ && sudo ctop -a 
```
