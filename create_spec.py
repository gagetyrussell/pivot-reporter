# -*- coding: utf-8 -*-
"""
Created on Sun Apr  5 21:18:37 2020

@author: GRussell
"""

import sys
import os

exe_path = sys.executable
venv_path = "\\".join(exe_path.rsplit("\\")[:-2]) + "\\Lib\\site-packages\\"
print(venv_path)
dir_path = os.path.dirname(os.path.realpath(__file__))
asset_path = dir_path + "\\assests\\"

with open('build.spec', "w") as f:
    venv_loc = os.system("pipenv --venv")
    s = rf"""# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['app.py'],
             pathex=['{dir_path}'],
             binaries=[],
             datas=[('{venv_path}', '.\')],
             hiddenimports=['pkg_resources.py2_warn'],
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
          name='GTR-spreadsheet-view',
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
               name='GTR-spreadsheet-view')
        """
    s = s.replace("\\", "\\\\")
    print(s)
    f.write(s)