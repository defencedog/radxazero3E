Here are overlays for *zero3E* both sources & build. An archived clone of https://github.com/radxa-pkg/radxa-overlays
```
sudo nano /boot/armbianEnv.txt
# modify -> overlay_prefix=rk3568
7z x radxa-zero3e_compiled_dtbo.7z
cp *.dtbo /boot/dtb/rockchip/overlay/
```
Now you can use `armbian-config` to activate / deactivate overlays easily

## Interesting Overlays
- Use zero3E power supply USB-C port as normal USB 2.0 storage port
Activate `rk3568-dwc3-host.dtbo` provided you are powering zero3E via GPIO correctly. [Read how](https://forum.radxa.com/t/power-the-zero-via-gpio-pins/13465/4)
- Use zero3E power supply USB-C port as normal USB 2.0 peripheral port
Activate `rk3568-dwc3-peripheral.dtbo`
