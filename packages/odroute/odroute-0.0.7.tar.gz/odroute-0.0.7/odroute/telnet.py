# -*- coding: utf-8 -*-
import re
import time
from tornado import gen
from tornado.iostream import StreamClosedError
from tornado.tcpserver import TCPServer

COMMANDS_HELP = '''
# odroute telnet interface
  commands:
  help:                     returns available list of commands
  input.list                returns router inputs [<port>]
  input.current             returns active input [<port>]
  input.force <port>|auto   force input on <port>; returns forced|auto input [<port>]
  output.list               returns router outputs [<tcp://host:port>]
'''

COMMANDS = [
    'help',
    'input.list',
    'input.list (?:[a-z]+)',
    'input.current',
    'input.force (?:[0-9]+|auto)',
    'output.list',
]


class TelnetServer(TCPServer):
    def __init__(self, router):

        self.router = router

        super(TelnetServer, self).__init__()

    @gen.coroutine
    def handle_stream(self, stream, address):
        """
        handle telnet connection
        http://www.tornadoweb.org/en/stable/gen.html#tornado-gen-simplify-asynchronous-code
        """
        while True:
            try:
                command = yield stream.read_until(b'\n')
                result = self.handle_command(command.strip())
                yield stream.write(result)
            except StreamClosedError:
                break

    def handle_command(self, command):
        """
        handles incoming telnet commands & calls respective methods
        telnet: 
        `foo.bar abc xzz`
        is mapped to:
        `self.cmd_foo_bar(*['abc', 'xyz'])`
        """
        if not re.match('(' + ')|('.join(COMMANDS) + ')', command):
            return b'invalid command. try "help"\n'

        _c = command.split(' ')
        _cmd, _args = _c[0].replace('.', '_'), _c[1:]

        return getattr(self, 'cmd_' + _cmd)(*_args)

    ###################################################################
    # commands available through telnet interface
    ###################################################################
    def cmd_help(self):
        """
        returns available list of commands
        """
        return COMMANDS_HELP

    def cmd_input_list(self, *args):
        """
        returns router inputs
        """
        result = b''

        if 'detail' in args:
            result += b'port\tinput\tcurrent\tlast beat\n'
            for input in self.router._inputs:
                result += b'{port}\t  {input}\t   {current}\t  {last_beat:.2f}s\n'.format(
                    port=input.port,
                    input='*' if input.is_available() else '-',
                    current='*' if self.router._current_input and self.router._current_input.port == input.port else '-',
                    last_beat=time.time() - input._last_beat
                )
        else:
            for input in self.router._inputs:
                result += b'{}\n'.format(input.port)

        return result

    def cmd_output_list(self):
        """
        returns router outputs
        """
        result = b''
        for output in self.router._outputs:
            result += b'{}\n'.format(output.output)
        return result

    def cmd_input_current(self):
        """
        returns active router input
        """
        if not self.router._current_input:
            return b'none\n'
        return b'{}\n'.format(self.router._current_input.port)

    def cmd_input_force(self, *args):
        """
        force input on given port
        """

        _forced_port = args[0].strip()
        _available_ports = [i.port for i in self.router._inputs] + ['auto']

        if _forced_port == 'auto':
            self.router._forced_input = None
            return b'auto\n'

        if not int(_forced_port) in _available_ports:
            return b'port {} not available\n'.format(_forced_port)

        self.router._forced_input = int(_forced_port)

        return b'{}\n'.format(_forced_port)
