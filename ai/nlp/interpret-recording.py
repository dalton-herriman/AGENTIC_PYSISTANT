import glob
from transformers.pipelines import pipeline

# Path to recordings
import os

recordings_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../data/raw/recordings/*.wav")
)

# Find the first file
files = glob.glob(recordings_path)
print("Found files:", files)  # Debug: print found files
if not files:
    print("No recordings found.")
    exit()

first_file = files[0]

# Load ASR pipeline from Hugging Face (English only)
asr = pipeline("automatic-speech-recognition", model="openai/whisper-base")

# Analyze the first recording
print(f"Analyzing: {first_file}")
result = asr(first_file)
if isinstance(result, str):
    transcript = result
elif isinstance(result, dict):
    transcript = result.get("text", str(result))
elif isinstance(result, list):
    transcript = "\n".join([item.get("text", str(item)) for item in result])
else:
    transcript = str(result)

print("Transcript:")
print(transcript)

# Save transcript to file
transcriptions_dir = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../data/raw/transcriptions")
)
os.makedirs(transcriptions_dir, exist_ok=True)
recording_basename = os.path.splitext(os.path.basename(first_file))[0]
transcription_file = os.path.join(
    transcriptions_dir, f"{recording_basename}_transcription.txt"
)
with open(transcription_file, "w", encoding="utf-8") as f:
    f.write(transcript)
print(f"Transcript saved to: {transcription_file}")
