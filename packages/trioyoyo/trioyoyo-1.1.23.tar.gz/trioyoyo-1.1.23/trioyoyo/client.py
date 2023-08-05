#!/usr/bin/python3
# Copyright (c) 2016-2017, henry232323
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.
"""
A small simple port of oyoyo to use trioyoyo instead of its original
threading client. Creating an IRCClient instance will create the protocol
instance.

To start the connection run IRCClient.connect(); (coroutine)
"""

import logging
from typing import Union, Callable, Type

import trio

from ._oyoyo.parse import parse_raw_irc_command
from ._oyoyo.cmdhandler import IRCClientError, CommandHandler


class IRCClient(object):
    host = None
    address = None
    port = None
    socket = None
    bufsize = 1024

    def __init__(self, host: str=None, port: int=None, bufsize: int=1024):
        """
        A basic Async IRC client. Use coroutine IRCClient.connect to initiate
        the connection. Takes the event loop, a host (address, port) and if
        wanted an alternate protocol can be defined. By default will use the
        ClientProtocol class, which just uses the IRCClient's tracebacks and
        passes received data to the client.
        """
        self.host = host
        self.port = port
        self.bufsize = bufsize

        self.logger = logging.getLogger("trioyoyo")
        self.logger.setLevel(logging.INFO)

    def __repr__(self):
        return "{0}(address={1}, port={2}, bufsize={3})".format(self.__class__.__name__, self.host[0], self.host[1], self.bufsize)

    ############# Callbacks #############

    async def connection_made(self):
        """Called on a successful connection, by default forwarded by
        protocol.connection_made"""
        logging.info('connecting to %s:%s' % self.address)

    async def data_received(self, data: bytes):
        """Called when data is received by the connection, by default
        forwarded by protocol.data_received, passes bytes not str"""
        logging.info('received: %s' % data.decode())

    async def connection_lost(self):
        """Called when the connection is dropped."""
        logging.info('connection dropped')

    ############# Methods #############

    async def connect(self) -> None:
        """Initiate the connection, creates a connection and assigns the created socket to `client.socket`. Blocking"""
        buffer = bytes()
        with trio.socket.socket() as client_sock:
            self.socket = client_sock
            self.address = await self.socket.resolve_remote_address((self.host, self.port))
            await client_sock.connect(self.address)
            async with trio.open_nursery() as nursery:
                nursery.spawn(self.connection_made)
                while True:
                    if not self.socket._sock._closed:
                        data = await client_sock.recv(self.bufsize)
                        if not data:
                            break
                        buffer += data
                        pts = buffer.split(b"\n")
                        buffer = pts.pop()
                        for el in pts:
                            nursery.spawn(self.data_received, el)
                    else:
                        break
                nursery.spawn(self.connection_lost)

    async def send(self, *args: Union[bytes, str]) -> None:
        """Send a message to the connected server. all arguments are joined
        with a space for convenience, for example the following are identical

        >>> cli.send("JOIN %s" % some_room)
        >>> cli.send("JOIN", some_room)

        In python 3, all args must be of type str or bytes, *BUT* if they are
        str they will be converted to bytes with the encoding specified by the
        'encoding' keyword argument (default 'utf8').
        """
        # Convert all args to bytes if not already
        bargs = []
        for arg in args:
            if isinstance(arg, str):
                bargs.append(arg.encode())
            elif isinstance(arg, bytes):
                bargs.append(arg)
            else:
                raise IRCClientError('Refusing to send one of the args from provided: %s'
                                     % repr([(type(arg), arg) for arg in args]))

        msg = b" ".join(bargs)
        await self.send_raw(msg + b"\r\n")
        logging.info('---> send "%s"' % msg)

    async def send_msg(self, message: str) -> None:
        """Send a str to the server from absolute raw, none of the formatting
        from IRCClient.send"""
        await self.socket.sendall(message.encode())

    async def send_raw(self, data: bytes) -> None:
        """Send raw bytes to the server, none of the formatting from IRCClient.send"""
        await self.socket.sendall(data)

    def close(self) -> None:
        """Close the connection"""
        logging.info('close transport')
        self.socket.close()

    def run(self) -> None:
        """Starts the client, blocking. Use `client.connect` for a runnable coro. Essentially `trio.run(self.connect)`"""
        trio.run(self.connect)


class CommandClient(IRCClient):
    """IRCClient, using a command handler"""
    def __init__(self, cmd_handler: Callable[[IRCClient], CommandHandler], *args, **kwargs):
        """Takes a command handler (see oyoyo.cmdhandler.CommandHandler)
        whose attributes are the commands you want callable, for example
        with a privmsg cmdhandler.privmsg will be awaited with the
        appropriate *args, decorate methods with @protected to make it
        uncallable as a command"""
        IRCClient.__init__(self, *args, **kwargs)
        self.command_handler: CommandHandler = cmd_handler(self)

    async def data_received(self, data):
        """On IRCClient.data_received parse for a command and pass to the
        command_handler to run()"""
        prefix, command, args = parse_raw_irc_command(data)
        await self.command_handler.run(command, prefix, *args)

