import random
import threading
from queue import Queue

import numpy as np

from chain import console, tts
from translate import (
    record_audio,
    transcribe,
    get_llm_response,
    get_random_prompt,
    play_audio,
)


if __name__ == "__main__":
    console.print("[cyan]Assistant started! Press Ctrl+C to exit.")

    try:
        while True:
            console.input(
                "Press Enter to start recording, then press Enter again to stop."
            )

            data_queue = Queue()  # type: ignore[var-annotated]
            stop_event = threading.Event()
            recording_thread = threading.Thread(
                target=record_audio,
                args=(stop_event, data_queue),
            )
            recording_thread.start()

            input()
            stop_event.set()
            recording_thread.join()

            audio_data = b"".join(list(data_queue.queue))
            audio_np = (
                np.frombuffer(audio_data, dtype=np.int16).astype(np.float32) / 32768.0
            )

            if audio_np.size > 0:
                with console.status("Transcribing...", spinner="earth"):
                    text = transcribe(audio_np)
                console.print(f"[yellow]You: {text}")

                text_key = random.choice(
                    ["random", "suggest", "suggestion", "advice", "question"]
                )

                if text_key in {"random", "suggest", "suggestion", "advice", "question"}:
                    with console.status("Fetching my mood...", spinner="earth"):
                        if text_key == "advice":
                            prompt_kind = "advice"
                        elif text_key == "question":
                            prompt_kind = "question"
                        else:
                            prompt_kind = "suggestion"
                        prompt = get_random_prompt(prompt_kind)
                    console.print(f"[cyan]Assistant {text_key}: {prompt}")
                    sample_rate, audio_array = tts.long_form_synthesize(prompt)
                    play_audio(sample_rate, audio_array)

                if text.strip().lower() == "you":
                    console.print("[red]No speech detected. Please try again.")
                    text = prompt

                with console.status("Generating response...", spinner="earth"):
                    response = get_llm_response(text)
                    sample_rate, audio_array = tts.long_form_synthesize(response)

                console.print(f"[cyan]Assistant: {response}")
                play_audio(sample_rate, audio_array)
            else:
                console.print(
                    "[red]No audio recorded. Please ensure your microphone is working."
                )

    except KeyboardInterrupt:
        console.print("\n[red]Exiting...")

    console.print("[blue]Session ended.")