# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['conways_game_of_life.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[
        'scipy.signal',
        'scipy.special',
        'scipy.special._ufuncs',
        'scipy.special._cdflib',
        'scipy.linalg',
        'scipy._lib',
        'scipy._lib._util'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    excludedimports=['api-ms-win-core-path-l1-1-0.dll']
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='conways_game_of_life',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
