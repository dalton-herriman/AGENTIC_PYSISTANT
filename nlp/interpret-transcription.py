import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from orchestrator import core
import glob
from datetime import datetime

TRANSCRIPTIONS_DIR = "data/raw/transcriptions"
INTERPRETATIONS_DIR = "data/processed/interpretations"

def get_latest_transcription_file(directory):
    files = glob.glob(os.path.join(directory, "*.txt"))
    if not files:
        raise FileNotFoundError("No transcription files found.")
    files_with_times = [(f, os.path.getmtime(f)) for f in files]
    latest_file = max(files_with_times, key=lambda x: x[1])[0]
    return latest_file

def save_interpretation(output, transcription_file):
    os.makedirs(INTERPRETATIONS_DIR, exist_ok=True)
    base_name = os.path.splitext(os.path.basename(transcription_file))[0]
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = os.path.join(INTERPRETATIONS_DIR, f"{base_name}_interpretation_{timestamp}.txt")
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(output)
    return output_file

def run_inference(transcription):
    # Assuming the new package exposes a similar interface
    return core.run_inference(transcription)

def main():
    try:
        latest_file = get_latest_transcription_file(TRANSCRIPTIONS_DIR)
        with open(latest_file, "r", encoding="utf-8") as f:
            transcription = f.read()
        inference_result = run_inference(transcription)
        output_file = save_interpretation(inference_result, latest_file)
        print(f"Latest transcription file: {latest_file}")
        print(f"Interpretation saved to: {output_file}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()