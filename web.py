# from flask import Flask, request, render_template_string, jsonify
# import re
# from datetime import datetime

# app = Flask(__name__)

# stored_data = {}

# # ------------------- BANK KYC FORM -------------------

# HTML_FORM = """
# <!DOCTYPE html>
# <html>
# <head>
# <title>Bank Customer Onboarding - KYC</title>
# <style>
# body { font-family: Arial; background:#f4f6f9; }
# .container { width:80%; margin:auto; background:white; padding:30px; margin-top:20px; }
# h2 { background:#002b5c; color:white; padding:10px; }
# h3 { border-bottom:1px solid #ccc; padding-top:15px; }
# input, select { width:100%; padding:8px; margin-bottom:10px; }
# button { padding:12px 25px; background:#003399; color:white; border:none; cursor:pointer; }
# .section { margin-bottom:25px; }
# </style>
# </head>
# <body>

# <div class="container">
# <h2>Customer Due Diligence (CDD) / KYC Application</h2>

# <form method="POST">

# <div class="section">
# <h3>1. Identification Details</h3>

# Customer ID:
# <input type="text" name="customerId" required>

# Full Name:
# <input type="text" name="fullName" required>

# Father / Spouse Name:
# <input type="text" name="guardianName" required>

# Date of Birth:
# <input type="date" name="dob" required>

# Gender:
# <select name="gender" required>
# <option value="">Select</option>
# <option>Male</option>
# <option>Female</option>
# <option>Other</option>
# </select>

# Nationality:
# <input type="text" name="nationality" required>

# PAN Number:
# <input type="text" name="panNo" required>

# Aadhaar Number:
# <input type="text" name="aadhaarNo" required>
# </div>

# <div class="section">
# <h3>2. Contact Details</h3>

# Mobile Number:
# <input type="text" name="mobile" required>

# Email:
# <input type="email" name="email" required>

# Residential Address:
# <input type="text" name="address" required>

# City:
# <input type="text" name="city" required>

# State:
# <input type="text" name="state" required>

# PIN Code:
# <input type="text" name="pincode" required>
# </div>

# <div class="section">
# <h3>3. Employment & Financial Details</h3>

# Occupation:
# <select name="occupation" required>
# <option value="">Select</option>
# <option>Salaried</option>
# <option>Self Employed</option>
# <option>Business</option>
# <option>Professional</option>
# <option>Student</option>
# <option>Retired</option>
# </select>

# Employer Name:
# <input type="text" name="employer">

# Annual Income (INR):
# <input type="number" name="annualIncome" required>

# Source of Funds:
# <input type="text" name="sourceOfFunds" required>
# </div>

# <div class="section">
# <h3>4. Regulatory Declarations</h3>

# Politically Exposed Person (PEP):
# <select name="pepStatus" required>
# <option value="">Select</option>
# <option>No</option>
# <option>Yes</option>
# </select>

# Tax Residency Country:
# <input type="text" name="taxCountry" required>

# <input type="checkbox" name="fatcaDeclaration" required>
# I confirm FATCA/CRS compliance.

# <br><br>
# <input type="checkbox" name="customerDeclaration" required>
# I confirm information provided is true.

# Signature:
# <input type="text" name="signature" required>

# Date:
# <input type="date" name="signatureDate" required>
# </div>

# <button type="submit">Submit Application</button>

# </form>
# </div>

# </body>
# </html>
# """

# # ------------------- ROUTE -------------------

# @app.route("/", methods=["GET", "POST"])
# def kyc_application():

#     global stored_data

#     if request.method == "GET":
#         return render_template_string(HTML_FORM)

#     data = request.form.to_dict()
#     errors = []

#     # ---------------- VALIDATION ----------------

#     if not re.fullmatch(r"\d{12}", data.get("aadhaarNo", "")):
#         errors.append("Invalid Aadhaar format")

#     if not re.fullmatch(r"[A-Z]{5}[0-9]{4}[A-Z]", data.get("panNo", "")):
#         errors.append("Invalid PAN format")

#     if not re.fullmatch(r"\d{10}", data.get("mobile", "")):
#         errors.append("Invalid mobile number")

#     if not re.fullmatch(r"\d{6}", data.get("pincode", "")):
#         errors.append("Invalid PIN code")

#     try:
#         datetime.strptime(data.get("dob"), "%Y-%m-%d")
#     except:
#         errors.append("Invalid Date of Birth")

#     try:
#         income = int(data.get("annualIncome", 0))
#         if income <= 0:
#             errors.append("Income must be greater than zero")
#     except:
#         errors.append("Invalid income value")

#     if errors:
#         return jsonify({
#             "data": {
#                 "errors": errors
#             }
#         }), 400

#     # ---------------- MASKING ----------------

#     masked_data = {
#         "customerId": data.get("customerId"),
#         "fullName": data.get("fullName"),
#         "guardianName": data.get("guardianName"),
#         "dob": data.get("dob"),
#         "gender": data.get("gender"),
#         "nationality": data.get("nationality"),
#         "maskedAadhaar": "XXXX XXXX " + data["aadhaarNo"][-4:],
#         "maskedPAN": data["panNo"][:5] + "XXXX",
#         "maskedMobile": "XXXXXX" + data["mobile"][-4:],
#         "email": data.get("email"),
#         "address": data.get("address"),
#         "city": data.get("city"),
#         "state": data.get("state"),
#         "pincode": data.get("pincode"),
#         "occupation": data.get("occupation"),
#         "employer": data.get("employer"),
#         "annualIncome": data.get("annualIncome"),
#         "sourceOfFunds": data.get("sourceOfFunds"),
#         "pepStatus": data.get("pepStatus"),
#         "taxCountry": data.get("taxCountry"),
#         "signature": data.get("signature"),
#         "signatureDate": data.get("signatureDate")
#     }

#     stored_data = masked_data

#     return jsonify({
#         "data": masked_data
#     })

# # No explicit port block (production ready)

from flask import Flask, request, render_template_string, jsonify
import re
from datetime import datetime
import uuid

app = Flask(__name__)

# In-memory storage
stored_kyc_data = None


# ---------------- MASKING FUNCTIONS ----------------

def mask_aadhaar(aadhaar):
    if aadhaar and len(aadhaar) == 12:
        return "XXXX XXXX " + aadhaar[-4:]
    return None

def mask_pan(pan):
    if pan and len(pan) == 10:
        return pan[:5] + "XXXX"
    return None

def mask_mobile(mobile):
    if mobile and len(mobile) == 10:
        return "XXXXXX" + mobile[-4:]
    return None


# ---------------- RBI STYLE FORM ----------------

HTML_FORM = """
<!DOCTYPE html>
<html>
<head>
<title>RBI Compliant KYC Form</title>
<style>
body { font-family: Arial; background:#eef2f7; }
.container { width:75%; margin:auto; background:white; padding:30px; margin-top:20px; }
h1 { text-align:center; color:#002b5c; }
h3 { border-bottom:2px solid #002b5c; padding-top:20px; }
input, select { width:100%; padding:8px; margin:6px 0 12px 0; }
button { padding:12px 25px; background:#002b5c; color:white; border:none; cursor:pointer; }
</style>
</head>
<body>

<div class="container">
<h1>Customer Due Diligence (CDD) – KYC Application</h1>

<form method="POST">

<h3>Identification Details</h3>
Customer ID: <input type="text" name="customerId" required>
Full Name: <input type="text" name="fullName" required>
Date of Birth: <input type="date" name="dob" required>
Nationality: <input type="text" name="nationality" required>

<h3>Officially Valid Documents</h3>
PAN Number: <input type="text" name="panNo" required>
Aadhaar Number: <input type="text" name="aadhaarNo" required>

<h3>Contact Details</h3>
Mobile: <input type="text" name="mobile" required>
Email: <input type="email" name="email" required>
City: <input type="text" name="city" required>
State: <input type="text" name="state" required>
PIN Code: <input type="text" name="pincode" required>

<h3>Financial Profile</h3>
Occupation: 
<select name="occupation" required>
<option value="">Select</option>
<option>Salaried</option>
<option>Self Employed</option>
<option>Business</option>
<option>Professional</option>
</select>

Annual Income: <input type="number" name="annualIncome" required>

<button type="submit">Submit KYC</button>

</form>
</div>
</body>
</html>
"""


# ---------------- FORM SUBMIT ----------------

@app.route("/", methods=["GET", "POST"])
def kyc():

    global stored_kyc_data

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
                "validationErrors": errors
            }
        }), 400

    # Generate reference number
    kyc_ref = "KYC-" + uuid.uuid4().hex[:8].upper()

    # Structured output
    stored_kyc_data = {
        "kycReferenceNumber": kyc_ref,
        "customerIdentification": {
            "customerId": data.get("customerId"),
            "fullName": data.get("fullName"),
            "dob": data.get("dob"),
            "nationality": data.get("nationality")
        },
        "officiallyValidDocuments": {
            "maskedPAN": mask_pan(data.get("panNo")),
            "maskedAadhaar": mask_aadhaar(data.get("aadhaarNo"))
        },
        "contactDetails": {
            "maskedMobile": mask_mobile(data.get("mobile")),
            "email": data.get("email"),
            "city": data.get("city"),
            "state": data.get("state")
        },
        "financialProfile": {
            "occupation": data.get("occupation"),
            "annualIncome": income
        }
    }

    return jsonify({
        "data": stored_kyc_data
    })


# ---------------- FETCH STORED DATA ----------------

@app.route("/get-data", methods=["GET"])
def get_data():

    if not stored_kyc_data:
        return jsonify({
            "data": {
                "message": "No KYC data available"
            }
        })

    return jsonify({
        "data": stored_kyc_data
    })

