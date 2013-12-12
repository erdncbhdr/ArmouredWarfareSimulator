# -*- mode: python -*-
a = Analysis(['ServerSetupForm.py'],
             pathex=['C:\\Users\\Harry\\Documents\\GitHub\\ArmouredWarfareSimulator\\Server'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)
a.datas += [('TankStats.db', 'C:\\Users\\Harry\\Documents\\GitHub\\ArmouredWarfareSimulator\\Server\\TankStats.db', 'DATA'),
            ('login.conf', 'C:\\Users\\Harry\\Documents\\GitHub\\ArmouredWarfareSimulator\\Server\\login.conf', 'DATA'),
            ('LoginDatabase','C:\\Users\\Harry\\Documents\\GitHub\\ArmouredWarfareSimulator\\Server\\LoginDatabase', 'DATA')]
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='ServerSetupForm.exe',
          debug=False,
          strip=None,
          upx=True,
          console=True )
