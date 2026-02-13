from flask import Flask, request, render_template_string, jsonify
import os

app = Flask(__name__)

# ✅ Global dictionary to store submitted data
stored_data = {}

# ------------------ HTML FORM ------------------
HTML_FORM = """
<!DOCTYPE html>
<html>
<head>
<title>KYC Form</title>
<style>
body { font-family: Arial; background:#f4f4f4; }
.container { width:60%; margin:auto; background:white; padding:20px; margin-top:40px; }
input { width:100%; padding:8px; margin-bottom:12px; }
button { padding:10px 20px; background:#003399; color:white; border:none; cursor:pointer; }
</style>
</head>
<body>

<div class="container">
<h2>KYC FORM</h2>

<form method="POST" action="/submit">

Customer Number:
<input type="text" name="customerNo" required>

Full Name:
<input type="text" name="fullName" required>

Aadhaar No:
<input type="text" name="aadhaarNo" required>

Mobile:
<input type="text" name="mobile" required>

Date of Birth:
<input type="date" name="dob" required>

Email:
<input type="email" name="email" required>

<button type="submit">Submit</button>

</form>
</div>

</body>
</html>
"""

# ------------------ ROUTES ------------------

# Show form
@app.route("/", methods=["GET"])
def home():
    return render_template_string(HTML_FORM)


# Store submitted data
@app.route("/submit", methods=["GET", "POST"])
def submit():
    global stored_data

    stored_data = {
        "customerNo": request.form.get("customerNo"),
        "fullName": request.form.get("fullName"),
        "aadhaarNo": request.form.get("aadhaarNo"),
        "mobile": request.form.get("mobile"),
        "dob": request.form.get("dob"),
        "email": request.form.get("email")
    }

    print("Stored Data:", stored_data)

    return """
    <html>
        <body style="font-family:Arial;text-align:center;margin-top:50px;">
            <h2>✅ KYC Submitted Successfully</h2>
            <p>You may close this window.</p>
        </body>
    </html>
    """


# When Wiiz calls API → return stored data
@app.route("/get-data", methods=["POST", "GET"])
def get_data():
    global stored_data

    if not stored_data:
        return jsonify({
            "status": "no_data",
            "message": "No form submitted yet"
        })

    return jsonify({
        "status": "success",
        "data": stored_data
    })


# Required for Render
port = int(os.environ.get("PORT", 4000))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=port)

