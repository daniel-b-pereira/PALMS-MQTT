# -*- mode: python ; coding: utf-8 -*-
# change de pathex every time you want to rebuild pyinstaller
block_cipher = None
added_files = [
         ( 'C:\\Users\\roger\\pms\\gui\\qtGui\\images\\femec.jpeg', 'data' ),
         ( 'C:\\Users\\roger\\pms\\gui\\qtGui\\images\\xml.svg', 'data' )
         ]

a = Analysis(['main.py'],
             pathex=['C:\\Users\\roger\\pms'],
             binaries=[],
             datas= added_files,
             hiddenimports=[],
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
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='palms',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False , icon='ico.ico')

