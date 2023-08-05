import click
import yo_client
from requests.exceptions import HTTPError

from src.data import get_account_details
from src.messages import USER_ERROR_MESSAGE, generate_successful_sent_yo, generate_unknown_error_message, \
    API_KEY_NOT_SET_MESSAGE, USERNAME_EXISTS_MESSAGE, USERNAME_DOES_NOT_EXIST_MESSAGE, \
    SUCCESSFULLY_UPDATED_API_KEY_MESSAGE, SUCCESSFULLY_UPDATED_USERNAME_MESSAGE


@click.group()
def yo():
    pass


@click.command()
@click.option('--username', type=click.STRING, prompt='Your username, please')
def set_username(username):
    try:
        details = get_account_details()
        details.username = username
        details.update_username()
        print(SUCCESSFULLY_UPDATED_USERNAME_MESSAGE)
    except BaseException as e:
        print(generate_unknown_error_message(e))


@click.command()
@click.option('--api_key', type=click.STRING, prompt='Your api key, please', hide_input=True)
def set_api_key(api_key):
    try:
        details = get_account_details()
        details.api_key = api_key
        details.update_api_key()
        print(SUCCESSFULLY_UPDATED_API_KEY_MESSAGE)
    except BaseException as e:
        print(generate_unknown_error_message(e))


@click.command()
@click.option('--to', type=click.STRING, prompt='Send to whom?')
@click.option('--message', type=click.STRING, prompt='What is your message?')
@click.option('--link', type=click.STRING)
def send(to, message, link):
    details = get_account_details()
    if details.api_key:
        client = yo_client.YoClient(details.api_key)
        try:
            response = client.send_yo(username=to, text=message, link=link)
            print(generate_successful_sent_yo(yo_id=response['yo_id'], recipient=response['recipient']['username']))
        except HTTPError:
            print(USER_ERROR_MESSAGE)
        except BaseException as e:
            print(generate_unknown_error_message(e))
    else:
        print(API_KEY_NOT_SET_MESSAGE)


@click.command()
@click.option('--username', type=click.STRING, prompt='Check the existence of which username?')
def username_exists(username):
    details = get_account_details()
    if details.api_key:
        client = yo_client.YoClient(details.api_key)
        try:
            response = client.username_exists(username)
            print(USERNAME_EXISTS_MESSAGE) if response['exists'] else print(USERNAME_DOES_NOT_EXIST_MESSAGE)
        except HTTPError:
            print(USER_ERROR_MESSAGE)
        except BaseException as e:
            print(generate_unknown_error_message(e))
    else:
        print(API_KEY_NOT_SET_MESSAGE)

yo.add_command(set_username)
yo.add_command(set_api_key)
yo.add_command(send)
yo.add_command(username_exists)
