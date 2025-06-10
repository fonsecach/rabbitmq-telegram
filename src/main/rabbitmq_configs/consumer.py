import pika
import json
from dotenv import load_dotenv
import os

load_dotenv()

def rabbitmq_callback(ch, method, properties, body):
    msg = body.decode("utf-8")
    formatted_msg = json.loads(msg)
    print(f" [x] Received {formatted_msg}")
    # Process the message here  

class RabbitMQConsumer:
    def __init__(self) -> None:
        self.__host = os.getenv("RABBITMQ_HOST")
        self.__port = int(os.getenv("RABBITMQ_PORT", 5672))
        self.__username = os.getenv("RABBITMQ_USERNAME")
        self.__password = os.getenv("RABBITMQ_PASSWORD")
        self.__queue = "telegram_messages"
        self.__channel = self.__create_channel()
        
    def __create_channel(self):
        connection_parameters = pika.ConnectionParameters(
            host=self.__host,
            port=self.__port,
            credentials=pika.PlainCredentials(
                username=self.__username,
                password=self.__password
            )
        )
        
        connection = pika.BlockingConnection(connection_parameters)
        channel = connection.channel()
        channel.queue_declare(queue=self.__queue, durable=True)
        
        channel.basic_consume(
            queue=self.__queue,
            on_message_callback=rabbitmq_callback,
            auto_ack=True
        )
        
        return channel
    
    def start(self):
        print(f" [*] Waiting for messages. To exit press CTRL+C")
        self.__channel.start_consuming()