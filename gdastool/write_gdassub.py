import datetime

directory = '/user/rstanley/CORSIKA/GDAS/'

ts_start = 1584748800 #2020/3/21 00:00:00 GMT
ts_end = 1269129600 #2010/3/21 00:00:00 GMT
number = int((ts_start - ts_end) / (3600 * 6))

filename = directory + 'qsub_ATM.txt'
outfile = open(filename, 'w')

num = number + 1

for i in range(num):

    ts = ts_start - (i * 3600 * 6)

    date = datetime.datetime.fromtimestamp(ts)
    year = int(date.year)
    month = int(date.month)
    day = int(date.day)
    hour = int(date.hour)

    outfile.write('qsub ' + directory + 'gdasin/ATM_' + str(year) + '_' + str(month) + '_' + str(day) + '_' + str(hour) + '.sh\n')
    outfile.write('sleep 60\n')

