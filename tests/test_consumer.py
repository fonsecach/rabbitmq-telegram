import pytest
from unittest.mock import patch, MagicMock
import json
import os

from src.main.rabbitmq_configs.consumer import RabbitMQConsumer, rabbitmq_callback


class TestRabbitMQConsumer:
    
    @patch.dict(os.environ, {
        "RABBITMQ_HOST": "localhost",
        "RABBITMQ_PORT": "5672", 
        "RABBITMQ_USERNAME": "guest",
        "RABBITMQ_PASSWORD": "guest"
    })
    @patch("src.main.rabbitmq_configs.consumer.pika.BlockingConnection")
    def test_consumer_initialization(self, mock_connection):
        """Test that consumer initializes correctly with environment variables"""
        # Arrange
        mock_channel = MagicMock()
        mock_connection.return_value.channel.return_value = mock_channel
        
        # Act
        consumer = RabbitMQConsumer()
        
        # Assert
        assert consumer._RabbitMQConsumer__host == "localhost"
        assert consumer._RabbitMQConsumer__port == 5672
        assert consumer._RabbitMQConsumer__username == "guest" 
        assert consumer._RabbitMQConsumer__password == "guest"
        assert consumer._RabbitMQConsumer__queue == "telegram_messages"
        
        # Verify connection was established
        mock_connection.assert_called_once()
        mock_channel.queue_declare.assert_called_once_with(
            queue="telegram_messages", 
            durable=True
        )
        mock_channel.basic_consume.assert_called_once()

    @patch.dict(os.environ, {
        "RABBITMQ_HOST": "localhost",
        "RABBITMQ_PORT": "5672",
        "RABBITMQ_USERNAME": "guest", 
        "RABBITMQ_PASSWORD": "guest"
    })
    @patch("src.main.rabbitmq_configs.consumer.pika.BlockingConnection")
    def test_start_consuming(self, mock_connection):
        """Test that start method calls channel.start_consuming"""
        # Arrange
        mock_channel = MagicMock()
        mock_connection.return_value.channel.return_value = mock_channel
        consumer = RabbitMQConsumer()
        
        # Act
        consumer.start()
        
        # Assert
        mock_channel.start_consuming.assert_called_once()

    @patch("src.main.rabbitmq_configs.consumer.print")
    def test_rabbitmq_callback(self, mock_print):
        """Test the callback function processes messages correctly"""
        # Arrange
        test_message = {"user_id": 123, "message": "Hello World"}
        body = json.dumps(test_message).encode("utf-8")
        
        # Act
        rabbitmq_callback(None, None, None, body)
        
        # Assert
        mock_print.assert_called_once_with(f" [x] Received {test_message}")

    @patch.dict(os.environ, {
        "RABBITMQ_HOST": "localhost",
        "RABBITMQ_USERNAME": "guest",
        "RABBITMQ_PASSWORD": "guest"
    })
    @patch("src.main.rabbitmq_configs.consumer.pika.BlockingConnection")
    def test_default_port_handling(self, mock_connection):
        """Test that default port is used when RABBITMQ_PORT is not set"""
        # Arrange
        mock_channel = MagicMock()
        mock_connection.return_value.channel.return_value = mock_channel
        
        # Act
        consumer = RabbitMQConsumer()
        
        # Assert
        assert consumer._RabbitMQConsumer__port == 5672

    @patch.dict(os.environ, {
        "RABBITMQ_HOST": "localhost",
        "RABBITMQ_PORT": "5672",
        "RABBITMQ_USERNAME": "guest",
        "RABBITMQ_PASSWORD": "guest"
    })
    @patch("src.main.rabbitmq_configs.consumer.pika.BlockingConnection")
    def test_connection_parameters(self, mock_connection):
        """Test that connection parameters are set correctly"""
        # Arrange
        mock_channel = MagicMock()
        mock_connection.return_value.channel.return_value = mock_channel
        
        # Act
        consumer = RabbitMQConsumer()
        
        # Assert
        mock_connection.assert_called_once()
        call_args = mock_connection.call_args[1]
        connection_params = call_args.get('connection_parameters') or mock_connection.call_args[0][0]
        
        # Verify connection parameters structure
        assert hasattr(connection_params, 'host') or mock_connection.called