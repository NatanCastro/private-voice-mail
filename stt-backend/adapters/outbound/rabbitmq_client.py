# TODO: implement rabbitmq client


import pika


class RabbitMQClient:
    def __init__(self):
        # TODO: use env variables for rabbitmq user and password
        credentials = pika.PlainCredentials("user", "password")
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
