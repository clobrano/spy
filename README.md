![pytest](https://github.com/clobrano/spy/actions/workflows/test.yml/badge.svg)

# spy
Filesystem events watcher in Python based on [Watchdog](https://duckduckgo.com/l/?uddg=https://pypi.org/project/watchdog/&notrut=duckduck_in)

# Usage

```
usage: Spy catches files changes and react with custom commands
       [-h] [--watch-dir WATCH_DIR] [--recursive RECURSIVE]
       [--on-create ON_CREATE] [--on-change ON_CHANGE] [--on-remove ON_REMOVE]
       [--extensions EXTENSIONS] [--timeout TIMEOUT]

optional arguments:
  -h, --help                            Show this help message and exit
  --watch-dir WATCH_DIR, -w WATCH_DIR   The directory to watch
  --recursive RECURSIVE, -r RECURSIVE   Whether to watch the subdirectories
  --on-create ON_CREATE                 Command to execute when a file is created inside the directory
  --on-change ON_CHANGE                 Command to execute on directory changes
  --on-remove ON_REMOVE                 Command to execute when a file is deleted from the directory
  --extensions EXTENSIONS               Comma separated list of extension file to track
  --timeout TIMEOUT                     Timeout in seconds for Spy to watch the directory (-1 is infinite)
```


