from flask import Flask, request, jsonify
from preprocess_sentiment_analysis import preprocess_dataframe
import pandas as pd
import pickle
import joblib
import os

app = Flask(__name__)

# Funcion to load environment variables from ../.env file
def load_env_file(path):
    with open(path) as f:
        for line in f:
            key, val = line.strip().split("=")
            os.environ[key] = val

load_env_file("../.env")
vectorizer_path = os.environ["VECTORIZER_MODEL"]
classifier_path = os.environ["CLASSIFIER_MODEL"]

vectorizer = pickle.load(open(vectorizer_path, "rb"))
classifier = joblib.load(classifier_path)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    review = data.get("Review", "")

    df = pd.DataFrame({"Review": [review]})
    processed_df = preprocess_dataframe(df)
    processed_review = processed_df.loc[0, "Processed_Review"]

    X_Fresh = vectorizer.transform([processed_review]).toarray()
    prediction = int(classifier.predict(X_Fresh)[0])
    
    return jsonify({"prediction": prediction})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=3000)