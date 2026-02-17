from flask import Flask, request, render_template_string, jsonify
import re
from datetime import datetime

app = Flask(__name__)

stored_data = None   # Initialize properly


# ------------------- BANK KYC FORM -------------------

HTML_FORM = """
<!DOCTYPE html>
<html>
<head>
<title>Bank Customer Onboarding - KYC</title>
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

<form method="POST">

<h3>Identification Details</h3>
Customer ID: <input type="text" name="customerId" required>
Full Name: <input type="text" name="fullName" required>
Guardian Name: <input type="text" name="guardianName" required>
Date of Birth: <input type="date" name="dob" required>
Gender:
<select name="gender" required>
<option value="">Select</option>
<option>Male</option>
<option>Female</option>
<option>Other</option>
</select>
Nationality: <input type="text" name="nationality" required>
PAN: <input type="text" name="panNo" required>
Aadhaar: <input type="text" name="aadhaarNo" required>

<h3>Contact Details</h3>
Mobile: <input type="text" name="mobile" required>
Email: <input type="email" name="email" required>
Address: <input type="text" name="address" required>
City: <input type="text" name="city" required>
State: <input type="text" name="state" required>
PIN Code: <input type="text" name="pincode" required>

<h3>Employment & Financial Details</h3>
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
Employer: <input type="text" name="employer">
Annual Income: <input type="number" name="annualIncome" required>
Source of Funds: <input type="text" name="sourceOfFunds" required>

<h3>Regulatory Declarations</h3>
PEP:
<select name="pepStatus" required>
<option value="">Select</option>
<option>No</option>
<option>Yes</option>
</select>
Tax Country: <input type="text" name="taxCountry" required>
Signature: <input type="text" name="signature" required>
Signature Date: <input type="date" name="signatureDate" required>

<br><br>
<button type="submit">Submit Application</button>

</form>
</div>
</body>
</html>
"""


# ------------------- MAIN ROUTE -------------------

@app.route("/", methods=["GET", "POST"])
def kyc_application():

    global stored_data

    if request.method == "GET":
        return render_template_string(HTML_FORM)

    data = request.form.to_dict()
    errors = []

    # Validation
    if not re.fullmatch(r"\d{12}", data.get("aadhaarNo", "")):
        errors.append("Invalid Aadhaar")

    if not re.fullmatch(r"[A-Z]{5}[0-9]{4}[A-Z]", data.get("panNo", "")):
        errors.append("Invalid PAN")

    if not re.fullmatch(r"\d{10}", data.get("mobile", "")):
        errors.append("Invalid Mobile")

    if not re.fullmatch(r"\d{6}", data.get("pincode", "")):
        errors.append("Invalid PIN Code")

    try:
        datetime.strptime(data.get("dob", ""), "%Y-%m-%d")
    except:
        errors.append("Invalid DOB")

    try:
        income = int(data.get("annualIncome", 0))
        if income <= 0:
            errors.append("Invalid Income")
    except:
        errors.append("Invalid Income")

    if errors:
        return jsonify({
            "data": {
                "errors": errors
            }
        }), 400

    # Masking
    stored_data = {
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
        "annualIncome": income,
        "sourceOfFunds": data.get("sourceOfFunds"),
        "pepStatus": data.get("pepStatus"),
        "taxCountry": data.get("taxCountry"),
        "signature": data.get("signature"),
        "signatureDate": data.get("signatureDate")
    }

    return jsonify({
        "data": stored_data
    })


# ------------------- GET STORED DATA -------------------

@app.route("/get-data", methods=["GET"])
def get_data():

    if not stored_data:
        return jsonify({
            "data": {
                "message": "No KYC data available"
            }
        })

    return jsonify({
        "data": stored_data
    })
