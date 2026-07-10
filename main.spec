# main.spec
from PyInstaller.building.build_main import Analysis, PYZ, EXE
import sys

block_cipher = None

a = Analysis(
    ['src/main.py'],
    pathex=['.'],
    binaries=[],
    datas=[
        ('assets', 'assets'),
        ('src/website.py', 'src'),
        ('src/webview_launch.py', 'src'),
        ('src/webpage.py', 'src'),    # main.py imports this too
    ],
    hiddenimports=[
        'pygame',
        'pygame_textinput',
        'PIL',
        'PIL.Image',
        'psutil',
        'urllib.parse',
        'asyncio',
        'threading',
        'subprocess',
        'json',
        'shutil',
        'webbrowser',
        'website',
        'webpage',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='Webber',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,          # no console window
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='assets/Webber.ico',
    onefile=True,
)