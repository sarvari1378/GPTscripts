
from persiantools.jdatetime import JalaliDate
from persiantools.jdatetime import JalaliDate

from datetime import datetime

date = JalaliDate(datetime.now()).strftime('%Y-%m-%d')
with open('date.txt', 'w') as f:
    f.write(date)
