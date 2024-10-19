import os
import time
from loguru import logger
import pika
from threading import Thread
from pika import exceptions as pk_exceptions
from pika import spec as pk_spec

from core.model.stt import stt_request_from_string
from core.services.stt_service import SttService


class RabbitMQServer:
    def __init__(self, stt_service: SttService):
        username = os.environ.get("RABBITMQ_USERNAME") or "user"
        password = os.environ.get("RABBITMQ_PASSWORD") or "password"
        credentials = pika.PlainCredentials(username, password)
        connection_params = pika.ConnectionParameters(
            host="localhost", credentials=credentials
        )
        self._stt_service = stt_service

        self._connection_params = connection_params
        self._server_thread = Thread(target=self._run_server)
        self._server_thread.start()
        logger.info("RabbitMQ server started")

    def _run_server(self) -> None:
        while True:
            try:
                self._setup_connection()
                self._channel.start_consuming()
            except pk_exceptions.ConnectionClosedByBroker:
                logger.error("Connection closed by broker, stopping server.")
                break
            except pk_exceptions.AMQPChannelError as err:
                logger.error(f"Channel error: {err}, stopping server.")
                break
            except pk_exceptions.AMQPConnectionError as err:
                logger.warning(f"Connection error: {err}, retrying...")
                self._reconnect()

    def _setup_connection(self):
        self._connection = pika.BlockingConnection(self._connection_params)
        self._channel = self._connection.channel()
        self._channel.queue_declare("stt_request")
        self._channel.basic_consume(
            queue="stt_request",
            on_message_callback=self._process_request,
            auto_ack=True,
        )

    def _process_request(
        self,
        ch: pika.BlockingConnection,
        method: pk_spec.Basic.Deliver,
        properties: pk_spec.BasicProperties,
        body: bytes,
    ) -> None:
        try:
            request = stt_request_from_string(body.decode()).unwrap()
            self._stt_service.add_task(request)
            logger.info("Task added to STT service")
        except Exception as e:
            logger.error(f"Failed to process request: {e}")

    def _reconnect(self):
        max_retries = 5
        delay = 1

        for attempt in range(1, max_retries + 1):
            try:
                if self._connection.is_open:
                    self._connection.close()
                self._setup_connection()
                logger.info(
                    f"Successfully reconnected to RabbitMQ on attempt {attempt}"
                )
                return
            except pk_exceptions.AMQPConnectionError as e:
                logger.warning(f"Reconnect attempt {attempt} failed: {e}")
                time.sleep(delay)
                delay *= 2

        logger.error("Exceeded maximum retries. Could not reconnect to RabbitMQ.")
