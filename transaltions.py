import json
from google.cloud import translate_v2 as translate

# Set up Google Translate Client
def get_translate_client(service_account_path):
    return translate.Client.from_service_account_json(service_account_path)

# Translate a single sentence to Nepali
def translate_to_nepali(client, text):
    result = client.translate(text, target_language='ne')
    return result['translatedText']

# Process the JSON file and translate captions
def translate_json(input_file, output_file, service_account_path):
    # Initialize the Google Translate API client
    client = get_translate_client(service_account_path)

    # Load the JSON file
    with open(input_file, "r", encoding="utf-8") as file:
        data = json.load(file)

    # Translate each sentence
    for sentence in data["sentences"]:
        original_tokens = sentence["tokens"]
        original_raw = sentence["raw"]

        # Translate tokenized words
        nepali_tokens = [translate_to_nepali(client, word) for word in original_tokens]
        sentence["tokens"] = nepali_tokens

        # Translate the full sentence (raw text)
        sentence["raw"] = translate_to_nepali(client, original_raw)

    # Save the updated JSON file
    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

    print(f"Translation completed. Saved to {output_file}")

# Paths and execution
SERVICE_ACCOUNT_PATH = ""  # Update this with your key file path
INPUT_FILE = "dataset_flickr8k.json"  # Input JSON file path
OUTPUT_FILE = "dataset_nepali_flickr8k.json"  # Output JSON file path

translate_json(INPUT_FILE, OUTPUT_FILE, SERVICE_ACCOUNT_PATH)
