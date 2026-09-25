import numpy as np
import sounddevice as sd

print(sd.query_devices())
print("Domyślne (wejście, wyjście):", sd.default.device)

t = np.linspace(0, 1, 44100, endpoint=False)
beep = (0.5 * np.sin(2 * np.pi * 440 * t)).astype(np.float32)

sd.play(beep, 44100)
sd.wait()