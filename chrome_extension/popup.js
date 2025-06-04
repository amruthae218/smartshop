document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("searchButton").addEventListener("click", async function () {
        let productInput = document.getElementById("productInput").value.trim();
        if (!productInput) {
            alert("Please enter a product name!");
            return;
        }

        // Show loading
        updateUI("🔍 Searching for best prices...");

        try {
            // Call Flask API
            let response = await fetch("http://127.0.0.1:5000/start-scraping", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ product: productInput }),
            });

            let data = await response.json();
            
            if (data.success && data.data) {
                // Display UiPath results
                displayResults(data.data);
            } else {
                updateUI("❌ " + (data.error || "No results found"));
            }

        } catch (error) {
            console.error("Error:", error);
            updateUI("❌ Server connection failed");
        }
    });
});

function updateUI(text) {
    document.getElementById("results").innerHTML = `<p>${text}</p>`;
}

function displayResults(outputArgs) {
    // Parse UiPath output arguments (JSON string)
    try {
        let results;
        if (typeof outputArgs === 'string') {
            results = JSON.parse(outputArgs);
        } else {
            results = outputArgs;
        }
        
        // Display the results from UiPath (adjust based on your output argument names)
        let html = "<h3>✅ Best Price Found</h3>";
        
        // Assuming your UiPath process returns out_LeastPrice and out_LeastPriceURL
        if (results.out_LeastPrice && results.out_LeastPriceURL) {
            html += `<p><strong>Price:</strong> ₹${results.out_LeastPrice}</p>`;
            html += `<p><a href="${results.out_LeastPriceURL}" target="_blank" class="buy-button">Buy Now</a></p>`;
        } else {
            html += `<p>${JSON.stringify(results)}</p>`;
        }
        
        document.getElementById("results").innerHTML = html;
        
    } catch (e) {
        // Fallback: display raw result
        document.getElementById("results").innerHTML = `<p>Result: ${outputArgs}</p>`;
    }
}
