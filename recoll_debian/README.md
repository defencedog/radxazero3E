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
**Note webUI will run only if valid index exists before**
```
git clone https://framagit.org/medoc92/recollwebui.git #python3 webui
```
contents appended to `sudo nano /etc/rc.local` **
```
su <user> -c 'cd /home/<user>/recollwebui && ./webui-standalone.py -p 9080 -a <host ip>' 
exit 0
```

** Alternatively create a user service via `systemd`

```
cd ~/.config/systemd/user #create path if doesn't exist
nano recollwebui.service
systemctl --user enable recollwebui.service
systemctl --user start recollwebui.service
systemctl --user status recollwebui.service
```
File contents _recollwebui.service_
```
[Unit]
Description=Recoll webUI

[Service]
ExecStart=/bin/bash -c 'cd /home/<USER>/recollwebui && ./webui-standalone.py -p 9080 -a <host ip>'

[Install]
WantedBy=default.target
```

At CasaOs homepage click + at top right _Add external link_
> Link: http://hostip:9080
> 
> Title: Recoll
> 
> Icon: https://www.recoll.org/pics/recoll64.png
>

## As Daemon Service
For live monitoring of folder
```
cd ~/.config/systemd/user
cp /usr/share/recoll/examples/recollindex.service . #examples are included in /share/examples
nano recollindex.service #ensure binary location & make some modifications to make it run in nonGUI environment
systemctl daemon-reload
systemctl --user enable recollindex.service
systemctl --user start recollindex.service
journalctl -f --user-unit recollindex
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
Restart=on-failure #better try -> always
RestartSec=60

[Install]
WantedBy=default.target
```

## Recoll & Remote access via Twingate
It must be notes that because the above services are _user_ based so to access webUI you need to first login or `ssh` as that particular user otherwise webUI will be not be invoked. To solve this use
```
sudo loginctl enable-linger <user>
loginctl list-users #to verify functionality
```
Now _<user>_ will be autologged at any boot

## Multithreading & Parallelism
This official links explains in depth the features that can be used if you have high-end processor like RK3588
> https://www.recoll.org/usermanual/webhelp/docs/RCL.INDEXING.CONFIG.THREADS.DOCPREP.html
> 
> https://www.recoll.org/pages/idxthreads/threadingRecoll.html

For my RK3566 at 1.8GHz (can be [safely overclocked](https://github.com/defencedog/radxazero3E/tree/main/dtb_dtbo/overclocked) to 2.0GHz). Following setting have provided a bit parallelism. Edit `.conf` file
```
# Using x2 threads parallelism
thrQSizes = 2 -1 -1
thrTCounts =  2 1 1
```
& then `systemctl --user restart recollindex.service`

## WebUI Browser Experience
**Skip enabling _Local File Access_ features in browser; its a hassle & not needed!**

Click on the **main title** of file in search results; to have streaming pdf experience such that browser always open pdf in built-in _PDFViewer.js_ better to install following plugin, available both in Chromium & Firefox based browsers. 
> https://chromewebstore.google.com/detail/no-pdf-download/ikhahkidgnljlniknmendeflkdlfhonj
>
> https://addons.mozilla.org/en-US/firefox/addon/no-pdf-download/
> 
This PDF viewer extension (made by Mozzila) available in Chrome provides editing & annotating features as well

> https://chromewebstore.google.com/detail/pdf-reader/ieepebpjnkhaiioojkepfniodjmjjihl
