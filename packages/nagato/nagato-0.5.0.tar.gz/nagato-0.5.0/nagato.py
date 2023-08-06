import argparse
import asyncio
import logging

from urllib.parse import urlparse


__version__ = '0.5.0'

_logger = logging.getLogger(__name__)

_loop = asyncio.get_event_loop()


def set_logger(level):
    try:
        log_level = [logging.WARNING, logging.INFO, logging.DEBUG][level]
        _logger.setLevel(log_level)
    except IndexError:
        _logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        '%(asctime)s {%(module)s:%(levelname)s}: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S')
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    _logger.addHandler(stream_handler)


@asyncio.coroutine
def tunnel_stream(reader, writer, closing):
    try:
        while True:
            buf = yield from reader.read(65536)
            if not buf:
                break
            writer.write(buf)
    finally:
        writer.close()
        closing()


@asyncio.coroutine
def tunnel_n(reader, writer, n):
    while n > 0:
        buf = yield from reader.read(65536)
        n -= len(buf)
        writer.write(buf)

        if not buf and n > 0:
            raise EOFError


class NagatoStream:
    def __init__(self, proxy_reader, proxy_writer):
        self.proxy_reader = proxy_reader
        self.proxy_writer = proxy_writer
        self.server_reader = None
        self.server_writer = None

    @asyncio.coroutine
    def _nextline(self):
        line = yield from self.proxy_reader.readline()
        if not line:
            raise EOFError
        return line

    @asyncio.coroutine
    def _handle_tunnel(self, host, port, version):
        # open a tunneling connection
        server_reader, server_writer \
            = yield from asyncio.open_connection(host, port, loop=_loop)

        self.proxy_writer.write((
            '{} 200 Connection established\r\n'.format(version) +
            'Proxy-Agent: Nagato/{}\r\n\r\n'.format(__version__)).encode())

        # set tunneling
        reader = tunnel_stream(self.proxy_reader, server_writer,
                               lambda: self.proxy_writer.close())
        writer = tunnel_stream(server_reader, self.proxy_writer,
                               lambda: server_writer.close())
        yield from asyncio.wait([reader, writer], loop=_loop)

    @asyncio.coroutine
    def _handle_request(self):
        # read the request line
        req_line = yield from self._nextline()
        method, url, version = req_line.decode().split(' ')
        version = version.rstrip('\r\n')
        _logger.info('{} {} {}'.format(method, url, version))

        if method == 'CONNECT':
            # handle the tunneling request
            host, port = url.rsplit(':', 1)
            port = int(port)

            # drop the rest, assuming no body
            while True:
                line = yield from self._nextline()
                if line == b'\r\n':
                    break

            yield from self._handle_tunnel(host, port, version)
            raise EOFError

        # handle the HTTP request
        # handle the request line
        parsed = urlparse(url)
        try:
            host, port = parsed.netloc.rsplit(':', 1)
            port = int(port)
        except ValueError:
            host = parsed.netloc
            port = 80

        if self.server_reader is None or self.server_writer is None:
            self.server_reader, self.server_writer \
                = yield from asyncio.open_connection(host, port, loop=_loop)
            _loop.create_task(tunnel_stream(
                self.server_reader, self.proxy_writer,
                lambda: self.server_writer.close()))

        # replace by HTTPS
        parsed = parsed._replace(scheme='https')
        req_line = '{} {} {}\r\n' \
            .format(method, parsed.geturl(), version) \
            .encode()
        self.server_writer.write(req_line)

        # handle the header fields
        # check the body length
        field_lines = []
        body_len = 0
        chunked = False

        while True:
            field_line = yield from self._nextline()
            if field_line == b'\r\n':
                field_lines.append(field_line)
                break

            name, value = field_line.decode().split(':', 1)
            name = name.strip(' ').lower()
            value = value.lstrip(' ').rstrip('\r\n')

            if name == 'Host'.lower():
                # host field segmentation
                field_lines.append(b'Ho')
                self.server_writer.write(b''.join(field_lines))
                yield from self.server_writer.drain()

                self.server_writer.write('st: {}\r\n'.format(value).encode())
                field_lines = []
                continue
            elif name == 'Proxy-Connection'.lower():
                field_lines.append('Connection: {}\r\n'.format(value).encode())
                continue
            elif name == 'Content-Length'.lower():
                body_len = int(value)
            elif name == 'Transfer-Encoding'.lower():
                codings = list(x.strip(' ') for x in value.split(','))
                if 'chunked' in codings:
                    chunked = True

            field_lines.append(field_line)

        self.server_writer.write(b''.join(field_lines))

        # handle the body
        if chunked:
            while True:
                line = yield from self._nextline()
                self.server_writer.write(line)

                chunk_len = int(line.rstrip(b'\r\n'), 16)
                if chunk_len > 0:
                    yield from tunnel_n(self.proxy_reader, self.server_writer,
                                        chunk_len)

                line = yield from self._nextline()
                self.server_writer.write(line)

                if chunk_len == 0:
                    return

        if body_len > 0:
            yield from tunnel_n(self.proxy_reader, self.server_writer,
                                body_len)

    @asyncio.coroutine
    def handle_requests(self):
        try:
            while True:
                # HTTP persistent connection
                yield from self._handle_request()
        except EOFError:
            pass
        finally:
            if self.server_writer is not None:
                self.server_writer.close()
            self.proxy_writer.close()


def nagato_stream(reader, writer):
    return _loop.create_task(NagatoStream(reader, writer).handle_requests())


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-H', '--host', help="Host to bind",
                        default="localhost")
    parser.add_argument('-p', '--port', type=int,
                        help="Port to bind", default="8080")
    parser.add_argument('-v', '--verbose', default=0, action='count',
                        help="Verbose output.")

    args = parser.parse_args()

    set_logger(args.verbose)

    _logger.info('Nagato {} Starting on {}:{}'.format(
        __version__, args.host, args.port))

    coro = asyncio.start_server(nagato_stream, args.host, args.port, loop=_loop)
    server = _loop.run_until_complete(coro)

    try:
        _loop.run_forever()
    except KeyboardInterrupt:
        pass

    server.close()
    _loop.run_until_complete(server.wait_closed())
    _loop.close()
