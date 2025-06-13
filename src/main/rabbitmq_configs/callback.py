import json
from src.drivers.telegram_sender import send_telegram_message


def rabbitmq_callback(ch, method, properties, body):
    """
    Callback function to process messages received from a RabbitMQ queue.

    Parameters:
    ch: BlockingChannel
        The channel object through which the message was received.
    method: spec.Basic.Deliver
        Method frame with delivery information.
    properties: spec.BasicProperties
        Properties of the message.
    body: bytes
        The message body as a byte string.
    Returns:
    None
    """
    msg = body.decode("utf-8")
    formatted_msg = json.loads(msg)
    telegram_message = formatted_msg['msg']
    send_telegram_message(telegram_message)


