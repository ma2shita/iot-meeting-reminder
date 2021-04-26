from __future__ import print_function
import datetime
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


def get_credentials():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            
            creds = flow.run_console()
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

def getEvent():
    creds = get_credentials()
    # http = credentials.authorize(httplib2.Http())
    # service = discovery.build('calendar', 'v3', http=http)
    service = build('calendar', 'v3', credentials=creds)

    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    # print('Getting the upcoming 10 events')
    eventsResult = service.events().list(
        calendarId='primary', timeMin=now, maxResults=2, singleEvents=True,
        orderBy='startTime').execute()
    events = eventsResult.get('items', [])

    if not events:
        print('予定が登録されていません')
        return {'time': datetime.datetime.now(pytz.timezone('Asia/Tokyo')), 'event': 'No Event', 'nextTime': datetime.datetime.now(pytz.timezone('Asia/Tokyo')), 'nextEvent': 'No Event'}
    else:
        event = events[0]
        time = event['start'].get('dateTime', event['start'].get('date'))
        dt = datetime.datetime.fromisoformat(time)
        if(len(events) == 2):
            nextEvent = events[1]
            nextTime = nextEvent['start'].get('dateTime', nextEvent['start'].get('date'))
            nextdt = datetime.datetime.fromisoformat(nextTime)
            print('最新の予定: {} {}\n次の予定: {}{}'.format(dt, event['summary'], nextdt, nextEvent['summary']))
            return {'time': dt, 'event': event['summary'], 'nextTime': nextdt, 'nextEvent': nextEvent['summary']}
        else:
            print('最新の予定: {} {}\n次の予定: {}{}'.format(dt, event['summary'], '', 'なし'))
            return {'time': dt, 'event': event['summary'], 'nextTime': dt, 'nextEvent': 'No Event'}

if __name__ == '__main__':
    getEvent()