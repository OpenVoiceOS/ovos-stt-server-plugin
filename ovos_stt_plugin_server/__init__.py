from typing import Optional
from queue import Queue
from uuid import uuid4

import requests
import random
from ovos_utils.log import LOG
from ovos_plugin_manager.stt import STT, StreamingSTT, StreamThread


class OVOSHTTPServerSTT(STT):
    """STT interface for the OVOS-HTTP-STT-Server"""

    def __init__(self, config=None):
        super().__init__(config)
        if not self.verify_ssl:
            LOG.warning("SSL verification disabled, this is not secure and should"
                             "only be used for test systems! Please set up a valid certificate!")

    @property
    def verify_ssl(self) -> bool:
        return self.config.get("verify_ssl", True)

    @property
    def public_servers(self):
        return [
            "https://fasterwhisper.ziggyai.online/stt",
            "https://stt.smartgic.io/fasterwhisper/stt"
        ]

    @property
    def urls(self) -> Optional[str]:
        urls = self.config.get("url", self.config.get("urls"))
        if urls and not isinstance(urls, list):
            urls = [urls]
        return urls

    def execute(self, audio, language=None):
        if self.urls:
            LOG.debug(f"Using user defined urls {self.urls}")
            urls = self.urls
        else:
            LOG.debug(f"Using public servers {self.public_servers}")
            urls = self.public_servers
            random.shuffle(urls)
        for url in urls:
            LOG.debug(f"chosen url {url}")
            try:
                self.response = requests.post(url, data=audio.get_wav_data(),
                                              headers={"Content-Type": "audio/wav"},
                                              params={"lang": language or self.lang},
                                              verify=self.verify_ssl)
                if self.response:
                    return self.response.text
            except:
                pass
            LOG.error(f"STT request to {url} failed")


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
                                             "uuid": self.session_id},
                                     verify=self.verify_ssl)

    def handle_audio_stream(self, audio, language):
        lang = language or self.language
        response = self.session.post(f"{self.url}/audio",
                                     params={"lang": lang,
                                             "uuid": self.session_id},
                                     data=audio, stream=True,
                                     verify=self.verify_ssl)
        self.text = response.json()["transcript"]
        return self.text

    def finalize(self):
        """ return final transcription """
        try:
            response = self.session.post(f"{self.url}/end",
                                         params={"lang": self.language,
                                                 "uuid": self.session_id},
                                         verify=self.verify_ssl)
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



# public instances
OVOSHTTPServerSTTConfig = {}

_whisper_lang = {
        "en": "english",
        "zh": "chinese",
        "de": "german",
        "es": "spanish",
        "ru": "russian",
        "ko": "korean",
        "fr": "french",
        "ja": "japanese",
        "pt": "portuguese",
        "tr": "turkish",
        "pl": "polish",
        "ca": "catalan",
        "nl": "dutch",
        "ar": "arabic",
        "sv": "swedish",
        "it": "italian",
        "id": "indonesian",
        "hi": "hindi",
        "fi": "finnish",
        "vi": "vietnamese",
        "iw": "hebrew",
        "uk": "ukrainian",
        "el": "greek",
        "ms": "malay",
        "cs": "czech",
        "ro": "romanian",
        "da": "danish",
        "hu": "hungarian",
        "ta": "tamil",
        "no": "norwegian",
        "th": "thai",
        "ur": "urdu",
        "hr": "croatian",
        "bg": "bulgarian",
        "lt": "lithuanian",
        "la": "latin",
        "mi": "maori",
        "ml": "malayalam",
        "cy": "welsh",
        "sk": "slovak",
        "te": "telugu",
        "fa": "persian",
        "lv": "latvian",
        "bn": "bengali",
        "sr": "serbian",
        "az": "azerbaijani",
        "sl": "slovenian",
        "kn": "kannada",
        "et": "estonian",
        "mk": "macedonian",
        "br": "breton",
        "eu": "basque",
        "is": "icelandic",
        "hy": "armenian",
        "ne": "nepali",
        "mn": "mongolian",
        "bs": "bosnian",
        "kk": "kazakh",
        "sq": "albanian",
        "sw": "swahili",
        "gl": "galician",
        "mr": "marathi",
        "pa": "punjabi",
        "si": "sinhala",
        "km": "khmer",
        "sn": "shona",
        "yo": "yoruba",
        "so": "somali",
        "af": "afrikaans",
        "oc": "occitan",
        "ka": "georgian",
        "be": "belarusian",
        "tg": "tajik",
        "sd": "sindhi",
        "gu": "gujarati",
        "am": "amharic",
        "yi": "yiddish",
        "lo": "lao",
        "uz": "uzbek",
        "fo": "faroese",
        "ht": "haitian creole",
        "ps": "pashto",
        "tk": "turkmen",
        "nn": "nynorsk",
        "mt": "maltese",
        "sa": "sanskrit",
        "lb": "luxembourgish",
        "my": "myanmar",
        "bo": "tibetan",
        "tl": "tagalog",
        "mg": "malagasy",
        "as": "assamese",
        "tt": "tatar",
        "haw": "hawaiian",
        "ln": "lingala",
        "ha": "hausa",
        "ba": "bashkir",
        "jw": "javanese",
        "su": "sundanese",
    }

if __name__ == "__main__":
    from speech_recognition import Recognizer, AudioFile

    engine = OVOSHTTPServerSTT()

    # inference
    jfk = "/home/miro/PycharmProjects/ovos-stt-plugin-fasterwhisper/jfk.wav"
    with AudioFile(jfk) as source:
        audio = Recognizer().record(source)

    pred = engine.execute(audio)
    print(pred)
