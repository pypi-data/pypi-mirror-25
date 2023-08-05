#!/usr/local/opt/python/bin/python2.7
import httplib, urllib
import json
import sys
from pprint import pprint

with open('pulsar.json', 'r') as jsonData:
    cfg = json.load(jsonData)

pulsarUrl = cfg['pulsar']['host']
iamUrl = cfg['iam']['host']

def getToken() :
    headers = {'Content-type': 'application/x-www-form-urlencoded', 'Accept': 'application/json'}
    data = 'grant_type=urn:ibm:params:oauth:grant-type:apikey&response_type=cloud_iam&apikey=' + cfg['iam']['apikey']

    conn = httplib.HTTPSConnection(iamUrl)
    conn.request('POST', '/oidc/token', data, headers)

    response = conn.getresponse()
    print ('token service response status code %s' % (response.status))
    if response.status == 200 :
        body = json.loads(response.read().decode())
        token = body['token_type'] + ' ' + body['access_token']
        print token
        return token
    else :
        sys.exit(2);

def pulsarReq ( token, action, body, endpoint ):
    print pulsarUrl, endpoint
    conn = httplib.HTTPConnection(pulsarUrl)
    headers = {'Content-Type': 'application/json', 'Authorization': token}
    conn.request(action, endpoint, body, headers)

    res = conn.getresponse()
    print ('pulsar response status code %s' % (res.status))
    if res.status == 200 :
        return res.read().decode()
    else :
        print ('pulsarUrl %s %s failed in %s' % (pulsarUrl, endpoint, action))
        sys.exit(3);

def allTopics () :
    topics = []
    for topic in json.loads(pulsarReq( getToken(), 'GET', '', '/v2/topics')) :
        topics.append(topic['topic'].encode("utf-8"))
    return topics

def list () :
    return pulsarReq(getToken(), 'GET', '', 'v2/subscriptions')

def addWh () :
    subscriptionsBody = json.dumps(cfg['pulsar']['subscriptions']['body'])
    pulsarReq(getToken(), 'POST', subscriptionsBody, 'v2/subscriptions')
    return

def deleteWh (webhookurl) :
    pulsarReq(getToken(), 'DELETE', '', 'v2/subscriptions/' + urllib.quote_plus(webhookurl))
    return

def usage () :
    print 'CLI to manage Pulsar webhook subscription.'
    print '--all all subscription under the current service Id'
    print '-l, --list List all Pular topics available for subscription'
    print '-a, --add <web hook registration body> Add web hook with Pulsar'
    print '-d, --delete <web hook url> Delete web hook url with Pulsar'

if len(sys.argv) < 2 :
    usage()
elif sys.argv[1] == '--all':
    tps = allTopics()
    print 'all available topics are:'
    pprint(tps)
elif sys.argv[1] == '-l' or sys.argv[1] == '--list':
    print(json.dumps(json.loads(list()), indent=2))
elif sys.argv[1] == '-a' or sys.argv[1] == '--add':
    addWh()
elif sys.argv[1] == '-d' or sys.argv[1] == '--delete':
    if len(sys.argv) > 2 :
        deleteWh(sys.argv[2])
    else :
        whUrl = cfg['pulsar']['subscriptions']['body']['webhook']
        print('delete url %s' % (whUrl))
        deleteWh(whUrl)
else :
    usage()
