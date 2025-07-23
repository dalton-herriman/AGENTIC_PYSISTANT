import glob
from transformers.pipelines import pipeline

# Path to recordings
recordings_path = "/data/raw/recordings/microphone_*.wav"

# Find the first file
files = glob.glob(recordings_path)
print("Found files:", files)  # Debug: print found files
if not files:
    print("No recordings found.")
    exit()

first_file = files[0]

# Load ASR pipeline from Hugging Face
asr = pipeline("automatic-speech-recognition", model="openai/whisper-base")

# Analyze the first recording
print(f"Analyzing: {first_file}")
result = asr(first_file)
print("Transcript:")
if isinstance(result, str):
    print(result)
elif isinstance(result, dict):
    print(result.get("text", result))
elif isinstance(result, list):
    for item in result:
        print(item.get("text", item))
else:
    print(result)
