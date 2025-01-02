Because both OPi3b & RadxaZero3 have RK3566 so the implemenation of overclocking is same. It is discussed in [detail here](https://github.com/defencedog/orangepi3b_v2.1/tree/main/files_tools/vendor_Kernel6.1/Overclocked_dtb)

The `.dtb` can be moved & overwritten to `/boot/dtb/rockchip/`

Only CPU is OC from 1.8GHz to 2.0GHz. 

1. Overwrite original `.dtb`
2. `sudo reboot`
3. `sudo armbian-config` -> System -> CPU -> true -> select 2GHz -> select ondemand
4. `sudo reboot`
5. Use `sudo htop` to see CPU oveclocked
