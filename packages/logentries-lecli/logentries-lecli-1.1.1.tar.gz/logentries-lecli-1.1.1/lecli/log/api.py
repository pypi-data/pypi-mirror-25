"""
Log API module.
"""
import sys
import requests

from lecli import api_utils
from lecli import response_utils


def _url(provided_parts=('logs',)):
    """
    Get rest query url of log resource id
    """
    ordered_path_parts = ['management']
    ordered_path_parts.extend(provided_parts)
    return api_utils.build_url(ordered_path_parts)


def handle_get_log_response(response):
    """
    Handle get log response
    """
    if response_utils.response_error(response):
        sys.exit(1)
    elif response.status_code == 200:
        api_utils.pretty_print_string_as_json(response.text)


def get_logs():
    """
    Get logs associated with the user
    """
    headers = api_utils.generate_headers('ro')
    try:
        response = requests.get(_url()[1], headers=headers)
        handle_get_log_response(response)
    except requests.exceptions.RequestException as error:
        sys.stderr.write(error)
        sys.exit(1)


def get_log(log_id):
    """
    Get a specific log
    """
    headers = api_utils.generate_headers('ro')
    try:
        response = requests.get(_url(('logs', log_id))[1], headers=headers)
        handle_get_log_response(response)
    except requests.exceptions.RequestException as error:
        sys.stderr.write(error)
        sys.exit(1)


def create_log(logname, params):
    """Add a new log to the current account.
    If a JSON object is given, use that as the request parameters.
    Otherwise, use the name provided
    """
    if params is not None:
        request_params = params
    else:
        request_params = {
            'log': {
                'name': logname
            }
        }

    headers = api_utils.generate_headers('rw')

    try:
        response = requests.post(_url()[1], json=request_params, headers=headers)
        if response_utils.response_error(response):
            sys.stderr.write('Create log failed, status code: %d' % response.status_code)
            sys.exit(1)
        elif response.status_code == 201:
            api_utils.pretty_print_string_as_json(response.text)
    except requests.exceptions.RequestException as error:
        sys.stderr.write(error)
        sys.exit(1)


def delete_log(log_id):
    """
    Delete a log with the provided log ID
    """
    headers = api_utils.generate_headers('rw')

    try:
        response = requests.delete(_url(('logs', log_id))[1], headers=headers)
        if response_utils.response_error(response):
            sys.stderr.write('Delete log failed.')
            sys.exit(1)
        elif response.status_code == 204:
            sys.stdout.write('Deleted log with id: %s \n' % log_id)
    except requests.exceptions.RequestException as error:
        sys.stderr.write(error)
        sys.exit(1)


def replace_log(log_id, params):
    """
    Replace the given log with the details provided
    """
    headers = api_utils.generate_headers('rw')

    try:
        response = requests.put(_url(('logs', log_id))[1], json=params, headers=headers)
        if response_utils.response_error(response):
            sys.stderr.write('Update log failed.\n')
            sys.exit(1)
        elif response.status_code == 200:
            sys.stdout.write('Log: %s updated to:\n' % log_id)
            api_utils.pretty_print_string_as_json(response.text)
    except requests.exceptions.RequestException as error:
        sys.stderr.write(error)
        sys.exit(1)


def rename_log(log_id, log_name):
    """
    Rename the given log with the provided name
    """
    headers = api_utils.generate_headers('ro')

    try:
        response = requests.get(_url(('logs', log_id))[1], headers=headers)
        if response_utils.response_error(response):
            sys.stderr.write('Rename log failed.\n')
            sys.exit(1)
        elif response.status_code == 200:
            params = response.json()
            params['log']['name'] = log_name
            replace_log(log_id, params)
    except requests.exceptions.RequestException as error:
        sys.stderr.write(error)
        sys.exit(1)


def check_logset_exists(params):
    """
    Check if a logset exists
    """
    if 'logsets_info' in params:
        if 'log' in params:
            updates = params['log']['logsets_info']
        else:
            updates = params['logsets_info']

        for item in updates:
            if item['id']:
                url = _url(('logsets', item['id']))[1]
                headers = api_utils.generate_headers('ro')
                try:
                    response = requests.get(url, headers=headers)
                    if response.status_code is not 200:
                        return False
                except requests.exceptions.RequestException as error:
                    sys.stderr.write(error)
                    sys.exit(1)
    return True


def update_log(log_id, params):
    """
    Update a log with the details provided
    """
    url = _url(('logs', log_id))[1]
    headers = api_utils.generate_headers('ro')

    if check_logset_exists(params):
        try:
            response = requests.get(url, headers=headers)
            existing_log = response.json()
            replace_log(log_id, api_utils.combine_objects(existing_log, params))
        except requests.exceptions.RequestException as error:
            sys.stderr.write(error)
            sys.exit(1)
    else:
        sys.stderr.write("One or more of the specified logsets does not exist.\n")
