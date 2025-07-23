import sounddevice as sd
import soundfile as sf
import os
from datetime import datetime


def list_input_devices():
    devices = sd.query_devices()
    input_devices = [
        (i, d)
        for i, d in enumerate(devices)
        if isinstance(d, dict) and d.get("max_input_channels", 0) > 0
    ]
    for idx, dev in input_devices:
        print(f"{idx}: {dev.name} (Channels: {dev.max_input_channels})")
    return input_devices


def record(device_index, samplerate, channels, duration, filename):
    print(f"Recording from device {device_index} into {filename}")
    recording = sd.rec(
        int(duration * samplerate),
        samplerate=samplerate,
        channels=channels,
        device=device_index,
    )
    sd.wait()
    sf.write(filename, recording, samplerate)
    print("Recording finished.")


def main():
    duration = 10
    samplerate = 44100
    input_devices = list_input_devices()
    if not input_devices:
        print("No input devices found.")
        return
    selected_idx = int(input("Enter the device index to record from: "))
    selected_device = dict(input_devices[selected_idx][1])
    channels = selected_device["max_input_channels"]
    os.makedirs("data/raw/recordings", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"data/raw/recordings/microphone_{selected_idx}_{timestamp}.wav"
    record(selected_idx, samplerate, channels, duration, filename)


if __name__ == "__main__":
    main()
