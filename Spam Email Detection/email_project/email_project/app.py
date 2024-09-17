from flask import Flask, request, render_template
import pickle

# Load the pipeline
with open("spam_detector_pipeline.pkl", "rb") as file:
    pipeline = pickle.load(file)

# Initialize Flask app
app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    prediction = ""
    if request.method == "POST":
        url = request.form.get('url')
        try:
            # Predict with the model
            prediction = pipeline.predict([url])[0]
            prediction = "Spam Mail" if prediction == 0 else "Ham Mail"
        except Exception as e:
            prediction = f"Error in prediction: {e}"

    return render_template("index.html", prediction=prediction)

if __name__ == "__main__":
    app.run(debug=True)
