from queue import Queue
from uuid import uuid4
import requests
from ovos_plugin_manager.stt import STT
from ovos_plugin_manager.stt import StreamingSTT, StreamThread


class OVOSHTTPServerSTT(STT):
    """STT interface for the OVOS-HTTP-STT-Server"""

    def __init__(self, config=None):
        super().__init__(config)
        self.url = self.config.get("url") or "https://stt.strongthany.cc/stt"

    def execute(self, audio, language=None):
        self.response = requests.post(self.url, data=audio.get_wav_data(),
                                      headers={"Content-Type": "audio/wav"},
                                      params={"session_id": language or self.lang})
        return self.response.text if self.response else None


class OVOSHTTPStreamServerStreamThread(StreamThread):
    def __init__(self, queue, language, url="https://stt.strongthany.cc/stream"):
        super().__init__(queue, language)
        self.url = url
        self.session = requests.Session()

    def reset_model(self, session_id=None):
        self.session_id = session_id or str(uuid4())
        # reset the model for this session
        response = self.session.post(f"{self.url}/start",
                          params={"lang": self.language,
                                  "uuid": self.session_id})

    def handle_audio_stream(self, audio, language):
        lang = language or self.language
        response = self.session.post(f"{self.url}/audio",
                                     params={"lang": lang,
                                             "uuid": self.session_id},
                                     data=audio, stream=True)
        self.text = response.json()["transcript"]
        return self.text

    def finalize(self):
        """ return final transcription """
        try:
            response = self.session.post(f"{self.url}/end",
                                         params={"lang": self.language,
                                                 "uuid": self.session_id})
            self.text = response.json()["transcript"] or self.text
        except:
            pass
        return self.text


class OVOSHTTPStreamServerSTT(StreamingSTT):
    """Streaming STT interface for the OVOS-HTTP-STT-Server"""

    def create_streaming_thread(self):
        url = self.config.get('url') or "https://stt.strongthany.cc/stream"
        self.queue = Queue()

        stream = OVOSHTTPStreamServerStreamThread(self.queue, self.lang, url)
        stream.reset_model()
        return stream
