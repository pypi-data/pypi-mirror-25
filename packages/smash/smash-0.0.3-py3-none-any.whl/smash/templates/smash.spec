# -*- mode: python -*-

block_cipher = None

#----------------------------------------------------------------------#

from pathlib import Path
import os

root_path = Path( os.getcwd() )

a = Analysis( ['smash.py'],
              pathex=[str(root_path)],
              binaries=[],
              datas=[],
              hiddenimports=[],
              hookspath=[],
              runtime_hooks=[],
              excludes=[],
              cipher=block_cipher,
              win_no_prefer_redirects=False,
              win_private_assemblies=False,
              )

pyz = PYZ(
    a.pure,
    a.zipped_data,
    cipher=block_cipher
)

exe = EXE(
    pyz,
    a.scripts,
    exclude_binaries=True,
    name='smash',
    debug=False,
    strip=False,
    upx=True,
    console=True
)

def collect_data( subpath ) :
    global a

    for path, _, _ in os.walk( str( root_path / subpath ) ) :
        rel_path = Path( path ).relative_to( root_path )
        a.datas += Tree( path, prefix=rel_path )


collect_data( 'pkgs' )
collect_data( 'envs' )
collect_data( 'repo' )
collect_data( 'sys' )

#----------------------------------------------------------------------#

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,

    strip=False,
    upx=True,
    name='smash'
)


#----------------------------------------------------------------------#
