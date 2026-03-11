from PyInstaller.building.build_main import Analysis, PYZ, EXE, COLLECT
import sys
from os import path

block_cipher = None

# Define all assets paths
assets_path = r'C:\Soft AI Pro\assets'
icon_path = path.join(assets_path, 'icon.ico')
logo_path = path.join(assets_path, 'SoftAI_Logo.png')

a = Analysis(
    ['Soft ΔI Code.py'],
    pathex=[r'C:\Soft AI Pro'],
    binaries=[],
    datas=[
        (path.join(assets_path, '*'), 'assets'),
    ],
    hiddenimports=[
        'PySide6.QtCore',
        'PySide6.QtGui',
        'PySide6.QtWidgets',
        'PySide6.QtWebEngineCore'
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

# Add specific assets
a.datas += [
    ('assets/SoftAI_Logo.png', logo_path, 'DATA'),
    ('assets/icon.ico', icon_path, 'DATA'),
    ('assets/new_project.png', path.join(assets_path, 'new_project.png'), 'DATA'),
    ('assets/archive.png', path.join(assets_path, 'archive.png'), 'DATA'),
    ('assets/docs.png', path.join(assets_path, 'docs.png'), 'DATA'),
    ('assets/cloud.png', path.join(assets_path, 'cloud.png'), 'DATA'),
    ('assets/settings.png', path.join(assets_path, 'settings.png'), 'DATA'),
]

pyz = PYZ(
    a.pure,
    a.zipped_data,
    cipher=block_cipher
)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='SoftΔI Pro',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,  # Set to True for debugging
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=icon_path
)

dist_path = r'C:\Soft AI Pro\dist\SoftΔI Pro.exe'