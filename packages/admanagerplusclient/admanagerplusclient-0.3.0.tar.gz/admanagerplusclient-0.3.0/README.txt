# admanagerplustclient
A python API client for Yahoo's Ad Manager Plus (formerly Brightroll Ad DSP)

# example for 1st time use

from admanagerplusclient import ampclient

brc = ampclient.BrightRollClient()

brc.cli_auth_dance()

brc.traffic_types('advertisers')

# example for ETC or nightly job server
from admanagerplusclient import ampclient

brc = ampclient.BrightRollClient()

brc.refresh_access_token()

brc.traffic_types('advertisers')

# available methods

# brc.traffic_types(traffic_type_object)

brc.traffic_types('advertisers')
brc.traffic_types('advertisers?page={page}&limit={limit}&sort={sort}&dir={dir}&query={query}')

Traffic_type_object can be:
* advertisers
* campaigns
* deals
* lines
* "dictionary"
* exchanges
* contextuals
* sitelists
* beacons (pixels)
* audiences (SRT & MRT)
* usergroups
* dictionary

brc.traffic_type_by_id(traffic_type_object, object_id)

brc.dictionary(targetingTypes)
