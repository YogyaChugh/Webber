from urllib.parse import urlparse
import urllib.parse
import exceptions
import shutil
import os
import json
from bs4 import BeautifulSoup
import cssbeautifier
import jsbeautifier
import webview
import threading
import traceback
import sys
import magic
from webpage import *
import random
from concurrent.futures import ThreadPoolExecutor, wait


class StoppableThread(threading.Thread):
    """Thread class with a stop() method. The thread itself has to check
    regularly for the stopped() condition."""

    def __init__(self,target, args=(),):
        super(StoppableThread, self).__init__()
        self._stop_event = threading.Event()
        self.result = None
        self.target = target
        self.args = args
        self.result = None

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()
    
    def run(self):
        try:
            if self.target is not None:
                self.result = self.target(*self.args)
        finally:
            del self.target, self.args

    def get_result(self):
        return self.result

class Website:
    """
        Class representing a website as in URL !
    """
    url = None
    stopped = False
    location = ""
    cors = False
    scrape_level = 0
    max_cors = 0
    index_file_location = ""
    refetch = False
    settings = {}
    logger = open("webber_unknown.log",'w')
    failed = False         # Whether fetching URLS failed
    thread_count = 0       # Num of threads
    threads = []           # List of tuples of (a thread, url associated with that thread)
    other_threads = []      # oTHER THREADS CREATEAD by download_webpage
    outputs = {}           # Dictionary mapping each file to it's local_name & all links inside that file with their changed names
    resources_downloaded = {} # Dictionary of resources already downloaded in format {resource_url: (new_url, in_progress #bool, success #bool, file_type)}
    webpages_scraped = {} # Webpages scrapes {url of webpage: (webpage object, in_progress #bool, success #bool)}
    webpages_created =[]
    done = False
    canceled = False
    logs = []
    deleted = False
    done = False
    completed = False
    hash = ""
    executor = ThreadPoolExecutor(max_workers=250)

    def __init__(self,settings):
        # Frequently used ones stored !
        urlji = urllib.parse.quote(settings.get('url').replace("\\","/"), safe=":/")
        atempo = urlparse(urlji)
        if str(atempo.scheme).strip() == "":
            urlji = "https://" + urlji
        self.url = urlparse(urlji)
        self.base_file = Webpage(self.url, self, "text/html", settings.get('same_origin_deviation'), settings.get('max_cors'), self.url.geturl(), None, settings.get('download_res'), settings.get('download_cors_res'))
        self.location = settings.get('location')
        self.cors = settings.get('cors')
        self.scrape_level = settings.get('same_origin_deviation') # Max grandchildren for same origin urls
        self.max_cors = settings.get("max_cors") # Max CORS
        self.refetch = settings.get("refetch") # Whether to avoid using cached urls or not !

        self.index_file_location = os.path.join(self.location, str(self.url.hostname))

        self.settings = settings
        self.hash = random.random()
        # Extra information storage
        os.makedirs(os.path.join(self.location, str(self.url.hostname)), exist_ok=True)
        self.special = open(os.path.join( self.index_file_location,"urls_scraped.log"),'w')
        
        if settings.get('maintain_logs') and self.location:
            self.logger.close()
            self.logger = open(os.path.join(self.index_file_location, "webber.log"),'w')
            self.logger.write(f"Scrape Started!\n\t\tWEBSITE | {self.url.geturl()} |")
            self.logger.flush()

    def __del__(self):
        self.special.close()
        if self.settings.get('maintain_logs'):
            try:
                self.logger.write(f"Logger for {self.url.geturl()} closed !")
                self.logger.flush()
                self.logger.close()
            except:
                return
            
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
        # print('Called lol')
        self.threads = []
        self.outputs = {}

        # Event set for loading animation
        # temp_event = threading.Event()
        # temp_event.set()
        # threading.Thread(target=loading_animation.load_animation, args=(["CLIMBING MT.EVEREST TO FETCH YOUR WEBSITE ","FIGHTING THE DEVILS TO PREVENT COPYRIGHT  ","GOING TO MARS FOR FASTER INTERNET SPEEEED ","ASKING YOUR CRUSH FOR APPROVAL # FETCHING "], temp_event)).start()
        # print(f"Thread started for {self.url.geturl()}")
        with ThreadPoolExecutor() as executor:
            self.executor.submit(self.download_webpage, self.base_file)
        if not self.stopped:
            maggi = []
            for i in self.threads.copy():
                maggi.append(i[1])
            wait(maggi)
            self.threads = []
            wait(self.other_threads)
            

        # print(self.webpages_scraped.get(self.url.geturl()))
        if self.webpages_scraped.get(self.url.geturl()):
            self.failed = not self.webpages_scraped.get(self.url.geturl())[2]
        else:
            self.failed = True

        # temp_event.clear()
        # self.done = True
        if not self.failed:
            if self.settings.get('maintain_logs'):
                self.logger.write(f"\n\t\t\t\t================================\n\t\t\t\tSUCCESS SCRAPING WEBSITE {self.url.geturl()}\n\t\t\t\t================================\n")
                self.logger.flush()
        else:
            if self.settings.get('maintain_logs'):
                self.logger.write(f"\n\t\t\t\t================================\n\t\t\t\tFAILED SCRAPING WEBSITE FOR {self.url.geturl()}\n\t\t\t\t================================\n")
                self.logger.flush()
        self.completed = True
    
    def download_webpage(self,web_page):
        try:
            if self.stopped:
                return
            self.logs.append(f"Downloading Webpage: {web_page.url.geturl()}")
            # print(f'CALLED FOR {web_page.url.geturl()}')
            ppp = web_page.create_offline_location(web_page.url, web_page.file_type,True)
            if not self.settings.get('refetch') and os.path.exists(os.path.join(ppp[0], ppp[1])):
                return
            done = False
            temp_threads = []
            gg = self.executor.submit(web_page.download)
            temp_threads.append(gg)
            self.other_threads.append(gg)
            self.webpages_scraped[web_page.prev_link] = (web_page, True, False)
            if web_page.content:
                done = True
                urls = web_page.find_urls(web_page.content)
                if not self.stopped:
                    for url in urls:
                        if self.stopped:
                            return
                        # print(f'Thread started for {url}')
                        t = self.executor.submit(self.check_and_call, web_page, url)
                        temp_threads.append(t)
                        self.other_threads.append(t)
                        self.special.write(f"\n- Thread started for {url}")
                        self.special.flush()
                else:
                    return

            # print("success: ",success)
            # sys.exit()
            if not done:
                wait([temp_threads[-1]])
                temp_threads = []
                urls = web_page.find_urls(web_page.content)
                if not self.stopped:
                    for url in urls:
                        if self.stopped:
                            return
                        # print(f'Thread started for {url}')
                        t = self.executor.submit(self.check_and_call, web_page, url)
                        temp_threads.append(t)
                        self.other_threads.append(t)
                        self.special.write(f"\n- Thread started for {url}")
                        self.special.flush()
                    
            
            wait(temp_threads)
            for t in temp_threads:
                self.other_threads.remove(t)
                
            for i in web_page.children:
                # print('Replaced ',i[0],' with ',i[1])
                web_page.content = web_page.content.replace(i[0], i[1])
                
            web_page.save_file(ppp[0], ppp[1], web_page.content, web_page.file_type)
            self.logs.append(f"Download Success | {web_page.url.geturl()} |")

        except Exception as e:
            self.logs.append(f"Download Failed | {web_page.url.geturl()} |")
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
            if self.stopped:
                return
            to_be_done = True
            if url in self.resources_downloaded:
                temp = self.resources_downloaded.get(url)
                if temp and temp[2]:
                    # print(f"Skipped | {url} |")
                    to_be_done = False
                    file_path = os.path.join(web_page.file_location, web_page.fileName)
                    
                    web_page.children.append([url, os.path.relpath(temp[4], web_page.file_location).replace("\\","/")])
                    # print(f'Sending 1 {url} to {os.path.relpath(temp[4], web_page.file_location).replace("\\","/")}')
                    self.logs.append(f"Resource Download Success | {url} |")
            if self.stopped:
                return
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
                with open("data/file_types.json","r") as f:
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
                if self.stopped:
                    return
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
                    if self.stopped:
                        return
                    if temp2 and temp==temp2[0]:
                        if temp2[1] or temp2[2]:
                            web_page.children.append([url, os.path.relpath(os.path.join(temp2[0].file_location, temp2[0].fileName), web_page.file_location).replace("\\","/")])
                            # print(f'Sending 2 {url} to {os.path.relpath(os.path.join(temp2[0].file_location, temp2[0].fileName), web_page.file_location).replace("\\","/")}')
                            return
                    self.webpages_scraped[url] = (temp, True, False)
                    t = self.executor.submit(self.download_webpage, temp)
                    some = temp.create_offline_location(temp.url, type_file, True)
                    web_page.children.append([url,os.path.relpath(os.path.join(some[0],some[1]), web_page.file_location)])
                    # print(f'Sending 3 {url} to {os.path.relpath(os.path.join(some[0],some[1]), web_page.file_location)}')
                    # print(f'THREAD | {url} |')
                    self.threads.append((url, t))
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
                        if self.stopped:
                            return
                        try:
                            web_page.save_file(location, file_name, a_temp.get('file_content'), a_temp.get('file_type'))
                            self.resources_downloaded[url] = (new_url, False, True, type_file, os.path.join(location, file_name))
                        except:
                            self.resources_downloaded[url] = (new_url, False, False, type_file, os.path.join(location, file_name))
                        
                        web_page.children.append([url, os.path.relpath(os.path.join(location, file_name), web_page.file_location).replace("\\","/")])
                        # print(f'Sending 4 {url} to {os.path.relpath(os.path.join(location, file_name), web_page.file_location).replace("\\","/")}')
                                
                        if self.settings.get('maintain_logs'):
                            self.logger.write(f"\n\nDownload Complete | {new_url} |")
                            self.logger.flush()
                        self.logs.append(f"Resource Download Success | {url} |")
                    else:
                        pass
                        # print(f"Skipped {url}")
                        # print(f"CORS RES: {web_page.download_cors_res}")
        except Exception as e:
            self.logs.append(f"Resource Download Failed | {url} |")
            if self.settings.get('maintain_logs'):
                exc_type, exc_value, exc_tb = sys.exc_info()
                if exc_type and exc_value:
                    tb = traceback.TracebackException(exc_type, exc_value, exc_tb)
                    exception_string = ''.join(tb.format())
                else:
                    exception_string = f"Error: {e.args[0]} \nExtra: Couldn't traceback"
                # print(f"Failed | {url} |")
                self.logger.write(f"\n\nDownload Failed | {url} |\n\n")
                self.logger.write(f"\nError: {exception_string}")
                self.logger.flush()
                
    def cancel(self,delete_later=False):
        self.logger.write("Cancelled Scraping Website !")
        self.stopped = True
        self.failed = True
        wait(self.other_threads)
        lii = []
        for j in self.threads:
            lii.append(j[1])
        wait(lii)
        
        for i in self.webpages_created:
            try:
                i.logs.close()
            except:
                pass
        try:
            self.special.close()
        except:
            pass
        try:
            self.logger.close()
        except:
            pass    
        
        completed_webpages = {}
        completed_resources = {}
        for t in self.webpages_scraped:
            if self.webpages_scraped[t][2] or (not self.webpages_scraped[t][1] and not self.webpages_scraped[t][2]):
                completed_webpages[t] = self.webpages_scraped[t]
                
        for w in self.resources_downloaded:
            if self.resources_downloaded[w][2] or (not self.resources_downloaded[w][1] and not self.resources_downloaded[w][2]):
                completed_resources[w] = self.resources_downloaded[w]
            
        self.logs.append(f"Paused Downloading Website | {self.url.geturl()} |")
        if delete_later:
            self.logs.append(f"Deleted Website Files | {self.url.geturl()} |")
        self.canceled = True
        self.done = False
        return [completed_webpages, completed_resources]
    
    def delete(self):
        self.done = True
        self.deleted = True
        self.failed = True
        loc = os.path.join(self.location, str(self.url.hostname))
        if os.path.isdir(loc):
            # self.logger.write("Deleted local Website !")
            try:
                shutil.rmtree(loc)
            except:
                pass
            # self.logs.append(f"Deleted Website | {self.url.geturl()} |")

def main(website_name):

    # Open settings file
    try:
        with open("data/settings.json") as file:
            url = json.load(file)
        settings = url.get(website_name)
    except:
        return None
    #! SET file_types of mime as os env
    with open("data/file_types.json",'r') as file_tp:
        a = json.load(file_tp)
    os.environ['file_types'] = str(a['file_types_to_mime'])

    # Website creation & download !
    website = Website(settings)
    success = website.download()
    if success:
        return os.path.join(website.index_file_location, "index.html")
    else:
        return None


if __name__ == "__main__":
    a = main("Website 1")
    if a:
        webview.settings['ALLOW_DOWNLOADS'] = True
        webview.settings['OPEN_EXTERNAL_LINKS_IN_BROWSER'] = False
        window = webview.create_window('MY WEBSITE',a)
        a = webview.start()
        # print('lalala')
    else:
        pass
        # print("bruhhhhhhhhhhhhhhhh")