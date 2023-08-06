#!C:\Anaconda\envs\_verify\python.exe
# EASY-INSTALL-ENTRY-SCRIPT: 'convergence==0.1','console_scripts','grid-convergence'
__requires__ = 'convergence==0.1'
import re
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(
        load_entry_point('convergence==0.1', 'console_scripts', 'grid-convergence')()
    )
