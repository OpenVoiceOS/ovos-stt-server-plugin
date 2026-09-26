# pylint: disable=missing-docstring,redefined-outer-name,protected-access
"""Unit tests for the server_type universal adapter (mocked HTTP)."""
from unittest.mock import patch, MagicMock

import pytest

from ovos_plugin_manager.utils.audio import AudioData
from ovos_stt_plugin_server import OVOSHTTPServerSTT


def _audio() -> AudioData:
    return AudioData(b"\x00\x00" * 16000, 16000, 2)


def _resp(ok=True, json_data=None, text="") -> MagicMock:
    r = MagicMock()
    r.ok = ok
    r.status_code = 200 if ok else 500
    r.text = text
    if json_data is not None:
        r.json.return_value = json_data
    return r


def test_default_server_type_is_ovos():
    assert OVOSHTTPServerSTT().server_type == "ovos"


def test_ovos_path_unchanged():
    stt = OVOSHTTPServerSTT(config={"url": "http://localhost:9666/stt"})
    with patch("ovos_stt_plugin_server.requests.post", return_value=_resp(text="hello")) as post:
        out = stt.execute(_audio(), language="en")
    assert out == "hello"
    assert post.call_args.args[0] == "http://localhost:9666/stt"


def test_openai_request_shape():
    stt = OVOSHTTPServerSTT(config={"server_type": "openai",
                                    "url": "http://localhost:8080",
                                    "api_key": "sk-test", "model": "whisper-1"})
    with patch("ovos_stt_plugin_server.requests.post",
               return_value=_resp(json_data={"text": "hello world"})) as post:
        out = stt.execute(_audio(), language="pt")
    assert out == "hello world"
    args, kwargs = post.call_args
    assert args[0] == "http://localhost:8080/v1/audio/transcriptions"
    assert kwargs["headers"]["Authorization"] == "Bearer sk-test"
    assert "file" in kwargs["files"]
    assert kwargs["data"]["model"] == "whisper-1"
    assert kwargs["data"]["language"] == "pt"


def test_openai_appends_v1_once():
    stt = OVOSHTTPServerSTT(config={"server_type": "openai", "url": "http://localhost:8080/v1"})
    with patch("ovos_stt_plugin_server.requests.post",
               return_value=_resp(json_data={"text": "x"})) as post:
        stt.execute(_audio())
    assert post.call_args.args[0] == "http://localhost:8080/v1/audio/transcriptions"


def test_deepgram_request_shape():
    stt = OVOSHTTPServerSTT(config={"server_type": "deepgram",
                                    "url": "http://localhost:8080/deepgram",
                                    "api_key": "dg-test"})
    payload = {"results": {"channels": [{"alternatives": [{"transcript": "hello world"}]}]}}
    with patch("ovos_stt_plugin_server.requests.post",
               return_value=_resp(json_data=payload)) as post:
        out = stt.execute(_audio(), language="en")
    assert out == "hello world"
    args, kwargs = post.call_args
    assert args[0] == "http://localhost:8080/deepgram/v1/listen"
    assert kwargs["headers"]["Authorization"] == "Token dg-test"


def test_vendor_type_requires_url():
    stt = OVOSHTTPServerSTT(config={"server_type": "openai"})
    with pytest.raises(RuntimeError):
        stt.execute(_audio())


def test_unknown_server_type_returns_none():
    stt = OVOSHTTPServerSTT(config={"server_type": "bogus", "url": "http://localhost:8080"})
    # unknown type raises internally, is caught, and execute exhausts urls -> None
    assert stt.execute(_audio()) is None
