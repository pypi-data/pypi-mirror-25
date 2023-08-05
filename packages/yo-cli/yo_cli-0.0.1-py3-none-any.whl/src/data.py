import json
import os

ACCOUNT_DETAILS_FILE_NAME = '.account_details.json'


class AccountDetails:
    def __init__(self, username, api_key):
        self.username = username
        self.api_key = api_key

    def update_username(self):
        update_username(self.username)

    def update_api_key(self):
        update_api_key(self.api_key)


def get_account_details_filename():
    directory = os.path.dirname(os.path.realpath('__file__'))
    return os.path.join(directory, '{ACCOUNT_DETAILS_FILE_NAME}'
                        .format(ACCOUNT_DETAILS_FILE_NAME=ACCOUNT_DETAILS_FILE_NAME))


def update_value(key, value):
    with open(get_account_details_filename()) as file:
        account_details = json.load(file)

    with open(get_account_details_filename(), 'w') as file:
        account_details[key] = value
        json.dump(account_details, file)


def update_username(value):
    update_value('username', value)


def update_api_key(value):
    update_value('api_key', value)


def get_account_details():
    filename = get_account_details_filename()

    if not os.path.isfile(filename) or os.path.getsize(filename) == 0:
        with open(filename, 'w') as file:
            json.dump({'username': None, 'api_key': None}, file)

    with open(filename) as file:
        account_details = json.load(file)

    return AccountDetails(username=account_details['username'], api_key=account_details['api_key'])
