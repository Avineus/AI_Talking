import time
import threading
from queue import Queue

import numpy as np
import sounddevice as sd
import whisper
from rich.console import Console

from langchain_community.llms import Ollama

from tts import TextToSpeechService

console = Console()
stt = whisper.load_model("base.en")
tts = TextToSpeechService()

template = """
You are a helpful and friendly AI assistant. You are polite, respectful, and aim to provide concise responses of less
than 20 words.
The conversation transcript is as follows:
{history}
And here is the user's follow-up: {input}
Your response:
"""


class SimpleConversationChain:
    def __init__(self, llm, template: str) -> None:
        self.llm = llm
        self.template = template
        self.history: list[str] = []

    def _format_history(self) -> str:
        return "\n".join(self.history)

    def predict(self, input: str) -> str:
        prompt = self.template.format(history=self._format_history(), input=input)
        try:
            response = self.llm.invoke(prompt)
        except Exception:
            response = self.llm(prompt)

        if not isinstance(response, str):
            response = getattr(response, "content", str(response))

        self.history.append(f"User: {input}")
        self.history.append(f"Assistant: {response}")
        return response


chain = SimpleConversationChain(llm=Ollama(), template=template)