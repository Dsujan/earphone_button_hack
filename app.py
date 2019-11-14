import sounddevice as earphone
import win32api
from threading import Event

FREQUENCY_SAMPLE = 1000  # 1000 frequency data points in one second
BLOCK_SIZE = 100  # One block size has one block of frequency sample. i.e. 1000 fs
AUDIO_CHANNEL = 1  # Default audio channel for earphone audio in

PRESS_THRESHOLD = 0.2  # Threshold time to take single button press
AMPLITUDE_THRESHOLD = 0.1  # Signal amplitude when button is pressed

BLOCKS_TO_PRESS = int((FREQUENCY_SAMPLE / BLOCK_SIZE) * PRESS_THRESHOLD)

VK_MEDIA_PLAY_PAUSE = 0xB3
VK_VOLUME_MUTE = 0xAD



class DeviceDriver:
    #audio signal preocessor callback for detecting btn press
    def processor(self, indata, frames, time, status):
        amplitude = sum([y for x in indata[:] for y in x]) / len(indata[:])
        if amplitude < AMPLITUDE_THRESHOLD:
            self.times_pressed += 1
            if self.times_pressed > BLOCKS_TO_PRESS and not self.is_held:
                self.is_held = True
                #mute/unmute
                #placed for older version if they don't support media player pause/play 
                win32api.keybd_event(VK_VOLUME_MUTE, 0, 0, 0)
                #pause/play
                win32api.keybd_event(VK_MEDIA_PLAY_PAUSE, 0, 0, 0)

        else:
            self.is_held = False
            self.times_pressed = 0

    def __init__(self):
        self.stream = earphone.InputStream(
            samplerate=FREQUENCY_SAMPLE,
            blocksize=BLOCK_SIZE,
            channels=AUDIO_CHANNEL,
            callback=self.processor,
        )
        self.stream.start()

        self.is_held = True
        self.times_pressed = 0

#runs earphone btn driver
if __name__ == "__main__":
    controller = DeviceDriver()
    
    Event().wait()
