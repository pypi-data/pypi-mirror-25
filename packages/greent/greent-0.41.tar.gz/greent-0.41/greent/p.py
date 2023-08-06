# Setup - virtualenv (Python 2 or 3)
# $ virtualenv -p /PATH/TO/PYTHON venv
# $ source venv/bin/activate
# $ pip install bravado
# $ python test-bravado.py

from bravado.client import SwaggerClient
import datetime
from pprint import pprint

local_swagger = 'PATH_TO/nih-exposures-api/specification/swagger.yml'
github_swagger = 'https://raw.githubusercontent.com/RENCI/nih-exposures-api/master/specification/swagger.yml'
#github_swagger = "https://exposures.renci.org/v1/swagger.json"
#github_swagger = "file:///Users/scox/dev/greent/greent/x.json"

# defaults to github_swagger, but should be changed to local_swagger if doing development work
client = SwaggerClient.from_url(
    github_swagger,
    config={'use_models': False}
)

# get valid exposures calls
dir_exp = dir(client.cmaq)
print('### dir(client.cmaq) ###')
pprint(dir_exp)
print('')

# get exposures types
exp_types = client.cmaq.get_cmaq().result( timeout=10 )
print('### client.cmaq.get_cmaq().result( timeout=10 ) ###')
pprint(exp_types)
print('')

# get exposures values for date range 2010-01-10 to 2010-10-20 for pm25 at latitude=34.15581748, longitude=-77.99258944
string_date = '2011-01-10 00:00:00.000'
sdate = datetime.datetime.strptime(string_date, "%Y-%m-%d %H:%M:%S.%f").date()
string_date = '2011-01-20 00:00:00.000'
edate = datetime.datetime.strptime(string_date, "%Y-%m-%d %H:%M:%S.%f").date()
lat = '34.15581748'
lon = '-77.99258944'

exp_values = client.cmaq.get_cmaq_getValues(
    exposureType='pm25',
    startDate=sdate,
    endDate=edate,
    latLon=lat + ',' + lon
).result()
print('### client.cmaq.get_cmaq_getValues ... ###')
pprint(exp_values)
print('')

# get exposures scores for date range 2010-01-10 to 2010-10-20 for pm25 at latitude=34.15581748, longitude=-77.99258944
exp_scores = client.cmaq.get_cmaq_getScores(
    exposureType='pm25',
    startDate=sdate,
    endDate=edate,
    latLon=lat + ',' + lon
).result()
print('### client.cmaq.get_cmaq_getScores ... ###')
pprint(exp_scores)

