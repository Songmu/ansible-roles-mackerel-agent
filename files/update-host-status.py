#!/usr/bin/env python
import sys
import simplejson as json
import httplib

api_key = sys.argv[1]
host_id = open('/var/lib/mackerel-agent/id', 'r').readline().rstrip('rn')

con = httplib.HTTPSConnection('mackerel.io')
headers = {
  'Content-Type': 'application/json',
  'X-Api-Key': api_key,
}
con.request('GET', '/api/v0/hosts/' + host_id, '', headers)
res = con.getresponse()
if res.status != 200:
  sys.exit(1)

data = json.loads(res.read())
current_status = data['host']['status']

working_status = 'working'
if current_status == working_status:
  sys.exit(0)

con.request('POST', '/api/v0/hosts/' + host_id + '/status', json.dumps({'status':working_status}), headers)
res = con.getresponse()
if res.status != 200:
  sys.exit(1)

data = json.loads(res.read())
if data['success']:
  sys.exit(11)

sys.exit(1)
