# Algorithm to follow for Radxa 3E running Headless

## Get OS
Use Debian Bookworm Server edition under Armbian [images available](https://www.armbian.com/radxa-zero-3/)
## OS setting up
### GPU & OpenCL / RustiCL
Get following packages not availble by default
```
sudo apt install update && sudo apt upgrade -y
sudo apt install -y mesa-utils mesa-opencl-icd clinfo linux-headers-vendor-rk35xx
```
### Samba sharing 
To be installed using `sudo armbian-config` > Software > Softy
- Samba
- OpenMediaVault (OMV) not working with Bookworm :(
- Setup windows drives with my [previous instructions](https://github.com/defencedog/orangepi3b_v2.1/blob/main/SAMBA_NAS_Videos.md)
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
### Favourite Docker Services
- ttydBridge
- Btop
- Glances
- Jellyfin (from default CasaOS store its RKMPP support produce better results. Please read Rockchip [VPU enabling instructions](https://jellyfin.org/docs/general/administration/hardware-acceleration/rockchip/))
### sist2 
Its an an advance file searcher / indexer. Had to be manually installed in CasaOS. My [instructions with image](https://github.com/simon987/sist2/issues/499#issue-2583469960)
