import requests
import os

REPO = "remla2025-team10/model-training"
GITHUB_API = f"https://api.github.com/repos/{REPO}/releases/latest"

def download_models():
    os.makedirs("models", exist_ok=True)
    response = requests.get(GITHUB_API)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch release: {response.text}")

    body = response.json()
    models = body["assets"]

    vectorizer_filename = None
    classifier_filename = None

    if not models:
        raise Exception("No models found.")
    else:
        for model in models:
            name = model["name"]
            url = model["browser_download_url"]

            r = requests.get(url)
            r.raise_for_status()
            filepath = os.path.join("models", name)

            with open(filepath, "wb") as f:
                f.write(r.content)

            # We assume the vectorizer will always be a .pkl file
            if name.endswith(".pkl"):
                print("Found vectorizer model.")
                vectorizer_filename = name
            
            # Also assume classifier always contains "classifier" in the name
            elif "classifier" in name.lower():
                print("Found classifier model.")
                classifier_filename = name
            
            print(f"Downloaded {name} sucessfully.")

    env_path = os.path.join("models", "models.env")
    with open(env_path, "w") as f:
        if vectorizer_filename:
            f.write(f"VECTORIZER_MODEL={vectorizer_filename}\n")
        if classifier_filename:
            f.write(f"CLASSIFIER_MODEL={classifier_filename}\n")

