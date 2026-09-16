#!/usr/bin/env bash
# Windows regression loop (no Windows required).
#
# Every exercise and every solution is cross compiled to a Windows PE binary
# with mingw-w64 and then executed through Wine, driving the twin's own runner
# so the CLI logic is covered as well:
#
#   verify    - all 185 solutions compile and pass under the Windows target
#   selftest  - every exercise still starts out failing
#
# This is the fast loop (seconds to a couple of minutes).  Real Windows
# ground truth comes from the windows-latest CI job; see docs/portability.md.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
# shellcheck source=tools/winbox.sh
source "$ROOT/tools/winbox.sh"
use_box

export CC="$MINGW_CC"
export CLINGS_TARGET=windows
export CLINGS_EXEC_PREFIX="$WINE"

cd "$ROOT"
status=0

# Wine costs several seconds per program when its server has to be restarted
# for every exercise, and about 20 ms when it stays alive.  Warm the prefix up
# once (bounded, because the very first start also initialises the registry and
# the driver host) and then keep the server from idling out.
printf '== warming up the Wine prefix\n'
timeout 180 "$WINE" cmd /c exit >/dev/null 2>&1 || true
( while :; do "$WINE" cmd /c exit >/dev/null 2>&1; sleep 2; done ) &
wine_keepalive=$!
trap 'kill "$wine_keepalive" 2>/dev/null || true' EXIT

# Unbuffered output so a long run can be watched while it happens, and stdin
# from /dev/null so an exercise that waits for keyboard input cannot block the
# loop (it sees end-of-file instead, exactly like a CI machine).
printf '== verifying solutions (CC=%s, runtime=wine)\n' "$CC"
python3 -u clings verify "$@" </dev/null || status=1
printf '\n== checking that exercises start unsolved\n'
python3 -u clings selftest "$@" </dev/null || status=1
exit "$status"
