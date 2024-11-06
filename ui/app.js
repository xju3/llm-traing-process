async function sendMessage() {
    const userInput = document.getElementById("user-input");
    if (!userInput) return;
    const message = {"prompt": userInput, "max_length": 100}

    displayMessage("You", message);
    userInput.value = "";

    try {
        const response = await fetch("http://127.0.0.1:8000/generate", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ message })
        });
        const data = await response.json();
        displayMessage("AI", data.response);
    } catch (error) {
        displayMessage("AI", "Error: Could not connect to the server.");
    }
}

function displayMessage(sender, message) {
    const chatBox = document.getElementById("chat-box");
    const messageElement = document.createElement("div");
    messageElement.className = sender === "You" ? "user-message" : "ai-message";
    messageElement.textContent = `${sender}: ${message}`;
    chatBox.appendChild(messageElement);
    chatBox.scrollTop = chatBox.scrollHeight;
}