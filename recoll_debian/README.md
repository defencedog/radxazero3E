## Setup files
Latest Recoll `1.4` for `arm64` is not available under Debian. These `.debs` are extracted from official Ubuntu Jammy PPA & offers no dependancy conflicts with Debian Bookworm
```
sudo apt install python-is-python3 python3-waitress -y
sudo apt install -s /*.deb # simulate install to know of any error
sudo apt install -y /*.deb
```
Archive contents
```
├── librecoll_1.40.3-1~ppa1~jammy1_arm64.deb
├── librecoll-dev_1.40.3-1~ppa1~jammy1_arm64.deb
├── python3-recoll_1.40.3-1~ppa1~jammy1_arm64.deb
├── recoll_1.40.3-1~ppa1~jammy1_all.deb
├── recollcmd_1.40.3-1~ppa1~jammy1_arm64.deb
└── recollgui_1.40.3-1~ppa1~jammy1_arm64.deb
```
Recoll data extraction from [external programs](https://www.recoll.org/pages/features.html#doctypes.helpers)
```
sudo apt install -y unrar gir1.2-poppler-0.18 pdftk-java ocrmypdf poppler-utils antiword unrtf python3-chm python3-py7zr djvulibre-bin 
```
## Configurations
Preparation to start search & create index
```
mkdir ~/.recoll
cd ~/.recoll
nano recoll.conf
```
contents of file
```
# search paths
topdirs = /media/nas_1/UK_Docz/Standards_API  /media/nas_1/UK_Docz/Books

# necessary parameter if running as daemon
monitordirs = /media/nas_1/UK_Docz/Standards_API  /media/nas_1/UK_Docz/Books

compressedfilemaxkbs = -1

aspellLanguage = en
noaspell = 1

pdfocr = 1
ocrprogs = tesseract
tesseractlang = eng

#disable multi-threading on arm64
thrQSizes = -1 -1 -1

#logging https://www.recoll.org/faqsandhowtos/logfilesetup.html
loglevel = 4
logfilename = stderr
```
After this initiate first command to index data `recollindex -z 2>&1 | tee ~/recollindex.log` [Manpage](https://www.recoll.org/manpages/recollindex.1.html) For incremental indexes use `recollindex -k 2>&1 | tee ~/recollindex.log`

## Recoll WebUI & CasaOS Startup
```
git clone https://framagit.org/medoc92/recollwebui.git #python3 webui
sudo nano /etc/rc.local
```
contents appended to file**
```
su <user> -c 'cd /home/<user>/recollwebui && ./webui-standalone.py -p 9080 -a <host ip>' 
exit 0
```
**Note webUI will run only if valid index exists before**

At CasaOs homepage click + at top right _Add external link_
> Link: http://hostip:9080
> 
> Title: Recoll
> 
> Icon: https://www.recoll.org/pics/recoll64.png
>

** Alternatively create a user service via `systemd`

```
cd ~/.config/systemd/user #create path if doesnt exist
nano recoll_webui.service
systemctl --user enable recoll_webui.service
systemctl --user start recoll_webui.service
systemctl --user status recoll_webui.service
```
File contents _recoll_webui.service_
```
[Unit]
Description=Recoll webUI

[Service]
ExecStart=/bin/bash -c 'cd /home/<USER>/recollwebui && ./webui-standalone.py -p 9080 -a 192.168.1.6'

[Install]
WantedBy=multi-user.target #in case of error try default.target
```

## As Daemon Service
For live monitoring of folder
```
cd ~/.config/systemd/user
cp /usr/share/recoll/examples/recollindex.service . #examples are included in /share/examples
nano recollindex.service #ensure binary location & make some modifications to make it run in nonGUI environment
systemctl daemon-reload
systemctl --user enable recollindex.service
systemctl --user start recollindex.service
journalctl -xef --user-unit recollindex
```
File contents _recollindex.service_
```
# Contributed by Frank Dana, licensed as Recoll itself
[Unit]
Description=Recoll real-time document indexing
After=network-online.target

[Service]
Type=exec
ExecStart=/usr/bin/recollindex -m -D -x -w 30 -c %h/.recoll/
Restart=on-failure
RestartSec=60

[Install]
WantedBy=multi-user.target #in case of error try default.target
```

## Multithreading & Parallelism
This official links explains in depth the features that can be used if you have high-end processor like RK3588
> https://www.recoll.org/usermanual/webhelp/docs/RCL.INDEXING.CONFIG.THREADS.DOCPREP.html
> https://www.recoll.org/pages/idxthreads/threadingRecoll.html

For my RK3566 at 1.8GHz (can be safely OC to 2.0GHz) following setting have provided a bit parallelism. Edit `.conf` file
```
# Using x2 threads parallelism
thrQSizes = 2 -1 -1
thrTCounts =  2 1 1
```
& then `systemctl --user start recollindex.service`
