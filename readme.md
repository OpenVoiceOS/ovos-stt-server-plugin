## Description

OpenVoiceOS companion plugin for [OpenVoiceOS STT Server](https://github.com/OpenVoiceOS/ovos-stt-http-server)

## Install

```bash
pip install ovos-stt-plugin-server
```

## Configuration

### Used with the [OpenVoiceOS STT Server](https://github.com/OpenVoiceOS/ovos-stt-http-server) to run a local STT server

In this example I am running a local [OpenVoiceOS STT Server](https://github.com/OpenVoiceOS/ovos-stt-http-server) using the [Vosk engine](https://github.com/OpenVoiceOS/ovos-stt-plugin-vosk) to understand Italian. Here we are also using Vosk as the fallback STT plugin.

This is the relevant `mycroft.conf` section 
```json
  "lang": "it-it",
  "stt": {
    "module": "ovos-stt-plugin-server",
    "fallback_module": "ovos-stt-plugin-vosk",
    "ovos-stt-plugin-server": {
      "url": "http://0.0.0.0:8080/stt",
      "model": "https://alphacephei.com/vosk/models/vosk-model-small-it-0.22.zip",
      "lang": "it-it"
    },
    "ovos-stt-plugin-vosk": {
      "model": "https://alphacephei.com/vosk/models/vosk-model-small-it-0.22.zip",
     "lang": "it-it"
    }
  },
```

Before to start mycroft, you have to launch the server with, in this case:

```sh
ovos-stt-server --engine ovos-stt-plugin-vosk
```

### Used with the [OpenVoiceOS STT Server](https://github.com/OpenVoiceOS/ovos-stt-http-server) on a remote STT server
This is the relevant `mycroft.conf` section 
```json
  "stt": {
    "module": "ovos-stt-plugin-server",
    "fallback_module": "ovos-stt-plugin-vosk",
    "ovos-stt-plugin-server": {
      "url": "https://stt.openvoiceos.com/stt",
    },
    "ovos-stt-plugin-vosk": {
    }
  },
```

## Docker

see [google-stt-proxy](https://github.com/OpenVoiceOS/ovos-stt-plugin-chromium/pkgs/container/google-stt-proxy) for an example

```dockerfile
FROM debian:buster-slim

RUN apt-get update && \
  apt-get install -y git python3 python3-dev python3-pip curl build-essential

RUN pip3 install ovos-stt-http-server==0.0.2a1
RUN pip3 install SpeechRecognition==3.8.1

COPY . /tmp/ovos-stt-chromium
RUN pip3 install /tmp/ovos-stt-chromium

ENTRYPOINT ovos-stt-server --engine ovos-stt-plugin-chromium
```tts
