import json
import logging
import multiprocessing
import socket
import subprocess
import sys
import time

import pika
import zmq
from msg import MsgTestSuiteStart, MsgStimuliExecuted, MsgTestCaseFinished, MsgTestSuiteReport, MsgAgentJSON, \
    MsgFlashSniffer, MsgSnifferStart, MsgSnifferChannel, MsgInteropSessionConfiguration, MsgAgentConfig, \
    MsgAgentSolicitation, MsgAgentPingRequest, MsgOpenvisualizerNotification

from agent_6tisch import (
    testsuite_shark,
    testcase_shark,
    AMQPService,
)
from agent_6tisch.env import get_from_environment

log = logging.getLogger(__name__)


def flash_mote(bootload, board, toolchain, openwsn_fw_folder, target):
    """

    :param target:
    :param toolchain:
    :param board:
    :param bootload:
    :param openwsn_fw_folder:
    :return:
    """
    flashing_process = subprocess.check_output(["sudo",
                                                "scons",
                                                "board=%s" % board,
                                                "toolchain=%s" % toolchain,
                                                "bootload=%s" % bootload,
                                                target],
                                               cwd=openwsn_fw_folder,
                                               stderr=subprocess.PIPE)
    return flashing_process


def sniff_pydispatcher_with_rover(amqp_url,
                                  admin_zmq, subscription_zmq, subscriptions=None,
                                  exchange=None, properties=None):
    """
    Forward event published on a sub ZMQ to the event-bus

    :param subscriptions:
    :param subscription_zmq:
    :param admin_zmq:
    :param exchange:
    :param properties:
    :param amqp_url:
    :return:
    """
    if exchange is None:
        exchange = "amq.topic"
    if properties is None:
        properties = pika.BasicProperties(content_type='text/plain',
                                          delivery_mode=1)
    if subscriptions is None:
        subscriptions = {"sub": [
            "fromMote.status",
        ]}
    connection = pika.BlockingConnection(pika.URLParameters(amqp_url))
    channel = connection.channel()

    # Turn on delivery confirmations
    channel.confirm_delivery()

    with zmq.Context() as context:

        # First we set up the event we are interested in
        with context.socket(zmq.REQ) as admin_socket:
            admin_socket.connect(admin_zmq)
            admin_socket.send_json(subscriptions)
            message = admin_socket.recv()
            print(message)

        # Then we launch the infinite loop
        with context.socket(zmq.SUB) as subscriber:
            subscriber.connect(subscription_zmq)
            subscriber.setsockopt(zmq.SUBSCRIBE, b"")
            while True:
                d = subscriber.recv_json()
                m = MsgOpenvisualizerNotification(**d)
                # Send a message
                channel.basic_publish(exchange=exchange,
                                      routing_key=m.routing_key,
                                      body=m.to_json(),
                                      mandatory=True,
                                      properties=properties)


def sniff_hexdump_with_tshark(amqp_url, exchange=None, properties=None, display_filter=""):
    """
    We want to analyze frame by frame.
    That's why we need hexdump to tell when a frame starts and ends.
    In raw mode there is simply no simple way to tell the limit of a frame.
    :return:
    """
    interface = "tun0"
    capture_filter = ""
    cmd = ["tshark",
           # Network interface targeted
           "-i", interface,

           # In case we want to limit the capture to a set of options
           "-f", capture_filter,

           # Add a binary dump of the packet
           # You can recreate the PCAP using
           # xxd -r -p test.hex | od -Ax -tx1 | text2pcap - test.pcap
           # We use hexdump
           "-x",

           # Flush immediately
           "-l",

           # Optional filter to avoid spamming the testing tool
           "-Y", display_filter
           ]
    print(cmd)
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE)

    if exchange is None:
        exchange = "amq.topic"
    if properties is None:
        properties = pika.BasicProperties(content_type='text/plain',
                                          delivery_mode=1)
    connection = pika.BlockingConnection(pika.URLParameters(amqp_url))
    channel = connection.channel()

    # Turn on delivery confirmations
    channel.confirm_delivery()

    buffer = ""
    while True:
        sys.stdout.flush()
        line = str(process.stdout.readline().decode())
        # No-empty line: we got a part of a packet we add it
        if line.strip():  # and line[:1] == "0":
            buffer += line
        # New line signaling the previous packet is over
        # We can send it to AMQP
        if not line.strip():
            # OpenVisualizer provides RawIP encapsulation we need to signal that
            # To have proper handling (prepend ethernet header)
            m = MsgAgentJSON(body=json.dumps({"format": "hexdump",
                                              "raw_ip": True,
                                              "value": buffer}))
            channel.basic_publish(exchange=exchange,
                                  routing_key=m.routing_key,
                                  body=m.to_json(),
                                  mandatory=True,
                                  properties=properties)

            # We make the buffer empty again
            buffer = ""


class OpenVisualizerException(Exception):
    pass


class Agent(AMQPService):
    """
    6TiSCH specific agent
    """

    def __init__(self, **kwargs):
        super(Agent, self).__init__(**kwargs)
        self.amqp_name = "6TiSCH Agent"
        self.debug = False

        self.mapping.update({
            # MsgTestSuiteStart.routing_key: self.handle_testsuite_start,
            MsgAgentConfig.routing_key: self.handle_agent_config,
            # MsgStepExecute.routing_key: self.handle_step_execute,
            MsgTestCaseFinished.routing_key: self.handle_testcase_finished,
            MsgTestSuiteReport.routing_key: self.handle_testsuite_report,
            # MsgTestCaseReady.routing_key: self.handle_testcase_ready
            MsgFlashSniffer.routing_key: self.handle_sniffer_flashing,
            MsgSnifferStart.routing_key: self.handle_sniffer_start,
            MsgAgentPingRequest.routing_key: self.handle_ping,
            MsgSnifferChannel.routing_key: self.handle_sniffing_channel
        })

        self.configured = multiprocessing.Event()
        self.tests = [
            "TD_6TiSCH_SYN_01",

            "TD_6TiSCH_MINIMAL_01",
            "TD_6TiSCH_MINIMAL_02",
            "TD_6TiSCH_MINIMAL_03",
            "TD_6TiSCH_MINIMAL_04",
            "TD_6TiSCH_MINIMAL_05",
            "TD_6TiSCH_MINIMAL_06",

            "TD_6TiSCH_L2SEC_01",

            "TD_6TiSCH_SECJOIN_01",
            "TD_6TiSCH_SECJOIN_02",
            "TD_6TiSCH_SECJOIN_03",
            "TD_6TiSCH_SECJOIN_04",

            "TD_6TiSCH_6P_01",
            "TD_6TiSCH_6P_02",
            "TD_6TiSCH_6P_03",
            "TD_6TiSCH_6P_04"
        ]
        self.already_sniffing = multiprocessing.Event()

        self.openwsn_fw_folder = get_from_environment("OPENWSN_FW", "/openwsn-fw")
        self.openvisualizer_folder = get_from_environment("OPENVISUALIZER", "/openwsn-sw/software/openvisualizer")
        self.admin_zmq = get_from_environment("ADMIN_ZMQ", "tcp://localhost:50001")
        self.sub_zmq = get_from_environment("SUB_ZMQ", "tcp://localhost:50002")
        self.inject_zmq = get_from_environment("INJECT_ZMQ", "tcp://localhost:60000")

    def handle_agent_config(self, channel, basic_deliver, properties, body):
        try:
            data = json.loads(body.decode())
        except ValueError:
            channel.basic_ack(delivery_tag=basic_deliver.delivery_tag)
            log.warning("No JSON could be decoded from %s" % body)
            return
        log.debug("Data: %s" % data)

        print("Agent: Received configuration")
        self.configured.set()
        self.received_msg.put(body)
        channel.basic_ack(delivery_tag=basic_deliver.delivery_tag)

    def handle_step_execute(self, channel, basic_deliver, properties, body):
        try:
            data = json.loads(body.decode())
        except ValueError:
            channel.basic_ack(delivery_tag=basic_deliver.delivery_tag)
            log.warning("No JSON could be decoded from %s" % body)
            return
        log.debug("Data: %s" % data)

        print("Agent: We received a question")
        msg = json.loads(body.decode())
        print("--------------------------")
        print(msg["question"])
        print("--------------------------")
        self.do_handle_step_execute(msg["question"])
        channel.basic_ack(delivery_tag=basic_deliver.delivery_tag)

    def handle_sniffer_flashing(self, channel, basic_deliver, properties, body):
        try:
            data = json.loads(body.decode())
        except ValueError:
            channel.basic_ack(delivery_tag=basic_deliver.delivery_tag)
            log.warning("No JSON could be decoded from %s" % body)
            return

        toolchain = {
            "telosb": "mspgcc",
            "openmote-cc2538": "armgcc"
        }

        # Check whether board is correct
        board = data.get("board", None)
        if board not in toolchain.keys():
            print("board %s not supported" % board)
            channel.basic_ack(delivery_tag=basic_deliver.delivery_tag)
            return

        # Check whether bootload is correct
        bootload = data.get("bootload", "")

        # Check whether target is correct
        target = data.get("target", "")
        if target not in ("oos_sniffer", "oos_openwsn"):
            print("target %s not supported" % target)
            channel.basic_ack(delivery_tag=basic_deliver.delivery_tag)
            return

        flashing_process = flash_mote(bootload=bootload,
                                      board=board,
                                      toolchain=toolchain[board],
                                      openwsn_fw_folder=self.openwsn_fw_folder,
                                      target=target)
        print(flashing_process)

        # TODO: We need to add check here to be sure that the flashing went smoothly
        channel.basic_ack(delivery_tag=basic_deliver.delivery_tag)

    def handle_sniffer_start(self, channel, basic_deliver, properties, body):
        """
        Launching of all the sniffing processes:

        - Openvisualizer with rover enabled
        - tshark on tun0
        - pydispatcher sniffer through rover

        :param channel:
        :param basic_deliver:
        :param properties:
        :param body:
        :return:
        """
        try:
            data = json.loads(body.decode())
        except ValueError:
            channel.basic_ack(delivery_tag=basic_deliver.delivery_tag)
            log.warning("No JSON could be decoded from %s" % body)
            return
        log.debug("Data: %s" % data)

        # Optional tshark filter
        display_filter = data.get("display_filter", "")

        openvisualizer_process = self.launch_openvisualizer()
        time.sleep(1)
        if openvisualizer_process.poll() is not None:
            print("Problem: The Agent didn't successfully launched openvisualizer")
            (stdout, stderr) = openvisualizer_process.communicate()
            print(stdout, stderr)
            return

        # We store this process to be able to terminate it gracefully later on
        self.sub_processes["openvisualizer"] = openvisualizer_process

        while not self.rover_socket_present():
            print("Rover socket not yet detected")
            time.sleep(1)

        while not self.tun_present():
            print("Tun interface not yet detected")
            time.sleep(1)

        # tshark sniffer
        print("Launching Tshark sniffer")
        tshark_process = multiprocessing.Process(target=sniff_hexdump_with_tshark,
                                                 kwargs={"amqp_url": self.amqp_url,
                                                         "display_filter": display_filter})
        self.sub_processes["tshark"] = tshark_process
        tshark_process.start()
        print("tshark sniffer launched")

        # Rover sniffer
        print("Launching Rover sniffer")
        rover_sniffer_process = multiprocessing.Process(target=sniff_pydispatcher_with_rover,
                                                        kwargs={
                                                            "amqp_url": self.amqp_url,
                                                            "subscription_zmq": self.sub_zmq,
                                                            "admin_zmq": self.admin_zmq
                                                        })
        self.sub_processes["openvisualizer_sniff"] = rover_sniffer_process
        rover_sniffer_process.start()
        print("Rover sniffer launched")
        channel.basic_ack(delivery_tag=basic_deliver.delivery_tag)

    def do_handle_step_execute(self, question):
        acceptable_answer = ("yes", "y")
        while "Didn't received a good answer":
            answer = str(input("Is it done? > "))
            if answer in acceptable_answer:
                self.notify(MsgStimuliExecuted())
                print("Agent: Done sending user answer")
                return
            else:
                print("Sorry %s is not a correct answer" % answer)
                print("Use answer in:")
                print(acceptable_answer)

    def launch_openvisualizer(self):
        """
        We launch openvisualizer

        :return:
        """
        print("We are going to launch openvisualizer")
        command = ["sudo", "scons", "runweb", "--rover"]
        openvisualizer_process = subprocess.Popen(command,
                                                  cwd=self.openvisualizer_folder,
                                                  stdout=subprocess.PIPE,
                                                  stderr=subprocess.PIPE)
        return openvisualizer_process

    @staticmethod
    def handle_testsuite_report(channel, basic_deliver, properties, body):
        try:
            data = json.loads(body.decode())
        except ValueError:
            channel.basic_ack(delivery_tag=basic_deliver.delivery_tag)
            log.warning("No JSON could be decoded from %s" % body)
            return
        log.debug("Data: %s" % data)

        print("Congratulations you made it to the final report")
        print("Here is the report: ")
        msg = json.loads(body.decode())
        print("-------------------")
        print(msg)
        print("-------------------")
        print("Congratulations from the F-Interop team!!")
        print(testsuite_shark)
        channel.basic_ack(delivery_tag=basic_deliver.delivery_tag)

    @staticmethod
    def handle_testcase_finished(channel, basic_deliver, properties, body):
        try:
            data = json.loads(body.decode())
        except ValueError:
            channel.basic_ack(delivery_tag=basic_deliver.delivery_tag)
            log.warning("No JSON could be decoded from %s" % body)
            return
        log.debug("Data: %s" % data)

        print("Yeah the test case is over")
        print("Here is the report: ")
        msg = json.loads(body.decode())
        print("-------------------")
        print(msg)
        print("-------------------")
        print("Let's swim to the next one")
        print(testcase_shark)

    def send_solicitation(self):
        print("Agent: Sending solicitation")
        self.notify(MsgAgentSolicitation(), mandatory=True)
        print("Agent: Solicitation sent.")

    def start_session(self):
        print("Let's start the session")
        self.notify(MsgInteropSessionConfiguration(tests=self.tests), mandatory=True)
        self.notify(MsgTestSuiteStart())

    @staticmethod
    def rover_socket_present():
        """
        Test if the rover admin socket is present.
        This socket is used to send control command to a mote through
        the Rover plugin in openvisualizer
        """
        host, port = "0.0.0.0", 60000
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        return sock.connect_ex((host, port)) == 0

    @staticmethod
    def tun_present():
        """
        Check if there is a tun interface to sniff upon
        :return:
        """
        tun_interface = "tun0"
        return subprocess.call(["ip", "a", "show", tun_interface]) == 0

    def handle_ping(self, channel, basic_deliver, properties, body):
        """

        Args:
            body:

        Returns:
        :param body:
        :param properties:
        :param channel:
        :param basic_deliver:
        """
        try:
            data = json.loads(body.decode())
        except ValueError:
            channel.basic_ack(delivery_tag=basic_deliver.delivery_tag)
            log.warning("No JSON could be decoded from %s" % body)
            return
        log.debug("Data: %s" % data)

        msg = json.loads(body.decode())

        if not msg:
            log.info("No message obtained")
            return

        command = []

        # Default version is ping
        version = {"IPv6": "ping6", "IPv4": "ping"}
        requested_version = msg.get("version", "IPv6")
        executable = version.get(requested_version)
        command.append(executable)

        # default packet count is 1
        count_option = msg.get("count", 1)
        command.extend(["-c", str(count_option)])

        # network interface, default is None
        interface_option = msg.get("interface", "")
        if interface_option:
            command.extend(["-I", interface_option])

        # run the ping
        command.append(msg["host"])
        log.info("command launched: %s" % command)
        p = subprocess.check_output(command)

        log.info("result: %s" % p)

        answer = {"mandatory": True, "body": p}
        if properties.correlation_id:
            answer["properties"] = pika.BasicProperties(correlation_id=properties.correlation_id)
            answer["routing_key"] = properties.reply_to
            answer["exchange"] = ""
        else:
            answer["exchange"] = self.exchange
            answer["routing_key"] = "control.agent.ping.reply"

        channel.basic_publish(**answer)
        # channel.basic_publish(
        #     exchange='',
        #     mandatory=True,
        #     routing_key=properties.reply_to,
        #     properties=pika.BasicProperties(correlation_id=properties.correlation_id),
        #     body=p
        # )
        print(answer)
        channel.basic_ack(delivery_tag=basic_deliver.delivery_tag)

    def handle_zmq_subscription_admin(self, channel, basic_deliver, properties, body):
        """
        Add a subscription to the list of message published by OpenWSN
        pydispatcher on a pub socket

        :param channel:
        :param basic_deliver:
        :param properties:
        :param body:
        :return:
        """
        try:
            data = json.loads(body.decode())
        except ValueError:
            channel.basic_ack(delivery_tag=basic_deliver.delivery_tag)
            log.warning("No JSON could be decoded from %s" % body)
            return
        log.debug("Data: %s" % data)

        d = json.loads(body.decode())
        with zmq.Context() as context:
            with context.socket(zmq.REQ) as admin_socket:
                admin_socket.connect(self.admin_zmq)
                # To subscribe
                admin_socket.send_json({
                    "sub": d.get("subscriptions", [])
                })
                response = admin_socket.recv()

                channel.basic_publish(
                    exchange='',
                    mandatory=True,
                    routing_key=properties.reply_to,
                    properties=pika.BasicProperties(correlation_id=properties.correlation_id),
                    body=response
                )
        channel.basic_ack(delivery_tag=basic_deliver.delivery_tag)

    def handle_zmq_injection(self, channel, basic_deliver, properties, body):
        """
        Inject a given message on the OpenWSN pydispatcher

        :param channel:
        :param basic_deliver:
        :param properties:
        :param body:
        :return:
        """
        try:
            data = json.loads(body.decode())
        except ValueError:
            channel.basic_ack(delivery_tag=basic_deliver.delivery_tag)
            log.warning("No JSON could be decoded from %s" % body)
            return
        log.debug("Data: %s" % data)

        d = json.loads(body.decode())
        with zmq.Context() as context:
            with context.socket(zmq.REQ) as publisher:
                publisher.connect(self.inject_zmq)
                publisher.send_json(d)

    def handle_sniffing_channel(self, channel, basic_deliver, properties, body):
        try:
            data = json.loads(body.decode())
        except ValueError:
            channel.basic_ack(delivery_tag=basic_deliver.delivery_tag)
            log.warning("No JSON could be decoded from %s" % body)
            return

        sniffing_channel = data.get("channel", None)
        if sniffing_channel not in range(11, 27):
            channel.basic_ack(delivery_tag=basic_deliver.delivery_tag)
            log.warning("Channel %d is incorrect" % channel)
            return

        serial_port = data.get("serial_port", None)
        if not serial_port:
            channel.basic_ack(delivery_tag=basic_deliver.delivery_tag)
            log.warning("Serial port %s is incorrect" % serial_port)
            return

        # TODO: Replace with a direct serial port write
        # with zmq.Context() as context:
        #     with context.socket(zmq.REQ) as publisher:
        #         publisher.connect(self.inject_zmq)
        #         publisher.send_json(
        #             transmitting_channel(channel=sniffing_channel,
        #                                  serial_port=serial_port)
        #         )
        #         print("sent request to change channel sniffing to %d on serial_port: %s" % (sniffing_channel, serial_port))
        #         r = publisher.recv_json()
        #         print(r)
