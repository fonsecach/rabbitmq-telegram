import pytest
from unittest.mock import patch, MagicMock
from publisher import RabbitMQPublisher

@patch("publisher.pika.BlockingConnection")
def test_create_channel(mock_blocking_connection):
    # Arrange
    mock_channel = MagicMock()
    mock_blocking_connection.return_value.channel.return_value = mock_channel

    # Act
    publisher = RabbitMQPublisher()
    channel = publisher.create_channel()

    # Assert
    mock_blocking_connection.assert_called()
    assert channel == mock_channel

@patch("publisher.pika.BlockingConnection")
def test_send_message(mock_blocking_connection):
    # Arrange
    mock_channel = MagicMock()
    mock_blocking_connection.return_value.channel.return_value = mock_channel
    publisher = RabbitMQPublisher()
    test_body = {"foo": "bar"}

    # Act
    publisher.send_message(test_body)

    # Assert
    mock_channel.basic_publish.assert_called_once()
    args, kwargs = mock_channel.basic_publish.call_args
    assert kwargs["exchange"] == publisher._RabbitMQPublisher__exchange
    assert kwargs["routing_key"] == publisher._RabbitMQPublisher__routing_key
    assert kwargs["body"] is not None  # Should be a JSON string

    # Optionally, check that the message body is correct
    import json
    assert json.loads(kwargs["body"]) == test_body
