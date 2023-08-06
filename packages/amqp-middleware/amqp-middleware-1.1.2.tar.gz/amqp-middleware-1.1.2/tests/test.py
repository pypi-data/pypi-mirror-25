import unittest

import pika
import json
import time
import requests
import threading

import amqpconsumer.components.agent


class AMQPTest(unittest.TestCase):

    def setUp(self):
        reg = requests.post('http://localhost/api/v1/insights/register',
                            data=json.dumps({'name': 'Unit Tester',
                                             'email': 'tester@unit.io'})
                           )
        if not reg.ok:
            raise Exception('Registration failed')

        res = reg.json()
        self.id = res['uuid']

        self.ws_kwargs = {
            url='localhost:8888/insights/socket',
            token=res['token'],
            secure=False,
            ca_certs=None,
        }

        self.cfy_kwargs = {
            'host': 'localhost',  # The API call to Cloudify Manager will fail.
            'secure': False,
            'verify': True,
            'credentials': {
                'username': '',
                'password': '',
                'ca_certs': None,
            },
            'ssl_enabled': False,
        }

        self.rmq_kwargs = {
            'host': 'localhost',
            'port': 5672,
            'credentials': {
                'username': 'guest',
                'password': 'guest',
                'ca_certs': None,
                'ssl_enabled': False,
             },
        }

    def tearDown(self):
        pass

    def test(self):
        publisher = amqpconsumer.components.agent.Publisher(
            id=self.id,
            kwargs={'ws': self.ws_kwargs, 'cfy': self.cfy_kwargs}
        )

        consumer = amqpconsumer.components.agent.AMQPConsumer(
            exchange='cloudify-metrics',
            exchange_type='topic', routing_key='*',
            data_processor=publisher.process_event,
            **self.rmq_kwargs,
        )

        def start(agent):
            agent.start()

        thread = threading.Thread(target=start, kwargs={'agent': consumer})
        thread.daemon = True
        thread.start()
        time.sleep(2)
        publish_event()
        thread.join(5)

        self.assertTrue(find_event(), 'Failed to find ES document')


def publish_event():

    event = {
        'host': 'dummy_host',
        'node_id': 'dummy_id',
        'node_name': 'dummy_name',
        'deployment_id': 'dummy_deployment',
        'name': 'test',
        'path': 'path',
        'metric': 1,
        'unit': '',
        'type': 'test_type',
        'time': time.time(),
    }

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost')
    )
    channel = connection.channel()
    channel.exchange_declare(exchange='cloudify-metrics', type='topic',
                             durable=False, auto_delete=True, internal=False)
    channel.basic_publish(exchange='cloudify-metrics', routing_key='metrics',
                          body=json.dumps(event))
    channel.close()
    connection.close()


def find_event():
    query = {
        "query": {
            "bool": {
                "must": [
                    {"match": {"@fields.host": "dummy_host"}},
                    {"match": {"@fields.node_id": "dummy_id"}},
                    {"match": {"@fields.node_name": "dummy_name"}},
                    {"match": {"@fields.deployment_id": "dummy_deployment"}},
                ],
            },
        },
    }

    req = requests.get('http://localhost:9200/*insights*/_search',
                        data=json.dumps(query))
    if req.ok:
        hits = req.json()['hits']['hits']
        if hits:
            return True
    return False


if __name__ == '__main__':
    unittest.main()
