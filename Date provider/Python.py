import subprocess
import sys

try:
    from persiantools.jdatetime import JalaliDate
except ModuleNotFoundError:
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'persiantools'])
    from persiantools.jdatetime import JalaliDate

from datetime import datetime

date = JalaliDate(datetime.now()).strftime('%Y-%m-%d')
with open('date.txt', 'w') as f:
    f.write(date)
