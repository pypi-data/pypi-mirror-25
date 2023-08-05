# process-watcher
Watch Linux processes and notify when they complete. Should also work with MacOS*.

Only needs the */proc* pseudo-filesystem to check and gather information about processes. Does not need to create/own the process, if you want a daemon manager, see the *Alternatives* section below.

Currently written for **Python3**, but shouldn't be difficult to make python2 compatible.


