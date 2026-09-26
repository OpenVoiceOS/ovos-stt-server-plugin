# pylint: disable=missing-docstring,redefined-outer-name,protected-access
"""End-to-end tests for the server_type adapter over a real socket.

The plugin *is* the client, so these run the real plugin (real ``requests``
HTTP) against a real local server speaking the vendor wire format. No mocking,
no external network.
"""
import json
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import pytest

from ovos_plugin_manager.utils.audio import AudioData
from ovos_stt_plugin_server import OVOSHTTPServerSTT


def _audio() -> AudioData:
    return AudioData(b"\x00\x00" * 16000, 16000, 2)


class _VendorHandler(BaseHTTPRequestHandler):
    def log_message(self, *_):
        pass

    def _json(self, obj):
        body = json.dumps(obj).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        self.rfile.read(length)
        path = self.path.split("?")[0]
        if path.endswith("/v1/audio/transcriptions"):  # OpenAI
            self._json({"text": "hello world"})
        elif path.endswith("/v1/listen"):  # Deepgram
            self._json({"results": {"channels": [
                {"alternatives": [{"transcript": "hello world"}]}]}})
        else:
            self.send_response(404)
            self.end_headers()


@pytest.fixture(scope="module")
def vendor_server():
    srv = ThreadingHTTPServer(("127.0.0.1", 0), _VendorHandler)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    yield f"http://127.0.0.1:{srv.server_address[1]}"
    srv.shutdown()


def test_openai_adapter_end_to_end(vendor_server):
    stt = OVOSHTTPServerSTT(config={"server_type": "openai", "url": vendor_server,
                                    "api_key": "sk-test"})
    assert stt.execute(_audio(), language="en") == "hello world"


def test_deepgram_adapter_end_to_end(vendor_server):
    stt = OVOSHTTPServerSTT(config={"server_type": "deepgram",
                                    "url": f"{vendor_server}/deepgram",
                                    "api_key": "dg-test"})
    assert stt.execute(_audio(), language="en") == "hello world"
