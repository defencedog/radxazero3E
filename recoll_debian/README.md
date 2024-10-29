Latest Recoll `1.4` for `arm64` is not avaialble under Debian. These `.debs` are extracted from official Ubuntu Jammy PPA & offers no dependancy conflicts with Debian Bookworm
```
sudo apt install python-is-python3 -y
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
Preparation to start search & create index
```
mkdir ~/.recoll
cd ~/.recoll
nano recoll.conf
```
contents of file
```
# search paths
topdirs = /media/nas_1/UK_Docz/Standards_API /media/nas_1/Unsorted_Books /media/nas_1/UK_Docz/Books

compressedfilemaxkbs = -1

aspellLanguage = en
noaspell = 1

pdfocr = 1
ocrprogs = tesseract
tesseractlang = eng

#disable multi-threading on arm64
thrQSizes = -1 -1 -1
```
After this initiate first command to index data `recollindex -z` [Manpage](https://www.recoll.org/manpages/recollindex.1.html)

Recoll WebUI & CasaOS
```
git clone https://github.com/koniu/recoll-webui.git
sudo nano /etc/rc.local
```
contents appended to file
```
su <user> -c 'cd /home/<user>/recoll-webui && ./webui-standalone.py -p 9080 -a <host ip>' 
exit 0
```
**Note webUI will run only if valid index exists before**

At CasaOs homepage click + at top right _Add external link_
> Link: http://192.168.1.6:9080
> 
> Title: Recoll
> 
> Icon: https://www.recoll.org/pics/recoll64.png
