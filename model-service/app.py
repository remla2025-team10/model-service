from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    review = data.get("review", "")
    prediction = 1

    return jsonify({"prediction": prediction})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=3000)