To manually set the CPU frequency in Armbian, follow these steps:

### **Check Available Frequencies and Governors**
1. Open a terminal and check the available frequencies:
   ```bash
   cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_available_frequencies
   ```
2. Check the available governors:
   ```bash
   cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_available_governors
   ```

### **Set CPU Governor**
To set the CPU governor to `performance`, `powersave`, or another mode:
```bash
echo performance | sudo tee /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor
```

### **Manually Set Frequency**
To manually set a specific frequency:
```bash
echo <desired_frequency> | sudo tee /sys/devices/system/cpu/cpu*/cpufreq/scaling_max_freq
echo <desired_frequency> | sudo tee /sys/devices/system/cpu/cpu*/cpufreq/scaling_min_freq
```
For example, to set the CPU to 1.8GHz:
```bash
echo 1800000 | sudo tee /sys/devices/system/cpu/cpu*/cpufreq/scaling_max_freq
echo 1800000 | sudo tee /sys/devices/system/cpu/cpu*/cpufreq/scaling_min_freq
```

### **Make Settings Persistent**
To apply these settings at boot:
1. Edit `/etc/rc.local`:
   ```bash
   sudo nano /etc/rc.local
   ```
2. Add the following before `exit 0`:
   ```bash
   echo 1800000 > /sys/devices/system/cpu/cpu*/cpufreq/scaling_max_freq
   echo 1800000 > /sys/devices/system/cpu/cpu*/cpufreq/scaling_min_freq
   echo performance > /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor
   ```
3. Save and exit, then reboot:
   ```bash
   sudo reboot
   ```
