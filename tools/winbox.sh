#!/usr/bin/env bash
# winbox - reproducible Linux-side toolbox for developing the Windows twin.
#
# It unpacks a mingw-w64 cross compiler and Wine 9 into .winbox/ without
# touching the host system (no root, no packages installed), so that Windows
# binaries can be produced and executed on a machine that has no Windows.
#
#   tools/winbox.sh fetch          # cross compiler + wine (for windows-check)
#   tools/winbox.sh fetch-native   # also w64devkit + Windows Python (for the
#                                  # packaged, "beginner" toolchain)
#   tools/winbox.sh env            # print shell exports (eval "$(... env)")
#   tools/winbox.sh check          # compile and run one PE binary through Wine
#
# The two packaging quirks of the Ubuntu wine64 package are repaired here; see
# fix_packaging() below.
# Strict mode only when executed; sourcing must not change the caller's shell.
if [ "${BASH_SOURCE[0]}" = "$0" ]; then
    set -euo pipefail
fi

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BOX="${WINBOX_DIR:-$ROOT/.winbox}"
DEBS="$BOX/debs"
ROOTFS="$BOX/root"
NATIVE="$BOX/native"
WINE_LIBDIR="$ROOTFS/usr/lib/x86_64-linux-gnu/wine"
WINE_DLLDIR="$WINE_LIBDIR/x86_64-windows"
# Wine's loader resolves wine64-preloader and wineserver relative to argv[0],
# so it must always be started through its real path.  Calling it through a
# symlink fails with "could not exec the wine loader".
WINE="$ROOTFS/usr/lib/wine/wine64"

MINGW_CC="${MINGW_CC:-x86_64-w64-mingw32-gcc-posix}"
W64DEVKIT_VERSION="${W64DEVKIT_VERSION:-2.10.0}"
PYTHON_EMBED_VERSION="${PYTHON_EMBED_VERSION:-3.12.10}"

# Download only: never install into the host, and never require root.
APT=(apt-get -o Debug::NoLocking=1 -o "Dir::Cache::archives=$DEBS"
     -o Dir::State::status=/var/lib/dpkg/status)
PACKAGES=(gcc-mingw-w64-x86-64-posix wine64 wine64-preloader)

log() { printf '[winbox] %s\n' "$*" >&2; }
die() { printf '[winbox] error: %s\n' "$*" >&2; exit 1; }

fetch() {
    command -v apt-get >/dev/null 2>&1 \
        || die "apt-get is required to fetch the Windows toolchain"
    command -v dpkg-deb >/dev/null 2>&1 || die "dpkg-deb is required"
    mkdir -p "$DEBS" "$ROOTFS"
    log "downloading ${PACKAGES[*]} into $DEBS"
    "${APT[@]}" update -qq \
        || log "apt-get update failed; using the existing package lists"
    "${APT[@]}" install --download-only -y --reinstall "${PACKAGES[@]}"
    log "unpacking packages into $ROOTFS"
    for deb in "$DEBS"/*.deb; do
        dpkg-deb -x "$deb" "$ROOTFS"
    done
    fix_packaging
    log "ready; run 'tools/winbox.sh check'"
}

# Ubuntu's wine64 package assumes it lives at the absolute paths /usr/lib/wine
# and /usr/lib/x86_64-linux-gnu/wine.  Two small repairs make the relocated
# copy work:
#   1. /usr/lib/wine/wineserver is a wrapper script hardcoding
#      /usr/lib/wine/wineserver64, which does not exist here.
#   2. user32.dll imports zlib1.dll, which the package ships in the mingw
#      sysroot (libz-mingw-w64) instead of the Wine DLL directory.
fix_packaging() {
    local wineserver="$ROOTFS/usr/lib/wine/wineserver"
    if [ -e "$wineserver" ] && [ ! -L "$wineserver" ]; then
        rm -f "$wineserver"
        ln -s wineserver64 "$wineserver"
    fi
    local zlib="$ROOTFS/usr/x86_64-w64-mingw32/lib/zlib1.dll"
    if [ -f "$zlib" ] && [ -d "$WINE_DLLDIR" ]; then
        cp -f "$zlib" "$WINE_DLLDIR/"
    fi
}

# Make the unpacked toolchain usable in the current shell.  The GCC driver has
# to be invoked through its real path, so the compiler is found through PATH
# rather than through a symlink.
use_box() {
    export WINEPREFIX="$BOX/prefix"
    export WINE
    export WINELOADER="$WINE"
    export WINESERVER="$ROOTFS/usr/lib/wine/wineserver64"
    export WINEDLLPATH="$WINE_DLLDIR"
    export WINEDLLOVERRIDES='mscoree,mshtml='
    export WINEDEBUG="${WINEDEBUG:--all}"
    export LD_LIBRARY_PATH="$ROOTFS/usr/lib/x86_64-linux-gnu${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
    export PATH="$ROOTFS/usr/bin:$PATH"
    export MINGW_CC="$MINGW_CC"
}

# Same thing, printable so callers can do: eval "$(tools/winbox.sh env)".
env_exports() {
    (
        use_box
        declare -p WINEPREFIX WINE WINELOADER WINESERVER WINEDLLPATH \
                   WINEDLLOVERRIDES WINEDEBUG LD_LIBRARY_PATH PATH MINGW_CC \
            | sed 's/^declare -x /export /'
    )
}

require_ready() {
    [ -x "$WINE" ] || die "run 'tools/winbox.sh fetch' first"
    command -v "$MINGW_CC" >/dev/null 2>&1 \
        || die "$MINGW_CC not found; run 'tools/winbox.sh fetch'"
}

check() {
    use_box
    require_ready
    local tmp
    tmp="$(mktemp -d)"
    trap 'rm -rf "$tmp"' RETURN
    printf '#include <stdio.h>\nint main(void) { printf("winbox ok\\n"); return 0; }\n' \
        >"$tmp/hello.c"
    "$MINGW_CC" -std=c17 -Wall -Wextra -Werror "$tmp/hello.c" -o "$tmp/hello.exe"
    "$WINE" "$tmp/hello.exe"
    printf 'compiler: %s\n' "$("$MINGW_CC" --version | head -1)"
    printf 'runtime:  %s\n' "$("$WINE" --version)"
}

# w64devkit is the toolchain the packaged Windows distribution ships: a
# self-contained mingw-w64 + make + gdb, extracted from a 7z self-extractor.
fetch_native() {
    fetch
    mkdir -p "$NATIVE"
    "${APT[@]}" install --download-only -y 7zip
    for deb in "$DEBS"/7zip_*.deb; do
        [ -e "$deb" ] && dpkg-deb -x "$deb" "$ROOTFS"
    done
    local unpack="$ROOTFS/usr/lib/7zip/7z"
    [ -x "$unpack" ] || die "7z not available after unpacking the 7zip package"

    local sfx="$NATIVE/w64devkit-x64-$W64DEVKIT_VERSION.7z.exe"
    if [ ! -f "$sfx" ]; then
        log "downloading w64devkit $W64DEVKIT_VERSION"
        curl -fSL -o "$sfx" \
            "https://github.com/skeeto/w64devkit/releases/download/v$W64DEVKIT_VERSION/w64devkit-x64-$W64DEVKIT_VERSION.7z.exe"
    fi
    log "unpacking w64devkit (about 750 MB)"
    "$unpack" x -y -o"$NATIVE" "$sfx" >/dev/null

    local python_zip="$NATIVE/python-$PYTHON_EMBED_VERSION-embed-amd64.zip"
    if [ ! -f "$python_zip" ]; then
        log "downloading Python $PYTHON_EMBED_VERSION (embeddable)"
        curl -fSL -o "$python_zip" \
            "https://www.python.org/ftp/python/$PYTHON_EMBED_VERSION/python-$PYTHON_EMBED_VERSION-embed-amd64.zip"
    fi
    mkdir -p "$NATIVE/python"
    python3 -m zipfile -e "$python_zip" "$NATIVE/python"
    log "native runtime ready: $NATIVE/w64devkit, $NATIVE/python"
}

# Sourced by tools/windows-check.sh, executed from the command line otherwise.
if [ "${BASH_SOURCE[0]}" = "$0" ]; then
    case "${1:-}" in
        fetch) fetch ;;
        fetch-native) fetch_native ;;
        env) env_exports ;;
        check) check ;;
        *)
            cat >&2 <<'EOF'
usage: tools/winbox.sh {fetch|fetch-native|env|check}
  fetch         unpack the mingw-w64 cross compiler and Wine into .winbox/
  fetch-native  also fetch w64devkit and Windows Python (packaged toolchain)
  env           print shell exports for the Wine loop
  check         compile and run one PE binary through Wine
EOF
            exit 2
            ;;
    esac
fi
