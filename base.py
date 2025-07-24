from urllib.parse import urlparse
import urllib.parse
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
import re
import traceback
import sys
import asyncio
import magic
import requests
import time
from collections import deque


import urllib.request
import http.client

import requests

def download_resource_safe(url, max=2):
    try:
        with urllib.request.urlopen(url) as response:
            try:
                # Try reading all content
                return response.read()
            except http.client.IncompleteRead as e:
                print(f"[WARN] IncompleteRead at {url}, accepting partial data")
                return e.partial  #  Accept partial chunked data
            except urllib.request.HTTPError as ok:
                if max>=0:
                    print(f'Message is {ok.msg}')
                    time.sleep(1)
                    return download_resource_safe(url, max-1)
                else:
                    raise exceptions.FileDownloadError(url)
            except http.client.InvalidURL as e:
                print(f"[WARN] InvalidURL: {url}")
                raise exceptions.FileDownloadError(url)
            except Exception as g:
                print("New Error: ",g)
                raise g
    except Exception as e:
        # print(f"[ERROR] Failed to download {url}: {e}")
        raise exceptions.FileDownloadError(url)

class Webpage:
    """Represents a webpage with multiple attributes & methods
    allowing the scrape of any webpage along with the urls & resources
    embedded inside the html,css and js files for that webpage !

    Raises:
        exceptions.NoInternetConnection: No connection while downloading resources
        exceptions.FileDownloadError: The requested URL doesn't return a valid response
        exceptions.FileSaveError: Local FileSystem Error ! Unable to save file
        e: Some other unknown python error

    """
    url = ""    #temp
    download_res = True     #temp
    download_cors_res = False   #temp
    cors = False    #temp
    cors_level = 0  #temp
    file_location = ""
    fileName = "index.html" #temp
    website = None  #temp
    parents = []
    failed_downloads = []
    loc = ""    #temp
    main_files = set() # Contains .html, .css and .js files !
    res_files = set() # Other files !
    type = None #temp
    maintain_logs = True #temp
    logs = open("webber_unkown.log",'w')
    is_busy = True
    is_success = None
    request_queue = []
    def __init__(self,url, website, file_type, same_origin_deviation, cors_level, prev_link, content = None, download_res = True, download_cors_res = True):
        self.url = url
        self.prev_link = prev_link
        self.download_res = download_res
        self.download_cors_res = download_cors_res
        self.cors = website.settings.get('cors')
        self.same_origin_deviation = same_origin_deviation
        self.cors_level = cors_level
        self.file_type = file_type
        self.website = website
        self.content = content

        self.loc = website.location
        
        self.maintain_logs = self.website.settings.get('maintain_logs')
        
        if self.maintain_logs:
            log_file_location = self.create_offline_location(url, file_type, True, 'logs')
            main_name = log_file_location[1].replace(file_type,"")
            os.makedirs(f"{log_file_location[0]}",exist_ok=True)
            self.logs.close()
            self.logs = open(f'{os.path.join(log_file_location[0], main_name)}.log','w')
            self.logs.write(f"\nWebpage Created | {url} |")
            self.logs.flush()

    def __del__(self):
        if self.maintain_logs:
            self.logs.close()
        
    def __eq__(self, another_webpage):
        if (self.cors==another_webpage.cors and self.cors_level>=another_webpage.cors_level and (self.same_origin_deviation>=another_webpage.same_origin_deviation) and (self.download_res==another_webpage.download_res or self.download_res) and (self.download_cors_res==another_webpage.download_cors_res or self.download_cors_res)):
            return True
        return False
    
    def download_resource(self, url, file_type, content=None):
        try:
            url = url.replace("\\","/")
            if not content:
                url_requested = urllib.parse.quote(url, safe=":/")
                content = download_resource_safe(url_requested)
            if self.maintain_logs:
                self.logs.write(f"\nRECEIVED CONTENTS SUCCESSFULLY | {url} |\n\n")
                self.logs.flush()
        except Exception as e:
            try:
                content = download_resource_safe("https://www.example.com")
            except Exception:
                raise exceptions.NoInternetConnection()
            raise exceptions.FileDownloadError(url)
        if file_type == "text/html":
            if not content:
                content = content.decode("utf-8")
            content = BeautifulSoup(content, features="html5lib").prettify()
        elif file_type == "text/css":
            if not content:
                content = content.decode("utf-8")
            content = str(cssbeautifier.beautify(content))
        elif file_type == "text/javascript":
            if not content:
                content = content.decode("utf-8")
            content = str(jsbeautifier.beautify(content))
        elif file_type == "text/xml" or file_type == "text/xhtml":
            if not content:
                content = content.decode('utf-8')
            content = BeautifulSoup(content, features="xml").prettify()
        return {'file_content': content, 'file_type': file_type}
    
    def create_offline_location(self, file_loc_url, file_type, main=False, inside_folder = ""):
        fileName = "index.html"
        file_loc_url = urlparse(urllib.parse.quote(file_loc_url.geturl().replace("\\","/"), safe=":/"))
        temp_split = (file_loc_url.geturl()).split("/")

        # print(file_loc_url)
        file_path = file_loc_url.path.replace("\\","/")
        if file_type=="text/html" and file_loc_url.path[-5:]!=".html":
            fileName = "index.html"
        elif file_type == "text/xml" and file_loc_url.path[-4:]!=".xml":
            fileName = "index.xml"
        elif file_type=="text/xhtml" and file_loc_url[-6:]!=".xhtml":
            fileName = "index.xhtml"
        else:
            fileName = file_loc_url.path.split("/")[-1]
            file_path = "/".join(file_path.split("/")[:-1])
            
        if (file_loc_url.path[-4:]!=".xml" and file_loc_url.path[-6:]!=".xhtml"):
            if file_type == "text/xml":
                fileName = "index.xml"
            elif file_type == "text/xhtml":
                fileName = "index.xhtml"

        while file_path.startswith("/") or file_path.startswith("\\"):
            file_path = "/".join(file_path.split("/")[1:])
        new_file_path = ""
        for i in range(len(file_path)):
            code = ord(file_path[i])
            if (code<47 or code>57) and (code<65 or code>172) and code not in [33,35,36,38,39,40,41,43,44,45,46,47,59,61,64,123,125,126]:
                new_file_path += chr((code % 65) + 65)
            else:
                new_file_path += file_path[i]
        # print(new_file_path)
        if inside_folder:
            tempy = os.path.join(inside_folder, new_file_path)
        else:
            tempy = new_file_path

        if self.website.url.hostname==file_loc_url.hostname:
            tempy = os.path.join(self.loc, str(file_loc_url.hostname), tempy)
        else:
            tempy = os.path.join(self.loc, str(self.website.url.hostname), str(file_loc_url.hostname), tempy)
        if main:
            self.file_location = tempy
            self.fileName = fileName
        # print(tempy)
        return (tempy.replace("\\","/"),fileName)
    
    def save_file(self, file_loc, fileName, file_content, file_type):
        # print(f"saving {os.path.join(file_loc, fileName)}")     
        try:
            # print(file_loc)
            os.makedirs(file_loc, exist_ok = True)
        except Exception:
            raise exceptions.FileSaveError(os.path.join(file_loc, fileName))
        
        encoding = 'utf-8'

        if file_type not in ["text/html", "text/css", "text/javascript", "text/xml", "text/xhtml", "text/plain"]:
            encoding = None
        
        if encoding:
            with open(os.path.join(file_loc, fileName), 'w', errors='replace',encoding=encoding) as file:
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
            with open(os.path.join(file_loc, fileName), 'wb') as file:
                try:
                    file.write(file_content)
                except Exception:
                    try:
                        file.write(str(file_content).encode('utf-8'))
                    except Exception:
                        result = chardet.detect(file_content)
                        encoding = result['encoding']
                        decoded_data = file_content.decode(encoding, errors="replace")
                        file.write(decoded_data)
        # print(f"\nFILE SAVED SUCCESSFULLY | {os.path.join(file_loc, fileName)} |\n\n")
        if self.maintain_logs:
            self.logs.write(f"\nFILE SAVED SUCCESSFULLY | {os.path.join(file_loc, fileName)} |\n\n")
            self.logs.flush()
    
    def find_urls(self, content, is_html = False):
        urls = set()
        final_content = ""
        #! ONLY THING WRITTEN BY AI (CHATGPT) #I_SUCK_AT_REGEX
        pattern = r'''
        ["']                                   # Opening quote
        (
            (?:                                # Case 1: Starts with path/prefix
                (?:https?:\/\/|www\.|\/{1,2}|\\{1,2}|\.{1,2}[\\/])
                [^"'\\\r\n]+
            )
            |
            (?:                                # Case 2: Ends with known extension
                [^"'\\\r\n]*?
                \.
                (?:DOCX?|EML|MSG|ODT|PAGES|RTF|TEX|TXT|WPD|AAE|CSV|DAT|KEY|LOG|MPP|OBB|
                PPTX?|RPT|TAR|VCF|XML|AIF|FLAC|M3U|M4A|MID|MP3|OGG|WAV|WMA|3GP|ASF|
                AVI|FLV|M4V|MOV|MP4|MPG|SRT|SWF|TS|VOB|WMV|3DM|3DS|BLEND|DAE|FBX|
                MAX|OBJ|BMP|DCM|DDS|DJVU|GIF|HEIC|JPG|PNG|PSD|TGA|TIF|AI|CDR|EMF|
                EPS|PS|SKETCH|SVG|VSDX|INDD|OXPS|PDF|PMD|PUB|QXP|XPS|NUMBERS|ODS|
                XLR|XLSX?|ACCDB|CRYPT14|DB|MDB|ODB|PDB|SQL|SQLITE|APK|BAT|BIN|CMD|
                EXE|IPA|JAR|RUN|SH|DEM|GAM|GBA|NES|PAK|PKG|ROM|SAV|DGN|DWG|DXF|
                STEP|STL|STP|GPX|KML|KMZ|OSM|ASPX?|CER|CFM|CSR|CSS|HTML|JS|JSON|
                JSP|PHP|XHTML|CRX|ECF|PLUGIN|SAFARIEXTZ|XPI|FNT|OTF|TTF|WOFF2?|
                ANI|CAB|CPL|CUR|DESKTHEMEPACK|DLL|DMP|DRV|ICNS|ICO)
            )
        )
        ["']                                   # Closing quote
        '''

        #! TILL HERE ONLY !

        if self.maintain_logs:
            self.logs.write("\n=========================\nFINDING INTERNAL URLS.....\n=========================")
            self.logs.flush()
        final_content = content
        found_urls = re.findall(pattern, final_content, re.IGNORECASE | re.VERBOSE)
        print(f"FOR: {self.url.geturl()}")
        for url in found_urls:
            if url[1].strip() in ["","/",".","'","\"","''","\"\""]:
                continue
            urls.add(url)
            print(url)
            yield url

        if self.maintain_logs:
            self.logs.write("\n=====================\nURL FIND COMPLETE !!!!\n=====================\n")
            self.logs.flush()
        
    def add_parent(self, parent):
        if self.file_location!="":
            parent.request_queue.append(self.url.geturl())
            if parent.is_success == False:
                return False
            if parent.request_queue[0]!=self.url.geturl():
                pass
                # print(f"waiting by {url}")
            elif parent.is_busy:
                pass
                # print(f"waiting by {url} ! Is busy")
                
            t = 1
            while parent.request_queue[0]!=self.url.geturl() or parent.is_busy:
                t+=1
            else:
                print(f"waiting complete by {self.url.geturl()}")
                a = parent.content
                tempi_lala = os.path.join(self.file_location, self.fileName)
                atemp = a.replace(self.prev_link, os.path.relpath(tempi_lala, parent.file_location).replace("\\","/"))
                parent.content = atemp
                del parent.request_queue[0]
                if len(parent.request_queue)==0:
                    print(f"Replaced for {self.url.geturl()}")
                    with open(os.path.join(parent.file_location, parent.fileName), 'w',encoding='utf-8') as file:
                        try:
                            file.write(atemp)
                        except Exception as g:
                            print(g)
                            try:
                                file.write(str(atemp))
                            except Exception as e:
                                print(e)
                                result = chardet.detect(atemp)
                                encoding = result['encoding']
                                decoded_data = atemp.decode(encoding, errors="replace")
                                file.write(decoded_data)
                return True
        else:
            return False

    def download(self):
        urls = []

        try:
            content = self.download_resource(self.url.geturl(), self.file_type, self.content)
        except Exception as e:
            self.is_success = False
            raise e
        self.type = content.get('file_type')
        file_content = content.get('file_content')
        self.content = file_content
        try:
            ppp = self.create_offline_location(self.url, content.get('file_type'),True)
        except Exception as e:
            self.is_success = False
            raise e

        go_on = True
        if not self.website.settings.get('refetch') and (os.path.exists(ppp[0] + ppp[1])):
            pass
        else:
            try:
                self.save_file(ppp[0], ppp[1], file_content, content.get('file_type'))
            except Exception as e:
                self.is_success = False
                raise e
        for i in self.parents:
            self.add_parent(i)
        self.is_busy = False
        self.is_success = True
        print(f"DOWNLOAD COMPLETE | {self.url.geturl()} |")
        return True


class Website:
    """
        Class representing a website as in URL !
    """
    url = None
    location = ""
    cors = False
    scrape_level = 0
    max_cors = 0
    index_file_location = ""
    refetch = False
    settings = {}
    logger = open("webber_unkown.log",'w')
    failed = False         # Whether fetching URLS failed
    thread_count = 0       # Num of threads
    threads = []           # List of tuples of (a thread, url associated with that thread)
    outputs = {}           # Dictionary mapping each file to it's local_name & all links inside that file with their changed names
    resources_downloaded = {} # Dictionary of resources already downloaded in format {resource_url: (new_url, in_progress #bool, success #bool, file_type)}
    webpages_scraped = {} # Webpages scrapes {url of webpage: (webpage object, in_progress #bool, success #bool)}

    def __init__(self,settings):

        # Frequently used ones stored !
        self.url = urlparse(urllib.parse.quote(settings.get('url').replace("\\","/"), safe=":/"))
        self.base_file = Webpage(self.url, self, "text/html", settings.get('same_origin_deviation'), settings.get('max_cors'), self.url.geturl(), None, settings.get('download_res'), settings.get('download_cors_res'))
        self.location = settings.get('location')
        self.cors = settings.get('cors')
        self.scrape_level = settings.get('same_origin_deviation') # Max grandchildren for same origin urls
        self.max_cors = settings.get("max_cors") # Max CORS
        self.refetch = settings.get("refetch") # Whether to avoid using cached urls or not !

        self.index_file_location = os.path.join(self.location, str(self.url.hostname))

        self.settings = settings

        # Extra information storage
        os.makedirs(os.path.join(self.location, str(self.url.hostname)), exist_ok=True)
        self.special = open("urls_scraped.log",'w')
        
        if settings.get('maintain_logs') and self.location:
            self.logger.close()
            self.logger = open(os.path.join(self.location, str(self.url.hostname), "webber.log"),'w')
            self.logger.write(f"Scrape Started!\n\t\tWEBSITE | {self.url.geturl()} |")
            self.logger.flush()

    def __del__(self):
        self.special.close()
        if self.settings.get('maintain_logs'):
            self.logger.write(f"Logger for {self.url.geturl()} closed !")
            self.logger.flush()
            self.logger.close()
            
    def correct_url(self, url, webpage = None):
        if not url.startswith("/") or not webpage:
            if not url.startswith("http") and not url.startswith("www"):
                return "https://"+url
            else:
                return url
        if webpage.url.hostname:
            return os.path.join(str(webpage.url.scheme)+ "://", str(webpage.url.hostname), url[1:])
        else:
            return os.path.join(str(self.url.scheme)+ "://", str(self.url.hostname), url[1:])

    def download(self):
        """Downloads a complete website based on the settings passed while construction.

        Returns:
            bool: Success or Failure
        """
        # RESET
        self.threads = []
        self.outputs = {}
        self.webpages_scraped = {}
        self.resources_downloaded = {}
        self.failed = False

        # Event set for loading animation
        # temp_event = threading.Event()
        # temp_event.set()
        # threading.Thread(target=loading_animation.load_animation, args=(["CLIMBING MT.EVEREST TO FETCH YOUR WEBSITE ","FIGHTING THE DEVILS TO PREVENT COPYRIGHT  ","GOING TO MARS FOR FASTER INTERNET SPEEEED ","ASKING YOUR CRUSH FOR APPROVAL # FETCHING "], temp_event)).start()
        # print(f"Thread started for {self.url.geturl()}")
        self.download_webpage(self.base_file)
        for i in self.threads:
            i[1].join()
            

        # print(self.webpages_scraped.get(self.url.geturl()))
        if self.webpages_scraped.get(self.url.geturl()):
            self.failed = not self.webpages_scraped.get(self.url.geturl())[2]
        else:
            self.failed = True

        # temp_event.clear()
        if not self.failed:
            if self.settings.get('maintain_logs'):
                self.logger.write(f"\n\t\t\t\t================================\n\t\t\t\tSUCCESS SCRAPING WEBSITE {self.url.geturl()}\n\t\t\t\t================================\n")
                self.logger.flush()
            return True
        else:
            if self.settings.get('maintain_logs'):
                self.logger.write(f"\n\t\t\t\t================================\n\t\t\t\tFAILED SCRAPING WEBSITE FOR {self.url.geturl()}\n\t\t\t\t================================\n")
                self.logger.flush()
            return False
    
    def download_webpage(self,web_page):
        try:
            done = False
            temp_threads = []
            gg = threading.Thread(target=web_page.download)
            temp_threads.append(gg)
            self.webpages_scraped[web_page.prev_link] = (web_page, True, False)
            gg.start()
            if web_page.content:
                done = True
                urls = web_page.find_urls(web_page.content)
                for url in urls:
                    # print(f'Thread started for {url}')
                    t = threading.Thread(target=self.check_and_call, args=(web_page, url))
                    temp_threads.append(t)
                    t.start()
                    self.special.write(f"\n- Thread started for {url}")
                    self.special.flush()
            else:
                temp_threads[-1].join()
            # print("success: ",success)
            # sys.exit()
            if web_page.is_success:
                self.webpages_scraped[web_page.prev_link] = (web_page, False, True)
                if not done:
                    urls = web_page.find_urls(web_page.content)
                    for url in urls:
                        # print(f'Thread started for {url}')
                        t = threading.Thread(target=self.check_and_call, args=(web_page, url))
                        temp_threads.append(t)
                        t.start()
                        self.special.write(f"\n- Thread started for {url}")
                        self.special.flush()

            else:
                self.webpages_scraped[web_page.prev_link] = (web_page, False, False)
            
            for t in temp_threads:
                t.join()

        except Exception as e:
            self.webpages_scraped[web_page.prev_link] = (web_page, False, False)
            if self.settings.get('maintain_logs'):
                exc_type, exc_value, exc_tb = sys.exc_info()
                if exc_type and exc_value:
                    tb = traceback.TracebackException(exc_type, exc_value, exc_tb)
                    exception_string = ''.join(tb.format())
                else:
                    exception_string = f"Error: {e.args[0]} \nExtra: Couldn't traceback"
                self.logger.write(f"\n\nDownload Failed | {web_page.url.geturl()} |\n\n")
                self.logger.write(f"Error: {exception_string}")
                self.logger.flush()
                # print(exception_string)
                
    def check_and_call(self, web_page, url):
        try:
            to_be_done = True
            if url in self.resources_downloaded:
                temp = self.resources_downloaded.get(url)
                if temp and temp[2]:
                    # print(f"Skipped | {url} |")
                    to_be_done = False
                    file_path = os.path.join(web_page.file_location, web_page.fileName)
                    web_page.request_queue.append(url)
                    if web_page.is_success == False:
                        raise exceptions.FileDownloadError(file_path)
                    if web_page.request_queue[0]!=url:
                        pass
                        # print(f"waiting by {url}")
                    elif web_page.is_busy:
                        pass
                        # print(f"waiting by {url} ! Is busy")
                    t = 1
                    while web_page.request_queue[0]!=url or web_page.is_busy:
                        t+=1
                    else:
                        print(f"waiting complete by {url}")
                        file_contents = web_page.content
                        file_contents = file_contents.replace(url, os.path.relpath(temp[4], web_page.file_location).replace("\\","/"))
                        web_page.content = file_contents
                        del web_page.request_queue[0]
                        if len(web_page.request_queue)==0:
                            print(f"Replaced for {url}")
                            with open(file_path, 'w',encoding='utf-8') as file:
                                try:
                                    file.write(file_contents)
                                except Exception as g:
                                    print(g)
                                    try:
                                        file.write(str(file_contents))
                                    except Exception as e:
                                        print(e)
                                        result = chardet.detect(file_contents)
                                        encoding = result['encoding']
                                        decoded_data = file_contents.decode(encoding, errors="replace")
                                        file.write(decoded_data)

            if to_be_done:
                # print(f'GOING FOR {url}')
                new_url = self.correct_url(url, web_page)
                new_url = new_url.replace("\\","/")
                url_requested = urllib.parse.quote(new_url, safe=":/")
                try:
                    content = download_resource_safe(url_requested)
                except Exception:
                    try:
                        content = download_resource_safe("https://www.example.com")
                    except Exception:
                        raise exceptions.NoInternetConnection()
                    raise exceptions.FileDownloadError(url)
                with open("file_types.json","r") as f:
                    mimes = json.load(f)
                    mimes = mimes['mime_types']
                redo = False
                type_file = None
                try:
                    type_file = magic.from_buffer(content, mime=True)
                except:
                    redo = True
                if redo or type_file == 'text/plain':
                    types_man = os.environ.get('file_types', '[]')
                    if types_man:
                        file_types=eval(types_man)
                        for file_type in file_types:
                            bobby = new_url[(len(new_url) - len(file_type)):].lower()
                            if file_type.lower() == bobby:
                                type_file = file_types[file_type].lower()
                temporary_made_url = urlparse(new_url)
                if type_file in ['text/html','text/css','text/javascript','text/plain','text/xhtml','text/xml']:
                    # print(f'THIS IS A WEBPAGE | {url} |')
                    content = content.decode("utf-8")
                    if type_file == "text/html":
                        content = BeautifulSoup(content, features="html5lib").prettify()
                    elif type_file == "text/css":
                        content = str(cssbeautifier.beautify(content))
                    elif type_file == "text/javascript":
                        content = str(jsbeautifier.beautify(content))
                    elif type_file == "text/xml" or type_file == "text/xhtml":
                        content = BeautifulSoup(content, features="xml").prettify()
                        
                    if web_page.url.hostname == temporary_made_url.hostname and web_page.same_origin_deviation>0:
                        temp = Webpage(temporary_made_url, self, type_file, web_page.same_origin_deviation-1, web_page.cors_level, url, content, web_page.download_res, web_page.download_cors_res)
                    elif web_page.url.hostname != temporary_made_url.hostname and web_page.cors and web_page.cors_level>0:
                        temp = Webpage(temporary_made_url, self, type_file, 0, web_page.cors_level - 1, url, content, self.settings.get('cors_download_res'), self.settings.get('cors_download_cors_res'))
                    else:
                        return
                    temp2 = self.webpages_scraped.get(url)
                    if temp2 and temp==temp2[0]:
                        if temp2[1]:
                            print(f"Skipped | {url} |")
                            atry = temp2[0].add_parent(web_page)
                            if not atry:
                                print(f"FALSE FOR URL {url}")
                                temp2[0].parents.append(web_page)
                            return
                        elif temp2[2]:
                            print(f"Skipped | {url} |")
                            temp2[0].add_parent(web_page)
                            return
                    self.webpages_scraped[url] = (temp, True, False)
                    temp.parents.append(web_page)
                    t = threading.Thread(target=self.download_webpage, args=(temp,))
                    self.threads.append((url, t))
                    # print(f'THREAD | {url} |')
                    t.start()
                    # print(f"Success started for {url}")
                    if self.settings.get('maintain_logs'):
                        self.logger.write(f"\n\nDownloading Webpage | {new_url} |")
                        self.logger.flush()
                else:
                    if ((web_page.url.hostname == temporary_made_url.hostname or self.url.hostname == temporary_made_url.hostname) and web_page.download_res) or (web_page.url.hostname!=temporary_made_url.hostname and self.url.hostname!=temporary_made_url.hostname and web_page.download_cors_res):
                        if self.settings.get('maintain_logs'):
                            self.logger.write(f"\n\nDownloading Resource | {new_url} |")
                            self.logger.flush()
                        self.resources_downloaded[url] = (new_url, True, False, type_file, None)
                        temp_location = os.path.join(web_page.file_location, web_page.fileName)
                        a_temp = web_page.download_resource(new_url, type_file, content)
                        location, file_name = web_page.create_offline_location(temporary_made_url, type_file)
                        try:
                            web_page.save_file(location, file_name, a_temp.get('file_content'), a_temp.get('file_type'))
                            self.resources_downloaded[url] = (new_url, False, True, type_file, os.path.join(location, file_name))
                        except:
                            self.resources_downloaded[url] = (new_url, False, False, type_file, os.path.join(location, file_name))
                        
                        web_page.request_queue.append(url)
                        if web_page.is_success == False:
                            raise exceptions.FileDownloadError(os.path.join(location, file_name))
                        if web_page.request_queue[0]!=url:
                            pass
                            # print(f"waiting by {url}")
                        elif web_page.is_busy:
                            pass
                            # print(f"waiting by {url} ! Is busy")
                        t = 1
                        while web_page.request_queue[0]!=url or web_page.is_busy:
                            t+=1
                        else:
                            print(f"waiting complete by {url}")
                            a = web_page.content
                            tempi_boi = os.path.join(location, file_name)
                            a_new = a.replace(url, os.path.relpath(tempi_boi, web_page.file_location).replace("\\","/"))
                            web_page.content = a_new
                            del web_page.request_queue[0]
                            if len(web_page.request_queue)==0:
                                print(f"Replaced for {url}")
                                with open(temp_location, 'w', encoding='utf-8') as file:
                                    try:
                                        file.write(a_new)
                                    except Exception as g:
                                        print(g)
                                        try:
                                            file.write(str(a_new))
                                        except Exception as e:
                                            print(e)
                                            result = chardet.detect(a_new)
                                            encoding = result['encoding']
                                            decoded_data = a_new.decode(encoding, errors="replace")
                                            file.write(decoded_data)
                        if self.settings.get('maintain_logs'):
                            self.logger.write(f"\n\nDownload Complete | {new_url} |")
                            self.logger.flush()
                    else:
                        print(f"Skipped {url}")
                        print(f"CORS RES: {web_page.download_cors_res}")
        except Exception as e:
            if self.settings.get('maintain_logs'):
                exc_type, exc_value, exc_tb = sys.exc_info()
                if exc_type and exc_value:
                    tb = traceback.TracebackException(exc_type, exc_value, exc_tb)
                    exception_string = ''.join(tb.format())
                else:
                    exception_string = f"Error: {e.args[0]} \nExtra: Couldn't traceback"
                print(f"Failed | {url} |")
                self.logger.write(f"\n\nDownload Failed | {url} |\n\n")
                self.logger.write(f"\nError: {exception_string}")
                self.logger.flush()
                    

def main(website_name):

    # Open settings file
    try:
        with open("settings.json") as file:
            url = json.load(file)
        settings = url.get(website_name)
    except:
        return None
    #! SET file_types of mime as os env
    with open("file_types.json",'r') as file_tp:
        a = json.load(file_tp)
    os.environ['file_types'] = str(a['file_types_to_mime'])

    # Website creation & download !
    website = Website(settings)
    success = website.download()
    if success:
        return os.path.join(website.index_file_location, "index.html")
    else:
        return None

a = main("Website 1")
if a:
    webview.settings['ALLOW_DOWNLOADS'] = True
    webview.settings['OPEN_EXTERNAL_LINKS_IN_BROWSER'] = False
    window = webview.create_window('MY WEBSITE',a)
    a = webview.start()
    print('lalala')
else:
    print("bruhhhhhhhhhhhhhhhh")