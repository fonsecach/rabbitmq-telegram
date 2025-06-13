import os
import json
import pytest
from unittest.mock import patch, MagicMock
from src.main.rabbitmq_configs.publisher import RabbitMQPublisher


class TestRabbitMQPublisher:

    @patch.dict(os.environ, {
        "RABBITMQ_HOST": "localhost",
        "RABBITMQ_PORT": "5672",
        "RABBITMQ_USERNAME": "guest",
        "RABBITMQ_PASSWORD": "guest"
    })
    @patch("src.main.rabbitmq_configs.publisher.pika.BlockingConnection")
    def test_publisher_initialization(self, mock_blocking_connection):
        """Test if the publisher initializes and connects properly"""
        mock_channel = MagicMock()
        mock_blocking_connection.return_value.channel.return_value = mock_channel

        publisher = RabbitMQPublisher()

        # Verifica se a conexão e o canal foram criados
        mock_blocking_connection.assert_called_once()
        mock_channel.exchange_declare.assert_called_once_with(
            exchange="bot_telegram",
            exchange_type="direct",
            durable=True
        )

    @patch.dict(os.environ, {
        "RABBITMQ_HOST": "localhost",
        "RABBITMQ_PORT": "5672",
        "RABBITMQ_USERNAME": "guest",
        "RABBITMQ_PASSWORD": "guest"
    })
    @patch("src.main.rabbitmq_configs.publisher.pika.BlockingConnection")
    def test_send_message(self, mock_blocking_connection):
        """Test if message is sent properly using basic_publish"""
        mock_channel = MagicMock()
        mock_blocking_connection.return_value.channel.return_value = mock_channel

        publisher = RabbitMQPublisher()
        test_body = {"user_id": 1, "message": "Olá"}

        publisher.send_message(test_body)

        mock_channel.basic_publish.assert_called_once()
        call_args = mock_channel.basic_publish.call_args

        assert call_args.kwargs["exchange"] == "bot_telegram"
        assert call_args.kwargs["routing_key"] == ""
        assert call_args.kwargs["body"] == json.dumps(test_body)

        props = call_args.kwargs["properties"]
        assert props.delivery_mode == 2
        assert props.content_type == "application/json"

    @patch.dict(os.environ, {
        "RABBITMQ_HOST": "localhost",
        "RABBITMQ_PORT": "5672",
        "RABBITMQ_USERNAME": "guest",
        "RABBITMQ_PASSWORD": "guest"
    })
    @patch("src.main.rabbitmq_configs.publisher.pika.BlockingConnection")
    def test_send_message_json_serialization(self, mock_blocking_connection):
        """Ensure that send_message serializes body to JSON string"""
        mock_channel = MagicMock()
        mock_blocking_connection.return_value.channel.return_value = mock_channel

        publisher = RabbitMQPublisher()
        message = {
            "event": "ping",
            "timestamp": "2025-06-13T20:00:00",
            "data": {"foo": "bar"}
        }

        publisher.send_message(message)

        sent_body = mock_channel.basic_publish.call_args.kwargs["body"]
        assert isinstance(sent_body, str)
        assert json.loads(sent_body) == message
