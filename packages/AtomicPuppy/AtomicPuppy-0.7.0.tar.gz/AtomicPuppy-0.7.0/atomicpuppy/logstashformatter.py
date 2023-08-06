# Copyright (c) 2012 Exoscale SA

# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:

# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

'''
This library is provided to allow standard python
logging to output log data as JSON formatted strings
ready to be shipped out to logstash.
'''

import logging
import socket
import datetime
import traceback as tb
import json


def _default_json_default(obj):
    """
    Coerce everything to strings.
    All objects representing time get output as ISO8601.
    """
    if isinstance(obj, (datetime.datetime, datetime.date, datetime.time)):
        return obj.isoformat()
    else:
        return str(obj)


def build_fields(defaults, fields):
    """Return provided fields including any in defaults

    >>> f = LogstashFormatter()
    # Verify that ``fields`` is used
    >>> f._build_fields({}, {'foo': 'one'}) == \
            {'foo': 'one'}
    True
    # Verify that ``@fields`` in ``defaults`` is used
    >>> f._build_fields({'@fields': {'bar': 'two'}}, {'foo': 'one'}) == \
            {'foo': 'one', 'bar': 'two'}
    True
    # Verify that ``fields`` takes precedence
    >>> f._build_fields({'@fields': {'foo': 'two'}}, {'foo': 'one'}) == \
            {'foo': 'one'}
    True
    """
    return dict(list(defaults.get('@fields', {}).items()) + list(fields.items()))


class LogstashFormatter(logging.Formatter):
    """
    A custom formatter to prepare logs to be
    shipped out to logstash.
    """

    def __init__(self,
                 fmt=None,
                 datefmt=None,
                 json_cls=None,
                 json_default=_default_json_default,
                 map_fields=build_fields,
    ):
        """
        :param fmt: Config as a JSON string, allowed fields;
               extra: provide extra fields always present in logs
               source_host: override source host name
        :param datefmt: Date format to use (required by logging.Formatter
            interface but not used)
        :param json_cls: JSON encoder to forward to json.dumps
        :param json_default: Default JSON representation for unknown types,
                             by default coerce everything to a string
        """

        if fmt is not None:
            self._fmt = json.loads(fmt)
        else:
            self._fmt = {}
        self.json_default = json_default
        self.json_cls = json_cls
        if 'extra' not in self._fmt:
            self.defaults = {}
        else:
            self.defaults = self._fmt['extra']
        if 'source_host' in self._fmt:
            self.source_host = self._fmt['source_host']
        else:
            try:
                self.source_host = socket.gethostname()
            except:
                self.source_host = ""
        self._map_fields = map_fields

    def format(self, record):
        """
        Format a log record to JSON, if the message is a dict
        assume an empty message and use the dict as additional
        fields.
        """

        fields = record.__dict__.copy()

        msg = record.getMessage()

        if 'msg' in fields:
            fields.pop('msg')

        if 'exc_info' in fields:
            if fields['exc_info']:
                formatted = tb.format_exception(*fields['exc_info'])
                fields['exception'] = formatted
            fields.pop('exc_info')

        if 'exc_text' in fields and not fields['exc_text']:
            fields.pop('exc_text')

        logr = self.defaults.copy()

        stamp = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        logr.update(
            {'@message': msg,
             '@timestamp': stamp,
             '@source_host': self.source_host,
             '@fields': self._map_fields(logr, fields)}
        )

        return json.dumps(logr, default=self.json_default, cls=self.json_cls)


def logstash_formatter_with_mapped_error_levels(*args, **kwargs):
    # import lib.loglevels  # has a side effect
    return LogstashFormatter(
        *args,
        # map_fields=lib.loglevels.map_error_levels,
        **kwargs
    )
