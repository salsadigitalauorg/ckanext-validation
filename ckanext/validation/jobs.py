# encoding: utf-8

import logging
import json

import ckan.lib.uploader as uploader

from goodtables import Inspector


log = logging.getLogger(__name__)


def run_validation_job(resource):

    log.debug(u'Validating resource {}'.format(resource['id']))

    source = None
    if resource.get(u'url_type') == u'upload':
        upload = uploader.get_resource_uploader(resource)
        if isinstance(upload, uploader.ResourceUpload):
            source = upload.get_path(resource[u'id'])
    if not source:
        source = resource[u'url']

    schema = resource.get(u'schema')
    if schema and isinstance(schema, basestring):
        schema = json.loads(schema)

    _format = resource[u'format'].lower()

    _validate_table(source, _format=_format, schema=schema)


def _validate_table(source, _format=u'csv', schema=None):

    inspector = Inspector()

    report = inspector.inspect(source, format=_format, schema=schema)

    log.debug(u'Source: %s' % source)

    return report