from queue import Queue

import requests
from ovos_plugin_manager.stt import StreamingSTT, StreamThread


class OVOSHTTPStreamServerStreamThread(StreamThread):
    def __init__(self, queue, language, url="http://0.0.0.0:8080"):
        super().__init__(queue, language)
        self.url = url

    def handle_audio_stream(self, audio, language):
        self.response = requests.post(self.url, data=audio, stream=True)
        self.text = self.response.text if self.response else None
        return self.text


class OVOSHTTPStreamServerSTT(StreamingSTT):
    """Streaming STT interface for the OVOS-HTTP-STT-Server"""

    def create_streaming_thread(self):
        self.queue = Queue()
        return OVOSHTTPStreamServerStreamThread(
            self.queue,
            self.lang,
            self.config.get('host') or "http://0.0.0.0:8080"
        )
