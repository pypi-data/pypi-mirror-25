from datetime import datetime
import logging
from flask import request
import urllib
from extensions import cache

log = logging.getLogger(__name__)

TIME_FORMATS = {
    'naive': "%Y-%m-%d %H:%M:%S",
    'with_timezone': "%Y-%m-%d %H:%M:%S %Z%z"
}

def print_datetime(dt, fmt=TIME_FORMATS['with_timezone']):
    """Print a datetime object with any format. See TIME_FORMATS for available
    formats.

    Args:
        dt (datetime.datetime): A datetime object (timezone aware or not)

    Returns:
        str: The datetime object representation as a string.
    """
    return dt.strftime(fmt)

def isbool(v):
    return v == 'True' or v == 'False'

def str2bool(v):
    return v == 'True'

def reprd(d):
    if not d:
        return []
    if isinstance(d, list):
        return [reprd(e) for e in d]
    data = {k: v for k, v in d.items()}
    for k, v in data.items():
        if k == 'id':
            continue
        if isinstance(v, unicode) and len(v) > 20:
            data[k] = v[:10] + '...' + v[-10:]
        if isinstance(v, datetime):
            data[k] = print_datetime(v)
    try:
        return convert(data)
    except UnicodeEncodeError:
        return data

def abort_400_if_not_belong(name, elem, group):
    """Raise APIException (404) if `elem` does not belong to `group`."""
    if not elem:
        raise APIException(400, "{} needs to be in input data".format(name.title()))
    if elem not in group:
        raise APIException(400, "{0} {1} is invalid. List of valid {2}s: {3}".format(name.title(), elem, name, group))

def convert(data):
    """Convert all unicode strings to strings in any iterable, mapping or
    basestring."""
    import collections
    if isinstance(data, basestring):
        return str(data)
    elif isinstance(data, collections.Mapping):
        return dict(map(convert, data.iteritems()))
    elif isinstance(data, collections.Iterable):
        return type(data)(map(convert, data))
    else:
        return data

def transform_html(data, headers=None):
    """Transform a string to an HTML-formatted string
    and return a Flask response.

    Args:
        data (str): A string to transform.
        headers (str, optional): The headers of the response.

    Return:
        A Flask response object.
    """
    data_html = "<br>".join(escape(data).split("\n"))
    resp = current_app.make_response(data_html)
    resp.headers.extend(headers or {})
    return resp

def get_required_args(func):
    args, varargs, varkw, defaults = inspect.getargspec(func)
    if defaults:
        args = args[:-len(defaults)]
    return args
