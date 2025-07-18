import webview

webview.settings['ALLOW_DOWNLOADS'] = True
window = webview.create_window('MY WEBSITE',"summer.hackclub.com/index.html")
webview.start()