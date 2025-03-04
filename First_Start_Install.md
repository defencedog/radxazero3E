# Algorithm to follow for Radxa 3E running Headless

## Get OS
Use Debian Bookworm Server edition under Armbian [images available](https://www.armbian.com/radxa-zero-3/)
## OS setting up
### GPU & OpenCL / RustiCL
Get following packages not availble by default
```
sudo apt install update && sudo apt upgrade -y
sudo apt install -y 7zip mesa-utils mesa-opencl-icd clinfo linux-headers-vendor-rk35xx python-is-python3 
```
## Install Recoll 
Instructions [in this repo](https://github.com/defencedog/radxazero3E/tree/main/recoll_debian)
## Install ripgrepall
Pre-compiled binaries [in this repo](https://github.com/defencedog/orangepi3b_v2.1/tree/main/files_tools/ripgrep-all)
## Replace `mv` & `cp` bash commands
> https://github.com/defencedog/orangepi3b_v2.1/tree/main/files_tools/advcpmv
## CasaOS
### Install
```
wget -qO- https://get.casaos.io | sudo bash
sudo reboot
```
### Add external stores
Compilation of [extensive list](https://awesome.casaos.io/content/3rd-party-app-stores/list.html). My favourites
```
https://casaos-appstore.paodayag.dev/linuxserver.zip
https://github.com/bigbeartechworld/big-bear-casaos/archive/refs/heads/master.zip
```
Watch how to add [external stores](https://community.zimaspace.com/t/how-to-add-casaos-linuxserver-app-store-to-casaos/292/1)
### Samba sharing (must be installed AFTER CasaOS; dependencies conflict otherwise)
To be installed using `sudo armbian-config` > Software > Softy
- ~~Samba~~ taken care by CasaOS
- OpenMediaVault (OMV) not working with Bookworm :( Alternative is `cockpit`
- Setup windows drives with my [previous instructions](https://github.com/defencedog/orangepi3b_v2.1/blob/main/SAMBA_NAS_Videos.md)
### Favourite Docker Services
- ttydBridge
- Btop
- Glances
- Dozzle
- NGINX Proxy Manager to get valid SSL certificates [Youtube tutorial](https://www.youtube.com/watch?v=qlcVx-k-02E)
### Favourite Docker Apps
Some CasaOS compatible `yamls` are present [here](https://github.com/defencedog/radxazero3E/tree/main/CasaOS_yaml)
- Jellyfin (from default CasaOS store its RKMPP support produce better results)

Please read Rockchip [VPU enabling instructions](https://jellyfin.org/docs/general/administration/hardware-acceleration/rockchip/) Remember to add x4 devices.  `/dev/mali0` is not present on RK3566 also remember to create `99-rk-device-permissions.rules` as written in instructions. In CasaOS `Priveleges` slider should be ON
- sist2

Its an an advance file searcher / indexer. Use [sqlite database](https://github.com/defencedog/radxazero3E/blob/main/CasaOS_yaml/sist2_less_resource.yaml) & other tweaks for saving resources. Had to be manually installed in CasaOS. My [instructions with image](https://github.com/simon987/sist2/issues/499#issue-2583469960)
- Syncthing

Its an synchronisation service to sync multiple locations in multiple devices
- ~Calibre~ Not good for notes / full text search; use Paperless-ngx

A library database creator / editor with _full-text search_ [FTS capability](https://calibre-ebook.com/new-in/fifteen)
- ~Calibre-Web~ Not good for notes / full text search; use Paperless-ngx

A GUI reader / webUI for library database created by Calibre
- [Paperless-ngx](https://github.com/defencedog/radxazero3E/tree/main/paperless-ngx) 
### Samba sharing with CasaOS
The normal `smb.conf` is not present & is replaced by `smb.casa.conf`. Lets assume we have a directory (external USB or memory card) mounted at `/media/sdcard` (use `df -hT` to know mount points) To make it a NAS with name _radxasdcard_
```
sudo chown -R $USER:$USER /media/sdcard #Step essential if partition is of ext4 type
sudo chmod 777 /media/sdcard #Step essential if partition is of ext4 type
sudo smbpasswd -a ukhansmb #add a user it can be any name & set password
sudo nano /etc/samba/smb.casa.conf #sometimes smb.conf
```
**Note** Adding user `ukhansmb` may give error _failed to add entry for the user_ so you have to do to `sudo useradd ukhansmb` or simply use linux username [source](https://askubuntu.com/a/362864/110979)

Append to file contents; share only available to user _ukhan_
```
[radxa2tb]
comment = CasaOS share external hdd ntfs
path = /media/radxa2tb
read only = No
#public = No #Yes, for Public access
#guest ok = No #Yes, for Public access
writable = Yes
browseable = Yes
valid users = ukhansmb #Delete line, for Public access

[radxa128gb]
comment = CasaOS share external sdcard ext4
path = /media/radxa128gb
read only = No
#public = No #Yes, for Public access
#guest ok = No #Yes, for Public access
writable = Yes
browseable = Yes
valid users = ukhansmb #Delete line, for Public access
create mask = 0777
directory mask = 0777
```
Test the `smb.conf` file by executing command at terminal `testparm` Finally to make changes persistent `sudo systemctl restart smbd`

**Note** In my test under Ubuntu following lines were throwing errors & `smbd.service` could not run, so I have to remove them
```
public = No #Yes, for Public access
guest ok = No #Yes, for Public access
```
**Error**
> set_variable_helper(No #Yes, for Public access): value is not boolean!
>
> smbd --foreground --no-process-group $SMBDOPTIONS (code=exited...
> 
Compare your `.conf` contents at `/etc/samba` with [mine](https://github.com/defencedog/radxazero3E/tree/main/etc_samba)
### Bug: OCI / Port-bind CasaOS or Resources not available or Cannot start new thread
Solution [in this repo](https://github.com/defencedog/radxazero3E/blob/main/CasaOS_Docker_Container_Bug.md)

### CLI Monitoring tools for containers
- `watch -n 1 'docker stats --no-stream | sort -k 4 -h -r | head -10'`
- `ctop`
```
echo "deb [signed-by=/usr/share/keyrings/azlux-archive-keyring.gpg] http://packages.azlux.fr/debian/ stable main" | sudo tee /etc/apt/sources.list.d/azlux.list
sudo wget -O /usr/share/keyrings/azlux-archive-keyring.gpg  https://azlux.fr/repo.gpg
sudo apt update
sudo apt install docker-ctop
sudo ctop -a -s mem #active containers only sorted by memory%
sudo ctop -a -s cpu #active containers only sorted by cpu%
```
> https://packages.azlux.fr/

## Python3
First install `sudo apt install python3-pip` then install packages **without root** like `pip install plotext psutil jupyter numpy sympy coolprop --break-system-packages` This will create a new _environment_ or a _directory_ that has all python executables & libraries. Afterwards restart terminal or _ssh session_. In terminal `echo $PATH` if output shows `/home/ukhan/.local/bin` following step is not required
### Optional Step
To make executables available system-wide `nano ~/.bashrc` & press `Alt`+`/` go to EOF. Add
```
# ukhan additions
export PATH="/home/ukhan/.local/bin:$PATH"
```
Afterwards restart terminal or _ssh session_

