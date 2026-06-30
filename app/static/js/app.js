const apiURL = "/api/v1/process-email";

// =============================================

async function processEmail() {

    const email = document.getElementById("email").value.trim();

    if (email.length === 0) {

        alert("Please enter an email.");

        return;

    }

    document.getElementById("loading").style.display = "block";

    document.getElementById("processBtn").disabled = true;

    try {

        const response = await fetch(apiURL, {

            method: "POST",

            headers: {

                "Content-Type": "application/json"

            },

            body: JSON.stringify({

                email: email

            })

        });

        const data = await response.json();

        document.getElementById("classification").innerHTML =
            data.classification || "--";

        document.getElementById("cache").innerHTML =
            data.cache_status || "MISS";

        document.getElementById("similarity").innerHTML =
            data.similarity_score ?? "--";

        document.getElementById("llm").innerHTML =
            data.source || "--";

        document.getElementById("context").textContent =
            data.rag_context || "No Context Retrieved";

        document.getElementById("response").textContent =
            data.response || "No Response";

    }

    catch (error) {

        alert("Server Error");

        console.error(error);

    }

    finally {

        document.getElementById("loading").style.display = "none";

        document.getElementById("processBtn").disabled = false;

    }

}

// =============================================

function clearForm() {

    document.getElementById("email").value = "";

    document.getElementById("classification").innerHTML = "--";

    document.getElementById("cache").innerHTML = "--";

    document.getElementById("similarity").innerHTML = "--";

    document.getElementById("llm").innerHTML = "--";

    document.getElementById("context").textContent =
        "No Context Retrieved";

    document.getElementById("response").textContent =
        "No Response Generated";

}

// =============================================

function copyResponse() {

    const text = document.getElementById("response").innerText;

    navigator.clipboard.writeText(text);

    alert("Response Copied");

}

// =============================================

function downloadResponse() {

    const text = document.getElementById("response").innerText;

    const blob = new Blob([text], {

        type: "text/plain"

    });

    const link = document.createElement("a");

    link.href = URL.createObjectURL(blob);

    link.download = "AI_Email_Response.txt";

    link.click();

}