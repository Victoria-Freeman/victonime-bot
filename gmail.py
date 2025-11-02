import base64
import os
from time import sleep
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from bs4 import BeautifulSoup

SCOPES = ['https://mail.google.com/']

def authenticate():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds
def get_email_html(service, msg_id):
    msg = service.users().messages().get(userId='me', id=msg_id, format='full').execute()

    def find_html(payload):
        if payload.get('mimeType') == 'text/html' and payload.get('body', {}).get('data'):
            return base64.urlsafe_b64decode(payload['body']['data']).decode('utf-8', errors='ignore')
        for part in payload.get('parts', []):
            html = find_html(part)
            if html:
                return html
        return None

    return find_html(msg['payload']) or ""

def get_email(email, subject):
    creds = authenticate()
    service = build('gmail', 'v1', credentials=creds)

    msgs = service.users().messages().list(userId='me', q=f'to:{email} subject:"{subject}"').execute().get('messages', [])
    if not msgs: return

    html = get_email_html(service, msgs[0]['id'])
    return BeautifulSoup(html, 'html.parser')

def getCouchdropCode(email):
    while True:
        soup = get_email(email, "Couchdrop - Confirm your email")
        if not soup:
            sleep(1)
            continue
        code = soup.find("a").get_text()
        return code


def getWasabiConfirmationLink(email):
    while True:
        soup = get_email(email, "Welcome to Wasabi Hot Cloud Storage")
        if not soup: 
            sleep(1)
            continue
        link = soup.find_all("a")[1]["href"]
        return link
    