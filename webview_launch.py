import webview
import sys
import dill


if __name__ == "__main__":
    url = sys.argv[1] if len(sys.argv) > 1 else None
    if url:
        webview.settings['ALLOW_DOWNLOADS'] = True
        webview.settings['OPEN_EXTERNAL_LINKS_IN_BROWSER'] = False
        window = webview.create_window('MY WEBSITE',url)
        with open(f"web_{url}.pkl","wb") as ok:
            dill.dump([url, window],ok)
        webview.start()