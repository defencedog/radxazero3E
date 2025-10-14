# Radxa 3E Armbian non-root access to GPIO

Add a new group & insert existing user (you) in it 
```
sudo groupadd gpio 
sudo usermod -aG gpio ukhan
getent group gpio #verify your username is present
sudo reboot
```
Verify following devices, locations & permissions
```
ls -lL /dev/gpio* #should return some gpiochip##
ls -lL /sys/class/gpio/ #should return same
```
Create a `udev` rule
```
sudo nano /etc/udev/rules.d/99-gpio-permissions.rules
sudo reboot
```
*99-gpio-permissions.rules* (its a single line entry)

`SUBSYSTEM=="gpio*", PROGRAM="/bin/sh -c 'chown -R root:gpio /sys/class/gpio && chmod -R 770 /sys/class/gpio; chown -R root:gpio /dev/gpiochip* && chmod -R 770 /dev/gpiochip*'"`

Finally repeat aforementioned permission codes at x2 different locations you will see `gpio` group being added
```
ukhan@radxa-zero3:~$ ls -lL /dev/gpio*
crwxrwx--- 1 root gpio 254, 0 Oct 14 02:05 /dev/gpiochip0
crwxrwx--- 1 root gpio 254, 1 Oct 14 02:05 /dev/gpiochip1
crwxrwx--- 1 root gpio 254, 2 Oct 14 02:05 /dev/gpiochip2
crwxrwx--- 1 root gpio 254, 3 Oct 14 02:05 /dev/gpiochip3
crwxrwx--- 1 root gpio 254, 4 Oct 14 02:05 /dev/gpiochip4
crwxrwx--- 1 root gpio 254, 5 Oct 14 02:04 /dev/gpiochip5
ukhan@radxa-zero3:~$ ls -lL /sys/class/gpio/
total 0
-rwxrwx--- 1 root gpio 4096 Oct 14 02:04 export
drwxr-xr-x 3 root root    0 Oct 14 02:04 gpiochip0
drwxr-xr-x 3 root root    0 Oct 14 02:04 gpiochip128
drwxr-xr-x 3 root root    0 Oct 14 02:04 gpiochip32
drwxr-xr-x 3 root root    0 Oct 14 02:04 gpiochip509
drwxr-xr-x 3 root root    0 Oct 14 02:04 gpiochip64
drwxr-xr-x 3 root root    0 Oct 14 02:04 gpiochip96
-rwxrwx--- 1 root gpio 4096 Oct 14 02:04 unexport
```
You can now run GPIO related scripts without `sudo` for instance [this project](https://github.com/defencedog/radxazero3E/blob/main/High_Power_Led_GPIO_Switch.md)
