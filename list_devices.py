# list_devices.py
import sounddevice as sd
for i, d in enumerate(sd.query_devices()):
    print(i, d['name'], "default_out" if i == sd.default.device[1] else "")
    