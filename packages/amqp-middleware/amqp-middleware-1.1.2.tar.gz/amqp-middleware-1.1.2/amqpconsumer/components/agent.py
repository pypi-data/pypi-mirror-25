import os
import ssl
import pika
import json
import time
import logging

from amqpconsumer.components.manager import CloudifyClient
from amqpconsumer.components.connection import WebSocketClient


logging.getLogger('requests').setLevel(logging.WARNING)
logging.basicConfig(level=logging.INFO,
                    filename='/opt/amqp-middleware/agent.log',
                    format='%(asctime)s [%(levelname)s] - '
                           '%(funcName)s: %(message)s')

log = logging.getLogger(__name__)


class AMQPConsumer(object):
    """An AMQP Middleware able to consume data from RabbitMQ and publish data
    to the desired destination endpoint through a WebSocket.
    """

    def __init__(self, host, port, credentials, data_processor,
                 exchange='', exchange_type='topic', routing_key='*'):
        """Initialize the AMQP Middleware by subscribing to the specified
        RabbitMQ exchange.

        :param host: the IP address of the RabbitMQ server.
        :param port: the port the RMQ server is listening at.
        :param credentials: credentials required to establish the connection.
        :param data_processor: invoked by the AMQPConsumer's callback method
         upon a receiving a new message.
        :param exchange: the RMQ exchange to subscribe to.
        :param exchange_type: the type of the RMQ exchange.
        :param routing_key: the routing key to be used.

        """
        self.process_data = data_processor

        connection_params = {'host': host, 'port': int(port)}
        connection_params = self.update_params(connection_params, credentials)

        # The `pika.adapters.blocking_connection.BlockingConnection` does not
        # respect the `connection_attempts` parameter.
        # See: pika.readthedocs.io/en/latest/examples/using_urlparameters.html
        retry_attempts = connection_params.pop('connection_attempts')
        retry_delay = connection_params.pop('retry_delay')

        # Wrap in a try/except statement to ensure compatibility with older
        # pika versions, which ignore certain connection parameters.
        # See: https://github.com/pika/pika/issues/354
        for _ in xrange(retry_attempts):
            try:
                self.connection = pika.BlockingConnection(
                    pika.ConnectionParameters(**connection_params)
                )
            except pika.exceptions.AMQPConnectionError:
                time.sleep(retry_delay)
            else:
                self.channel = self.connection.channel()
                break
        else:
            raise pika.exceptions.AMQPConnectionError()

        # Declare RMQ exchange.
        self.channel.exchange_declare(exchange=exchange,
                                      exchange_type=exchange_type,
                                      durable=False, auto_delete=True,
                                      internal=False)

        # Declare and bind queue.
        result = self.channel.queue_declare(durable=False,
                                            exclusive=False,
                                            auto_delete=True)
        queue = result.method.queue
        self.channel.queue_bind(exchange=exchange, queue=queue,
                                routing_key=routing_key)

        self.channel.basic_consume(consumer_callback=self._callback,
                                   queue=queue, no_ack=True)

    @staticmethod
    def update_params(params, creds, max_retries=3, retry_delay=1,
                      socket_timeout=2):
        """Prepares the connection parameters to be used for connecting
        to RabbitMQ.

        :param params: the initial dict of connection parameters.
        :param creds: a dict containing authentication credentials.
        :param max_retries: the number of total connection attempts.
        :param retry_delay: the delay in between connection attempts.
        :param socket_timeout: maximum socket time-out.

        :return: the updated dict of connection parameters to be used.

        """
        params['credentials'] = pika.credentials.PlainCredentials(
            creds['username'], creds['password'])

        if creds['ssl_enabled']:
            if not creds['ca_certs']:
                raise Exception('Missing path to ca_certs')
            params['ssl'] = creds['ssl_enabled']
            params['ssl_options'] = {
                'cert_reqs': ssl.CERT_REQUIRED,
                'ca_certs': creds['ca_certs']
            }

        params['connection_attempts'] = max_retries
        params['retry_delay'] = retry_delay
        params['socket_timeout'] = socket_timeout

        return params

    def start(self):
        """Start consuming data from RabbitMQ."""
        self.channel.start_consuming()

    def _callback(self, channel, method, properties, body):
        """The callback method invoked upon receiving a new message."""
        try:
            self.process_data(json.loads(body))
        except Exception as exc:
            log.error('Data processing failed: %s', exc)
            raise exc


class Publisher(WebSocketClient):
    """The publishing part of the AMQP Middleware."""

    def __init__(self, id, kwargs, max_batch_size=100, max_batch_delay=2):
        """Initializes a WebSocket-based Publisher.

        This part of the AMQP Middleware is responsible for processing new
        messages consumed by the AMQPConsumer and sending them to the
        specified  destination URL in batches.

        The AMQPConsumer directly invokes the Publisher's `process_event`
        method as its callback function. The Publiser also utilizes the
        CloudifyClient in order to query the Cloudify Manager's REST API
        regarding deployments and node instances.

        :param url: the destination URL the data will be sent to.
        :param id: a unique ID among Cloudify Manager installations.
        :param token: a token to be used for authentication on WebSocket open.
        :param secure: specifies whether data will be transmitted over SSL.
        :param ca_certs: the path to the bundle of CA certificates.
        :param validate: denotes whether certificates are required from the
         other side of the connection.
        :param max_batch_size: the size of each batch to send.
        :param max_batch_delay: the maximum period of time to wait between
         consecutive pushes of data.

        """
        super(Publisher, self).__init__(**kwargs.pop('ws'))

        self.cfy = CloudifyClient(**kwargs.pop('cfy'))

        # A UUID associated with the AMQP Middleware.
        self.mid = id

        # Declare maximum batch size/delay.
        self.batch_size = max_batch_size
        self.batch_delay = max_batch_delay

        # Initialize conditions for publishing data.
        self.current_batch = ''
        self.current_batch_size = 0
        self.last_push = time.time()

    def process_event(self, event):
        """Processes new messages received by the AMQPConsumer.

        Publishes batches of data to the desired destination.

        This method is practically the callback function of the AMQPConsumer.
        """
        if 'metric' in event:
            # Process event, before sending it out.
            self._process_event__edit_fields(event)

            # Incrementally create the batch to send out, delimited by `\n`.
            self.current_batch += json.dumps(event) + '\n'
            self.current_batch_size += 1

            # Push data via the WebSocket, if appropriate.
            if self.current_batch_size < self.batch_size and \
               time.time() < self.last_push + self.batch_delay:
                return
            self.send_data(self.current_batch)

            # Reset batch counters.
            self.current_batch = ''
            self.current_batch_size = 0
            self.last_push = time.time()

    def _process_event__edit_fields(self, event):
        """Edits the fields of a new event.

        This method is responsible for injecting into the event dict the
        corresponding cloud provider's resource ID for identification purposes.

        This method is meant to be called by `process_event`.
        """
        event['time'] = time.time()
        event['owner_id'] = str(self.mid)

        # Get the resource ID corresponding to this event.
        self.cfy.get_rid(event)

    def send_data(self, data):
        """Push data through the WebSocket."""
        log.debug('Sending batch of size %s within %s seconds',
                  self.current_batch_size, time.time() - self.last_push)
        self.write_message(json.dumps(data))


def bootstrap():
    """Initialize the AMQP Middleware.

    Main method to start the AMQP Middleware by first fetching the required
    configuration options from the systemd env file.

    NOTE: All boolean expresseions are handled as strings for compatibility
    with Cloudify Blueprints.

    """

    # Set of parameters required by the WebSocket client.
    ws_kwargs = {
        'url': os.getenv('DESTINATION_URL'),
        'token': os.getenv('TOKEN'),
        'secure': True if os.getenv('STREAM_SECURE') == 'True' else False,
        'ca_certs': os.getenv('STREAM_CA_CERTS'),
    }

    # Parameters required to communicate with Cloudify Manager's HTTP API.
    cfy_kwargs = {
        'host': os.getenv('HOST'),
        'secure': True if os.getenv('SECURE') == 'True' else False,
        'verify': True if os.getenv('VERIFY') == 'True' else False,
        'credentials': {
            'tenant': os.getenv('TENANT'),
            'username': os.getenv('USERNAME'),
            'password': os.getenv('PASSWORD'),
            'ca_certs': os.getenv('CA_CERTS'),
        },
        'ssl_enabled': True if os.getenv('SSL_ENABLED') == 'True' else False,
    }

    publisher = Publisher(
        id=os.getenv('MANAGER_ID'),
        kwargs={'ws': ws_kwargs, 'cfy': cfy_kwargs}
    )

    consumer = AMQPConsumer(
        host=os.getenv('RABBITMQ_HOST'),
        port=os.getenv('RABBITMQ_PORT'),
        credentials={
            'username': os.getenv('RABBITMQ_USERNAME'),
            'password': os.getenv('RABBITMQ_PASSWORD'),
            'ca_certs': os.getenv('RABBITMQ_CERT_PUBLIC'),
            'ssl_enabled':
                True if os.getenv('RABBITMQ_SSL_ENABLED') == 'True' else False,
        },
        exchange='cloudify-monitoring',
        exchange_type='topic', routing_key='*',
        data_processor=publisher.process_event
    )

    # Actually start the AMQP Middleware.
    consumer.start()


if __name__ == '__main__':
    bootstrap()
