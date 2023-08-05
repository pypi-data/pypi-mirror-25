# -*- coding: utf-8 -*-
import logging
import sys
import time
from functools import partial
from multiprocessing import Queue

import zmq
from zmq.eventloop import ioloop
from zmq.eventloop.zmqstream import ZMQStream

logger = logging.getLogger(__name__)

ioloop.install()


class StreamInput(object):
    """
    Input instance.
    """

    connected = False

    def __init__(self, zmq_ctx, port, failover_seconds):
        self.zmq_ctx = zmq_ctx
        self.port = port
        self.failover_seconds = failover_seconds
        self._last_beat = time.time() - float(failover_seconds)
        self.stream = self.bind()

    def __str__(self):
        return '<StreamInput: port {}>'.format(self.port)

    def bind(self):
        """
        bind zmq input port 
        """
        logger.debug('Binding socket on port {} - failover delay: {}s'.format(
            self.port,
            self.failover_seconds,
        ))
        s = self.zmq_ctx.socket(zmq.SUB)
        s.bind('tcp://*:{port}'.format(port=self.port))
        s.setsockopt(zmq.SUBSCRIBE, "")
        self.connected = True
        return ZMQStream(s)

    def stop(self):
        logger.debug('Stopping socket on port {}'.format(self.port))
        # close zmq socket
        self.stream.close()
        self.connected = False

    def tick(self):
        # triggered on every `on_recv` - used to track input availability.
        self._last_beat = time.time()

    def is_available(self):
        """
        check if the input instance is 'available':
        "last time ticked less than failover duration"
        """
        return self._last_beat > (time.time() - float(self.failover_seconds))


class StreamOutput(object):
    """
    Output instance. Connects to remote socket and relies the zmq frames.
    """

    connected = False

    def __init__(self, zmq_ctx, output):
        self.zmq_ctx = zmq_ctx
        self.output = output
        self.connection = self.connect()

    def __str__(self):
        return '<StreamOutput: port {}>'.format(self.output)

    def connect(self):
        logger.debug('Connecting output to {}'.format(self.output))
        c = self.zmq_ctx.socket(zmq.PUB)
        c.connect(self.output)
        self.connected = True
        return c

    def send(self, frame):
        """
        passing the zmq frame to the output's connection
        """
        self.connection.send(frame, zmq.NOBLOCK)


class StreamRouter(object):
    """
    Router instance. Handles input and output connections & routing (priority).
    """
    _inputs = []
    _current_input = None
    _forced_input = None
    _outputs = []
    _router = None
    _telnet_server = None

    def __init__(self, source_ports, destinations, delay, **options):

        self.failover_seconds = delay
        self.zmq_ctx = zmq.Context()
        self.source_ports = source_ports
        self.destinations = destinations
        self.input_queue = Queue()
        self.output_queue = Queue()

    def connect(self):

        self.bind_inputs()
        self.connect_outputs()

    def bind_inputs(self):

        for port in self.source_ports:
            i = StreamInput(self.zmq_ctx, port, self.failover_seconds)
            logger.info('Created socket on port {}'.format(port))
            self._inputs.append(i)

    def connect_outputs(self):

        for destination in self.destinations:
            o = StreamOutput(self.zmq_ctx, destination)
            logger.info('Connected output to {}'.format(destination))
            self._outputs.append(o)

    def set_current_input(self):

        current_input = None

        # force input
        if self._forced_input:
            current_input = next(i for i in self._inputs if i.port == self._forced_input)

        # Loop through the inputs and return the first available one.
        if not current_input:
            current_input = next(i for i in self._inputs if i.is_available())
            # for i in self._inputs:
            #     if i.is_available():
            #         current_input = i
            #         break

        if (current_input and self._current_input) and (current_input != self._current_input):
            logger.info('Switching inputs: {} to {}'.format(
                self._current_input.port, current_input.port)
            )

        self._current_input = current_input

    def route(self, stream, msg, input):
        """
        Routes the active input to all outputs
        """

        # Trigger a 'heartbeat' tick on the input.
        input.tick()

        self.set_current_input()

        if input == self._current_input:
            for o in self._outputs:
                o.send(msg[0])

    def run(self):

        for i in self._inputs:
            i.stream.on_recv_stream(partial(self.route, input=i))

        # self.telnet_server = TelnetServer(router=self)
        # self.telnet_server.listen(4444)

        if self._telnet_server:
            self._telnet_server.start()

        # Start the tornado ioloop
        # http://pyzmq.readthedocs.io/en/latest/eventloop.html#futures-and-coroutines
        ioloop.IOLoop.instance().start()

        while True:
            pass

    def stop(self):

        logger.info('Stopping router')

        for i in self._inputs:
            logger.info('Stopping input on port {}'.format(i.port))
            i.stop()

        sys.exit()
