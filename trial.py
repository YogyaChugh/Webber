import webview
import os
import sys

class Api:
    def __init__(self, window, pages):
        self.window = window
        self.pages = [os.path.abspath(p) for p in pages]
        self.current_index = 0

    def go_back(self):
        if self.current_index > 0:
            self.current_index -= 1
            self.load_current_page()

    def go_next(self):
        if self.current_index < len(self.pages) - 1:
            self.current_index += 1
            self.load_current_page()

    def load_current_page(self):
        path = self.pages[self.current_index]
        self.window.load_url(f"file://{path}")

def create_js_overlay():
    return """
    <script>
    function createNavButtons() {
        const backBtn = document.createElement('button');
        backBtn.innerText = '← Back';
        backBtn.style.cssText = 'position:fixed;top:10px;left:10px;z-index:9999;padding:10px;font-size:16px;';
        backBtn.onclick = () => pywebview.api.go_back();

        const nextBtn = document.createElement('button');
        nextBtn.innerText = 'Next →';
        nextBtn.style.cssText = 'position:fixed;top:10px;right:10px;z-index:9999;padding:10px;font-size:16px;';
        nextBtn.onclick = () => pywebview.api.go_next();

        document.body.appendChild(backBtn);
        document.body.appendChild(nextBtn);
    }

    window.onload = createNavButtons;
    </script>
    """

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python main.py <file1.html> <file2.html> ...")
        sys.exit(1)

    html_files = sys.argv[1:]
    for file in html_files:
        if not os.path.exists(file):
            print(f"File not found: {file}")
            sys.exit(1)

    api = Api(None, html_files)
    initial_file = api.pages[0]

    window = webview.create_window(
        "Local Page Viewer",
        f"{initial_file}",
        js_api=api,
        width=800,
        height=600
    )
    api.window = window

    def on_loaded():
        webview.evaluate_js(create_js_overlay())

    webview.start(on_loaded, window, gui='cef' if webview.platform == 'windows' else None)
