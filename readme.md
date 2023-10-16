## Description

OpenVoiceOS companion plugin for [OpenVoiceOS STT Server](https://github.com/OpenVoiceOS/ovos-stt-http-server)

## Install

```bash
pip install ovos-stt-plugin-server
```

## Configuration

```json
  "stt": {
    "module": "ovos-stt-plugin-server",
    "ovos-stt-plugin-server": {"url": "https://0.0.0.0:8080/stt"}
 }
```

## Public servers

public server status page can be found at https://github.com/OpenVoiceOS/status

the default public servers run [Whisper](https://github.com/OpenVoiceOS/ovos-stt-plugin-fasterwhisper), but [Nemo](https://github.com/NeonGeckoCom/neon-stt-plugin-nemo) is also available

- https://stt.smartgic.io/nemo/stt

**Warning** there are associated risk with using a public server, read Jarbas blog post [The Trust Factor in Public Servers](https://jarbasal.github.io/blog/2023/10/14/the-trust-factor-in-public-servers.html)

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
