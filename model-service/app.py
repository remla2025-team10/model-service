from flask import Flask, request, jsonify
from preprocess_sentiment_analysis import preprocess_dataframe
import pandas as pd

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    review = data.get("Review", "")

    # Right now we don't actually have anything relevant here so this is just placehoder code
    original_df = pd.DataFrame({"Review": [review]})
    preprocessed_df = preprocess_dataframe(original_df)
    
    processed_review = preprocessed_df.loc[0, "Processed_Review"]

    prediction = 1

    return jsonify({"prediction": prediction})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=3000)