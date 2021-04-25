from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import datetime

import pytz


try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/calendar-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Calendar API Python Quickstart'


def get_credentials():
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'calendar-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def getEvent():
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    # print('Getting the upcoming 10 events')
    eventsResult = service.events().list(

        calendarId='primary', timeMin=now, maxResults=2, singleEvents=True,
        orderBy='startTime').execute()
    events = eventsResult.get('items', [])

    if not events:
        # return {'time': datetime.datetime.now(pytz.timezone('Asia/Tokyo')) + datetime.timedelta(hours=3), 'event': 'No Event', 'nextTime': None, 'nextEvent': 'No Event'} # 直近の予定がない場合、3時間後にまたデータを取りに行く
        # return {'time': datetime.datetime.now(pytz.timezone('Asia/Tokyo')) + datetime.timedelta(hours=3), 'event': 'No Event', 'nextTime': datetime.datetime.now(pytz.timezone('Asia/Tokyo')) + datetime.timedelta(hours=3), 'nextEvent': 'No Event'} # 直近の予定がない場合、3時間後にまたデータを取りに行く
        return {'time': datetime.datetime.now(pytz.timezone('Asia/Tokyo')), 'event': 'No Event', 'nextTime': datetime.datetime.now(pytz.timezone('Asia/Tokyo')), 'nextEvent': 'No Event'}
    else:
        event = events[0]
        time = event['start'].get('dateTime', event['start'].get('date'))
        dt = datetime.datetime.fromisoformat(time)
        if(len(events) == 2):
            nextEvent = events[1]
            nextTime = nextEvent['start'].get('dateTime', nextEvent['start'].get('date'))
            nextdt = datetime.datetime.fromisoformat(nextTime)
            return {'time': dt, 'event': event['summary'], 'nextTime': nextdt, 'nextEvent': nextEvent['summary']}
        else:
            return {'time': dt, 'event': event['summary'], 'nextTime': dt, 'nextEvent': 'No Event'}
