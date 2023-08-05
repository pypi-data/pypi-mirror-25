from __future__ import print_function
import os
import webbrowser

import twitter
from requests_oauthlib import OAuth1Session
from swag import swagprinter

REQUEST_TOKEN_URL = 'https://api.twitter.com/oauth/request_token'
ACCESS_TOKEN_URL = 'https://api.twitter.com/oauth/access_token'
AUTHORIZATION_URL = 'https://api.twitter.com/oauth/authorize'
SIGNIN_URL = 'https://api.twitter.com/oauth/authenticate'


def check_keys(keys):
    try:
        return [os.environ[key] for key in keys]
    except:
        return False


def check_env_creds():
    swagprinter.print_yellow("Checking if API credentials are set in the environment variables...")
    has_consumer_keys = check_keys(["consumer_key", "consumer_secret"])
    has_access_token = check_keys(["access_token_key", "access_token_secret"])

    return {"has_consumer_keys": has_consumer_keys,
            "has_access_token": has_access_token}


def get_access_token(consumer_key=None, consumer_secret=None):
    if consumer_key is None:
        consumer_key = os.environ["consumer_key"]

    if consumer_secret is None:
        consumer_secret = os.environ["consumer_secret"]

    oauth_client = OAuth1Session(consumer_key, client_secret=consumer_secret, callback_uri='oob')

    swagprinter.print_cyan('\nRequesting temp token from Twitter...\n')

    try:
        response = oauth_client.fetch_request_token(REQUEST_TOKEN_URL)
    except ValueError as e:
        raise 'Invalid response from Twitter requesting temp token: {0}'.format(e)

    url = oauth_client.authorization_url(AUTHORIZATION_URL)

    swagprinter.print_yellow('Trying to start a browser to visit the following Twitter page '
                             'if a browser will not start, copy the URL to your browser '
                             'and retrieve the pincode to be used '
                             'in the next step to obtaining an Authentication Token: \n'
                             '\n\t{0}'.format(url))

    webbrowser.open(url)
    pincode = input('\nEnter your pincode? ')

    swagprinter.print_yellow('\nGenerating and signing request for an access token...\n')

    oauth_client = OAuth1Session(consumer_key, client_secret=consumer_secret,
                                 resource_owner_key=response.get('oauth_token'),
                                 resource_owner_secret=response.get('oauth_token_secret'),
                                 verifier=pincode)
    try:
        response = oauth_client.fetch_access_token(ACCESS_TOKEN_URL)
    except ValueError as e:
        raise 'Invalid response from Twitter requesting temp token: {0}'.format(e)

    swagprinter.print_cyan('''Your tokens/keys are as follows:
        consumer_key         = {}
        consumer_secret      = {}
        access_token_key     = {}
        access_token_secret  = {}'''.format(
        consumer_key, consumer_secret,
        response.get('oauth_token'), response.get('oauth_token_secret')))

    return (response.get('oauth_token'), response.get('oauth_token_secret'))


def print_env_hint():
    swagprinter.print_purple("""You need to at least provide the consumer_key and consumer_secret !

    You can set the credentials through these environment variables:
    - consumer_key
    - consumer_secret
    - access_token_key
    - access_token_secret

    """)

    swagprinter.print_green("Or you can provide them now:")

    consumer_key = input("Enter your consumer_key:")
    consumer_secret = input("Enter your consumer_secret:")

    return (consumer_key, consumer_secret)


def get_authenticated_api(consumer_key=None, consumer_secret=None, access_token_key=None, access_token_secret=None):
    swagprinter.print_yellow("Getting the api ...")

    if consumer_secret is not None and consumer_key is not None and access_token_key is not None and access_token_secret is not None:
        return twitter.Api(consumer_key=consumer_key,
                           consumer_secret=consumer_secret,
                           access_token_key=access_token_key,
                           access_token_secret=access_token_secret)

    creds = check_env_creds()

    if not creds["has_consumer_keys"] and not creds["has_access_token"]:
        consumer_key, consumer_secret = print_env_hint()
        access_token_key, access_token_secret = get_access_token(consumer_key=consumer_key,
                                                                 consumer_secret=consumer_secret)
    elif not creds["has_access_token"]:
        access_token_key, access_token_secret = get_access_token(*creds["has_consumer_keys"])
    else:
        consumer_key, consumer_secret = print_env_hint()
        access_token_key, access_token_secret = get_access_token(consumer_key, consumer_secret)

    return twitter.Api(consumer_key=consumer_key,
                       consumer_secret=consumer_secret,
                       access_token_key=access_token_key,
                       access_token_secret=access_token_secret)
