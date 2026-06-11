"""Verify SpeechRecognition is declared and importable (issue #45)."""
import importlib
import os

REQUIREMENTS_FILE = os.path.join(
    os.path.dirname(__file__), "..", "requirements", "requirements.txt"
)


def test_speechrecognition_in_requirements():
    with open(REQUIREMENTS_FILE) as f:
        contents = f.read()
    assert "SpeechRecognition" in contents, (
        "SpeechRecognition must be listed in requirements/requirements.txt"
    )


def test_speech_recognition_importable():
    """SpeechRecognition must be importable (no ImportError at package boundary)."""
    mod = importlib.import_module("speech_recognition")
    assert mod is not None
