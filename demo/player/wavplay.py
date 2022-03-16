import logging
from sys import float_repr_style
import pyaudio
import wave
import io

logger = logging.getLogger(__name__)


class WavPlay:
    CHUNK = 1024

    def __init__(self):
        self.p = pyaudio.PyAudio()
        self._wf = None
        self.paused = False
 
    def __del__(self):
        # close PyAudio
        logger.warning("close")
        self.p.terminate()
       
    def load(self, audio_in: bytes):
        """Play WAV audio data

        :param audio_in: audio_in is bytes containing WAV audio.
        :type audio_in: bytes
        """

        self._wf = wave.open(io.BytesIO(audio_in), 'rb')

        self._stream = self.p.open(
            format=self.p.get_format_from_width(self._wf.getsampwidth()),
            channels=self._wf.getnchannels(),
            rate=self._wf.getframerate(),
            output=True)

    def play(self):
        data = next(self._frames(), None)
        if data:
            logger.debug(f"data {len(data)}")
            self._stream.write(data)
        elif self._wf:
            # stop stream
            self._stream.stop_stream()
            self._stream.close()
            self._wf = None
        else:
            self.paused = True

    def _frames(self):
        # read data
        if self._wf:
            data = self._wf.readframes(WavPlay.CHUNK)
            while len(data) > 0:
                yield data
                data = self._wf.readframes(WavPlay.CHUNK)


if __name__ == "__main__":
    wp = WavPlay()
    with open("sample.wav", "rb") as f:
        wp.play(f.read())
    with open("sample.wav", "rb") as f:
        wp.play(f.read())
