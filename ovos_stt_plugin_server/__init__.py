import requests
from ovos_plugin_manager.stt import STT



class OVOSHTTPServerSTT(STT):
    """STT interface for the OVOS-HTTP-STT-Server"""
    def __init__(self, config=None):
        super().__init__(config)
        self.url = self.config.get("url") or "http://0.0.0.0:8080/stt"

    def execute(self, audio, language=None):
        self.response = requests.post(self.url, data=audio.get_wav_data(),
                                      headers ={"Content-Type": "audio/wav"},
                                      params={"lang": language or self.lang})
        return self.response.text if self.response else None

