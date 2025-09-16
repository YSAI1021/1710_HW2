import numpy as np, sounddevice as sd

sr = 44100
t = np.linspace(0, 1, sr, False)
tone = 0.2 * np.sin(2 * np.pi * 440 * t)  # 440 Hz @ 20% volume
sd.play(tone, sr)
sd.wait()
print("Beep played")
