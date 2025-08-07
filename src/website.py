from urllib.parse import urlparse, urlunparse
import urllib.error
import exceptions
import shutil
import os
import json
from bs4 import BeautifulSoup
import cssbeautifier
import jsbeautifier
import threading
import traceback
import sys
import magic
from webpage import *


def remove_unnecessary(url):
    a = urlparse(url)
    aa = str(a.scheme) + "://" if a.scheme else ""
    b = str(a.hostname) + "/" if a.hostname else ""
    c = str(a.path)
    return os.path.join(aa, b, c)

# from concurrent.futures import ThreadPoolExecutor, wait

# executor = ThreadPoolExecutor(max_workers=3)


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
    logger = open("temp/webber_unknown.log",'w')
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
    ab = 0
    max_threads = 50
    sema = None
    base_loc = ""

    def __init__(self,settings):
        # Frequently used ones stored !
        urlji = urllib.parse.quote(settings.get('url').replace("\\","/"), safe=":/()=-$#';\\`~!@%,.^&+={}[]")
        atempo = urlparse(urlji)
        if str(atempo.scheme).strip() == "":
            urlji = "https://" + urlji
        self.url = urlparse(urlji)
        self.location = settings.get('location')
        self.cors = settings.get('cors')
        self.scrape_level = settings.get('same_origin_deviation') # Max grandchildren for same origin urls
        self.max_cors = settings.get("max_cors") # Max CORS
        self.refetch = settings.get("refetch") # Whether to avoid using cached urls or not !
        self.base_file = Webpage(self.url, self, "text/html", settings.get('same_origin_deviation'), settings.get('max_cors'), self.url.geturl(), None, settings.get('download_res'), settings.get('download_cors_res'))

        self.max_threads = settings.get('max_threads')
        self.sema = threading.Semaphore(self.max_threads)
        self.index_file_location = os.path.join(self.location, str(self.url.hostname))

        self.settings = settings
        self.hash = settings.get('hash')
        # Extra information storage
        os.makedirs(os.path.join(self.location, str(self.url.hostname)), exist_ok=True)
        self.special = open(os.path.join( self.index_file_location,"urls_scraped.log"),'w')
        
        if settings.get('maintain_logs') and self.location:
            self.logger.close()
            self.logger = open(os.path.join(self.index_file_location, "webber.log"),'w')
            self.logger.write(f"Scrape Started!\n\t\tWEBSITE | {self.url.geturl()} |")
            self.logger.flush()
            
        info = {
            "file_location": str(self.index_file_location),
            "settings": self.settings
        }
            
        # with open(f"temp/{self.hash}.json",'w') as jalebi:
        #     json.dump(info, jalebi)

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
        
    def smart_urljoin(self, base, next):
        a = str(base.path)
        a = a.replace('\\','/')
        b = os.path.dirname(a)
        # self.special.write(f'\nnext is given: {next} with base url as {base.geturl()} with dirname: {b} and hostname {str(base.hostname)}')
        # self.special.flush()
        temp = str(base.scheme) + ("://" if base.scheme else "")+ str(base.hostname)
        temp2 = os.path.join(b, next).replace("\\",'/')
        if temp2.startswith('/'):
            return (temp+temp2).replace("\\",'/')
        else:
            return (temp+'/'+temp2).replace("\\",'/')

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
        doc = StoppableThread(target=self.download_webpage, args=(self.base_file,))
        doc.start()
        doc.join()
        if not self.stopped:
            for i in self.threads.copy():
                try:
                    i[1].join()
                except:
                    pass
            self.threads = []
            for rd in self.other_threads:
                try:
                    rd.join()
                except:
                    pass
            

        # print(self.webpages_scraped.get(self.url.geturl()))
        if self.webpages_scraped.get(self.url.geturl()):
            self.failed = not self.webpages_scraped.get(self.url.geturl())[2]
        else:
            self.failed = True

        # temp_event.clear()
        if not self.failed:
            self.done = True
            print("$@1$@", flush=True)
            if self.settings.get('maintain_logs'):
                self.logger.write(f"\n\t\t\t\t================================\n\t\t\t\tSUCCESS SCRAPING WEBSITE {self.url.geturl()}\n\t\t\t\t================================\n")
                self.logger.flush()
        else:
            print("$@0$@", flush=True)
            if self.settings.get('maintain_logs'):
                self.logger.write(f"\n\t\t\t\t================================\n\t\t\t\tFAILED SCRAPING WEBSITE FOR {self.url.geturl()}\n\t\t\t\t================================\n")
                self.logger.flush()
        self.completed = True
    
    def download_webpage(self,web_page):
        with self.sema:
            # print(f'FOR {web_page.url.geturl()}')
            # print('wtf')
            try:
                if self.stopped:
                    # print('it was stopped')
                    return
                # print('wtf part 2')
                self.logs.append(f"Downloading Webpage: {web_page.url.geturl()}")
                print(f"$@Downloading Webpage: {web_page.url.geturl()}$@", flush=True)
                self.special.write(f"Downloading Webpage: {web_page.url.geturl()}")
                self.special.flush()
                # print(f'CALLED FOR {web_page.url.geturl()}')
                # print("jojo")
                ppp = web_page.create_offline_location(web_page.url, web_page.file_type,True)
                # print("joko")
                if not self.settings.get('refetch') and os.path.exists(os.path.join(ppp[0], ppp[1])):
                    self.webpages_scraped[web_page.prev_link] = (web_page, False, True)
                    return
                done = False
                temp_threads = []
                # print('no issue before download()')
                web_page.download()
                web_page.save_file(ppp[0], ppp[1], web_page.content, web_page.file_type)
                gg = StoppableThread(target=web_page.download)
                gg.start()
                temp_threads.append(gg)
                self.other_threads.append(gg)
                # gg.join()
                # temp_threads.remove(gg)
                # self.other_threads.remove(gg)
                # print('thread issue ??')
                self.webpages_scraped[web_page.prev_link] = (web_page, True, False)
                if web_page.content:
                    done = True
                    urls = web_page.find_urls(web_page.content)
                    if not self.stopped:
                        for url in urls:
                            if self.stopped:
                                return
                            # print(f'Thread started for {url}')
                            t = StoppableThread(target=self.check_and_call, args=(web_page,url))
                            t.start()
                            temp_threads.append(t)
                            self.other_threads.append(t)
                            # t.join()
                            # temp_threads.remove(t)
                            # self.other_threads.remove(t)
                    else:
                        return

                # print("success: ",success)
                # sys.exit()
                # print('reached here')
                if not done:
                    temp_threads[-1].join()
                    temp_threads = []
                    urls = web_page.find_urls(web_page.content)
                    if not self.stopped:
                        for url in urls:
                            if self.stopped:
                                return
                            # print(f'Thread started for {url}')
                            t = StoppableThread(target=self.check_and_call,args=(web_page, url))
                            t.start()
                            temp_threads.append(t)
                            self.other_threads.append(t)
                            # t.join()
                            # temp_threads.remove(t)
                            # self.other_threads.remove(t)

                for t in temp_threads:
                    t.join()
                    self.other_threads.remove(t)

                self.special.write(f"\n\n\n\nCHILDREN FOR {web_page.url.geturl()} : {web_page.children}\n\n\n\n")
                self.special.flush()
                d = []
                for i in web_page.children:
                    # print('Replaced ',i[0],' with ',i[1])
                    if i[0] not in d:
                        web_page.content = web_page.content.replace(i[0], i[1])
                        # print('\nReplaced !!\n')
                        # print("p"+i[0]+"\n")
                        # print("n"+i[1]+"\n")
                        self.special.write(f"Replaced {i[0]} with {i[1]}")
                        self.special.flush()
                        d.append(i[0])

                web_page.save_file(ppp[0], ppp[1], web_page.content, web_page.file_type)
                self.logs.append(f"Download Success | {web_page.url.geturl()} |")
                print(f"$@Download Success | {web_page.url.geturl()} |$@", flush=True)
                self.special.write(f"Download Success | {web_page.url.geturl()} |")
                self.special.flush()
                self.ab -= 1

            except Exception as e:
                # print('problem')
                self.ab -= 1
                self.logs.append(f"Download Failed | {web_page.url.geturl()} |")
                print(f"$@Download Failed | {web_page.url.geturl()} |$@", flush=True)
                # except:
                try:
                    if not isinstance(e, urllib.error.HTTPError) and not e.code == 404:
                        print(f"$@Download Failed | {web_page.url.geturl()} |$@", flush=True)
                except:
                    pass
                self.special.write(f"Download Failed | {web_page.url.geturl()} |")
                self.special.flush()
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
                if isinstance(e, exceptions.NoInternetConnection):
                    print("$@No Internet Connection !!$@", flush=True)
                
    def check_and_call(self, web_page, url, main=True, last_try=False):
        # self.special.write(f"\n\n\n\n\nCHECKING THE KIDDY: {url}\n\n\n\n")
        with self.sema:
            the_simple_url = url
            url = remove_unnecessary(url)
            url2 = self.smart_urljoin(web_page.url, url)
            url3 = None
            if main:
                url3 = self.smart_urljoin(self.url, url)
            # print('New: ',url2)
            # self.special.write(f'\nNEW: {url2}')
            # self.special.flush()
            try:
                if self.stopped:
                    return
                to_be_done = True
                if the_simple_url in self.resources_downloaded:
                    temp = self.resources_downloaded.get(the_simple_url)
                    if temp and temp[2] and temp[5] != os.path.join(web_page.file_location, web_page.fileName):
                        # print(f"Skipped | {url} |")
                        to_be_done = False
                        file_path = os.path.join(web_page.file_location, web_page.fileName)

                        web_page.children.append([the_simple_url, os.path.relpath(temp[4], web_page.file_location).replace("\\","/")])
                        # self.special.write(f"\n\nFor {the_simple_url} with { os.path.relpath(temp[4], web_page.file_location).replace("\\","/")} where the details are:\n\n1st: {temp[4]} and {web_page.file_location}")
                        # print(f'Sending 1 {url} to {os.path.relpath(temp[4], web_page.file_location).replace("\\","/")}')
                        self.logs.append(f"Using Cached | {url2} |")
                        print(f"$@Using Cached | {url2} |$@", flush=True)
                        self.special.write(f"Using Cached | {url2} |")
                        self.special.flush()
                if self.stopped:
                    return
                if to_be_done:
                    # print(f'GOING FOR {url}')
                    new_url = self.correct_url(url2, web_page)
                    new_url = new_url.replace("\\","/")
                    url_requested = urllib.parse.quote(new_url, safe=":/()=-$#';\\`~!@%,.^&+={}[]")
                    try:
                        content = download_resource_safe(url_requested)
                    except Exception:
                        try:
                            content = download_resource_safe("https://www.example.com")
                        except Exception:
                            raise exceptions.NoInternetConnection()
                        raise exceptions.FileDownloadError(the_simple_url)
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
                        # elif type_file == "text/css":
                        #     content = str(cssbeautifier.beautify(content))
                        elif type_file == "text/javascript":
                            content = str(jsbeautifier.beautify(content))
                        elif type_file == "text/xml" or type_file == "text/xhtml":
                            content = BeautifulSoup(content, features="xml").prettify()

                        if web_page.url.hostname == temporary_made_url.hostname and web_page.same_origin_deviation>0:
                            temp_wow = Webpage(temporary_made_url, self, type_file, web_page.same_origin_deviation-1, web_page.cors_level, the_simple_url, content, web_page.download_res, web_page.download_cors_res)
                        elif web_page.url.hostname != temporary_made_url.hostname and web_page.cors and web_page.cors_level>0:
                            temp_wow = Webpage(temporary_made_url, self, type_file, 0, web_page.cors_level - 1, the_simple_url, content, self.settings.get('cors_download_res'), self.settings.get('cors_download_cors_res'))
                        else:
                            return
                        temp2 = self.webpages_scraped.get(the_simple_url)
                        if self.stopped:
                            return
                        if temp2 and temp_wow==temp2[0]:
                            if temp2[1] or temp2[2]:
                                web_page.children.append([the_simple_url, os.path.relpath(os.path.join(temp2[0].file_location, temp2[0].fileName), web_page.file_location).replace("\\","/")])
                                # self.special.write(f"\n\nFor {the_simple_url} with {os.path.relpath(os.path.join(temp2[0].file_location, temp2[0].fileName), web_page.file_location).replace("\\","/")} where the details are:\n\n1st: {os.path.join(temp2[0].file_location, temp2[0].fileName)} and {web_page.file_location}")
                                # self.special.flush()
                                print(f"$@Using Cached | {url2} |$@", flush=True)
                                # print(f'Sending 2 {url} to {os.path.relpath(os.path.join(temp2[0].file_location, temp2[0].fileName), web_page.file_location).replace("\\","/")}')
                                return
                        self.webpages_scraped[the_simple_url] = (temp_wow, True, False)
                        t = StoppableThread(target=self.download_webpage,args=(temp_wow,))
                        t.start()
                        # self.download_webpage(temp_wow)
                        some = temp_wow.create_offline_location(temp_wow.url, type_file, True)
                        web_page.children.append([the_simple_url, os.path.relpath(os.path.join(some[0],some[1]), web_page.file_location)])
                        # self.special.write(f"\n\nFor {the_simple_url} with {os.path.relpath(os.path.join(some[0],some[1]), web_page.file_location)} where the details are:\n\n1st: {os.path.join(some[0],some[1])} and {web_page.file_location}")
                        # self.special.flush()
                        # print(f'Sending 3 {url} to {os.path.relpath(os.path.join(some[0],some[1]), web_page.file_location)}')
                        # print(f'THREAD | {url} |')
                        self.threads.append((the_simple_url, t))
                        # print(f"Success started for {url}")
                        if self.settings.get('maintain_logs'):
                            self.logger.write(f"\n\nDownloading Webpage | {new_url} |")
                            self.logger.flush()
                    else:
                        if ((web_page.url.hostname == temporary_made_url.hostname or self.url.hostname == temporary_made_url.hostname) and web_page.download_res) or (web_page.url.hostname!=temporary_made_url.hostname and self.url.hostname!=temporary_made_url.hostname and web_page.download_cors_res):
                            if self.settings.get('maintain_logs'):
                                self.logger.write(f"\n\nDownloading Resource | {new_url} |")
                                self.logger.flush()
                            self.resources_downloaded[the_simple_url] = (new_url, True, False, type_file, None,os.path.join(web_page.file_location,web_page.fileName))
                            temp_location = os.path.join(web_page.file_location, web_page.fileName)
                            a_temp = web_page.download_resource(new_url, type_file, content)
                            location, file_name = web_page.create_offline_location(temporary_made_url, type_file)
                            if self.stopped:
                                return
                            try:
                                web_page.save_file(location, file_name, a_temp.get('file_content'), a_temp.get('file_type'))
                                self.resources_downloaded[the_simple_url] = (new_url, False, True, type_file, os.path.join(location, file_name), os.path.join(web_page.file_location, web_page.fileName))
                            except:
                                self.resources_downloaded[the_simple_url] = (new_url, False, False, type_file, os.path.join(location, file_name), os.path.join(web_page.file_location, web_page.fileName))

                            web_page.children.append([the_simple_url, os.path.relpath(os.path.join(location, file_name), web_page.file_location).replace("\\","/")])
                            # self.special.write(f"\n\nFor {the_simple_url} with {os.path.relpath(os.path.join(location, file_name), web_page.file_location).replace("\\","/")} where the details are:\n\n1st: {os.path.join(location, file_name)} and {web_page.file_location}")
                            # self.special.flush()
                            # print(f'Sending 4 {url} to {os.path.relpath(os.path.join(location, file_name), web_page.file_location).replace("\\","/")}')

                            if self.settings.get('maintain_logs'):
                                self.logger.write(f"\n\nDownload Complete | {new_url} |")
                                self.logger.flush()
                            self.logs.append(f"Resource Download Success | {the_simple_url} |")
                            print(f"$@Resource Download Success | {url2} |$@", flush=True)
                            self.special.write(f"Resource Download Success | {the_simple_url} |")
                            self.special.flush()
                        else:
                            pass
                            # print(f"Skipped {url}")
                            # print(f"CORS RES: {web_page.download_cors_res}")
            except Exception as e:
                if main:
                    # self.special.write(f"\n\n\n\naaaaaaaa: {url}\n\n\n\n")
                    self.check_and_call(web_page, url3, False)
                if not main:
                    self.logs.append(f"Resource Download Failed | {the_simple_url} |")
                    print(f"$@Resource Download Failed | {url2} |$@", flush=True)
                    try:
                        if not isinstance(e, urllib.error.HTTPError) and not e.code==404:
                            print(f"$@Resource Download Failed | {url2} |$@", flush=True)
                    except:
                        pass
                    self.special.write(f"Resource Download Failed | {the_simple_url} |")
                    self.special.flush()
                    if self.settings.get('maintain_logs'):
                        exc_type, exc_value, exc_tb = sys.exc_info()
                        if exc_type and exc_value:
                            tb = traceback.TracebackException(exc_type, exc_value, exc_tb)
                            exception_string = ''.join(tb.format())
                        else:
                            exception_string = f"Error: {e.args[0]} \nExtra: Couldn't traceback"
                        # print(f"Failed | {url} |")
                        self.logger.write(f"\n\nDownload Failed | {the_simple_url} |\n\n")
                        self.logger.write(f"\nError: {exception_string}")
                        self.logger.flush()
                
    def cancel(self,delete_later=False):
        self.logger.write("Cancelled Scraping Website !")
        self.stopped = True
        self.failed = True
        for hp in self.other_threads:
            try:
                hp.stop()
            except:
                pass
        for hp in self.other_threads:
            try:
                hp.join()
            except:
                pass
        lii = []
        for j in self.threads:
            try:
                j[1].stop()
                j[1].join()
            except:
                pass
        
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
        print(f"$@Paused Downloading Website | {self.url.geturl()} |$@", flush=True)
        self.special.write(f"Paused Downloading Website | {self.url.geturl()} |")
        self.special.flush()
        if delete_later:
            self.logs.append(f"Deleted Website Files | {self.url.geturl()} |")
            print(f"$@Deleted Website Files | {self.url.geturl()} |$@", flush=True)
            self.special.write(f"Deleted Website Files | {self.url.geturl()} |")
            self.special.flush()
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

# def main(website_name):

#     # Open settings file
#     try:
#         with open("data/settings.json") as file:
#             url = json.load(file)
#         settings = url.get(website_name)
#     except:
#         return None
#     #! SET file_types of mime as os env
#     # with open("data/file_types.json",'r') as file_tp:
#     #     a = json.load(file_tp)

#     # Website creation & download !
#     website = Website(settings)
#     success = website.download()
#     if success:
#         return os.path.join(website.index_file_location, "index.html")
#     else:
#         return None


if __name__ == "__main__":
    os.environ['file_types'] = str({
      ".DOC": "application/msword",
      ".DOCX": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
      ".EML": "message/rfc822",
      ".ODT": "application/vnd.oasis.opendocument.text",
      ".PAGES": "application/vnd.apple.pages",
      ".RTF": "application/rtf",
      ".TEX": "text/x-tex",
      ".TXT": "text/plain",
      ".WPD": "application/vnd.wordperfect",
      ".CSV": "text/csv",
      ".KEY": "application/pgp-keys",
      ".MPP": "application/vnd.ms-project",
      ".PPT": "application/vnd.ms-powerpoint",
      ".PPTX": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
      ".TAR": "application/x-tar",
      ".VCF": "text/vcard",
      ".XML": "application/xml",
      ".AIF": "audio/x-aiff",
      ".FLAC": "audio/flac",
      ".M3U": "audio/mpegurl",
      ".M4A": "audio/mp4",
      ".MID": "audio/sp-midi",
      ".MP3": "audio/mpeg",
      ".OGG": "audio/ogg",
      ".WAV": "audio/x-wav",
      ".WMA": "audio/x-ms-wma",
      ".3GP": "audio/3gpp",
      ".ASF": "application/vnd.ms-asf",
      ".AVI": "video/x-msvideo",
      ".FLV": "video/x-flv",
      ".M4V": "video/mp4",
      ".MOV": "video/quicktime",
      ".MP4": "video/mp4",
      ".MPG": "video/mpeg",
      ".SRT": "text/plain",
      ".SWF": "application/vnd.adobe.flash.movie",
      ".TS": "text/vnd.trolltech.linguist",
      ".WMV": "video/x-ms-wmv",
      ".3DM": "text/vnd.in3d.3dml",
      ".DAE": "model/vnd.collada+xml",
      ".OBJ": "model/obj",
      ".BMP": "image/bmp",
      ".DCM": "application/dicom",
      ".DJVU": "image/vnd.djvu",
      ".GIF": "image/gif",
      ".HEIC": "image/heic",
      ".JPG": "image/jpeg",
      ".PNG": "image/png",
      ".PSD": "image/vnd.adobe.photoshop",
      ".TIF": "image/tiff",
      ".AI": "application/postscript",
      ".CDR": "image/x-coreldraw",
      ".EMF": "image/emf",
      ".EPS": "application/postscript",
      ".PS": "application/postscript",
      ".SVG": "image/svg+xml",
      ".OXPS": "application/oxps",
      ".PDF": "application/pdf",
      ".PUB": "application/vnd.exstream-package",
      ".XPS": "application/vnd.ms-xpsdocument",
      ".NUMBERS": "application/vnd.apple.numbers",
      ".ODS": "application/vnd.oasis.opendocument.spreadsheet",
      ".XLS": "application/vnd.ms-excel",
      ".XLSX": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
      ".MDB": "application/msaccess",
      ".ODB": "application/vnd.oasis.opendocument.base",
      ".PDB": "chemical/x-pdb",
      ".SQL": "application/sql",
      ".SQLITE": "application/vnd.sqlite3",
      ".APK": "application/vnd.android.package-archive",
      ".BAT": "application/x-msdos-program",
      ".BIN": "application/octet-stream",
      ".EXE": "application/x-msdos-program",
      ".JAR": "application/java-archive",
      ".SH": "text/x-sh",
      ".GAM": "chemical/x-gamess-input",
      ".PKG": "application/vnd.apple.installer+xml",
      ".DWG": "image/vnd.dwg",
      ".DXF": "image/vnd.dxf",
      ".STEP": "model/step",
      ".STL": "model/stl",
      ".STP": "model/step",
      ".KML": "application/vnd.google-earth.kml+xml",
      ".KMZ": "application/vnd.google-earth.kmz",
      ".OSM": "application/vnd.openstreetmap.data+xml",
      ".CER": "application/pkix-cert",
      ".CSS": "text/css",
      ".HTML": "text/html",
      ".JS": "text/javascript",
      ".JSON": "application/json",
      ".XHTML": "application/xhtml+xml",
      ".XPI": "application/x-xpinstall",
      ".OTF": "font/otf",
      ".TTF": "font/ttf",
      ".WOFF": "font/woff",
      ".WOFF2": "font/woff2",
      ".CAB": "application/vnd.ms-cab-compressed",
      ".CPL": "application/cpl+xml",
      ".DLL": "application/x-msdos-program",
      ".DMP": "application/vnd.tcpdump.pcap",
      ".ICO": "image/vnd.microsoft.icon"
    })
    settings = {
        "url": sys.argv[1],
        "download_res": eval(sys.argv[2]),
        "download_cors_res": eval(sys.argv[3]),
        "cors": eval(sys.argv[4]),
        "cors_download_res": eval(sys.argv[5]),
        "cors_download_cors_res": eval(sys.argv[6]),
        "max_cors": eval(sys.argv[7]),
        "same_origin_deviation": eval(sys.argv[8]),
        "location": sys.argv[9],
        "maintain_logs": eval(sys.argv[10]),
        "show_failed_files": eval(sys.argv[11]),
        "refetch": eval(sys.argv[12]),
        "hash": eval(sys.argv[13]),
        "max_threads": eval(sys.argv[14])
    }

    a = Website(settings)
    a.resources_downloaded = eval(sys.argv[15])
    a.webpages_scraped = eval(sys.argv[16])
    a.base_loc = sys.argv[17]
    a.download()