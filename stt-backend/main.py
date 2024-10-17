from threading import Thread
import pika
import time
from adapters.outbound.stt_service_whisper import WhisperSttService
from core.services.audio_service import AudioService
from core.services.request_service import RequestService
from core.services.stt_service import SttService
from adapters.inbound.rabbitmq_server import RabbitMQServer


def client():
    credentials = pika.PlainCredentials("user", "password")
    connection_params = pika.ConnectionParameters(
        host="localhost", credentials=credentials
    )
    connection = pika.BlockingConnection(connection_params)
    channel = connection.channel()
    channel.queue_declare(queue="stt_request")
    for _ in range(2):
        message = str.encode("1,url,portuguese")
        channel.basic_publish(exchange="", routing_key="stt_request", body=message)
        time.sleep(0.1)
    connection.close()


def main():
    Thread(target=client).start()
    RabbitMQServer()


# def main():
#     request_service = RequestService()
#     audio_service = AudioService(request_service)
#     stt_whisper_service = WhisperSttService()
#     stt_service = SttService(audio_service, stt_whisper_service)


if __name__ == "__main__":
    main()
