# -*- mode: python -*-
a = Analysis(['main.py'],
             pathex=['C:\\Users\\Harry\\Documents\\GitHub\\ArmouredWarfareSimulator\\Client'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)
a.datas += [('TankStats.db', 'C:\\Users\\Harry\\Documents\\GitHub\\ArmouredWarfareSimulator\\Client\\TankStats.db', 'DATA'),
	    ('login.conf', 'C:\\Users\\Harry\\Documents\\GitHub\\ArmouredWarfareSimulator\\Client\\login.conf', 'DATA')]

pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='main.exe',
          debug=False,
          strip=None,
          upx=True,
          console=True )
