# encoding: utf-8

import pika
import uuid
import threading

__author__ = 'BetaS'


class MessageSender:
    def __init__(self, queue):
        self.queue = queue

        self._connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self._channel = self._connection.channel()

        result = self._channel.queue_declare(exclusive=True)
        self._callback_queue = result.method.queue

        self._channel.basic_consume(self._result, no_ack=True, queue=self._callback_queue)
        self._results = {}

    def _result(self, ch, method, props, body):
        self._results[props.correlation_id] = body

    def _send(self, message):
        _corr_id = str(uuid.uuid4())
        _prop = pika.BasicProperties(reply_to=self._callback_queue, correlation_id=_corr_id)
        self._channel.basic_publish(exchange='', routing_key=self.queue, properties=_prop, body=message)

        self._results[_corr_id] = None

        while self._results[_corr_id] is None:
            self._connection.process_data_events()

        result = self._results[_corr_id]
        del self._results[_corr_id]
        return result

    def _send_async(self, message, callback):
        result = self._send(message)
        callback(result)

    def send(self, message, callback=None):
        if callback:
            threading.Thread(target=self._send_async, args=[message, callback]).start()
            return None
        else:
            return self._send(message)
