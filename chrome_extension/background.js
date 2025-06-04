chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === "sendToAPI") {
    fetch("http://127.0.0.1:5000/start-scraping", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ product: request.product }),
    })
      .then((response) => response.json())
      .then((data) => {
        sendResponse({ success: true, data: data });
      })
      .catch((error) => {
        console.error("Error:", error);
        sendResponse({ success: false, error: "Connection failed" });
      });

    return true; 
  }
});
