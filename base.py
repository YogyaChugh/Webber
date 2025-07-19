from urllib.parse import urlparse
import urllib.request
import exceptions
import os
import json
from bs4 import BeautifulSoup
import cssbeautifier
import jsbeautifier
import chardet
import webview
import threading
import logging
import re
import traceback
import sys
import time
import asyncio
import loading_animation
import magic
import tldextract


def dir(self) -> str:
    return os.path.join(sys._MEIPASS, self._DATA_DIR)


class Webpage:
    def __init__(self,url, website,download_res = True, download_cors_res = True):
        self.url = url
        self.download_res = download_res
        self.download_cors_res = download_cors_res
        self.file_location = None
        self.fileName = "index.html"
        self.website = website
        

        self.failed_downloads = []

        self.loc = os.path.join(os.getcwd(), website.location)

        # Sets
        self.main_files = set() # Contains .html, .css and .js files !
        self.res_files = set() # Other files !

        self.type = None

        # # Forming base url
        # temp = eval(os.environ.get("file_types"))
        # done = False
        # for i in temp:
        #     if self.url[len(self.url) - len(i):].lower() == i.lower():
        #         self.base_url = "/".join((self.url.split("/")[:-1])) + "/"
        #         done = True
        #         self.type = i
        #         break
        
        # if not done:
        #     self.base_url = self.url + ("/" if not self.url.endswith("/") else "")
        #     self.type = ".HTML"

        filetype = ".html"
        aa = url.replace('\\','/')
        for i in eval(os.environ.get('file_types')):
            if i.lower() in (aa.split('/')[-1]).lower():
                filetype = i.lower()
                break
        
        log_file_location = self.create_offline_location(url, filetype, True, 'logs')

        main_name = log_file_location[1].replace(filetype,"")
        os.makedirs(f"{log_file_location[0]}",exist_ok=True)
        self.logs = open(f'{log_file_location[0]+main_name}.log','w')
        self.logs.write(f"Webpage created for {url}")

    def __del__(self):
        try:
            self.logs.close()
        except Exception:
            pass
    
    def download_resource(self,url,file_type = None):
        urlpath = str(url.path)
        file_type = file_type
        if not file_type or file_type==".txt":
            if ".css" == urlpath[-4:]:
                file_type = ".css"
            elif ".js" == urlpath[-3:]:
                file_type = ".js"
            elif ".html" == urlpath[-5:]:
                file_type = ".html"
            elif ".xml" == urlpath[-4:]:
                file_type = ".xml"
            else:
                for i in eval(os.environ.get('file_types')):
                    if i.lower() in urlpath.lower():
                        file_type = i.lower()
                        break
            if file_type==None:
                file_type = ".html"
        try:
            if file_type in ['.html','.css','.js','.xml','.txt']:
                self.logs.write(f"\n\nURL REQUESTED: {url.geturl()}")
            else:
                self.logs.write(f"\n\nRESOURCE REQUESTED: {url.geturl()}")
            gggg = (url.geturl()).replace(" ","%20")
            content = urllib.request.urlopen(gggg).read()
            self.logs.write("\nRECEIVED CONTENTS SUCCESSFULLY !\n\n")
        except Exception:
            try:
                content = urllib.request.urlopen("https://www.example.com").read()
            except Exception:
                raise exceptions.NoInternetConnection()
            self.logs.write("\nFile Couldn't be downloaded!")
            raise exceptions.FileDownloadError(urlpath)
    
        if file_type == ".html":
            content = content.decode("utf-8")
            content = BeautifulSoup(content, features="html5lib")
        elif file_type == ".css":
            content = content.decode("utf-8")
            content = str(cssbeautifier.beautify(content))
        elif file_type == ".js":
            content = content.decode("utf-8")
            content = str(jsbeautifier.beautify(content))
        elif file_type == ".xml":
            content = content.decode('utf-8')
            content = BeautifulSoup(content, features="xml")
        return {'file_content': content, 'file_type': file_type}
    
    def create_offline_location(self, file_loc_url, file_type, main=False, inside_folder = ""):
        fileName = "index.html"
        file_loc_url = file_loc_url.replace("\\","/")
        temp_split = file_loc_url.split("/")

        temp = urlparse(self.url)

        file_path = ""
        if not( file_type==".html" and file_loc_url[-5:]!=".html"):
            fileName = temp_split[-1]
        
        if fileName!="index.html":
            file_path = "/".join(temp_split[:-1])
        else:
            file_path = file_loc_url

        mid = "://" if str(temp.scheme) else ""
        file_path = file_path.replace(str(temp.scheme) + mid + str(temp.hostname), "")
        while file_path.startswith("/"):
            file_path = file_path[1:]
        new_file_path = ""
        for i in range(len(file_path)):
            code = ord(file_path[i])
            if (code<47 or code>57) and (code<65 or code>172) and code not in [33,35,36,37,38,39,40,41,43,44,45,46,47,59,61,64,123,125,126]:
                new_file_path += chr((code % 65) + 65)
            else:
                new_file_path += file_path[i]

        if inside_folder:
            tempy = inside_folder + "/" + new_file_path + ("/" if new_file_path else "")
        else:
            tempy = new_file_path + ("/" if new_file_path else "")

        if self.website.url.hostname==temp.hostname:
            tempy = self.loc + ("/" if self.loc else "") + str(temp.hostname) + ("/" if temp.hostname else "") + tempy
        else:
            tempy = self.loc + ("/" if self.loc else "") + str(self.website.url.hostname) + ("/" if str(self.website.url.hostname) else "") + str(temp.hostname) + ("/" if str(temp.hostname) else "") + tempy
        if main:
            self.file_location = tempy
            self.fileName = fileName
        return (tempy,fileName)
    
    def save_file(self, file_loc, fileName, file_content, file_type):        
        try:
            os.makedirs(file_loc, exist_ok = True)
        except Exception:
            raise exceptions.FileSaveError(file_loc + fileName)
        
        enc = None
        encoding = "utf-8"
        skip_last = False

        if file_type==".html" and fileName[-5:]!='.html':
            enc = "w"
        else:
            if file_type in [".html",".css",".js",".xml"]:
                enc = "w"
            else:
                encoding = None
                enc = "wb"
            skip_last = True
        
        if encoding:
            with open(file_loc + fileName, 'w', errors='replace',encoding=encoding) as file:
                try:
                    file.write(file_content)
                except Exception:
                    try:
                        file.write(str(file_content))
                    except Exception:
                        result = chardet.detect(file_content)
                        encoding = result['encoding']
                        decoded_data = file_content.decode(encoding, errors="replace")
                        file.write(decoded_data)
        else:
            with open(file_loc + fileName, 'wb') as file:
                try:
                    file.write(file_content)
                except Exception:
                    try:
                        file.write(str(file_content))
                    except Exception:
                        result = chardet.detect(file_content)
                        encoding = result['encoding']
                        decoded_data = file_content.decode(encoding, errors="replace")
                        file.write(decoded_data)
        self.logs.write(f"\nFILE SAVED SUCCESSFULLY ! {file_loc + fileName}\n\n")
    
    def find_urls(self, content, is_html = False):
        urls = set()
        final_content = ""
        self.logs.write("\n=========================\nFINDING INTERNAL URLS.....\n=========================")
        if is_html:
            for i in content.find_all(True):
                content_to_search = i
                if i.name not in ["script","style"]:
                    attributes = list(i.attrs.values())
                    content_to_search = "".join(str(attributes))
                else:
                    content_to_search = str(i)

                # This takes care of all absolute urls
                urlsji = re.findall(r'https?://[^\s]+', content_to_search)
                for url in urlsji:
                    ext = tldextract.extract(url)
                    if ext.suffix:  # Valid TLD
                        urls.add(url)
                # This takes care of relative urls
                final_content += content_to_search
        else:
            final_content = content
            urlsji = re.findall(r'https?://[^\s]+', content_to_search)
            for url in urlsji:
                ext = tldextract.extract(url)
                if ext.suffix:  # Valid TLD
                    urls.add(url)
            urls = urls.union(extractor.find_urls(final_content))
        self.logs.write("\nAUTO FIND COMPLETE :)")
        for i in urls.copy():
            if i in self.website.urls_searched:
                self.logs.write(f"\n\t\tSkipped URL: {i}")
                urls.remove(i)
            else:
                self.logs.write(f"\n\t\t{i}")
        self.website.urls_searched.union(urls)
        main_link = urlparse(self.url)
        prev_links = {}
        link = ""
        self.logs.write("\n\nMANUAL FIND START !")

        #! ONLY THING WRITTEN BY CHATGPT ! I SUCK AT REGEX !
        pattern = re.compile(r'''
            (['"])                    # Group 1: opening quote
            (                         # Group 2: full path inside quotes
                (\\{1,2}|/{1,2})      # starts with 1 or 2 slashes or backslashes
                (?=                   # lookahead: must have at least one alphanumeric after slashes
                    [^'"\\\n]*[a-zA-Z0-9]
                )
                [^'"\\\n]{1,}         # at least one character (excluding quote/backslash/newline)
            )
            \1                        # closing quote matching opening
        ''', re.VERBOSE)
        #! YEP ! THAT's IT
        for match in pattern.finditer(final_content):
            full_string = match.group(0)
            full_string = str(full_string)
            if full_string.strip() not in ['/','\\','']:
                if full_string[1:].startswith("//") or full_string[1:].startswith("\\"):
                    temp = str(main_link.scheme) + ":" + full_string[1:-1]
                else:
                    temp = str(main_link.scheme) + "://" + str(main_link.hostname) + full_string[1:-1]
                if temp not in self.website.urls_searched:
                    self.website.urls_searched.add(temp)
                    urls.add(temp)
                    prev_links[temp] = full_string[1:-1]
                    self.logs.write(f"\n\t\t{temp}")
                else:
                    self.logs.write(f"\n\t\tSkipped URL: {temp}")


        # while temp_i<len(final_content):
        #     if not waiting:
        #         if final_content[temp_i]=="\"" or final_content[temp_i]=="'":
        #             if final_content[temp_i + 1] in ["\\", "/"]:
        #                 waiting = True
        #                 temp_i+=1
        #                 if final_content[temp_i + 1] in ["\\", "/"]:
        #                     add_beginner_text = False
        #                     temp_i +=1
        #     else:
        #         if final_content[temp_i]=="\"" or final_content[temp_i]=="'":
        #             self.logs.write(f"     ADDED: {link}")
        #             if link.strip() not in ['/','\\','']:
        #                 if add_beginner_text:
        #                     temporary = self.base_url + link
        #                     try:
        #                         a = urllib.request.urlopen(temporary).read()
        #                     except Exception:
        #                         gg = urlparse(self.url)
        #                         temporary = str(gg.scheme) + "://" + str(gg.hostname) + "/" + link
        #                     prev_links["/" + link] = temporary
        #                     if temporary not in self.website.urls_searched:
        #                         self.website.urls_searched.add(temporary)
        #                         urls.add(temporary)
        #                 else:
        #                     if (str(main_link.scheme) + "://" + link) not in self.website.urls_searched:
        #                         self.website.urls_searched.add(str(main_link.scheme) + "://" + link)
        #                         urls.add(str(main_link.scheme) + "://" + link)
        #                     prev_links["//" + link] = str(main_link.scheme) + "://" + link
        #             waiting = False
        #             link = ""
        #             add_beginner_text = True
        #         else:
        #             link += final_content[temp_i]
        #     temp_i += 1
        if link.strip()!="":
            urls.add(link)
        self.logs.write("\n=====================\nURL FIND COMPLETE !!!!\n=====================\n")
        return (urls,prev_links)

    def download(self, thread_num):
        link = urlparse(self.url)
        urls = []

        try:
            content = self.download_resource(link)
        except Exception as e:
            raise e
        
        self.type = content.get('file_type')
        urls = self.find_urls(content.get('file_content'),content.get('file_type')==".html")

        file_content = content.get('file_content')
        if self.type==".html":
            file_content = file_content.prettify()

        file_types = eval(os.environ.get('file_types'))
        if not file_types:
            raise exceptions.FileDownloadError(self.url)
        
        ppp = self.create_offline_location(self.url, content.get('file_type'),True)
        
        just_chilling = urls[1]
        for i in urls[0]:
            found = True
            found_type = None
            temp_link = urlparse(i)
            try:
                atempi = urllib.request.urlopen(i.replace(" ","%20")).read()
                mimes = eval(os.environ.get('file_mime_types'))
                type_file = magic.from_buffer(atempi, mime=True)
                if type_file in ['text/html','text/css','text/js','text/plain']:
                    found = False
                    if not self.website.cors and str(temp_link.hostname)!=str(self.website.url.hostname):
                        break
                found_type = mimes[type_file].lower()
            except:
                for file_type in file_types:
                    if file_type not in [".HTML",".CSS",".JS"]:
                        bobby = i[(len(i) - len(file_type)):].lower()
                        if file_type.lower() == bobby:
                            found_type = file_type.lower()
                    else:
                        found = False
            if found:
                self.res_files.add(i)
                if self.download_res and (temp_link.hostname == link.hostname or self.download_cors_res):
                    try:
                        temp_content = self.download_resource(temp_link, found_type)
                    except Exception as e:
                        self.failed_downloads.append(i)
                        continue
                    path = self.create_offline_location(i,temp_content.get('file_type'))
                    go_on = True
                    if (os.path.exists(path[0] + path[1]) and not eval(os.environ.get("REFETCH"))):
                        go_on = False
                    else:
                        go_on = True
                    
                    relpath = path[0] + path[1]
                    # rint("Relpath: ",relpath)
                    # rint("Main file loc: ",ppp[0])
                    relpath = os.path.relpath(relpath, ppp[0])
                    # print("Found path: ",relpath)
                    relpath = (rf"{relpath}").replace("\\","/")
                    if go_on:
                        self.save_file(path[0],path[1],temp_content.get('file_content'),temp_content.get('file_type'))
                    if just_chilling.get(i):
                        file_content = file_content.replace(just_chilling.get(i), relpath) # type: ignore
                        del just_chilling[i]
                    else:
                        file_content = file_content.replace(i, relpath) # type: ignore

            else:
                self.main_files.add(i)
                if i not in just_chilling:
                    just_chilling[i] = None

        go_on = True
        if (os.path.exists(ppp[0] + ppp[1])):
            if ".html" in ppp[1] or ".css" in ppp[1] or ".js" in ppp[1]:
                with open(ppp[0] + ppp[1],'r') as fs:
                    try:
                        maggi = fs.read()
                        if maggi.strip() not in ['None','',' ']:
                            go_on = False
                    except Exception:
                        go_on = True
            else:
                go_on = False
        if go_on:
            self.save_file(ppp[0], ppp[1], file_content, content.get('file_type'))
        else:
            with open(ppp[0] + ppp[1],'w', encoding='utf-8') as fs:
                a = file_content.encode('utf-8', errors="replace")
                a = a.decode('utf-8')
                fs.write(a)
        return [ppp[0] + ppp[1], self.main_files, just_chilling, self.res_files]


class Website:
    location = ""
    def __init__(self, url, scrape_level, location = "", cors = True):
        self.url = urlparse(url)
        self.base_file = Webpage(url, self)
        self.location = location
        self.index_file_location = None
        self.cors = cors
        self.scrape_level = scrape_level

        self.failed = False

        self.urls_searched = set()

        self.thread_count = 0

        self.threads = []
        self.outputs = {}

        self.urls_inner_scraped = {url}

        self.urls_hostname_list = {self.url.hostname}

    async def download(self):
        self.threads = []
        self.outputs = {}
        self.urls_searched = set()
        self.urls_inner_scraped = {self.url.geturl()}
        self.failed = False
        self.index_file_location = None
        # Event set for loading animation
        temp_event = threading.Event()
        temp_event.set()
        threading.Thread(target=loading_animation.load_animation, args=(["CLIMBING MT.EVEREST TO FETCH YOUR WEBSITE ","FIGHTING THE DEVILS TO PREVENT COPYRIGHT  ","GOING TO MARS FOR FASTER INTERNET SPEEEED ","ASKING YOUR CRUSH FOR APPROVAL # FETCHING "], temp_event)).start()
        b = threading.Thread(target=self.download_webpage, args=(self.base_file, self.scrape_level))
        b.start()
        self.threads.append([b,self.url.geturl()])
        self.urls_hostname_list = {self.url.hostname}
        for i in self.threads:
            i[0].join()
        dada = 0
        for i in self.threads:
            if dada==0:
                try:
                    self.index_file_location = self.outputs[i[1]][0]
                except:
                    pass
                dada+=1
            if self.outputs.get(i[1]):
                gg_temp = self.outputs[i[1]]
                with open(gg_temp[0],"r", encoding="utf-8") as fi:
                    a = fi.read()
                with open(gg_temp[0],"w", encoding="utf-8") as fi:
                    temp = gg_temp[1]
                    for j in temp:
                        if self.outputs.get(j):
                            relpath = os.path.relpath(self.outputs[j][0],gg_temp[0])
                            relpath = (rf"{relpath}").replace("\\","/")
                            if temp[j]:
                                a = a.replace(temp[j], relpath)
                            else:
                                a = a.replace(j, relpath)
                    fi.write(a)
            else:
                globals()['logger'].critical(f"FAILED REPLACING URLS FOR {i[0]} !\nOUTPUTS: {self.outputs}")

        temp_event.clear()
        if not self.failed:
            globals()['logger'].info(f"\n\t\t\t\t================================\n\t\t\t\tSUCCESS SCRAPING WEBSITE {self.url.geturl()}\n\t\t\t\t================================\n")
            return True
        else:
            globals()['logger'].critical(f"\n\t\t\t\t================================\n\t\t\t\tFAILED SCRAPING WEBSITE FOR {self.url.geturl()}\n\t\t\t\t================================\n")
            return False
    
    def download_webpage(self,file,level):
        try:
            if not file:
                return None
            path, main_files, prev_names, res_files = file.download(len(self.threads)-1)
            if file.failed_downloads:
                globals()['logger'].critical(f"\n================================\nDOWNLOADS FAILED FOR {file.url} ARE:\n")
                for a in file.failed_downloads:
                    globals()['logger'].critical(f"\n\t\t{a}")
            for i in main_files:
                if i in self.urls_inner_scraped:
                    continue
                self.urls_inner_scraped.add(i)
                temp = urlparse(i)
                if (temp.hostname == self.url.hostname and (level+1)>0):
                    web_page = Webpage(i, self)
                    t = threading.Thread(target=self.download_webpage, args=(web_page, level))
                    t.start()
                    self.thread_count +=1
                    globals()['logger'].info(f"\nThread Started: {len(self.threads)}")
                    self.threads.append([t, i])
                elif level>0 and self.cors:
                    web_page = Webpage(i, self)
                    t = threading.Thread(target=self.download_webpage, args=(web_page, level-1))
                    t.start()
                    self.thread_count +=1
                    globals()['logger'].info(f"\nThread Started: {len(self.threads)}")
                    self.threads.append([t, i])
                else:
                    globals()['logger'].warning(f"\nURL SKIPPED TO PREVENT RECURSION: {i}")

        except Exception as e:
            exc_type, exc_value, exc_tb = sys.exc_info()
            tb = traceback.TracebackException(exc_type, exc_value, exc_tb)
            exception_string = ''.join(tb.format())
            globals()['logger'].critical(exception_string)
            self.thread_count -=1
            return

        self.outputs[file.url] = (path,prev_names)
        self.thread_count -=1

if __name__ == "__main__":
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


    file = {
        "file_types_list": [
            ".DOC", ".DOCX", ".EML", ".MSG", ".ODT", ".PAGES", ".RTF", ".TEX", ".TXT", ".WPD",
            ".AAE", ".CSV", ".DAT", ".KEY", ".LOG", ".MPP", ".OBB", ".PPT", ".PPTX",
            ".RPT", ".TAR", ".VCF", ".XML", ".AIF", ".FLAC", ".M3U", ".M4A", ".MID", ".MP3",
            ".OGG", ".WAV", ".WMA", ".3GP", ".ASF", ".AVI", ".FLV", ".M4V", ".MOV", ".MP4",
            ".MPG", ".SRT", ".SWF", ".TS", ".VOB", ".WMV", ".3DM", ".3DS", ".BLEND", ".DAE",
            ".FBX", ".MAX", ".OBJ", ".BMP", ".DCM", ".DDS", ".DJVU", ".GIF", ".HEIC", ".JPG",
            ".PNG", ".PSD", ".TGA", ".TIF", ".AI", ".CDR", ".EMF", ".EPS", ".PS", ".SKETCH",
            ".SVG", ".VSDX", ".INDD", ".OXPS", ".PDF", ".PMD", ".PUB", ".QXP", ".XPS",
            ".NUMBERS", ".ODS", ".XLR", ".XLS", ".XLSX", ".ACCDB", ".CRYPT14", ".DB", ".MDB",
            ".ODB", ".PDB", ".SQL", ".SQLITE", ".APK", ".BAT", ".BIN", ".CMD",
            ".EXE", ".IPA", ".JAR", ".RUN", ".SH", ".DEM", ".GAM", ".GBA", ".NES", ".PAK",
            ".PKG", ".ROM", ".SAV", ".DGN", ".DWG", ".DXF", ".STEP", ".STL", ".STP", ".GPX",
            ".KML", ".KMZ", ".OSM", ".ASP", ".ASPX", ".CER", ".CFM", ".CSR", ".CSS", ".HTML",
            ".JS", ".JSON", ".JSP", ".PHP", ".XHTML", ".CRX", ".ECF", ".PLUGIN", ".SAFARIEXTZ",
            ".XPI", ".FNT", ".OTF", ".TTF", ".WOFF", ".WOFF2", ".ANI", ".CAB", ".CPL", ".CUR",
            ".DESKTHEMEPACK", ".DLL", ".DMP", ".DRV", ".ICNS", ".ICO"
        ],
        "mime_types": {
          "application/msword": ".DOC",
          "application/vnd.openxmlformats-officedocument.wordprocessingml.document": ".DOCX",
          "message/rfc822": ".EML",
          "application/vnd.oasis.opendocument.text": ".ODT",
          "application/vnd.apple.pages": ".PAGES",
          "application/rtf": ".RTF",
          "text/x-tex": ".TEX",
          "text/plain": ".TXT",
          "text/csv": ".CSV",
          "application/vnd.ms-powerpoint": ".PPT",
          "application/vnd.openxmlformats-officedocument.presentationml.presentation": ".PPTX",
          "application/x-tar": ".TAR",
          "text/vcard": ".VCF",
          "application/xml": ".XML",
          "audio/x-aiff": ".AIF",
          "audio/flac": ".FLAC",
          "audio/mp4": ".M4A",
          "audio/mpeg": ".MP3",
          "audio/ogg": ".OGG",
          "audio/x-wav": ".WAV",
          "audio/x-ms-wma": ".WMA",
          "audio/3gpp": ".3GP",
          "video/x-msvideo": ".AVI",
          "video/x-flv": ".FLV",
          "video/mp4": ".MP4",
          "video/quicktime": ".MOV",
          "video/mpeg": ".MPG",
          "application/vnd.adobe.flash.movie": ".SWF",
          "text/vnd.trolltech.linguist": ".TS",
          "video/x-ms-wmv": ".WMV",
          "image/bmp": ".BMP",
          "image/gif": ".GIF",
          "image/heic": ".HEIC",
          "image/jpeg": ".JPG",
          "image/png": ".PNG",
          "image/vnd.adobe.photoshop": ".PSD",
          "image/tiff": ".TIF",
          "application/postscript": ".PS",
          "image/svg+xml": ".SVG",
          "application/pdf": ".PDF",
          "application/vnd.ms-excel": ".XLS",
          "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": ".XLSX",
          "application/vnd.android.package-archive": ".APK",
          "application/x-msdos-program": ".EXE",
          "application/java-archive": ".JAR",
          "text/x-sh": ".SH",
          "text/html": ".HTML",
          "text/css": ".CSS",
          "text/javascript": ".JS",
          "application/json": ".JSON",
          "application/xhtml+xml": ".XHTML",
          "font/ttf": ".TTF",
          "font/otf": ".OTF",
          "font/woff": ".WOFF",
          "font/woff2": ".WOFF2",
          "image/vnd.microsoft.icon": ".ICO"
        }

    }

    # OS VARIABLES
    os.environ['file_types'] = str(file['file_types_list'])
    os.environ['file_mime_types'] = str(file['mime_types'])
    os.environ['REFETCH'] = str('False')


    # INPUT
    print("\t\t\t=======================\n\t\t\t\tWEBBER\n\t\t\t=======================")
    link = input("Enter URL: ")
    file_location = input("Enter file location( Press 'Enter' for current directory ): ")
    level = int(input("Enter scrape level: "))
    print("=======================================================")

    # Make dirs
    ll = urlparse(link)

    # Logging
    if file_location.strip()!="":
        os.makedirs(file_location)
        logging.basicConfig(filename=f"{file_location}/{ll.hostname}.log",level=logging.DEBUG)
    else:
        logging.basicConfig(filename=f"{ll.hostname}.log",level=logging.DEBUG)
    logger = logging.getLogger(__name__)
    globals()["logger"] = logger

    logger.info(f"SCRAPING WEBSITE: {link}\n\n")



    # Website creation & download !
    if file_location.strip()!="":
        website = Website(link, level, file_location)
    else:
        website = Website(link, level)
    website.cors = False
    
    success = asyncio.run(website.download())

    # Opening the embedded browser !
    time.sleep(2)
    print("\t\t\t=======================\n\t\t\t\tWEBBER\n\t\t\t=======================\n")
    print("\t\t\t   SCRAPE: ",end="")
    if success:
        print("SUCCESS !")
        webview.settings['ALLOW_DOWNLOADS'] = True
        window = webview.create_window('MY WEBSITE',website.index_file_location)
        webview.start()
    else:
        print("FAILED !")
