import pika
import json
from dotenv import load_dotenv
import os
from typing import Dict, Any

load_dotenv()


class RabbitMQPublisher:
    """Publisher for RabbitMQ messages with proper configuration management"""
    
    def __init__(self) -> None:
        self.__host = os.getenv("RABBITMQ_HOST")
        self.__port = int(os.getenv("RABBITMQ_PORT", 5672))  
        self.__username = os.getenv("RABBITMQ_USERNAME")
        self.__password = os.getenv("RABBITMQ_PASSWORD")
        self.__exchange = "bot_telegram"
        self.__routing_key = ""
        self.__channel = self.__create_channel()

    def __create_channel(self):
        """Create and configure RabbitMQ channel"""
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
        
        channel.exchange_declare(
            exchange=self.__exchange,
            exchange_type='direct',
            durable=True
        )
        
        return channel

    def send_message(self, body: Dict[str, Any]) -> None:
        """
        Send message to RabbitMQ
        
        Args:
            body: Dictionary containing the message data
        """
        try:
            self.__channel.basic_publish(
                exchange=self.__exchange,
                routing_key=self.__routing_key,
                body=json.dumps(body),
                properties=pika.BasicProperties(
                    delivery_mode=2,
                    content_type="application/json"
                )
            )
            print(f"Message sent successfully: {body}")
        except Exception as e:
            print(f"Error sending message: {e}")
            raise

    def close_connection(self) -> None:
        """Close the RabbitMQ connection"""
        if hasattr(self, '_RabbitMQPublisher__channel') and self.__channel:
            self.__channel.connection.close()


if __name__ == "__main__":
    publisher = RabbitMQPublisher()
    try:
        publisher.send_message({
            "msg": "Projeto finalizado com sucesso!",
        })
    finally:
        publisher.close_connection()