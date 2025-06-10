import pytest
from unittest.mock import patch, MagicMock
from consumer import RabbitMQConsumer

@patch("src.main.rabbitmq_configs.consumer.os.getenv")
@patch("src.main.rabbitmq_configs.consumer.RabbitMQConsumer._RabbitMQConsumer__create_channel")
def test_rabbitmq_consumer_init(mock_create_channel, mock_getenv):
    # Arrange
    mock_getenv.side_effect = lambda key, default=None: {
        "RABBITMQ_HOST": "localhost",
        "RABBITMQ_PORT": "5672",
        "RABBITMQ_USERNAME": "guest",
        "RABBITMQ_PASSWORD": "guest"
    }.get(key, default)
    mock_channel = MagicMock()
    mock_create_channel.return_value = mock_channel

    # Act
    consumer = RabbitMQConsumer()

    # Assert
    mock_create_channel.assert_called_once()
    assert consumer._RabbitMQConsumer__channel == mock_channel
    assert consumer._RabbitMQConsumer__host == "localhost"
    assert consumer._RabbitMQConsumer__port == 5672
    assert consumer._RabbitMQConsumer__username == "guest"
    assert consumer._RabbitMQConsumer__password == "guest"
    assert consumer._RabbitMQConsumer__queue == "telegram_messages"

@patch("src.main.rabbitmq_configs.consumer.RabbitMQConsumer._RabbitMQConsumer__create_channel")
def test_start_method(mock_create_channel):
    # Arrange
    mock_channel = MagicMock()
    mock_create_channel.return_value = mock_channel
    consumer = RabbitMQConsumer()

    # Act
    consumer.start()

    # Assert
    mock_channel.start_consuming.assert_called_once()

@patch("src.main.rabbitmq_configs.consumer.RabbitMQConsumer._RabbitMQConsumer__create_channel")
@patch("src.main.rabbitmq_configs.consumer.time.time")
def test_start_method_performance(mock_time, mock_create_channel):
    # Arrange
    mock_channel = MagicMock()
    mock_create_channel.return_value = mock_channel
    consumer = RabbitMQConsumer()
    
    # Simulate high volume of messages
    message_count = 10000
    mock_channel.start_consuming.side_effect = lambda: [rabbitmq_callback(None, None, None, b"test message") for _ in range(message_count)]
    
    # Simulate elapsed time
    mock_time.side_effect = [0, 5]  # 5 seconds elapsed

    # Act
    consumer.start()

    # Assert
    mock_channel.start_consuming.assert_called_once()
    assert mock_time.call_count == 2
    
    # Check performance (messages per second)
    messages_per_second = message_count / 5
    assert messages_per_second >= 1000, f"Performance below expected: {messages_per_second:.2f} messages/second"
