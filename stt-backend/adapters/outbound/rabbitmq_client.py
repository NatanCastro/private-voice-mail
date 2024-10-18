import os
import pika


class RabbitMQClient:
    def __init__(self):
        username = os.environ.get("RABBITMQ_USERNAME") or "user"
        password = os.environ.get("RABBITMQ_PASSOWORD") or "password"
        credentials = pika.PlainCredentials(username, password)
        connection_params = pika.ConnectionParameters(
            host="localhost", credentials=credentials
        )

        self._connection = pika.BlockingConnection(connection_params)
        self._channel = self._connection.channel()
        self._channel.queue_declare(queue="stt_response")

    def __del__(self):
        self._connection.close()

    def send_message(self, message: str):
        self._channel.basic_publish(
            exchange="", routing_key="stt_response", body=message
        )
