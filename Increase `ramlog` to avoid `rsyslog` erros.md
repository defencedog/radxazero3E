## Symptoms
High CPU% usage for `rsyslogd`. Plethora of errors oozed out by `journalctl -f -u rsyslog.service`. `df -h` confirms no space left for /var/log
```
Filesystem                Size  Used Avail Use% Mounted on
tmpfs                     769M   24M  745M   4% /run
/dev/mmcblk1p2            116G   32G   84G  28% /
tmpfs                     3.8G  100K  3.8G   1% /dev/shm
tmpfs                     5.0M     0  5.0M   0% /run/lock
tmpfs                     3.8G  4.0K  3.8G   1% /tmp
/dev/md127                439G   65G  352G  16% /media/radxaRaid480gb
/dev/mmcblk1p1            256M  157M  100M  62% /boot
/dev/sdd1                 117G   37G   75G  34% /media/radxa128gb
/dev/zram1                 47M   46M     0 100% /var/log
```
## Solution
If you go to the /etc/default directory, there should be a file called <distro>-ramlog. If you're on armbian it will be `armbian-ramlog` or `orangepi-ramlog`

In this file there will be a line reading
```
"SIZE=50M"
```
Simply edit this line to whatever value you'd like, and then reboot the device.

If rebooting the system will cause serious problems, you can use the following command on armbian:
 
```
service armbian-zram-config restart
#or
service orangepi-zram-config restart 
```
Don't panic if you notice that this command results in the creation of a zram2 and zram3, as these duplicates will automatically remove themselves the next time you reboot the machine

## Caution
For now, I've set /dev/zram1 to be 256MB instead of 50, to hopefully allow more time for the logs to properly rotate / clean themselves up.  The larger question I have is, what is the intent of having this configured?  Is it to prevent wear & tear on the SD card with all of the log writing? The answer is **YES**
**Sacrifice small RAM for sdcard reliability**
