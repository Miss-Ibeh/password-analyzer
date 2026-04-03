from flask import Flask, render_template, request
import random
import string
import math

app = Flask(__name__)

def estimate_crack_time(password):
    charset = 0
    if any(c.islower() for c in password): charset += 26
    if any(c.isupper() for c in password): charset += 26
    if any(c.isdigit() for c in password): charset += 10
    if any(c in "!@#$%^&*()" for c in password): charset += 10

    if charset == 0:
        return "Very weak"

    combinations = charset ** len(password)
    guesses_per_sec = 1e9  # 1 billion guesses/sec
    seconds = combinations / guesses_per_sec

    if seconds < 60:
        return "Instantly"
    elif seconds < 3600:
        return f"{int(seconds/60)} minutes"
    elif seconds < 86400:
        return f"{int(seconds/3600)} hours"
    elif seconds < 31536000:
        return f"{int(seconds/86400)} days"
    else:
        return f"{int(seconds/31536000)} years"

def generate_password():
    characters = string.ascii_letters + string.digits + "!@#$%^&*()"
    return ''.join(random.choice(characters) for _ in range(12))

def check_password(password):
    score = 0
    feedback = []

    if len(password) >= 12:
        score += 25
    else:
        feedback.append("Use at least 12 characters")

    if any(c.islower() for c in password):
        score += 15
    else:
        feedback.append("Add lowercase letters")

    if any(c.isupper() for c in password):
        score += 15
    else:
        feedback.append("Add uppercase letters")

    if any(c.isdigit() for c in password):
        score += 15
    else:
        feedback.append("Add numbers")

    if any(c in "!@#$%^&*()" for c in password):
        score += 15
    else:
        feedback.append("Add special characters")

    if score < 40:
        strength = "Weak"
    elif score < 70:
        strength = "Medium"
    else:
        strength = "Strong"

    crack_time = estimate_crack_time(password)

    return score, strength, feedback, crack_time

@app.route("/", methods=["GET", "POST"])
def index():
    score = None
    strength = None
    feedback = []
    crack_time = None
    generated = None

    if request.method == "POST":
        if "generate" in request.form:
            generated = generate_password()
        else:
            password = request.form["password"]
            score, strength, feedback, crack_time = check_password(password)

    return render_template("index.html",
                           score=score,
                           strength=strength,
                           feedback=feedback,
                           crack_time=crack_time,
                           generated=generated)

if __name__ == "__main__":
    app.run(debug=True)
