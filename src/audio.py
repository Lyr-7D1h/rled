import queue
import sys
from typing import Optional

import sounddevice as sd
import numpy as np


class Audio:
    def __init__(
        self,
        device_name: str | int,
        on_update,
        channel: int,
        samplerate: Optional[int] = None,
    ) -> None:
        self.on_update = on_update
        sd.default.device = device_name
        self.device = sd.query_devices(sd.default.device, "output")
        if samplerate is None:
            self.samplerate: float = self.device["default_samplerate"]
        else:
            self.samplerate = samplerate
        index = self.device["index"]
        # https://python-sounddevice.readthedocs.io/en/0.3.15/api/streams.html
        self.stream = sd.InputStream(
            channels=channel,
            device=index,
            samplerate=self.samplerate,
            callback=self.update,
        )
        print(
            f"Listening on '{device_name}' ({index}) with sample rate {int(self.samplerate)}"
        )

    def __enter__(self):
        print("Starting audio stream")
        self.stream.start()

    def __exit__(self, type, value, traceback):
        print("Closing audio stream")
        self.stream.close()

    def close(self):
        print("Closing audio stream")
        self.stream.close()

    def update(
        self,
        indata: np.ndarray,
        frames: int,
        time,
        status: sd.CallbackFlags,
    ):
        """This is called (from a separate thread) for each audio block."""
        if status:
            print("Audio:", status, file=sys.stderr)
        self.on_update(indata, frames, time)
