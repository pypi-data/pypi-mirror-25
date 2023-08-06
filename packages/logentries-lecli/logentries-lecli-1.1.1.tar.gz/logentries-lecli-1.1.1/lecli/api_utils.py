"""
Configuration and api keys util module.
"""
import sys
import ConfigParser
import base64
import hashlib
import hmac
import os
import json

import datetime

import click
import validators
from appdirs import user_config_dir

import lecli

AUTH_SECTION = 'Auth'
URL_SECTION = 'Url'
LOGGROUPS_SECTION = 'LogGroups'
CLI_FAVORITES_SECTION = 'Cli_Favorites'
CONFIG = ConfigParser.ConfigParser()
CONFIG_FILE_PATH = os.path.join(user_config_dir(lecli.__name__), 'config.ini')
DEFAULT_API_URL = 'https://rest.logentries.com'


def print_config_error_and_exit(section=None, config_key=None, value=None):
    """
    Print appropriate apiutils error message and exit.
    """
    if not section:
        click.echo("Error: Configuration file '%s' not found" % CONFIG_FILE_PATH, err=True)
    elif not config_key:
        click.echo("Error: Section '%s' was not found in configuration file(%s)" %
                   (section, CONFIG_FILE_PATH), err=True)
    elif not value:
        click.echo("Error: Configuration key for %s was not found in configuration file(%s) in "
                   "'%s' section" % (config_key, CONFIG_FILE_PATH, section), err=True)
    else:
        click.echo("Error: %s = '%s' is not in section: '%s' of your configuration file: '%s'" %
                   (config_key, value, section, CONFIG_FILE_PATH), err=True)

    sys.exit(1)


def init_config():
    """
    Initialize config file in the OS specific config path if there is no config file exists.
    """
    config_dir = user_config_dir(lecli.__name__)

    if not os.path.exists(CONFIG_FILE_PATH):
        if not os.path.exists(config_dir):
            os.makedirs(config_dir)

        dummy_config = ConfigParser.ConfigParser()
        config_file = open(CONFIG_FILE_PATH, 'w')
        dummy_config.add_section(AUTH_SECTION)
        dummy_config.set(AUTH_SECTION, 'account_resource_id', '')
        dummy_config.set(AUTH_SECTION, 'owner_api_key_id', '')
        dummy_config.set(AUTH_SECTION, 'owner_api_key', '')
        dummy_config.set(AUTH_SECTION, 'rw_api_key', '')
        dummy_config.set(AUTH_SECTION, 'ro_api_key', '')

        dummy_config.add_section(CLI_FAVORITES_SECTION)
        dummy_config.add_section(URL_SECTION)
        dummy_config.set(URL_SECTION, 'api_url', 'https://rest.logentries.com')

        dummy_config.write(config_file)
        config_file.close()
        click.echo("An empty config file created in path %s, please check and configure it. To "
                   "learn how to get necessary api keys, go to this Logentries documentation "
                   "page: https://docs.logentries.com/docs/api-keys" % CONFIG_FILE_PATH)
    else:
        click.echo("Config file exists in the path: " + CONFIG_FILE_PATH, err=True)

    sys.exit(1)


def load_config():
    """
    Load config from OS specific config path into ConfigParser object.
    :return:
    """
    files_read = CONFIG.read(CONFIG_FILE_PATH)
    if len(files_read) != 1:
        click.echo("Error: Config file '%s' not found, generating one..." % CONFIG_FILE_PATH,
                   err=True)
        init_config()
        print_config_error_and_exit()
    if not CONFIG.has_section(AUTH_SECTION):
        print_config_error_and_exit(section=AUTH_SECTION)
    if CONFIG.has_section(LOGGROUPS_SECTION):
        replace_loggroup_section()


def replace_loggroup_section():
    """
    If config has legacy LogGroup section, take all its items and add
    them to the CLI_Favorites section - then delete the legacy section.
    Update the config file with the changes.
    """
    existing_groups = CONFIG.items(LOGGROUPS_SECTION)
    if not CONFIG.has_section(CLI_FAVORITES_SECTION):
        CONFIG.add_section(CLI_FAVORITES_SECTION)
    for group in existing_groups:
        CONFIG.set(CLI_FAVORITES_SECTION, group[0], group[1])
    CONFIG.remove_section(LOGGROUPS_SECTION)
    config_file = open(CONFIG_FILE_PATH, 'w')
    CONFIG.write(config_file)
    config_file.close()


def get_ro_apikey():
    """
    Get read-only api key from the config file.
    """

    config_key = 'ro_api_key'
    try:
        ro_api_key = CONFIG.get(AUTH_SECTION, config_key)
        if not validators.uuid(ro_api_key):
            return get_rw_apikey()
        else:
            return ro_api_key
    except ConfigParser.NoOptionError:
        # because read-write api key is a superset of read-only api key
        return get_rw_apikey()


def get_rw_apikey():
    """
    Get read-write api key from the config file.
    """

    config_key = 'rw_api_key'
    try:
        rw_api_key = CONFIG.get(AUTH_SECTION, config_key)
        if not validators.uuid(rw_api_key):
            print_config_error_and_exit(AUTH_SECTION, 'Read/Write API key(%s)' % config_key,
                                        rw_api_key)
        else:
            return rw_api_key
    except ConfigParser.NoOptionError:
        print_config_error_and_exit(AUTH_SECTION, 'Read/Write API key(%s)' % config_key)


def get_owner_apikey():
    """
    Get owner api key from the config file.
    """

    config_key = 'owner_api_key'
    try:
        owner_api_key = CONFIG.get(AUTH_SECTION, config_key)
        if not validators.uuid(owner_api_key):
            print_config_error_and_exit(AUTH_SECTION, 'Owner API key(%s)' % config_key,
                                        owner_api_key)
            return
        else:
            return owner_api_key
    except ConfigParser.NoOptionError:
        print_config_error_and_exit(AUTH_SECTION, 'Owner API key(%s)' % config_key)


def get_owner_apikey_id():
    """
    Get owner api key id from the config file.
    """

    config_key = 'owner_api_key_id'
    try:
        owner_apikey_id = CONFIG.get(AUTH_SECTION, config_key)
        if not validators.uuid(owner_apikey_id):
            print_config_error_and_exit(AUTH_SECTION, 'Owner API key ID(%s)' % config_key,
                                        owner_apikey_id)
            return
        else:
            return owner_apikey_id
    except ConfigParser.NoOptionError:
        print_config_error_and_exit(AUTH_SECTION, 'Owner API key ID(%s)' % config_key)


def get_account_resource_id():
    """
    Get account resource id from the config file.
    """

    config_key = 'account_resource_id'
    try:
        account_resource_id = CONFIG.get(AUTH_SECTION, config_key)
        if not validators.uuid(account_resource_id):
            print_config_error_and_exit(AUTH_SECTION, 'Account Resource ID(%s)' % config_key,
                                        account_resource_id)
            return
        else:
            return account_resource_id
    except ConfigParser.NoOptionError:
        print_config_error_and_exit(AUTH_SECTION, 'Account Resource ID(%s)' % config_key)


def get_named_logkey_group(name):
    """
    Get named log-key list from the config file.

    :param name: name of the log key list
    """

    section = CLI_FAVORITES_SECTION
    try:
        groups = dict(CONFIG.items(section))
        name = name.lower()
        if name in groups:
            logkeys = [line for line in str(groups[name]).splitlines() if line is not None]
            for logkey in logkeys:
                if not validators.uuid(logkey):
                    print_config_error_and_exit(section, 'Named Logkey Group(%s)' % name, logkey)
            return logkeys
        else:
            print_config_error_and_exit(section, 'Named Logkey Group(%s)' % name)
    except ConfigParser.NoSectionError:
        print_config_error_and_exit(section)


def generate_headers(api_key_type, method=None, action=None, body=None):
    """
    Generate request headers according to api_key_type that is being used.
    """
    headers = None

    if api_key_type is 'ro':
        headers = {
            'x-api-key': get_ro_apikey(),
            "Content-Type": "application/json"
        }
    elif api_key_type is 'rw':
        headers = {
            'x-api-key': get_rw_apikey(),
            "Content-Type": "application/json"
        }
    elif api_key_type is 'owner':  # Uses the owner-api-key
        date_h = datetime.datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")
        content_type_h = "application/json"
        signature = gensignature(get_owner_apikey(), date_h, content_type_h, method, action, body)
        headers = {
            "Date": date_h,
            "Content-Type": content_type_h,
            "authorization-api-key": "%s:%s" % (
                get_owner_apikey_id().encode('utf8'), base64.b64encode(signature))
        }

    headers['User-Agent'] = 'lecli'

    return headers


def gensignature(api_key, date, content_type, request_method, query_path, request_body):
    """
    Generate owner access signature.

    """
    hashed_body = base64.b64encode(hashlib.sha256(request_body).digest())
    canonical_string = request_method + content_type + date + query_path + hashed_body

    # Create a new hmac digester with the api key as the signing key and sha1 as the algorithm
    digest = hmac.new(api_key, digestmod=hashlib.sha1)
    digest.update(canonical_string)

    return digest.digest()


def get_api_url():
    """
    Get management url from the config file
    """
    config_key = 'api_url'
    try:
        url = CONFIG.get(URL_SECTION, config_key)
        if validators.url(str(url)):
            return url
        else:
            print_config_error_and_exit(URL_SECTION, 'REST API URL(%s)' % config_key)
    except (ConfigParser.NoOptionError, ConfigParser.NoSectionError):
        return DEFAULT_API_URL


def build_url(nodes):
    """
    Build a url with the given array of nodes for the url and return path and url respectively
    Ordering is important
    """
    path = str.join('/', nodes)
    url = str.join('/', [get_api_url(), path])
    return path, url


def pretty_print_string_as_json(text):
    """
    Pretty prints a json string
    """
    print json.dumps(json.loads(text), indent=4, sort_keys=True)


def combine_objects(left, right):
    """
    Merge two objects
    """
    if isinstance(left, dict) and isinstance(right, dict):
        result = {}
        for key, value in left.iteritems():
            if key not in right:
                result[key] = value
            else:
                result[key] = combine_objects(value, right[key])
        for key, value in right.iteritems():
            if key not in left:
                result[key] = value
        return result
    if isinstance(left, list) and isinstance(right, list):
        return left + right
    return right
