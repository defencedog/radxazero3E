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
## Setup CasaOS
```
wget -qO- https://get.casaos.io | sudo bash
sudo reboot
```
