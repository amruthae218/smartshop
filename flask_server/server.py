from flask import Flask, request, jsonify
import requests, time
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

CLIENT_ID = "your_client_id"
CLIENT_SECRET = "your_client_secret"
TENANT_NAME = "your_tenant"
ACCOUNT_LOGICAL_NAME = "your_account"
RELEASE_KEY = "your_release_key"
ORCH_URL = f"https://cloud.uipath.com/{ACCOUNT_LOGICAL_NAME}/{TENANT_NAME}/orchestrator_"

def get_token():
    resp = requests.post(
        "https://cloud.uipath.com/identity_/connect/token",
        data={
            "grant_type": "client_credentials",
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "scope": "OR.Jobs OR.Execution OR.Assets"
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    resp.raise_for_status()
    return resp.json()["access_token"]

def start_job(product_name):
    token = get_token()
    url = ORCH_URL + "odata/Jobs/UiPath.Server.Configuration.OData.StartJobs"
    headers = {
        "Authorization": f"Bearer {token}",
        "X-UIPATH-TenantName": TENANT_NAME,
        "Content-Type": "application/json"
    }
    payload = {
        "startInfo": {
            "ReleaseKey": RELEASE_KEY,
            "Strategy": "ModernJobsCount",
            "JobsCount": 1,
            "InputArguments": f'{{"in_ProductName": "{product_name}"}}'
        }
    }
    resp = requests.post(url, json=payload, headers=headers)
    resp.raise_for_status()
    return resp.json()["value"][0]["Id"], token

def poll_job(job_id, token, timeout=120):
    url = ORCH_URL + f"odata/Jobs({job_id})"
    headers = {"Authorization": f"Bearer {token}", "X-UIPATH-TenantName": TENANT_NAME}
    start = time.time()
    while time.time() - start < timeout:
        resp = requests.get(url, headers=headers)
        resp.raise_for_status()
        job = resp.json()
        if job["State"] == "Successful":
            return job.get("OutputArguments")
        elif job["State"] in ["Faulted", "Stopped"]:
            return None
        time.sleep(5)
    return None

#comment out to test flask integration
@app.route("/start-scraping", methods=["POST"])
def start_scraping():
    product = request.json.get("product")
    if not product:
        return jsonify({"error": "No product name provided"}), 400
    job_id, token = start_job(product)
    result = poll_job(job_id, token)
    if result:
        return jsonify({"result": result})
    else:
        return jsonify({"error": "Job failed or timed out"}), 500
    
    
# MOCKED RESPONSE (simulate UiPath output)uncomment to test chrome extension and flask server integration
# @app.route("/start-scraping", methods=["POST"])
# def start_scraping():
#     data = request.json
#     product = data.get("product")
#     if not product:
#         return jsonify({"error": "No product name provided"}), 400

#     mock_result = {
#         "out_LeastPrice": "₹59,400",
#         "out_LeastPriceURL": "https://www.amazon.in/example",
#         "out_LeastProductTitle": f"Sample Product: Apple iPhone 15 (128 GB) - Pink"
#     }
#     return jsonify({"success": True, "data": mock_result})

if __name__ == "__main__":
    app.run(port=5000, debug=True)
