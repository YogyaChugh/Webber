from urllib.parse import urlparse
import urllib.request
import exceptions
import os
import json
from urlextract import URLExtract
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
import loading_animation

extractor = URLExtract()


class Webpage:
    def __init__(self,url, loc,website,download_res = True, download_cors_res = True):
        self.url = url
        self.download_res = download_res
        self.download_cors_res = download_cors_res
        self.file_location = None
        self.fileName = "index.html"
        self.website = website
        

        self.failed_downloads = []

        self.loc = loc

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
        if not file_type:
            if ".css" == urlpath[-4:]:
                file_type = ".css"
            elif ".js" == urlpath[-3:]:
                file_type = ".js"
            else:
                file_type = ".html"
        try:
            if file_type in ['.html','.css','.js']:
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
            content = BeautifulSoup(content,features="html5lib")
        elif file_type == ".css":
            content = content.decode("utf-8")
            content = str(cssbeautifier.beautify(content))
        elif file_type == ".js":
            content = content.decode("utf-8")
            content = str(jsbeautifier.beautify(content))
        return {'file_content': content, 'file_type': file_type}
    
    def create_offline_location(self, file_loc_url, file_type, main=False, inside_folder = None):
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
            tempy = self.loc + ("/" if self.loc else "") + inside_folder + "/" + new_file_path + ("/" if new_file_path else "")
        else:
            tempy = self.loc + ("/" if self.loc else "") + new_file_path + ("/" if new_file_path else "")
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
            if file_type in [".html",".css",".js"]:
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
                urls = urls.union(extractor.find_urls(content_to_search))
                # This takes care of relative urls
                final_content += content_to_search
        else:
            final_content = content
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
        
        just_chilling = urls[1]
        for i in urls[0]:
            found = None
            temp_link = urlparse(i)
            for file_type in file_types:
                if file_type not in [".HTML",".CSS",".JS"]:
                    bobby = i[(len(i) - len(file_type)):].lower()
                    if file_type.lower() == bobby:
                        found = file_type.lower()
            if found:
                self.res_files.add(i)
                if self.download_res and (temp_link.hostname == link.hostname or self.download_cors_res):
                    try:
                        temp_content = self.download_resource(temp_link, found)
                    except Exception as e:
                        self.failed_downloads.append(i)
                        continue
                    path = self.create_offline_location(i,temp_content.get('file_type'))
                    go_on = True
                    if (os.path.exists(path[0] + path[1]) and eval(os.environ.get("REFETCH"))):
                        go_on = True
                    else:
                        go_on = False
                    
                    relpath = path[0].replace(self.loc + "/","") + path[1]
                    if go_on:
                        self.save_file(path[0],path[1],temp_content.get('file_content'),temp_content.get('file_type'))
                    if just_chilling.get(i):
                        file_content = file_content.replace(just_chilling.get(i), relpath) # type: ignore
                        del just_chilling[i]
                    else:
                        file_content = file_content.replace(i, relpath) # type: ignore

            else:
                self.main_files.add(i)

        ppp = self.create_offline_location(self.url, content.get('file_type'),True)
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
    def __init__(self, url, scrape_level, location = ".", cors = True):
        print(f"WEB-PAGE CREATED: {url}")
        self.url = urlparse(url)
        self.base_file = Webpage(url,location,self)
        self.location = location
        self.cors = cors
        self.scrape_level = scrape_level

        self.failed = False

        self.urls_searched = set()

        self.threads = []
        self.outputs = {}

        self.urls_hostname_list = {self.url.hostname}

    def download(self):
        b = threading.Thread(target=self.download_webpage, args=(self.base_file, self.scrape_level))
        b.start()
        self.threads.append([b,self.url])
        self.urls_hostname_list = {self.url.hostname}
        for i in self.threads:
            i[0].join()
        for i in self.threads:
            if self.outputs.get(i[0]):
                gg_temp = self.outputs[i[1]]
                with open(gg_temp[0],"r", encoding="utf-8") as fi:
                    a = fi.read()
                with open(gg_temp[0],"w", encoding="utf-8") as fi:
                    temp = gg_temp[1]
                    for i in temp:
                        a = a.replace(temp[i], gg_temp[i][0])
                    fi.write(a)
            else:
                globals()['logger'].critical(f"FAILED REPLACING URLS FOR {i[0]}")
        if not self.failed:
            globals()['logger'].info(f"\n\t\t\t\t================================\n\t\t\t\tSUCCESS SCRAPING WEBSITE {self.url.geturl()}\n\t\t\t\t================================\n")
            return True
        else:
            globals()['logger'].critical(f"\n\t\t\t\t================================\n\t\t\t\tFAILED SCRAPING WEBSITE FOR {self.url.geturl()}\n\t\t\t\t================================\n")
            return False
    
    def download_webpage(self,file,level):
        # try:
        if not file:
            return None
        path, main_files, prev_names, res_files = file.download(len(self.threads)-1)
        if file.failed_downloads:
            globals()['logger'].critical(f"\n================================\nDOWNLOADS FAILED FOR {file.url} ARE:\n")
            for a in file.failed_downloads:
                globals()['logger'].critical(f"\n\t\t{a}")
        for i in main_files:
            if i in self.urls_searched:
                continue
            self.urls_searched.add(i)
            temp = urlparse(i)
            if (temp.hostname == self.url.hostname and (level+1)>0):
                web_page = Webpage(i, self.location, self)
                t = threading.Thread(target=self.download_webpage, args=(web_page, level))
                t.start()
                globals()['logger'].info(f"\nThread Started: {len(self.threads)}")
                self.threads.append([t, i])
            elif level>0 and self.cors:
                web_page = Webpage(i, self.location, self)
                t = threading.Thread(target=self.download_webpage, args=(web_page, level-1))
                t.start()
                globals()['logger'].info(f"\nThread Started: {len(self.threads)}")
                self.threads.append([t, i])
            else:
                globals()['logger'].warning(f"\nURL SKIPPED TO PREVENT RECURSION: {i}")

        # except:
        #     exc_type, exc_value, exc_tb = sys.exc_info()
        #     tb = traceback.TracebackException(exc_type, exc_value, exc_tb)
        #     exception_string = ''.join(tb.format())
        #     globals()['logger'].critical(exception_string)
        #     self.failed = True
        #     return None

        self.outputs[file.url] = (path,prev_names)

if __name__ == "__main__":
    with open('file_types.json') as f:
        file = json.load(f)
    os.environ['file_types'] = str(file['file_types_list'])
    os.environ['REFETCH'] = str('False')
    print("=======================\n        WEBBER\n=======================")
    link = input("Enter URL: ")
    ll = urlparse(link)
    os.makedirs(str(ll.hostname),exist_ok=True)
    logging.basicConfig(filename=f"{str(ll.hostname)}/webber.log",level=logging.DEBUG)
    logger = logging.getLogger(__name__)
    globals()["logger"] = logger
    logger.info(f"WEBSITE SCRAPED: {link}\n\n")
    temp_event = threading.Event()
    temp_event.set()
    loading_animation.load_animation("Scraping Your Website Buddy ", temp_event)
    website = Website(link,0,str(ll.hostname),False)
    success = website.download()

    if success:
        temp_event.clear()
        print("SUCCESS !")
        webview.settings['ALLOW_DOWNLOADS'] = True
        window = webview.create_window('MY WEBSITE',f"{str(ll.hostname)}/index.html")
        webview.start()
    else:
        temp_event.clear()
        print("FAILED !")