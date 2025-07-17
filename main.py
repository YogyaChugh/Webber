import urllib.request
import urllib.error
import chardet

import os
import sys
from bs4 import BeautifulSoup
import threading

file_types_list = [
    ".DOC", ".DOCX", ".EML", ".MSG", ".ODT", ".PAGES", ".RTF", ".TEX", ".TXT", ".WPD",
    ".AAE", ".BIN", ".CSV", ".DAT", ".KEY", ".LOG", ".MPP", ".OBB", ".PPT", ".PPTX",
    ".RPT", ".TAR", ".VCF", ".XML", ".AIF", ".FLAC", ".M3U", ".M4A", ".MID", ".MP3",
    ".OGG", ".WAV", ".WMA", ".3GP", ".ASF", ".AVI", ".FLV", ".M4V", ".MOV", ".MP4",
    ".MPG", ".SRT", ".SWF", ".TS", ".VOB", ".WMV", ".3DM", ".3DS", ".BLEND", ".DAE",
    ".FBX", ".MAX", ".OBJ", ".BMP", ".DCM", ".DDS", ".DJVU", ".GIF", ".HEIC", ".JPG",
    ".PNG", ".PSD", ".TGA", ".TIF", ".AI", ".CDR", ".EMF", ".EPS", ".PS", ".SKETCH",
    ".SVG", ".VSDX", ".INDD", ".OXPS", ".PDF", ".PMD", ".PUB", ".QXP", ".XPS",
    ".NUMBERS", ".ODS", ".XLR", ".XLS", ".XLSX", ".ACCDB", ".CRYPT14", ".DB", ".MDB",
    ".ODB", ".PDB", ".SQL", ".SQLITE", ".APK", ".APP", ".BAT", ".BIN", ".CMD", ".COM",
    ".EXE", ".IPA", ".JAR", ".RUN", ".SH", ".DEM", ".GAM", ".GBA", ".NES", ".PAK",
    ".PKG", ".ROM", ".SAV", ".DGN", ".DWG", ".DXF", ".STEP", ".STL", ".STP", ".GPX",
    ".KML", ".KMZ", ".OSM", ".ASP", ".ASPX", ".CER", ".CFM", ".CSR", ".CSS", ".HTML",
    ".JS", ".JSON", ".JSP", ".PHP", ".XHTML", ".CRX", ".ECF", ".PLUGIN", ".SAFARIEXTZ",
    ".XPI", ".FNT", ".OTF", ".TTF", ".WOFF", ".WOFF2", ".ANI", ".CAB", ".CPL", ".CUR",
    ".DESKTHEMEPACK", ".DLL", ".DMP", ".DRV", ".ICNS", ".ICO"
]

download_outputs = []


def download_file(link,url,enc=None,first = False):
    global download_outputs
    base_link = "" # Base link to store URL without the base domain
    cors = False
    fileName = "index.html"

    print("\n\n===========================\nURL SENT: ",link)
    if link.strip()=="/":
        download_outputs.append((link,None))
        return

    # For relative URLs
    if link[0:2]=="//":
        base_link = link[2:]
        link = "https://" + link[2:]
    elif link[0]=="/":
        base_link = link
        if url[-1]=="/":
            link = url + link
        else:
            link = url + "/" + link
    else:
        base_link = link.replace(url,"")

    if base_link.strip()=="/":
        download_outputs.append((link,None))
        return

    if url not in link[0:len(url)+1]:
        chacha = False
        for i in file_types_list:
            if i.lower() in link.lower():
                chacha = True
        if not chacha:
            download_outputs.append((link,None))
            return

    try:
        content = urllib.request.urlopen(link).read()
        text_files = ['.css','.html','.json','.js','.doc','.docx','.pdf','.txt']
        for pp in text_files:
            if pp == content[len(content) - len(pp):]:
                content = content.decode('utf-8')
                break
    except urllib.error.URLError as errorbaba:
        print(f"\n\n===========================================\nCouldn't process url ! {link}\nError msg: {errorbaba.reason}")
        download_outputs.append((link,None))
        return

    base_link = base_link.replace('"',"____dq")
    base_link = base_link.replace('<',"____lt")
    base_link = base_link.replace('>',"____gt")
    base_link = base_link.replace('|',"____vb")
    base_link = base_link.replace(':',"____col")
    base_link = base_link.replace('*',"____ast")
    base_link = base_link.replace('?',"____qm")
    base_link = base_link.replace(',',"____com")
    base_link = base_link.replace('\\',"____bs")
    
    if link!=url:
        temp = base_link.split("/")
        found = False
        new_link = ""
        for gg in file_types_list:
            bobby = temp[-1][(len(temp[-1]) - len(gg)):].lower()
            if gg.lower() == bobby:
                print(f'FOUND TYPE: {gg}')
                if temp[0]=="":
                    new_link = "/".join(temp[1:-1])
                else:
                    new_link = "/".join(temp[:-1])
                if new_link!="":
                    fileName = new_link + "/" + temp[-1]
                else:
                    fileName = temp[-1]
                found = True
                break
        if not found:
            new_link = base_link
            fileName = base_link + "/" + fileName
        print("Base URL: ",base_link)
        print("New Link: ",new_link)
        if new_link!="":
            os.makedirs(new_link,exist_ok=True)

    if (".html" not in fileName and ".js" not in fileName and ".css" not in fileName):
        file_type = "wb"
    else:
        file_type = "w"
            # detected_encoding = str(chardet.detect(content)["encoding"])
            # print("Encoding detected: ",detected_encoding)
            # if "None" not in detected_encoding and detected_encoding in ['ascii','utf-8']:
            #     content = str(content, encoding=detected_encoding)
            # else:
    if ".html" in fileName:
        content = BeautifulSoup(content,features="lxml").prettify()
    if ".html" in fileName or ".js" in fileName or ".css" in fileName:
        with open(fileName, file_type,encoding="utf-8") as file:
            try:
                file.write(content)
            except Exception as e:
                try:
                    file.write(content)
                except Exception as aa:
                    print("PROBLEM !!!!!!")
                    file.write(content.decode('utf-8'))
            print(f"[DEBUG] fileName={repr(fileName)}, type={file_type}\n\n")
    else:
        with open(fileName, file_type) as file:
            try:
                file.write(content)
            except Exception as e:
                print("PROBLEM !!!!!!")
                file.write(content.encode('utf-8'))
            print(f"[DEBUG] fileName={repr(fileName)}, type={file_type}\n\n")
    
    download_outputs.append((link,fileName))
    if first:
        return content
    return


url = input("WEBBER\n===========================\n\nEnter URL: ")

cont = download_file(url,url,"utf-8",first = True)
if cont==None:
    print("NOT POSSIBLE !")
    sys.exit()

count = 0
contenthji = cont
i = 0
links = []
while (i<len(contenthji)):
    if contenthji[i]=='"' and ( contenthji[i+1:i+5] == "http" or contenthji[i+1] == "/"):
        link = ""
        j = i
        i+=1
        while contenthji[i]!='"':
            if contenthji[i]==" ":
                link+= "%20"
            else:
                link += contenthji[i]
            i+=1
        links.append((link,j))
        #temp = download_file(link,url)
        #if temp:
        #    if link != temp[1]:
        #        contents.replace(link,temp[1])

    elif contenthji[i]=='"':
        i+=1
        while contenthji[i]!='"':
            i+=1
    i+=1


threads = []
for i in links:
    t = threading.Thread(target=download_file, args=(i[0],url))
    threads.append(t)
    temp = download_file(i[0],url)
    if temp:
        if i[0] != temp[1]:
            contenthji.replace(i[0],temp[1])

for t in threads:
    t.start()

for t in threads:
    t.join()

print(download_outputs)
for i in download_outputs:
    if i[1]:
        print("Replaced !")
        contenthji = contenthji.replace(i[0],i[1])

print(type(contenthji))
print(contenthji)

with open(download_outputs[0][1],"w",encoding="utf-8") as file:
    file.write(contenthji)