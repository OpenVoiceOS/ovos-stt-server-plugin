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
    "ovos-stt-plugin-server": {"url": "https://0.0.0.0:8080/stt"},
    "verify_ssl": true
 }
```

### Security warning

Please note that while you can set `verify_ssl` to `false` to disable SSL
verification, this is not recommended and should only be used for testing
purposes. Consider using a private CA or certificates signed using
[Let's Encrypt](https://letsencrypt.org/) instead.

## Public servers

public server status page can be found at https://github.com/OpenVoiceOS/status

the default public servers run [Whisper](https://github.com/OpenVoiceOS/ovos-stt-plugin-fasterwhisper), but [Nemo](https://github.com/NeonGeckoCom/neon-stt-plugin-nemo) is also available

- https://stt.smartgic.io/nemo/stt

While there are associated risks with public servers, we value your trust in our products, learn more in Jarbas blog post [The Trust Factor in Public Servers](https://jarbasal.github.io/blog/2023/10/14/the-trust-factor-in-public-servers.html)

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
