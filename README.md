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

### Universal adapter (`server_type`)

By default the plugin talks to a native `ovos-stt-http-server`
(`server_type: "ovos"`). Set `server_type` to target any other compatible STT
API — the plugin becomes a universal adapter and can point at a vendor service
or any self-hosted OpenAI-compatible server:

```json
  "stt": {
    "module": "ovos-stt-plugin-server",
    "ovos-stt-plugin-server": {
      "server_type": "openai",
      "url": "https://api.openai.com",
      "api_key": "sk-...",
      "model": "whisper-1"
    }
 }
```

| `server_type` | Endpoint used | `url` example | Notes |
|---|---|---|---|
| `ovos` (default) | `/stt` | `https://0.0.0.0:8080/stt` | native ovos-stt-http-server |
| `openai` | `/v1/audio/transcriptions` | `https://api.openai.com` | also covers **Groq** (`url: https://api.groq.com/openai`), self-hosted **whisper.cpp** server, **LocalAI** |
| `deepgram` | `/v1/listen` | `https://api.deepgram.com` | |

`api_key` is sent as `Authorization: Bearer` (openai) or `Authorization: Token`
(deepgram). For vendor server types an explicit `url` is required.

### Security warning

Please note that while you can set `verify_ssl` to `false` to disable SSL
verification, this is not recommended and should only be used for testing
purposes. Consider using a private CA or certificates signed using
[Let's Encrypt](https://letsencrypt.org/) instead.

## Public servers

public server status page can be found at https://github.com/OpenVoiceOS/status

the default public servers run [Whisper](https://github.com/OpenVoiceOS/ovos-stt-plugin-fasterwhisper)

While there are associated risks with public servers, we value your trust in our products, learn more in Jarbas blog post [The Trust Factor in Public Servers](https://jarbasal.github.io/blog/2023/10/14/the-trust-factor-in-public-servers.html)

