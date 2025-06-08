import random
import time
from typing import Optional, List, Tuple

import requests
from ovos_config import Configuration
from ovos_plugin_manager.stt import STT
from ovos_plugin_manager.templates.transformers import AudioLanguageDetector
from ovos_utils import classproperty
from ovos_utils.log import LOG
from requests.utils import default_user_agent
from speech_recognition import AudioData


class OVOSServerLangClassifier(AudioLanguageDetector):
    def __init__(self, config=None):
        super().__init__("ovos-audio-lang-server-plugin", 10, config)

    @property
    def verify_ssl(self) -> bool:
        return self.config.get("verify_ssl", True)

    @property
    def user_agent(self) -> str:
        return self.config.get("user_agent") or default_user_agent()

    @property
    def urls(self) -> Optional[List[str]]:
        urls = self.config.get("urls") or []
        if urls and not isinstance(urls, list):
            urls = [urls]
        return urls

    @property
    def public_servers(self):
        return ["https://stt.smartgic.io/fasterwhisper/lang_detect"]

    def detect(self, audio_data: bytes, valid_langs=None) -> Tuple[str, float]:
        valid_langs = valid_langs or self.valid_langs
        if len(valid_langs) == 1:
            return valid_langs[0], 1.0
        if isinstance(audio_data, AudioData):
            audio_data = audio_data.get_wav_data()
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
                response = requests.post(url, data=audio_data,
                                         headers={"Content-Type": "audio/wav",
                                                  "User-Agent": self.user_agent},
                                         params={"valid_langs": ",".join(valid_langs)},
                                         timeout=self.config.get("timeout", 5),
                                         verify=self.verify_ssl)
                if not response.ok:
                    LOG.error(f"{response.status_code} response from {url}: "
                              f"{response.content}")
                else:
                    data = response.json()
                    return data["lang"], data["conf"]
            except Exception as e:
                LOG.exception(e)
            LOG.error(f"Lang detect request to {url} failed")
        return Configuration().get("lang"), 0.0

    @classproperty
    def available_languages(cls) -> set:
        return set()  # TODO


class OVOSHTTPServerSTT(STT):
    """STT interface for the OVOS-HTTP-STT-Server"""

    def __init__(self, config=None):
        super().__init__(config)
        if not self.verify_ssl:
            LOG.warning("SSL verification disabled, this is not secure and should"
                        "only be used for test systems! Please set up a valid certificate!")
        self._detector = OVOSServerLangClassifier()

    @property
    def verify_ssl(self) -> bool:
        return self.config.get("verify_ssl", True)

    @property
    def user_agent(self) -> str:
        return self.config.get("user_agent") or default_user_agent()

    @property
    def public_servers(self):
        return [
            "https://whisper.tigregotico.pt/stt",
            "https://stt.smartgic.io/fasterwhisper/stt",
            # "https://whisper.neonaiservices.com/stt"  # TODO -restore once it moves to whisper-turbo
        ]

    @property
    def urls(self) -> Optional[List[str]]:
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
                response = requests.post(url, data=audio.get_wav_data(),
                                         headers={"Content-Type": "audio/wav",
                                                  "User-Agent": self.user_agent},
                                         params={"lang": language or self.lang},
                                         timeout=self.config.get("timeout", 5),
                                         verify=self.verify_ssl)
                if not response.ok:
                    LOG.error(f"{response.status_code} response from {url}: "
                              f"{response.content}")
                else:
                    return response.text
            except Exception as e:
                LOG.exception(e)
            LOG.error(f"STT request to {url} failed")


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
    d = OVOSServerLangClassifier()

    # inference
    jfk = "/home/miro/PycharmProjects/ovos-stt-plugin-fasterwhisper/jfk.wav"
    ca = "/home/miro/PycharmProjects/ovos-stt-plugin-vosk/example.wav"
    with AudioFile(jfk) as source:
        audio = Recognizer().record(source)

    s = time.monotonic()
    pred = d.detect(audio, valid_langs=["en", "es", "ca"])
    e = time.monotonic() - s
    print(pred)
    print(f"took {e} seconds")

    s = time.monotonic()
    pred = engine.execute(audio, language="ca")
    e = time.monotonic() - s
    print(pred)
    print(f"took {e} seconds")
