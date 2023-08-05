import logging
import time
import uuid

import pika

from agent_6tisch.env import get_from_environment
from msg import MsgTestSuiteFinish

log = logging.getLogger(__name__)

shark = """
                       ,-,
                     ,' /
                   ,'  (          _          _
           __...--'     `-....__,'(      _,-'/
  _,---''''                     ````-._,'  ,'
,'  o                                  `  <
`.____  )))                          ...'  \
   `--..._        .   .__....----''''   `-. \
          ```7--i-`.  \                    `-`
             `.(    `-.`.
               `'      `'
"""
testcase_shark = """
               ,
             .';
         .-'` .'
       ,`.-'-.`\
      ; /     '-'
      | \       ,-,
      \  '-.__   )_`'._
       '.     ```      ``'--._
      .-' ,                   `'-.
       '-'`-._           ((   o   )
              `'--....(`- ,__..--'
                       '-'`
"""
testsuite_shark = '''
                                |.
                               ::.
                               :::
              ___              |::
             `-._''--.._       |::
                 `-._   `-._  .|::
                    `-._    `-::::
                       `.     |:::.
                         )    |::`:"-._ 
                       <'   _.7  ::::::`-,.._
                        `-.:        `` '::::::".
                        .:'       .    .   `::::\
                      .:'        .           .:::}
                   _.:'    __          .     :::/
     ,-.___,,..--'' --.""``  ``"".-- --,.._____.-.
    ((   ___ """   -- ...     ....   __  ______  (D
     "-'`   ```''-.  __,,.......,,__      ::.  `-"
                   `<-....,,,,....-<   .:::'
                     "._       ___,,._:::(
                        ::--=''       `\:::.
                       / :::'           `\::.
                      / ::'               `\::
                     / :'                   `\:
                    ( /                       `"
                     "
'''


def notify(amqp_url, message, mandatory=False, exchange=None, properties=None):
    """

    :param properties:
    :param message:
    :param amqp_url:
    :param mandatory:
    :param exchange:
    :return:
    """
    if exchange is None:
        exchange = "amq.topic"
    if properties is None:
        properties = pika.BasicProperties(content_type='text/plain',
                                          delivery_mode=1)

    connection = pika.BlockingConnection(pika.URLParameters(amqp_url))

    log.debug("Notify with URL: {amqp_url}".format(amqp_url=amqp_url))
    log.debug("Notify with message: %s" % message)

    # Open the channel
    channel = connection.channel()
    # Turn on delivery confirmations
    channel.confirm_delivery()
    log.debug("Notify {routing_key} with {body} on exchange {exchange}".format(repr=message,
                                                                               routing_key=message.routing_key,
                                                                               exchange=exchange,
                                                                               body=message.to_json()))

    # Send a message
    if channel.basic_publish(exchange=exchange,
                             routing_key=message.routing_key,
                             body=message.to_json(),
                             mandatory=mandatory,
                             properties=properties) or not mandatory:
        log.debug('Message publish was confirmed')
        channel.close()
        return True
    else:
        log.error("Hum something went wrong with message: %s" % message)
        log.error('Message could not be confirmed')
        log.error("Mandatory: %s" % mandatory)
        channel.close()
        return False


def request_reply(amqp_url, req_msg, rep_msg=None, delay=1, exchange=None):
    """
    - Ask a question on the event-bus
    - Block until receiving the answer

    :param amqp_url:
    :param exchange:
    :param req_msg:
    :param rep_msg:
    :type delay: Time (in seconds) we are waiting
        for an answer before sending the question again.
    """
    if exchange is None:
        exchange = "amq.topic"
    connection = pika.BlockingConnection(pika.URLParameters(amqp_url))

    print("Req with URL: {amqp_url}".format(amqp_url=amqp_url))
    print("Req with message: %s" % req_msg)

    # Open the channel
    channel = connection.channel()
    result = channel.queue_declare(auto_delete=True,
                                   exclusive=True)
    callback_queue = result.method.queue

    print("Notify {routing_key} with {body} on exchange {exchange}".format(routing_key=req_msg.routing_key,
                                                                           exchange=exchange,
                                                                           body=req_msg.to_json()))
    correlation_id = str(uuid.uuid1())
    # IMPORTANT: The answer won't be send on the exchange.
    # It will be posted directly to the callback_queue
    result = channel.basic_publish(exchange=exchange,
                                   routing_key=req_msg.routing_key,
                                   mandatory=True,
                                   properties=pika.BasicProperties(
                                       reply_to=callback_queue,
                                       correlation_id=correlation_id,
                                   ),
                                   body=req_msg.to_json().encode())
    if result:
        print("The request was successfully published")

    while "We didn't yet received an answer":
        method_frame, header_frame, body = channel.basic_get(callback_queue)
        if method_frame is None:
            print('No message returned')
            print("Waiting on the queue with this name: %s" % callback_queue)
            print("Let's wait for %d" % delay)
            time.sleep(delay)
        else:
            print("Just received this AMQP frame:")
            print((method_frame, header_frame, body))
            if correlation_id != header_frame.correlation_id:
                print("The correlation id don't match")
            channel.basic_ack(method_frame.delivery_tag)
            channel.queue_delete(callback_queue)
            channel.close()
            print("We received an answer to the question")
            return body


class AMQPService(object):
    """
    Base class for all AMQP components
    """

    def __init__(self, **kwargs):
        self.exchange = get_from_environment("EXCHANGE_NAME", "amq.topic")
        if "amqp_url" in kwargs:
            self.amqp_url = kwargs["amqp_url"]
        else:
            self.amqp_url = get_from_environment("AMQP_URL", 'amqp://guest:guest@localhost')
        self.ready = kwargs["ready"]
        self.received_msg = kwargs["received_msg"]

        self.amqp_name = "Default AMQP Service"
        self.mapping = {
            MsgTestSuiteFinish.routing_key: self.handle_testsuite_finish
        }
        self.sub_processes = {}
        self.debug = getattr(kwargs, "debug", False)
        self.debug_msg_max_size = getattr(kwargs, "debug_msg_max_size", 42)

        self._connection = pika.BlockingConnection(pika.connection.URLParameters(self.amqp_url))
        self._channel = self._connection.channel()
        self._closing = False
        self._consumer_tag = None

    def __enter__(self):
        self.bootstrap()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("We are exiting from %s" % self.amqp_name)
        self.terminate()
        print("We are done terminating %s" % self.amqp_name)

    def signal_end_session(self):
        print("We signal the end of the testsuite")
        self.notify(MsgTestSuiteFinish, mandatory=True)
        print("Done signaling the end of the test suite")

    def handle_testsuite_finish(self, unused_channel, basic_deliver, properties, body):
        print("The testsuite is over. Closing...")
        self.terminate()
        print("Bye")

    def run(self):
        """Run the example consumer by connecting to RabbitMQ and then
        start consuming.

        """
        self._channel.start_consuming()

    def terminate(self):
        """Cleanly shutdown the connection to RabbitMQ by stopping the consumer
        with RabbitMQ. When RabbitMQ confirms the cancellation, on_cancelok
        will be invoked by pika, which will then closing the channel and
        connection.
        """
        for name, p in self.sub_processes.items():
            print("Try to terminate (%s, %s)" % (name, p))
            p.terminate()
        if self._channel.is_open:
            print('%s: Stopping' % self.amqp_name)
            self._channel.close()
            print('%s: Stopped' % self.amqp_name)

    def bootstrap(self, ):
        # Binding of all routing keys to a given queue
        for key, handler in self.mapping.items():
            queue_name = self.amqp_name + " | " + key
            # Creation of the queue
            self._channel.queue_declare(queue=queue_name,
                                        auto_delete=True)

            self._channel.queue_bind(queue=queue_name,
                                     routing_key=key,
                                     exchange=self.exchange)

            # Add callback to the queue
            self._channel.basic_consume(queue=queue_name,
                                        consumer_callback=handler)
            print("%s: Binding %s to %s" % (self.amqp_name, queue_name, handler))

        print("%s is ready" % self.amqp_name)
        self.ready.set()

    def notify(self, message, mandatory=False):
        notify(self.amqp_url, message=message, mandatory=mandatory, exchange=self.exchange)

    def request_reply(self, req_msg, rep_msg, delay=3):
        request_reply(self.amqp_url,
                      req_msg=req_msg, rep_msg=rep_msg,
                      delay=delay, exchange=self.exchange)


