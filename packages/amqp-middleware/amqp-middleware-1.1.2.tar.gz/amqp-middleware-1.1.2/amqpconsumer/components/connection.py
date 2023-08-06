from ws4py.client.threadedclient import WebSocketClient as _WebSocketClient

import ssl
import logging


logging.basicConfig(level=logging.INFO,
                    filename='/opt/amqp-middleware/agent.log',
                    format='%(asctime)s [%(levelname)s] - '
                           '%(funcName)s: %(message)s')

log = logging.getLogger(__name__)


class WebSocketClient(_WebSocketClient):
    """A simple WebSocket client."""

    def __init__(self, url, token, secure=False, ca_certs=None, validate=True):
        """Initializes a WebSocket client and connects to the server.

        :param url: the address of the server.
        :param token: the token to be used for authentication with the server.
        :param ca_certs: the file of CA certificates to be used in case of SSL.
        :param validate: specifies whether a certificate is required.
        :param secure: specifies whether or not to use a secure ws.

        """
        scheme = 'ws'
        ssl_options = {}
        if secure:
            if not ca_certs:
                raise Exception('SSL is enabled, but path to ca_certs is '
                                'missing')
            scheme = 'wss'
            reqs = ssl.CERT_REQUIRED if validate else ssl.CERT_NONE
            ssl_options = {
                'ca_certs': ca_certs,
                'cert_reqs': reqs
            }

        super(WebSocketClient, self).__init__(
            '%s://%s/insights/socket/' % (scheme, url),
            headers=[('Authorization', token)], ssl_options=ssl_options
        )

        self.connect()

    def opened(self):
        """Invoked when a new WebSocket is opened."""
        log.info('Connection OPEN')

    def closed(self, code, reason):
        """Invoked when the WebSocket is closed."""
        log.warning('Connection CLOSED with code %s: %s', code, reason)

    def write_message(self, data):
        """Sends the given payload out."""
        self.send(data)
