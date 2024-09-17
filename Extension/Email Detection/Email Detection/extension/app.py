from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import numpy as np

app = Flask(__name__)
CORS(app)

# Load the trained model and the vectorizer
model = joblib.load('spam_detector_model.pkl')
vectorizer = joblib.load('vectorizer.pkl')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    
    print("Received data:", data)
    
    if 'email_content' not in data or not data['email_content']:
        return jsonify({'error': 'email_content key is missing or empty'}), 400
    
    email_content = [data['email_content']]
    print("Input email content:", email_content)
    
    # Transform text data to numeric
    email_content_transformed = vectorizer.transform(email_content)
    print("Transformed email content shape:", email_content_transformed.shape)
    
    # Get both the prediction and the probability
    prediction = model.predict(email_content_transformed)
    probability = model.predict_proba(email_content_transformed)
    
    print("Raw prediction:", prediction)
    print("Prediction probabilities:", probability)
    
    # Check the model's classes
    print("Model classes:", model.classes_)
    
    # Determine which class corresponds to spam
    spam_index = np.where(model.classes_ == 0)[0][0] if 1 in model.classes_ else 0
    is_spam = bool(prediction[0] == spam_index)
    spam_probability = probability[0][spam_index]
    
    print(f"Is spam: {is_spam}, Spam probability: {spam_probability}")
    
    return jsonify({
        'is_spam': is_spam,
        'spam_probability': float(spam_probability),
        'raw_prediction': int(prediction[0]),
        'model_classes': model.classes_.tolist()
    })

if __name__ == '__main__':
    app.run(debug=True)