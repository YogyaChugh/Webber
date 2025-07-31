# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['src\\main.py'],
    pathex=[],
    binaries=[],
    datas=[('src/exceptions.py', '.'), ('src/webpage.py', '.'), ('src/website.py', '.'), ('src/webview_launch.py', '.'), ('data/details.json', 'data'), ('data/file_types.json', 'data'), ('assets/bgimg.png', 'assets'), ('assets/cancel.gif', 'assets'), ('assets/cancel.png', 'assets'), ('assets/del.gif', 'assets'), ('assets/delete.gif', 'assets'), ('assets/delete.png', 'assets'), ('assets/eye.png', 'assets'), ('assets/fs.jpeg', 'assets'), ('assets/github.png', 'assets'), ('assets/gmail.png', 'assets'), ('assets/hanging_spider.png', 'assets'), ('assets/i-cursor.png', 'assets'), ('assets/idea.gif', 'assets'), ('assets/internet.gif', 'assets'), ('assets/leftji.png', 'assets'), ('assets/main_logo_webber.png', 'assets'), ('assets/man.gif', 'assets'), ('assets/meditation.gif', 'assets'), ('assets/mouse.png', 'assets'), ('assets/mouse2.png', 'assets'), ('assets/pause.png', 'assets'), ('assets/play.png', 'assets'), ('assets/rocket_icon.png', 'assets'), ('assets/sad.gif', 'assets'), ('assets/slack.png', 'assets'), ('assets/some_catie.gif', 'assets'), ('assets/spider_logo_main.png', 'assets'), ('assets/spider.png', 'assets'), ('assets/ss.png', 'assets'), ('assets/success.gif', 'assets'), ('assets/tick.png', 'assets'), ('assets/w_button_ji_animated.png', 'assets'), ('assets/w_button_ji.png', 'assets'), ('assets/fonts/FiraSans-Bold.ttf', 'assets/fonts'), ('assets/fonts/HappyMonkey-Regular.ttf', 'assets/fonts'), ('assets/fonts/LuckiestGuy-Regular.ttf', 'assets/fonts'), ('assets/fonts/VarelaRound-Regular.ttf', 'assets/fonts')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='Webber',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['assets\\spider_logo_main.ico'],
)
