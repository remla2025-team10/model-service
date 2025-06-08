from flask import Flask, request, jsonify
from preprocess_sentiment_analysis import preprocess_dataframe
import pandas as pd
import pickle
import joblib
import os
from flasgger import Swagger
from download_models import download_models

app = Flask(__name__)
swagger = Swagger(app)

model_env_path = os.path.join("models", "models.env")

if not os.path.exists(model_env_path):
    print("Models not found. Downloading models...")
    download_models()

# Funcion to load environment variables from ../.env file
def load_env_file(path):
    with open(path) as f:
        for line in f:
            key, val = line.strip().split("=")
            os.environ[key] = val

load_env_file(model_env_path)
vectorizer_path = os.path.join("models", os.environ["VECTORIZER_MODEL"])
classifier_path = os.path.join("models", os.environ["CLASSIFIER_MODEL"])
port = int(os.environ.get("PORT", 3000))

print(vectorizer_path)

vectorizer = pickle.load(open(vectorizer_path, "rb"))
classifier = joblib.load(classifier_path)

example_password = None
password_path = os.environ.get("PASSWORD_PATH")

if password_path and os.path.exists(password_path):
    try:
        with open(password_path, "r") as f:
            example_password = f.read().strip()
        
        if example_password:
            print(f"Example password loaded from {password_path}")
    except Exception as e:
        print(f"Error reading password file: {e}")


@app.route('/predict', methods=['POST'])
def predict():
    """
    Predict the sentiment of a review.
    ---
    summary: Returns either 1 or 0, based on whether the predicted sentiment is positive or negative.
    param review: The review text to be analyzed.
    parameters:
        -   in: body
            name: body
            required: true
            schema:
                type: object
                required:
                    - Review
                properties:
                    Review:
                        type: string
                        example: "We are so glad we found this place."
    
    responses:
        200:
            description: A JSON object containing the prediction.
            schema:
                type: object
                properties:
                    prediction:
                        type: integer
                        example: 1
    """
    data = request.get_json()
    review = data.get("Review", "")

    df = pd.DataFrame({"Review": [review]})
    processed_df = preprocess_dataframe(df)
    processed_review = processed_df.loc[0, "Processed_Review"]

    X_Fresh = vectorizer.transform([processed_review]).toarray()
    prediction = int(classifier.predict(X_Fresh)[0])

    return jsonify({"prediction": prediction})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=port)