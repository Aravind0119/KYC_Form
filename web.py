# from flask import Flask, request, render_template_string, jsonify
# import requests

# app = Flask(__name__)

# # ======= PASTE YOUR GENERATED WIIZ WEBHOOK HERE =======
# WEBHOOK_URL = "https://sandbox.wiiz.it/aiwf/webhook/595b131b-73b6-45a3-986f-080d2aa5ffbc/96dc3084-955b-4f61-b84c-8e366b628a49"
# # =======================================================

# HTML_FORM = """
# <!DOCTYPE html>
# <html>
# <head>
# <title>Indian Bank - KYC Form</title>
# <style>
# body { font-family: Arial, sans-serif; background: #f4f4f4; }
# .container { width: 70%; margin: auto; background: white; padding: 20px; border: 1px solid #ccc; }
# .header { background: #003399; color: white; padding: 10px; font-size: 22px; }
# h3 { text-align: center; }
# .row { display: flex; gap: 10px; margin-bottom: 10px; }
# .col { flex: 1; }
# input, textarea, select { width: 100%; padding: 6px; }
# .box { border: 1px solid #ccc; padding: 10px; margin-bottom: 10px; }
# </style>
# </head>
# <body>

# <div class="container">
# <div class="header">INDIAN BANK</div>
# <h3>KYC FORM FOR EXISTING CUSTOMERS</h3>

# <form method="POST" action="/submit">

# <div class="box">
# <div class="row">
#   <div class="col">A/C Type:
#     <select name="ac_type">
#       <option>Saving</option>
#       <option>Current</option>
#     </select>
#   </div>
#   <div class="col">e-KYC Registered:
#     <select name="ekyc">
#       <option>Yes</option>
#       <option>No</option>
#     </select>
#   </div>
#   <div class="col">Branch:
#     <input type="text" name="branch">
#   </div>
# </div>

# <div class="row">
#   <div class="col">Branch Code:
#     <input type="text" name="branch_code">
#   </div>
#   <div class="col">A/C No.:
#     <input type="text" name="account_no">
#   </div>
#   <div class="col">Customer Number:
#     <input type="text" name="customer_no">
#   </div>
# </div>
# </div>

# <div class="box">
# <div class="row">
#   <div class="col">Date of Birth:
#     <input type="date" name="dob">
#   </div>
#   <div class="col">Category:
#     <select name="category">
#       <option>General</option>
#       <option>SC/ST</option>
#       <option>OBC</option>
#     </select>
#   </div>
# </div>

# Name (Full Name in BLOCK LETTER):
# <input type="text" name="full_name"><br><br>

# Father’s Name:
# <input type="text" name="father_name"><br><br>

# Mother’s Name:
# <input type="text" name="mother_name"><br><br>

# Marital Status:
# <select name="marital_status">
#   <option>Unmarried</option>
#   <option>Married</option>
# </select><br><br>

# Nationality:
# <select name="nationality">
#   <option>Indian</option>
#   <option>Others</option>
# </select><br><br>

# Gender:
# <select name="gender">
#   <option>Male</option>
#   <option>Female</option>
# </select><br><br>

# Proof of Identity (POI):
# <input type="text" name="poi"><br><br>

# Proof of Address (POA):
# <input type="text" name="poa"><br><br>

# PAN Submitted:
# <select name="pan_submitted">
#   <option>No</option>
#   <option>Yes</option>
# </select><br><br>

# PAN No:
# <input type="text" name="pan_no"><br><br>

# Aadhaar No:
# <input type="text" name="aadhaar_no"><br><br>

# Mobile Number:
# <input type="text" name="mobile"><br><br>

# Email:
# <input type="email" name="email"><br><br>

# Educational Qualification:
# <input type="text" name="education"><br><br>

# Annual Income:
# <input type="text" name="income"><br><br>

# Employer Name:
# <input type="text" name="employer"><br><br>

# No. of Dependents:
# <input type="number" name="dependents"><br><br>

# Net Worth as on date:
# <input type="text" name="net_worth"><br><br>

# Residential Status:
# <input type="text" name="residential_status"><br><br>

# Address of Employer:
# <textarea name="employer_address"></textarea><br><br>

# Signature:
# <input type="text" name="signature"><br><br>

# Date:
# <input type="date" name="signature_date"><br><br>

# Place:
# <input type="text" name="place"><br><br>

# <button type="submit">Submit</button>

# </form>
# </div>

# </body>
# </html>
# """

# @app.route("/")
# def home():
#     return render_template_string(HTML_FORM)

# @app.route("/submit", methods=["POST"])
# def submit():
#     payload = {
#         "ac_type": request.form.get("ac_type"),
#         "ekyc": request.form.get("ekyc"),
#         "branch": request.form.get("branch"),
#         "branch_code": request.form.get("branch_code"),
#         "account_no": request.form.get("account_no"),
#         "customer_no": request.form.get("customer_no"),
#         "dob": request.form.get("dob"),
#         "category": request.form.get("category"),
#         "full_name": request.form.get("full_name"),
#         "father_name": request.form.get("father_name"),
#         "mother_name": request.form.get("mother_name"),
#         "marital_status": request.form.get("marital_status"),
#         "nationality": request.form.get("nationality"),
#         "gender": request.form.get("gender"),
#         "poi": request.form.get("poi"),
#         "poa": request.form.get("poa"),
#         "pan_submitted": request.form.get("pan_submitted"),
#         "pan_no": request.form.get("pan_no"),
#         "aadhaar_no": request.form.get("aadhaar_no"),
#         "mobile": request.form.get("mobile"),
#         "email": request.form.get("email"),
#         "education": request.form.get("education"),
#         "income": request.form.get("income"),
#         "employer": request.form.get("employer"),
#         "dependents": request.form.get("dependents"),
#         "net_worth": request.form.get("net_worth"),
#         "residential_status": request.form.get("residential_status"),
#         "employer_address": request.form.get("employer_address"),
#         "signature": request.form.get("signature"),
#         "signature_date": request.form.get("signature_date"),
#         "place": request.form.get("place")
#     }

#     print("Sending to Wiiz:", payload)

#     try:
#         response = requests.post(
#             WEBHOOK_URL,
#             json=payload,
#             headers={"Content-Type": "application/json"},
#             timeout=15
#         )

#         return jsonify({
#             "status": "success",
#             "message": "Data sent to Wiiz Webhook",
#             "wiiz_status": response.status_code,
#             "data_sent": payload
#         })

#     except Exception as e:
#         return jsonify({
#             "status": "failed",
#             "error": str(e)
#         }), 500

# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=4000, debug=True)



from flask import Flask, request, render_template_string, jsonify
import requests
import os
import threading

app = Flask(__name__)

# ======= PASTE YOUR WIIZ GENERATED WEBHOOK HERE =======
WIIZ_WEBHOOK_URL = os.environ.get("https://sandbox.wiiz.it/aiwf/webhook/595b131b-73b6-45a3-986f-080d2aa5ffbc/96dc3084-955b-4f61-b84c-8e366b628a49")
# =======================================================

HTML_FORM = """
<!DOCTYPE html>
<html>
<head>
<title>Indian Bank - KYC Form</title>
<style>
body { font-family: Arial, sans-serif; background: #f4f4f4; }
.container { width: 70%; margin: auto; background: white; padding: 20px; border: 1px solid #ccc; }
.header { background: #003399; color: white; padding: 10px; font-size: 22px; }
h3 { text-align: center; }
.row { display: flex; gap: 10px; margin-bottom: 10px; }
.col { flex: 1; }
input, textarea, select { width: 100%; padding: 6px; }
.box { border: 1px solid #ccc; padding: 10px; margin-bottom: 10px; }
</style>
</head>
<body>

<div class="container">
<div class="header">INDIAN BANK</div>
<h3>KYC FORM FOR EXISTING CUSTOMERS</h3>

<form method="POST" action="/submit">

<div class="box">
<div class="row">
  <div class="col">A/C Type:
    <select name="ac_type">
      <option>Saving</option>
      <option>Current</option>
    </select>
  </div>
  <div class="col">e-KYC Registered:
    <select name="ekyc">
      <option>Yes</option>
      <option>No</option>
    </select>
  </div>
  <div class="col">Branch:
    <input type="text" name="branch">
  </div>
</div>

<div class="row">
  <div class="col">Branch Code:
    <input type="text" name="branch_code">
  </div>
  <div class="col">A/C No.:
    <input type="text" name="account_no">
  </div>
  <div class="col">Customer Number:
    <input type="text" name="customer_no">
  </div>
</div>
</div>

<div class="box">
<div class="row">
  <div class="col">Date of Birth:
    <input type="date" name="dob">
  </div>
  <div class="col">Category:
    <select name="category">
      <option>General</option>
      <option>SC/ST</option>
      <option>OBC</option>
    </select>
  </div>
</div>

Name (Full Name in BLOCK LETTER):
<input type="text" name="full_name"><br><br>

Father’s Name:
<input type="text" name="father_name"><br><br>

Mother’s Name:
<input type="text" name="mother_name"><br><br>

Marital Status:
<select name="marital_status">
  <option>Unmarried</option>
  <option>Married</option>
</select><br><br>

Nationality:
<select name="nationality">
  <option>Indian</option>
  <option>Others</option>
</select><br><br>

Gender:
<select name="gender">
  <option>Male</option>
  <option>Female</option>
</select><br><br>

Proof of Identity (POI):
<input type="text" name="poi"><br><br>

Proof of Address (POA):
<input type="text" name="poa"><br><br>

PAN Submitted:
<select name="pan_submitted">
  <option>No</option>
  <option>Yes</option>
</select><br><br>

PAN No:
<input type="text" name="pan_no"><br><br>

Aadhaar No:
<input type="text" name="aadhaar_no"><br><br>

Mobile Number:
<input type="text" name="mobile"><br><br>

Email:
<input type="email" name="email"><br><br>

Educational Qualification:
<input type="text" name="education"><br><br>

Annual Income:
<input type="text" name="income"><br><br>

Employer Name:
<input type="text" name="employer"><br><br>

No. of Dependents:
<input type="number" name="dependents"><br><br>

Net Worth as on date:
<input type="text" name="net_worth"><br><br>

Residential Status:
<input type="text" name="residential_status"><br><br>

Address of Employer:
<textarea name="employer_address"></textarea><br><br>

Signature:
<input type="text" name="signature"><br><br>

Date:
<input type="date" name="signature_date"><br><br>

Place:
<input type="text" name="place"><br><br>

<button type="submit">Submit</button>

</form>
</div>

</body>
</html>
"""



def send_to_wiiz(payload):
    try:
        requests.post(
            WIIZ_WEBHOOK_URL,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=5   # short timeout, don't block
        )
    except Exception as e:
        print("Wiiz send error:", e)


@app.route("/submit", methods=["POST"])
def submit():

     payload = {
        "acType": request.form.get("ac_type"),
        "ekyc": request.form.get("ekyc"),
        "branch": request.form.get("branch"),
        "branchCode": request.form.get("branch_code"),
        "accountNo": request.form.get("account_no"),
        "customerNo": request.form.get("customer_no"),
        "dob": request.form.get("dob"),
        "category": request.form.get("category"),
        "fullName": request.form.get("full_name"),
        "fatherName": request.form.get("father_name"),
        "motherName": request.form.get("mother_name"),
        "maritalStatus": request.form.get("marital_status"),
        "nationality": request.form.get("nationality"),
        "gender": request.form.get("gender"),
        "poi": request.form.get("poi"),
        "poa": request.form.get("poa"),
        "panSubmitted": request.form.get("pan_submitted"),
        "panNo": request.form.get("pan_no"),
        "aadhaarNo": request.form.get("aadhaar_no"),
        "mobile": request.form.get("mobile"),
        "email": request.form.get("email"),
        "education": request.form.get("education"),
        "income": request.form.get("income"),
        "employer": request.form.get("employer"),
        "dependents": request.form.get("dependents"),
        "netWorth": request.form.get("net_worth"),
        "residentialStatus": request.form.get("residential_status"),
        "employerAddress": request.form.get("employer_address"),
        "signature": request.form.get("signature"),
        "signatureDate": request.form.get("signature_date"),
        "place": request.form.get("place")
    }

    # 🔥 Send to Wiiz in background thread (no blocking)
    threading.Thread(target=send_to_wiiz, args=(payload,)).start()

    # 🔥 Immediately respond to browser / Wiiz
    return """
    <h3>✅ KYC Submitted Successfully</h3>
    <p>You may close this window.</p>
    """

# Render requires dynamic port
port = int(os.environ.get("PORT", 4000))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=port)


