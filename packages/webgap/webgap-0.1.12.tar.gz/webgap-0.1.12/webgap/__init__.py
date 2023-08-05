import logging
import steov

class RequestsWebGap:
    _noop_house = steov.Anon(persist=steov.noop)

    def __init__ (self, requests, session_factory=None, house=None, logger=None):
        self._requests = requests
        self._session_factory = session_factory or self._requests.Session
        self._house = house or self._noop_house
        self._logger = logger or logging.getLogger(__name__)

    def _log_call_request (self, id, request, timeout):
        self._logger.debug("call.request.id: " + str(id))
        self._logger.debug("call.request.url: " + request.url)
        self._logger.debug("call.request.method: " + request.method)
        for k, v in request.headers.items():
            self._logger.debug("call.request.header." + k + ": " + v)
        self._logger.debug("call.request.body.sha256: " + str(self._house.persist(request.body)))
        self._logger.debug("call.request.timeout: " + str(None if timeout is None else timeout.total_seconds()))

    def _log_call_error (self, id, exception, stacktrace):
        self._logger.debug("call.error.id: " + str(id))
        for k, v in getattr(exception, "__dict__", {}).items():
            self._logger.debug("call.error.exception." + k + ": " + repr(v))
        for line in stacktrace.splitlines(keepends=False):
            self._logger.debug("call.error.stacktrace.line: " + line)

    def _log_call_response (self, id, response):
        self._logger.debug("call.response.id: " + str(id))
        self._logger.debug("call.response.status: " + str(response.status_code))
        self._logger.debug("call.response.message: " + response.reason)
        for k, v in response.headers.items():
            self._logger.debug("call.response.header." + k + ": " + v)
        self._logger.debug("call.response.body.sha256: " + str(self._house.persist(response.content)))
        self._logger.debug("call.response.elapsed: " + str(response.elapsed.total_seconds()))

    def call (self, url, method="GET", headers={}, body=None, timeout=None):
        import uuid
        call_id = uuid.uuid4()
        timeout_sec = None if timeout is None else timeout.total_seconds()
        request = self._requests.Request(url=url, method=method, headers=headers, data=body)
        with self._session_factory() as session:
            prepared_request = session.prepare_request(request)
            self._log_call_request(call_id, prepared_request, timeout)
            try:
                response = session.send(prepared_request, timeout=timeout, stream=True)
            except Exception as ex:
                # TODO sometimes `ex` can hold a response object. log it?
                self._log_call_error(call_id, ex, steov.format_exc())
                raise
            for i, historical_response in enumerate(list(response.history) + [response]):
                if i > 0:
                    self._log_call_request(call_id, historical_response.request)
                self._log_call_response(call_id, historical_response)
            return steov.Anon({
                "status": response.status_code,
                "message": response.reason,
                "headers": dict(response.headers),
                "body": response.content,
                "_orig_response": response,
            })
