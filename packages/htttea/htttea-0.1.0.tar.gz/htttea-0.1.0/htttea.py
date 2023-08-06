import cgi
import datetime
import errno
import http
import random
import tempfile
import threading
import time
from typing import (
    Any,
    Callable,
    Dict,
    Iterator,
    List,
    Optional,
    Tuple,
)
import wsgiref.handlers
import wsgiref.simple_server


__all__ = ['Htttea', 'Response', 'HttteaError', 'TimeoutError']
__author__ = "Motoki Naruse"
__copyright__ = "Motoki Naruse"
__credits__ = ["Motoki Naruse"]
__email__ = "motoki@naru.se"
__license__ = "MIT"
__maintainer__ = "Motoki Naruse"
__version__ = '0.1.0'


class HttteaError(Exception):
    pass


class TimeoutError(HttteaError):
    pass


class Response:
    def __init__(
            self,
            *,
            body: bytes=b"",
            status: http.HTTPStatus=http.HTTPStatus.OK,
            headerlist: List[Tuple[str, str]]=[],
            content_type: str="text/plain; charset=utf-8"
    ) -> None:
        self.body = body
        self.status = status
        self.headerlist = headerlist
        self.content_type = content_type


class Request:
    method = None
    content_type = None
    raw_body = None
    data: Dict[str, Any] = {}
    path: str = None


class ServerHandler(wsgiref.handlers.SimpleHandler):  # type: ignore
    server_software = "Htttea/{}".format(__version__)


class RequestHandler(wsgiref.simple_server.WSGIRequestHandler):  # type: ignore
    def handle(self):
        self.raw_requestline = self.rfile.readline(65537)
        if not self.parse_request():
            return

        handler = ServerHandler(self.rfile, self.wfile, self.get_stderr(), self.get_environ())
        handler.request_handler = self
        handler.run(self.server.get_app())


class Application:
    def __init__(self) -> None:
        self.response = Response()
        self.request = Request()
        self.requested = False

    def _to_data(self, body: bytes, environ: Dict[str, Any]) -> Dict[str, Any]:
        with tempfile.TemporaryFile() as f:
            f.write(self.request.raw_body)
            f.seek(0)
            try:
                form = cgi.FieldStorage(fp=f, environ=environ, keep_blank_values=True)
            except TypeError:
                return {}
            else:
                return {key: form[key].value for key in form}  # type: ignore

    def __call__(
            self,
            environ: Dict[str, Any],
            start_response: Callable[[str, List[Tuple[str, str]]], None]
    ) -> Iterator[bytes]:
        self.request.content_type = environ['CONTENT_TYPE']
        self.request.method = environ['REQUEST_METHOD']
        if self.request.method in {'POST', 'PUT'}:
            self.request.raw_body = environ['wsgi.input'].read(int(environ['CONTENT_LENGTH']))
            self.request.data = self._to_data(self.request.raw_body, environ)
        else:
            pass

        self.request.path = environ['PATH_INFO']
        self.requested = True
        start_response(
            "{} {}".format(self.response.status.value, self.response.status.name),
            [
                ('Content-Type', self.response.content_type),
                ('Content-Length', str(len(self.response.body)))
            ] + self.response.headerlist
        )
        return iter([self.response.body])


class Server:
    def __init__(self, host: str, port: int, application: Application) -> None:
        self.port = port
        self._server = wsgiref.simple_server.make_server(  # type: ignore
            host, port, application, handler_class=RequestHandler)
        self._thread = threading.Thread(target=self._server.serve_forever)

    def start(self):
        self._thread.start()

    def stop(self):
        self._server.shutdown()


class Htttea:
    def __init__(self, *, host: str='localhost', port: Optional[int]=None) -> None:
        """

        :param port: Specify port number. If you use same port number in short time, the number
        might not released yet.
        """
        self._host = host
        self._request = None
        self._application = Application()
        self._server = self._bind_server(port)
        self._port = self._server.port

    def _bind_server(self, port: Optional[int]) -> Server:
        def bind_server(port: int) -> Server:
            return Server(self._host, port, self._application)

        if port is not None:
            return bind_server(port)

        while True:
            try:
                return bind_server(random.randint(49152, 65535))
            except OSError as e:
                if e.errno != errno.EADDRINUSE:
                    raise

    @property
    def url(self) -> str:
        return "http://{}:{}".format(self._host, self._port)

    @property
    def request(self) -> Request:
        return self._application.request

    @property
    def response(self) -> Response:
        return self._application.response

    @response.setter
    def response(self, response: Response) -> None:
        self._application.response = response

    def __enter__(self) -> 'Htttea':
        self._server.start()
        return self

    def __exit__(self, exec_type, exec_value, exec_traceback) -> bool:
        self._server.stop()
        return False

    def wait_until_request(self, *, timeout: float=10.0) -> None:
        elapsed_time = 0.0
        reference_time = datetime.datetime.now()
        while elapsed_time < timeout and not self._application.requested:
            time.sleep(0.01)
            elapsed_time = (datetime.datetime.now() - reference_time).total_seconds()

        if not self._application.requested:
            raise TimeoutError("No request in {} seconds".format(timeout))
