from flask import Flask, request, render_template_string
import requests
import os
import threading

app = Flask(__name__)

# ✅ Read Wiiz webhook URL from Render Environment Variable
WIIZ_WEBHOOK_URL = os.environ.get("https://sandbox.wiiz.it/aiwf/webhook/595b131b-73b6-45a3-986f-080d2aa5ffbc/96dc3084-955b-4f61-b84c-8e366b628a49")

if not WIIZ_WEBHOOK_URL:
    print("ERROR: WIIZ_WEBHOOK_URL environment variable is missing")


# ✅ Background sender (so Wiiz doesn't timeout)
def send_to_wiiz(payload):
    try:
        print("Sending payload to Wiiz:", payload)

        response = requests.post(
            WIIZ_WEBHOOK_URL,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=8
        )

        print("Wiiz response:", response.status_code)

    except Exception as e:
        print("Wiiz send error:", str(e))


# ✅ KYC FORM UI
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
h2 { color:#003399; }
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


# ✅ When Wiiz opens URL → show form
@app.route("/", methods=["GET", "POST"])
def home():
    return render_template_string(HTML_FORM)

# ✅ Handle form submit
from flask import jsonify   # add this import at top if not present


@app.route("/submit", methods=["POST"])
def submit():
    payload = {
        "customerNo": request.form.get("customerNo"),
        "fullName": request.form.get("fullName"),
        "aadhaarNo": request.form.get("aadhaarNo"),
        "mobile": request.form.get("mobile"),
        "dob": request.form.get("dob"),
        "email": request.form.get("email")
    }

    print("Form submitted:", payload)

    # Send to Wiiz asynchronously (no timeout)
    threading.Thread(target=send_to_wiiz, args=(payload,)).start()

    # ✅ Return submitted data back to Wiiz
    return jsonify({
        "status": "submitted",
        "message": "KYC captured successfully",
        "data": payload
    })


# ✅ Required for Render deployment
port = int(os.environ.get("PORT", 4000))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=port)



