import os
import pika
from threading import Thread
from pika import exceptions as pk_exceptions
from pika import spec as pk_spec

from core.model.stt import stt_request_from_string
from core.services.stt_service import SttService


class RabbitMQServer:
    def __init__(self, stt_service: SttService):
        username = os.environ.get("RABBITMQ_USERNAME") or "user"
        password = os.environ.get("RABBITMQ_PASSOWORD") or "password"
        credentials = pika.PlainCredentials(username, password)
        connection_params = pika.ConnectionParameters(
            host="localhost", credentials=credentials
        )
        self._stt_service = stt_service

        self._connection = pika.BlockingConnection(connection_params)
        self._channel = self._connection.channel()
        self._server_thread = Thread(target=self._run_server)
        self._server_thread.start()

    def _run_server(self) -> None:
        self._channel.queue_declare("stt_request")
        while True:
            try:
                self._channel.basic_consume(
                    queue="stt_request",
                    on_message_callback=self._process_request,
                    auto_ack=True,
                )
                self._channel.start_consuming()
            except Exception as e:
                match e:
                    case pk_exceptions.ConnectionClosedByBroker():
                        break
                    case pk_exceptions.AMQPChannelError():
                        break
                    case pk_exceptions.AMQPConnectionError():
                        __import__("pprint").pprint(e)
                        continue

    def _process_request(
        self,
        ch: pika.BlockingConnection,
        method: pk_spec.Basic.Deliver,
        properties: pk_spec.BasicProperties,
        body: bytes,
    ) -> None:
        request = stt_request_from_string(body.decode()).unwrap()
        self._stt_service.add_task(request)
