# SmartShop Price Finder

A robust automation solution that leverages **UiPath Orchestrator** and a **Python Flask API** to deliver instant, reliable product price comparisons. Designed for scalability and easy integration, SmartShop connects backend automation with modern browser tools.

---

## 🎯 Project Overview

SmartShop allows you to:

- **Automate price comparison** for products using a UiPath workflow, eliminating manual browser searches.
- **Trigger and monitor automations** via a RESTful Flask API, enabling integration with any client (browser extension, app, etc.).
- **Receive structured results** (best price, link, and product title) from the UiPath workflow, ready for use in any frontend.

---

## 🏗️ Architecture

- **Backend: Python Flask API**
  - **Receives product search requests from clients (e.g., Chrome extension or any HTTP client).**
  - **Authenticates with UiPath Orchestrator via OAuth2 and starts a job using the Orchestrator API.**
  - **Polls the job status by calling Orchestrator’s job status API endpoint.**
  - **Returns the workflow’s output arguments (best price and URL) to the client as soon as the job completes.**
  - Includes a mock/test mode for development or when UiPath robots are unavailable.

- **Automation: UiPath Workflow (`.nupkg` package)**
  - Accepts an input argument `in_ProductName` (string).
  - Scrapes prices from e-commerce sites, compares them, and outputs the lowest price and corresponding URL.
  - Designed for cloud/serverless robots managed by Orchestrator.
    
---

## 📁 Project Structure

```
SmartShop/
├── flask_server/            # Flask API backend
│   └── server.py
├── uipath_workflow/         # UiPath .nupkg package
│   └── SmartShopProcess.nupkg
├── chrome_extension/        # Extension UI
├── requirements.txt         # Python dependencies
├── README.md
```

---

## 🚀 Setup & Usage

**1. Clone the repository**
```sh
git clone https://github.com/yourusername/smartshop-price-finder.git
cd smartshop-price-finder
```

**2. Install Python dependencies**
```sh
pip install flask flask-cors requests
```

**3. Configure and run the Flask server**
- Edit `flask_server/server.py` to add your UiPath Orchestrator credentials (client ID, secret, tenant, etc.).
- Start the server:
  ```sh
  python flask_server/server.py
  ```

**4. Deploy the UiPath workflow**
- Go to **Orchestrator > Tenant > Packages** and upload `SmartShopProcess.nupkg`.
- Create a process from this package in a folder with an available unattended or serverless robot.
- Ensure the process expects an input argument named `in_ProductName` (type: String).

**5. Trigger the workflow**
- Send a POST request to the Flask endpoint `/start-scraping` with JSON:  
  `{ "product": "iphone 15 pro" }`
- The server will trigger the UiPath job, poll for completion, and return the result.

---

## 🧪 Testing Scenarios

**1. Local Process Testing:**  
- Run and debug the UiPath workflow directly in UiPath cloud Orchestrator by starting a job or UiPath Assistant on your machine.  
- This verifies your automation logic and output without needing robot units or Orchestrator.

**2. Cloud Orchestrator or UiPath Assistant Execution:**  
- When robot units are available, start the job from UiPath Cloud Orchestrator or UiPath Assistant.  
- This runs the full automation in the cloud or on your local machine, producing live results.

**3. Flask and Chrome Extension Integration (Mock Testing):**  
- If robot units are unavailable, you can test the Flask backend and Chrome extension integration by configuring the Flask API to return sample results.  
- This allows you to verify the UI and API communication independently of the actual automation execution.

---

## 📷 Example Screenshots

**UiPath Workflow:**  
![image_alt](https://github.com/amruthae218/smartshop/blob/100a99549bc54e346958071042f90ba154c8ed86/workflow1.png)
![image_alt](https://github.com/amruthae218/smartshop/blob/100a99549bc54e346958071042f90ba154c8ed86/workflow2.png)

---

## 🛠️ Tech Stack

- **Backend:** Python Flask, REST API, CORS
- **Automation:** UiPath Cloud Orchestrator, .nupkg workflow
- **API Auth:** OAuth2 (Bearer token)
- **Testing:** Supports mock mode for local/dev

---

## 📋 Notes

- For production, ensure you have available robot units and correct Orchestrator setup.
- For local/demo or testing, use the mock mode (enabled by default if robots are unavailable).



## ⚠️ UiPath Web Automation Extension

> **Important:**  
> The UiPath workflow relies on browser automation.  
> Please ensure the UiPath Chrome or Edge extension is installed and enabled on the robot machine.  
> - For Cloud Robots (Serverless): No action needed, extension is pre-installed.  
> - For Unattended Robots/Studio/Assistant:  
>   - Install via UiPath Studio (`Home > Tools > UiPath Extensions > Chrome/Edge`)  
>   - Or from the [Chrome Web Store](https://chrome.google.com/webstore/detail/uipath-web-automation/ljfoeinjpaedjfecbmggjgodbgkmjkjk)



