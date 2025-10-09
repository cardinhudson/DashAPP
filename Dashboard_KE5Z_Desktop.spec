# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_all
from PyInstaller.utils.hooks import copy_metadata

import os
base_path = os.path.abspath('.')
datas = [
    (os.path.join(base_path, 'app.py'), '.'),
    (os.path.join(base_path, 'auth_simple.py'), '.'),
    (os.path.join(base_path, 'Extracao.py'), '.'),
    (os.path.join(base_path, 'pages'), 'pages'),
    (os.path.join(base_path, 'KE5Z'), 'KE5Z'),
    (os.path.join(base_path, 'Extracoes'), 'Extracoes'),
    (os.path.join(base_path, 'arquivos'), 'arquivos'),
    (os.path.join(base_path, 'usuarios.json'), '.'),
    (os.path.join(base_path, 'usuarios_padrao.json'), '.'),
    (os.path.join(base_path, 'dados_equipe.json'), '.'),
    (os.path.join(base_path, 'Dados SAPIENS.xlsx'), '.'),
    (os.path.join(base_path, 'Fornecedores.xlsx'), '.')
]
binaries = []
hiddenimports = ['altair', 'auth_simple', 'Extracao', 'base64', 'datetime.datetime', 'gc', 'io.BytesIO', 'os', 'pandas', 'plotly.graph_objects', 'plotly', 'streamlit', 'sys']
datas += copy_metadata('streamlit')
datas += copy_metadata('streamlit-desktop-app')
datas += copy_metadata('plotly')
datas += copy_metadata('altair')
datas += copy_metadata('pandas')
tmp_ret = collect_all('streamlit')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]


a = Analysis(
    ['C:\\Users\\u235107\\AppData\\Local\\Temp\\tmpiap_dy0s.py'],
    pathex=['.'],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
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
    [],
    exclude_binaries=True,
    name='Dashboard_KE5Z_Desktop',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='Dashboard_KE5Z_Desktop',
)
