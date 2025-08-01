from urllib.parse import urlparse
import urllib.parse
import urllib.request
import exceptions
import os
from bs4 import BeautifulSoup
import cssbeautifier
import jsbeautifier
import chardet
import re
import time
import urllib.request
import http.client



def download_resource_safe(url, max=2):
    try:
        with urllib.request.urlopen(url) as response:
            try:
                # Try reading all content
                return response.read()
            except http.client.IncompleteRead as e:
                # print(f"[WARN] IncompleteRead at {url}, accepting partial data")
                return e.partial  #  Accept partial chunked data
            except urllib.request.HTTPError as ok:
                if max>=0:
                    # print(f'Message is {ok.msg}')
                    time.sleep(1)
                    return download_resource_safe(url, max-1)
                else:
                    raise exceptions.FileDownloadError(url)
            except http.client.InvalidURL as e:
                # print(f"[WARN] InvalidURL: {url}")
                raise exceptions.FileDownloadError(url)
            except Exception as g:
                # print("New Error: ",g)
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
    maintain_logs = True #temp
    logs = open("temp/webber_unknown.log",'w')
    children = []
    def __init__(self,url, website, file_type, same_origin_deviation, cors_level, prev_link, content = None, download_res = True, download_cors_res = True):
        website.webpages_created.append(self)
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
            try:
                self.logs.close()
            except:
                return
        
    def __eq__(self, another_webpage):
        if (self.cors==another_webpage.cors and self.cors_level>=another_webpage.cors_level and (self.same_origin_deviation>=another_webpage.same_origin_deviation) and (self.download_res==another_webpage.download_res or self.download_res) and (self.download_cors_res==another_webpage.download_cors_res or self.download_cors_res)):
            return True
        return False
    
    def download_resource(self, url, file_type, content=None):
        try:
            url = url.replace("\\","/")
            if not content:
                url_requested = urllib.parse.quote(url, safe=":/()=-$#';\\`~!@%,.^&+={}[]")
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
        self.website.special.write(f"\n\n\nPasta Man: {file_loc_url}\n\n\n")
        self.website.special.flush()
        # print("$@"+str((file_loc_url.geturl().split("/"))[-1])+"$@")
        fileName = "index.html"
        file_loc_url = urlparse(urllib.parse.quote(file_loc_url.geturl().replace("\\","/"), safe=":/()=-$#';\\`~!@%,.^&+={}[]"))
        temp_split = (file_loc_url.geturl()).split("/")

        # print(file_loc_url)
        file_path = file_loc_url.path
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

        while file_path.startswith("/"):
            file_path = "/".join(file_path.split("/")[1:])
        while file_path.startswith("\\"):
            file_path = "/".join(file_path.split("\\")[1:])
        new_file_path = ""
        self.website.special.write(f"\n\n\nPasta Ji: {file_path}\n\n\n")
        self.website.special.flush()
        for i in range(len(file_path)):
            code = ord(file_path[i])
            if (code<47 or code>57) and (code<65 or code>172) and code not in [33,35,36,37,38,39,40,41,43,44,45,46,47,59,61,64,123,125,126]:
                new_file_path += chr((code % 65) + 65)
            else:
                new_file_path += file_path[i]
        # print("$@New: ",new_file_path,'$@')
        if inside_folder:
            tempy = os.path.join(inside_folder, new_file_path)
        else:
            tempy = new_file_path
        
        self.website.special.write(f"\n\n\nJust Before: {tempy}\n\n\n")
        self.website.special.flush()

        if self.website.url.hostname==file_loc_url.hostname:
            tempy = os.path.join(self.loc, str(file_loc_url.hostname), tempy)
        else:
            tempy = os.path.join(self.loc, str(self.website.url.hostname), str(file_loc_url.hostname), tempy)
        if main:
            self.file_location = tempy
            self.fileName = fileName
        # print(tempy)
        self.website.special.write(f"\n\n\nPasta: {tempy.replace("\\","/")}  and {fileName}\n\n\n")
        self.website.special.flush()
        return (tempy.replace("\\","/"),fileName)
    
    def save_file(self, file_loc, fileName, file_content, file_type):
        # print(f"saving {os.path.join(file_loc, fileName)}")
        # if file_type=='text/html':
        #     print('Content: ',file_content)  
        # print(f"Saved at {file_loc}")   
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
        self.website.webpages_scraped[self.prev_link] = (self, False, True)
    
    def find_urls(self, content, is_html = False):
        urls = set()
        final_content = ""
        #! ONLY THING WRITTEN BY AI (CHATGPT) #I_SUCK_AT_REGEX
        pattern = r'''
            ["']                             # Opening quote
            (
                (?:                          # Case 1: Starts with known path/prefix
                    (?:https?:\/\/|www\.|\/{1,2}|\\{1,2}|\.{1,2}[\\/])  # path or protocol
                    [^"'\s\\$<>\r\n][^"'\s\\<>\r\n]*                   # non-empty, avoids symbols
                )
                |
                (?:                          # Case 2: Ends in known extension
                    [^"'\s\\<>\r\n]+?        # non-empty content
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
            ["']                             # Closing quote
        '''


        #! TILL HERE ONLY !

        if self.maintain_logs:
            self.logs.write("\n=========================\nFINDING INTERNAL URLS.....\n=========================")
            self.logs.flush()
        final_content = str(content)
        found_urls = re.findall(pattern, final_content, re.IGNORECASE | re.VERBOSE)
        # print(f"FOR: {self.url.geturl()}")
        for url in found_urls:
            if url[1].strip() in ["","/",".","'","\"","''","\"\""]:
                continue
            urls.add(url)
            # print(url)
            yield url

        if self.maintain_logs:
            self.logs.write("\n=====================\nURL FIND COMPLETE !!!!\n=====================\n")
            self.logs.flush()
        


    def download(self):
        with self.website.sema:
            content = self.download_resource(self.url.geturl(), self.file_type, self.content)
            self.file_type = content.get('file_type')
            file_content = content.get('file_content')
            self.content = file_content
            # print(f"DOWNLOAD COMPLETE | {self.url.geturl()} |")
            return True
