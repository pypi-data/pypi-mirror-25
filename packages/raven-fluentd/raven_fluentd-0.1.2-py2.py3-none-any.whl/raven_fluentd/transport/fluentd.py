from fluent import sender

from raven.transport.base import Transport

import base64
from six.moves.urllib import parse


class FluentdTransport(Transport):
    scheme = ['fluentd']

    def __init__(self, *args, **kwargs):
        super(FluentdTransport, self).__init__(*args, **kwargs)

    def send(self, url, data, headers):
        u = parse.urlparse(url)
        project_id = int(u.path.split('/')[2])
        payload = {
            'data': base64.b64encode(data),
            'auth_header': headers['X-Sentry-Auth'],
            'project_id': project_id,
            'options': {'content_type': 'application/octet-stream'}}

        logger = sender.FluentSender('sentry', host=u.hostname, port=u.port)
        logger.emit('error', payload)
