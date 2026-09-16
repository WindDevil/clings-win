SOURCE ?= ../cling
PYTHON ?= python3

.PHONY: help sync check winbox winbox-native windows-check package clean

help:
	@printf '%s\n' \
		'clings-win targets:' \
		'  make sync            copy exercises/solutions from $(SOURCE) and apply Windows overrides' \
		'  make check           fail if the twin is out of sync with $(SOURCE)' \
		'  make winbox          fetch the Linux-side mingw-w64 + Wine toolbox into .winbox/' \
		'  make winbox-native   also fetch w64devkit and Windows Python for packaging' \
		'  make windows-check   cross compile + run everything through Wine' \
		'  make package         build the beginner zip in dist/' \
		'  make clean           remove build artifacts'

sync:
	$(PYTHON) tools/sync_from_source.py --source $(SOURCE)

check:
	$(PYTHON) tools/sync_from_source.py --source $(SOURCE) --check

winbox:
	tools/winbox.sh fetch

winbox-native:
	tools/winbox.sh fetch-native

windows-check:
	tools/windows-check.sh

package:
	$(PYTHON) tools/package_windows.py

clean:
	rm -rf build .clings dist
