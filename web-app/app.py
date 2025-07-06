from flask import Flask, render_template, request
import pickle
import re
import nltk
from nltk.corpus import stopwords

nltk.download('stopwords')
stop_words = set(stopwords.words('english'))

# Load vectorizer and model
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))
model = pickle.load(open("emotion_model.pkl", "rb"))

def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    words = text.split()
    words = [word for word in words if word not in stop_words]
    return " ".join(words)

def predict_emotion(text):
    cleaned = clean_text(text)
    vect_text = vectorizer.transform([cleaned])
    prediction = model.predict(vect_text)
    return prediction[0]

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    emotion = None
    if request.method == "POST":
        user_text = request.form["user_text"]
        emotion = predict_emotion(user_text)
    return render_template("index.html", emotion=emotion)

if __name__ == "__main__":
    app.run(debug=True)
