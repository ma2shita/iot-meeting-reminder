# Original is https://github.com/googleworkspace/python-samples/commit/41f82a79bcd67ba4de329126a8fdcc4e3c0826ff
# Change history is after https://github.com/ma2shita/iot-meeting-reminder/commit/69828d5b2b5c0ba88262d6af2bf31d26b343c22e
# 
# NOTE:
#   The license of the original quickstart.py is Apache 2.0.
#   This file has been modified to comply with the license of this entire repository.

# [START calendar_quickstart]
from __future__ import print_function
import datetime
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import urllib.request
import json

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


def get_userdata():
  """Get userdata from SORACOM metadata service.

  Returns:
    str: Raw value in userdata.

  Examples:
    >>> get_userdata()
    b'FooBar'

  Note:
    An environment that can access the SORACOM Air metadata service is required.
    For example, there is a way to use a USB dongle + SORACOM IoT SIM.
  """
  req = urllib.request.Request("http://metadata.soracom.io/v1/userdata")
  with urllib.request.urlopen(req) as res:
    body = res.read()
  return body

def main():
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
            try:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
            except FileNotFoundError:
                print("## Get the credential from Metadata(userdata) instead of credentials.json")
                client_config = json.loads(get_userdata())
                flow = InstalledAppFlow.from_client_config(client_config, SCOPES)
            creds = flow.run_console()
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('calendar', 'v3', credentials=creds)

    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    print('Getting the upcoming 10 events')
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                        maxResults=10, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])


if __name__ == '__main__':
    main()
# [END calendar_quickstart]
