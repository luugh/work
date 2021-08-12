# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['getting_work_hours.py'],
             pathex=['E:\\untitled3\\venv\\Lib\\site-packages', 'E:\\untitled3\\Getting_Work_Hours'],
             binaries=[],
             datas=[],
             hiddenimports=['openpyxl,xlrd,xlwt,datetime'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='getting_work_hours',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='getting_work_hours')
