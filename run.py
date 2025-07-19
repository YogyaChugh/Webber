import webview

webview.settings['ALLOW_DOWNLOADS'] = True
webview.settings['OPEN_EXTERNAL_LINKS_IN_BROWSER'] = False
a = input("Enter local url to open: ")
window = webview.create_window('MY WEBSITE',f"{a}/index.html")
webview.start()