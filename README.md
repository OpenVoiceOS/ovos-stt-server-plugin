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
    "ovos-stt-plugin-server": {
      "urls": ["https://0.0.0.0:8080/stt"],
      "verify_ssl": true
    },
 }
```

for audio language detection

```json
  "listener": {
    "audio_transformers": {
        "ovos-audio-lang-server-plugin": {
          "urls": ["https://0.0.0.0:8080/lang_detect"],
          "verify_ssl": true
        }
    }
  }
```

### Security warning

Please note that while you can set `verify_ssl` to `false` to disable SSL
verification, this is not recommended and should only be used for testing
purposes. Consider using a private CA or certificates signed using
[Let's Encrypt](https://letsencrypt.org/) instead.

## Self-hosting (recommended)

Run your own server. It keeps your audio on your own hardware, it does not
depend on somebody else's uptime, and you choose the model.

```bash
pip install ovos-stt-http-server ovos-stt-plugin-onnx-asr
ovos-stt-server --engine ovos-stt-plugin-onnx-asr
```

[ovos-stt-plugin-onnx-asr](https://github.com/OpenVoiceOS/ovos-stt-plugin-onnx-asr)
is the recommended engine: it runs ONNX models on CPU, ships a best-model-per-language
registry covering ~90 languages, and loads a model per request language, so one
server can serve all of them. Point the plugin at it:

```json
  "stt": {
    "module": "ovos-stt-plugin-server",
    "ovos-stt-plugin-server": {
      "urls": ["https://your-server.example/stt"]
    }
  }
```

The server runs one engine at a time, and you choose the engine with
`--engine`. This example serves Italian with the
[Vosk engine](https://github.com/OpenVoiceOS/ovos-stt-plugin-vosk):

```bash
pip install ovos-stt-http-server ovos-stt-plugin-vosk
ovos-stt-server --engine ovos-stt-plugin-vosk
```

```json
  "stt": {
    "module": "ovos-stt-plugin-server",
    "ovos-stt-plugin-server": {
      "urls": ["http://0.0.0.0:8080/stt"]
    },
    "ovos-stt-plugin-vosk": {
      "lang": "it-IT",
      "model": "https://alphacephei.com/vosk/models/vosk-model-small-it-0.22.zip"
    }
  }
```

In this example the server and the listener run on the same machine, so one
`mycroft.conf` carries the whole block: the server reads the
`ovos-stt-plugin-vosk` section, and the listener reads the
`ovos-stt-plugin-server` section. If you move the server to another machine,
that machine keeps the `ovos-stt-plugin-vosk` section, and the listener keeps
only the `ovos-stt-plugin-server` section.

When the server is down, the listener can use a local STT plugin as a
fallback. Set `fallback_module` and give that plugin its own config:

```json
  "stt": {
    "module": "ovos-stt-plugin-server",
    "fallback_module": "ovos-stt-plugin-vosk",
    "ovos-stt-plugin-server": {
      "urls": ["https://your-server.example/stt"]
    },
    "ovos-stt-plugin-vosk": {
      "model": "https://alphacephei.com/vosk/models/vosk-model-small-it-0.22.zip"
    }
  }
```

## Public servers

If you set no `urls`, the plugin falls back to public servers.

> **These are a community courtesy, not a service.** They exist so you can try
> OVOS without setting anything up first. They are provided on a best-effort
> basis with **no guarantees** of uptime, latency, accuracy, privacy, or
> continued existence, and they can change or disappear without notice. They
> are meant for demos, evaluation and onboarding — **not for production, and
> not for anything you would not want a third party to receive**. Audio you
> send is processed on hardware you do not control.
>
> For anything beyond trying it out, [self-host](#self-hosting-recommended).

