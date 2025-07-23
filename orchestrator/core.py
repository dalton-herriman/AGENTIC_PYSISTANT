import requests

API_URL = "http://127.0.0.1:1234/v1/completions"
API_IDENTIFIER = "liquid/lfm2-1.2b"

def run_inference(prompt):
    payload = {
        "model": API_IDENTIFIER,
        "prompt": prompt,
        "max_tokens": 64
    }
    response = requests.post(API_URL, json=payload)
    response.raise_for_status()
    result = response.json()
    return result.get("choices", [{}])[0].get("text", "").strip()

# Example
result = run_inference("What is the capital of Texas?")
print(result)