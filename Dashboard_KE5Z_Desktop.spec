# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_all
from PyInstaller.utils.hooks import copy_metadata

datas = [('C:\\GitHub\\Dash-V3\\app.py', '.')]
binaries = []
hiddenimports = ['altair', 'auth_simple.adicionar_usuario_simples', 'auth_simple.criar_hash_senha', 'auth_simple.eh_administrador', 'auth_simple.exibir_header_usuario', 'auth_simple.get_modo_operacao', 'auth_simple.get_usuarios_cloud', 'auth_simple.is_modo_cloud', 'auth_simple.verificar_autenticacao', 'auth_simple.verificar_status_aprovado', 'base64', 'datetime.datetime', 'gc', 'io.BytesIO', 'os', 'pandas', 'plotly.graph_objects', 'streamlit', 'sys']
datas += copy_metadata('streamlit')
tmp_ret = collect_all('streamlit')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]


a = Analysis(
    ['C:\\Users\\hudso\\AppData\\Local\\Temp\\tmp6zpxdi9o.py'],
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
