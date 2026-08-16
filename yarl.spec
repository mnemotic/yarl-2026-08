#
# See <https://github.com/microsoft/apm/issues/487>.
#

import subprocess
import sys
from pathlib import Path

from PyInstaller.building.api import COLLECT, EXE, PYZ
from PyInstaller.building.build_main import Analysis


def is_upx_available():
    try:
        subprocess.run(["upx", "--version"], capture_output=True, check=True)
        return True
    except subprocess.CalledProcessError, FileNotFoundError:
        return False


def should_use_upx():
    """Enable UPX only on non-Windows platforms where it is available.

    UPX-compressed PE binaries trigger ML-based AV false positives
    (e.g. Trojan:Win32/Bearfoos.B!ml) on Windows Defender.
    """
    if sys.platform == "win32":
        return False
    return is_upx_available()


def read_version_from_pyproject(repo_root: Path) -> tuple[int, int, int, int]:
    import tomlrt

    pyproject = repo_root / "pyproject.toml"
    if not pyproject.exists():
        return (0, 0, 0, 0)
    with open(pyproject, "rb") as fp:
        content = tomlrt.load(fp)
        version = content["project"]["version"].split(".")
        return (int(version[0]), int(version[1]), int(version[2]), 0)


# `SPECPATH` is a global variable set by PyInstaller.
repo_root = Path(SPECPATH)  # ty: ignore[unresolved-reference]  # noqa: F821
entry_point = repo_root / "src" / "yarl" / "__main__.py"


win_version_info = None
if sys.platform == "win32":
    try:
        from PyInstaller.utils.win32 import versioninfo

        ver = read_version_from_pyproject(repo_root)
        ver_str = f"{ver[0]}.{ver[1]}.{ver[2]}"
        win_version_info = versioninfo.VSVersionInfo(
            ffi=versioninfo.FixedFileInfo(
                filevers=ver,
                prodvers=ver,
                mask=0x3F,
                flags=0x0,
                OS=0x40004,
                fileType=0x1,
                subtype=0x0,
            ),
            kids=[
                versioninfo.StringFileInfo(
                    [
                        versioninfo.StringTable(
                            "040904B0",
                            [
                                versioninfo.StringStruct("CompanyName", "Martin Green"),
                                versioninfo.StringStruct(
                                    "FileDescription", "YARL - Yet Another Roguelike"
                                ),
                                versioninfo.StringStruct("FileVersion", ver_str),
                                versioninfo.StringStruct("InternalName", "yarl"),
                                versioninfo.StringStruct(
                                    "LegalCopyright", "Copyright (c) Martin Green"
                                ),
                                versioninfo.StringStruct(
                                    "OriginalFilename", "yarl.exe"
                                ),
                                versioninfo.StringStruct("ProductName", "YARL"),
                                versioninfo.StringStruct("ProductVersion", ver_str),
                            ],
                        )
                    ]
                ),
                versioninfo.VarFileInfo(
                    [versioninfo.VarStruct("Translation", [0x0409, 0x04B0])]
                ),
            ],
        )
    except ImportError:
        win_version_info = None

a = Analysis(
    [str(entry_point)],
    pathex=[str(repo_root / "src")],
    binaries=[],
    datas=[("src/yarl/assets/*", "assets")],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=2,
)
pyz = PYZ(a.pure)

strip = sys.platform != "win32"

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="yarl",
    debug=False,
    bootloader_ignore_signals=False,
    strip=strip,
    upx=should_use_upx(),
    upx_exclude=[],
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    version=win_version_info,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=strip,
    upx=should_use_upx(),
    upx_exclude=[],
    name="yarl",
)
