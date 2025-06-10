import pika
import json
from dotenv import load_dotenv
import os

load_dotenv()

class RabbitMQPublisher:
    def __init__(self) -> None:
        self.__host = os.getenv("RABBITMQ_HOST")
        self.__port = os.getenv("RABBITMQ_PORT")
        self.__username = os.getenv("RABBITMQ_USERNAME")
        self.__password = os.getenv("RABBITMQ_PASSWORD")
        self.__channel = self.create_channel()
        self.__exchange = "bot_telegram"
        self.__routing_key = ""

    def create_channel(self):
        connection_parameters = pika.ConnectionParameters(
            host=self.__host,
            port=self.__port,
            credentials=pika.PlainCredentials(
                username=self.__username,
                password=self.__password
            )
        )
        channel = pika.BlockingConnection(connection_parameters).channel()
        print(channel)
        return channel

    def send_message(self, body: dict):
        self.__channel.basic_publish(
            exchange=self.__exchange,
            routing_key=self.__routing_key,
            body=json.dumps(body),
            properties=pika.BasicProperties(
                delivery_mode=2,
                content_type="application/json"
            )
        )

rabbit_mq_publisher = RabbitMQPublisher()
rabbit_mq_publisher.send_message({
    "message": "Teste no rabbitmq"
})
