import webview
import sys

def back():
    webview.windows[0].evaluate_js("history.back();")
    
def next():
    webview.windows[0].evaluate_js("history.forward();")

def webber():
    pass

menu = [
    webview.menu.MenuAction('Back',back),
    webview.menu.MenuAction('                                                                                                                               Webber                                                                                                                                    ',webber),
    webview.menu.MenuAction('Next',next)
]



if __name__ == "__main__":
    url = sys.argv[1] if len(sys.argv) > 1 else None
    name = sys.argv[2] if len(sys.argv) >2 else None
    if url and name:
        webview.settings['ALLOW_DOWNLOADS'] = True
        webview.settings['OPEN_EXTERNAL_LINKS_IN_BROWSER'] = False
        window = webview.create_window(
            name,
            url,
            confirm_close=True,
            zoomable=True,
            width=1000,
            height= 700,
            resizable=False
        )
        webview.start(menu=menu, icon='assets/spider_logo_main.png')