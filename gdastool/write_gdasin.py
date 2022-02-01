import datetime

directory = '/user/rstanley/CORSIKA/GDAS/gdasin/'

ts_start = 1584748800 #2020/3/21 00:00:00 GMT
ts_end = 1269129600#2010/3/21 00:00:00 GMT

number = int((ts_start - ts_end) / (3600 * 6))
lat = -77.666667
long = 157.666667

for i in range(number+1):

    ts = ts_start - (i * 3600 * 6)

    date = datetime.datetime.fromtimestamp(ts)
    year = int(date.year)
    month = int(date.month)
    day = int(date.day)
    hour = int(date.hour)

    filename = directory + 'ATM_' + str(year) + '_' + str(month) + '_' + str(day) + '_' + str(hour) + '.sh'
    outfile = open(filename, 'w')
    outfile.write('#PBS -N GDAS\n')
    outfile.write('mkdir $TMPDIR/GDAS/\n') 
    outfile.write('cd /software/corsika/corsika-77100/src/utils/\n')
    outfile.write('eval `/cvmfs/icecube.opensciencegrid.org/py2-v3.1.1/setup.sh`\n')
    outfile.write('python gdastool -c {5} {6} -t {0} -p /$TMPDIR/GDAS/ -o /user/rstanley/CORSIKA/GDAS/atmfiles/ATM_{1}_{2}_{3}_{4}.DAT\n'.format(ts, year, month, day, hour, lat, long))
    outfile.write('rm -rf $TMPDIR/GDAS\n')
    outfile.write('exit')
