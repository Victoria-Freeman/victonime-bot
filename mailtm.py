from time import sleep
from bs4 import BeautifulSoup
from faker import Faker
import requests
import random
import string
from typing import Tuple, Dict,  Union
import helper

class MailTM:
    # BASE_URL = "https://api.mail.tm"
    BASE_URL = "https://api.mail.gw"
    
    def __init__(self, token: str = None, proxy_dict: Dict = None):
        self.token = token
        self.proxy_dict = proxy_dict
        self.headers = {'Accept': 'application/json', 'Content-Type': 'application/json' }
        if token:
            self.headers['Authorization'] = f'Bearer {token}'

    def _make_request(self, method: str, endpoint: str, data: Dict = None) -> Union[Dict, int]:
        url = f"{self.BASE_URL}/{endpoint}"
        response = requests.request(
            method=method,
            url=url,
            json=data,
            headers=self.headers,
            proxies=self.proxy_dict
        )
        if response.status_code in [200, 201]:
            return response.json()
        elif response.status_code == 204:
            return response.json()
        return response.json()

    def create_account(self, email: str = None, password: str = None) -> Dict:
        fake = Faker()
        idk = f"{fake.first_name().lower()}{fake.last_name().lower()}{helper.generate_random_string(2)}"
        if not email:
            email = f"{idk}@teihu.com" 
        if not password:
            password = ''.join(random.choices(string.ascii_letters + string.digits + "!@#$%^&*()_+-=[]{}|;:,.<>?/", k=16))
        data = self._make_request('POST', 'accounts', {'address': email, 'password': password})
        data['password'] = password
        return data

    def create_token(self, email: str, password: str) -> str:
        response = self._make_request('POST', 'token', {'address': email, 'password': password})
        if isinstance(response, dict):
            self.token = response['token']
            self.headers['Authorization'] = f'Bearer {self.token}'
            return self.token
        return response

    def get_account_by_id(self, account_id: str) -> Union[Dict, int]:
        return self._make_request('GET', f'accounts/{account_id}')

    def delete_account(self, account_id: str) -> Tuple[bool, int]:
        response = self._make_request('DELETE', f'accounts/{account_id}')
        return response == 204, response

    def get_me(self) -> Union[Dict, int]:
        return self._make_request('GET', 'me')

    def get_email_by_token(self) -> Union[Dict, int]:
        return self._make_request('GET', 'me')
    
    def get_domains(self) -> Union[Dict, int]:
        return self._make_request('GET', 'domains')

    def get_domain_by_id(self, domain_id: str) -> Union[Dict, int]:
        return self._make_request('GET', f'domains/{domain_id}')

    def get_messages(self) -> Union[Dict, int]:
        return self._make_request('GET', 'messages')

    def get_message_by_id(self, message_id: str) -> Union[Dict, int]:
        return self._make_request('GET', f'messages/{message_id}')

    def delete_message(self, message_id: str) -> Tuple[bool, int]:
        response = self._make_request('DELETE', f'messages/{message_id}')
        return response == 204, response

    def mark_message_read(self, message_id: str, read: bool = True) -> Tuple[bool, int]:
        response = self._make_request('PATCH', f'messages/{message_id}', {'read': read})
        return isinstance(response, dict), response

    def get_message_attachment(self, message_id: str, attachment_id: str) -> Union[Dict, int]:
        return self._make_request('GET', f'messages/{message_id}/attachment/{attachment_id}')

    def download_message(self, message_id: str) -> Union[Dict, int]:
        return self._make_request('GET', f'messages/{message_id}/download')

    def get_source(self, source_id: str) -> Union[Dict, int]:
        return self._make_request('GET', f'sources/{source_id}')

def generate_mail():
    mail = MailTM()
    account = mail.create_account()
    return mail, account

def getBunnyConfirmationEmail(mail, account):
    token = mail.create_token(account['address'], account['password'])
    print(account, token)
    while True:
        messages = mail.get_messages()
        print("Messages:", messages)
        
        if messages != []:
            message_details = mail.get_message_by_id(messages[0]['id'])
            soup = BeautifulSoup(message_details['html'][0], 'html.parser')
            return soup.find_all('a')[1]['href']
        sleep(1)