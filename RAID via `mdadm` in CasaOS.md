This [youtube video](https://www.youtube.com/watch?v=ktfAQ363NmY) by *TECHNiCKR Global* is perhaps the most straightfoward solution to install `cockpit` alongside CasaOS. Cockpit then will be used to create & manage RAID arrays. I only use RAID1 (mirroring)

## The Bug in Cockpit
One of the Cockpit module is using [too much resources](https://askubuntu.com/questions/1399191/pmproxy-using-100-cpu) & perhaps not suitable for SBC environment. Remove x2 packages `sudo apt remove --purge cockpit-pcp pcp`

## `mdadm` Management
Check for `mdadm` devices names & RAID type
```
$ cat /proc/mdstat
Personalities : [raid1] [linear] [multipath] [raid0] [raid6] [raid5] [raid4] [raid10]
md127 : active raid1 sdb[1]
      468719424 blocks super 1.2 [2/1] [_U]
      bitmap: 4/4 pages [16KB], 65536KB chunk
```
Check health of a particular array
```
$ sudo mdadm --D /dev/md127
/dev/md127:
           Version : 1.2
     Creation Time : Tue May 20 22:09:14 2025
        Raid Level : raid1
        Array Size : 468719424 (447.01 GiB 479.97 GB)
     Used Dev Size : 468719424 (447.01 GiB 479.97 GB)
      Raid Devices : 2
     Total Devices : 1
       Persistence : Superblock is persistent

     Intent Bitmap : Internal

       Update Time : Sun Jun 29 02:55:08 2025
             State : clean, degraded
    Active Devices : 1
   Working Devices : 1
    Failed Devices : 0
     Spare Devices : 0

Consistency Policy : bitmap

              Name : radxa-zero3:radxaRaid480gb  (local to host radxa-zero3)
              UUID : 05f7715d:dc7fca1e:b48190c6:cb14bdbb
            Events : 83219

    Number   Major   Minor   RaidDevice State
       -       0        0        0      removed
       1       8       16        1      active sync   /dev/sdb
```
**Degraded state** & one hardisk is not detected or powered off
### Troubleshooting
`cockpit` webui can also tell you these stuff. The device /dev/sda` seems to be problematic or the USB port is faulty. Test these x2 possibilities via using`sda` on another computer. Another USB or peripheral can be inserted into suspected USB port; use `lsusb` to check if its detected
### Solution
If the `sda` & port are both healthy then simply removing & re-adding the storage to RAID array will do the trick.
```
mdadm --manage /dev/md127 -r /dev/sda #hot remove
sleep 10
mdadm --manage /dev/md127 -a /dev/sda #re-add device
watch cat /proc/mdstat #resyncing will begin may take hours
```
### Bugs
Array stopping didn't work even though array was properly unmounted. I tried disabling services like `smbd`, `casaos`  ...but to no avail
- https://superuser.com/questions/471327/how-to-force-mdadm-to-stop-raid5-array
### Resources
- https://www.thomas-krenn.com/en/wiki/Mdadm_recovery_and_resync
#storage #linux
