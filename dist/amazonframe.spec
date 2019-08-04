# -*- mode: python -*-

block_cipher = None


a = Analysis(['amazonframe.py'],
             pathex=['D:\\BaiduYunDownload\\tmp2\\login\\dist'],
             binaries=[],
             datas=[],
             hiddenimports=['_cffi_backend'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='amazonframe',
          debug=False,
          strip=False,
          upx=True,
          console=False )
