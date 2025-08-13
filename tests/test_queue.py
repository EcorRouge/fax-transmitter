"""
Test module for RabbitMQ integration
"""
import json

import pika
from rococo.config import BaseConfig


def test_send_fax_message():
    """
    Establish a connection to RabbitMQ server and send a fax message
    """
    config = BaseConfig()

    credentials = pika.PlainCredentials(
        username=config.get_env_var("RABBITMQ_USER"),
        password=config.get_env_var("RABBITMQ_PASSWORD")
    )
    parameters = pika.ConnectionParameters(
        host=config.get_env_var("RABBITMQ_HOST"),
        port=int(config.get_env_var("RABBITMQ_PORT")),
        virtual_host=config.get_env_var("RABBITMQ_VIRTUAL_HOST"),
        credentials=credentials
    )

    connection = pika.BlockingConnection(parameters)

    channel = connection.channel()

    # Declare a queue
    processor_class_name = config.get_env_var("PROCESSOR_TYPE")
    queue_name = config.get_env_var("QUEUE_NAME_PREFIX")+config.get_env_var(
        processor_class_name+"_QUEUE_NAME")
    channel.queue_declare(queue=queue_name, durable=True)

    message = {
        'recipient': {
            'number': "+12192061797",
        },
        'faxes': [
            {
                'type': 'local',
                'filename': 'test_document.pdf',
                'path': '/app/test_volume/test_document.pdf'
            },
        ]
    }

    if config.get_env_var('AWS_TEST_DOCUMENT_PATH'):
        message['faxes'].append({
            'type': 's3',
            'filename': 'test_document.pdf',
            'path': config.get_env_var('AWS_TEST_DOCUMENT_PATH'),
            'aws_key': config.get_env_var("AWS_ACCESS_KEY_ID"),
            'aws_secret_key': config.get_env_var("AWS_SECRET_ACCESS_KEY"),
            'aws_region': config.get_env_var("AWS_REGION")
        })
    
    # Publish a message to the queue
    channel.basic_publish(
        exchange='',
        routing_key=queue_name,
        body=str.encode(json.dumps(message))
    )

    print("Fax message sent to RabbitMQ.")

    # Close the connection
    connection.close()
