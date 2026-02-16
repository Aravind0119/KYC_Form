from flask import Flask, request, render_template_string, jsonify
import os
import re
from datetime import datetime

app = Flask(__name__)

stored_data = {}

# ------------------- BANK KYC FORM -------------------

HTML_FORM = """
<!DOCTYPE html>
<html>
<head>
<title>Bank KYC Application</title>
<style>
body { font-family: Arial; background:#f4f6f9; }
.container { width:80%; margin:auto; background:white; padding:30px; margin-top:20px; }
h2 { background:#002b5c; color:white; padding:10px; }
h3 { border-bottom:1px solid #ccc; padding-top:15px; }
input, select { width:100%; padding:8px; margin-bottom:10px; }
button { padding:12px 25px; background:#003399; color:white; border:none; cursor:pointer; }
.section { margin-bottom:25px; }
</style>
</head>
<body>

<div class="container">
<h2>Customer Due Diligence (CDD) / KYC Application</h2>

<form method="POST" action="/submit">

<div class="section">
<h3>1. Identification Details</h3>

Customer ID:
<input type="text" name="customerId" required>

Full Name:
<input type="text" name="fullName" required>

Father / Spouse Name:
<input type="text" name="guardianName" required>

Date of Birth:
<input type="date" name="dob" required>

Gender:
<select name="gender" required>
<option value="">Select</option>
<option>Male</option>
<option>Female</option>
<option>Other</option>
</select>

Nationality:
<input type="text" name="nationality" required>

PAN Number:
<input type="text" name="panNo" required>

Aadhaar Number:
<input type="text" name="aadhaarNo" required>
</div>

<div class="section">
<h3>2. Contact Details</h3>

Mobile Number:
<input type="text" name="mobile" required>

Email:
<input type="email" name="email" required>

Residential Address:
<input type="text" name="address" required>

City:
<input type="text" name="city" required>

State:
<input type="text" name="state" required>

PIN Code:
<input type="text" name="pincode" required>
</div>

<div class="section">
<h3>3. Employment & Financial Details</h3>

Occupation:
<select name="occupation" required>
<option value="">Select</option>
<option>Salaried</option>
<option>Self Employed</option>
<option>Business</option>
<option>Professional</option>
<option>Student</option>
<option>Retired</option>
</select>

Employer Name:
<input type="text" name="employer">

Annual Income (INR):
<input type="number" name="annualIncome" required>

Source of Funds:
<input type="text" name="sourceOfFunds" required>
</div>

<div class="section">
<h3>4. Regulatory Declarations</h3>

Politically Exposed Person (PEP):
<select name="pepStatus" required>
<option value="">Select</option>
<option>No</option>
<option>Yes</option>
</select>

Tax Residency Country:
<input type="text" name="taxCountry" required>

<input type="checkbox" name="fatcaDeclaration" required>
I confirm FATCA/CRS compliance.

<br><br>
<input type="checkbox" name="customerDeclaration" required>
I confirm information provided is true.

Signature:
<input type="text" name="signature" required>

Date:
<input type="date" name="signatureDate" required>
</div>

<button type="submit">Submit Application</button>

</form>
</div>

</body>
</html>
"""

# ------------------- ROUTES -------------------

@app.route("/", methods=["GET"])
def home():
    return render_template_string(HTML_FORM)


@app.route("/submit", methods=["POST"])
def submit():

    global stored_data
    data = request.form.to_dict()
    errors = []

    # ------------------- VALIDATIONS -------------------

    # Aadhaar (12 digits)
    if not re.fullmatch(r"\d{12}", data.get("aadhaarNo", "")):
        errors.append("Invalid Aadhaar format")

    # PAN (ABCDE1234F)
    if not re.fullmatch(r"[A-Z]{5}[0-9]{4}[A-Z]", data.get("panNo", "")):
        errors.append("Invalid PAN format")

    # Mobile (10 digits)
    if not re.fullmatch(r"\d{10}", data.get("mobile", "")):
        errors.append("Invalid mobile number")

    # PIN (6 digits)
    if not re.fullmatch(r"\d{6}", data.get("pincode", "")):
        errors.append("Invalid PIN code")

    # Income
    try:
        if int(data.get("annualIncome", 0)) <= 0:
            errors.append("Income must be greater than 0")
    except:
        errors.append("Invalid income value")

    # DOB
    try:
        datetime.strptime(data.get("dob"), "%Y-%m-%d")
    except:
        errors.append("Invalid DOB format")

    if errors:
        return jsonify({
            "status": "REJECTED",
            "validation_errors": errors
        }), 400

    # ------------------- RISK LOGIC -------------------

    decision = "APPROVED"
    risk_flag = "LOW"

    if data.get("pepStatus") == "Yes":
        decision = "REVIEW_REQUIRED"
        risk_flag = "HIGH_PEP"

    if int(data.get("annualIncome")) < 100000:
        decision = "REVIEW_REQUIRED"
        risk_flag = "LOW_INCOME"

# ------------------- MASKING -------------------

masked_data = {
    "customerId": data.get("customerId"),
    "fullName": data.get("fullName"),
    "guardianName": data.get("guardianName"),
    "dob": data.get("dob"),
    "gender": data.get("gender"),
    "nationality": data.get("nationality"),
    "maskedAadhaar": "XXXX XXXX " + data["aadhaarNo"][-4:],
    "maskedPAN": data["panNo"][:5] + "XXXX",
    "maskedMobile": "XXXXXX" + data["mobile"][-4:],
    "email": data.get("email"),
    "address": data.get("address"),
    "city": data.get("city"),
    "state": data.get("state"),
    "pincode": data.get("pincode"),
    "occupation": data.get("occupation"),
    "employer": data.get("employer"),
    "annualIncome": data.get("annualIncome"),
    "sourceOfFunds": data.get("sourceOfFunds"),
    "pepStatus": data.get("pepStatus"),
    "taxCountry": data.get("taxCountry"),
    "signature": data.get("signature"),
    "signatureDate": data.get("signatureDate")
}

stored_data = masked_data

return jsonify({
    "data": masked_data
})



@app.route("/get-data", methods=["GET", "POST"])
def get_data():

    if not stored_data:
        return jsonify({
            "status": "no_data",
            "message": "No KYC submitted"
        })

    return jsonify(stored_data)


# ------------------- DEPLOYMENT -------------------

port = int(os.environ.get("PORT", 4000))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=port)

