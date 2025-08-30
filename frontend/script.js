const sendBtn = document.getElementById("send-btn");
const userInput = document.getElementById("user-input");
const chatBox = document.getElementById("chat-box");

sendBtn.addEventListener("click", async () => {
    const prompt = userInput.value.trim();
    if (!prompt) return;

    chatBox.innerHTML += `<div class="user-msg">You: ${prompt}</div>`;
    userInput.value = "";

    try {
        const res = await fetch("http://127.0.0.1:5000/api/ask", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ prompt }),
        });

        const data = await res.json();
        chatBox.innerHTML += `<div class="bot-msg">AI: ${data.reply}</div>`;
        chatBox.scrollTop = chatBox.scrollHeight;
    } catch (err) {
        chatBox.innerHTML += `<div class="bot-msg error">Error: ${err.message}</div>`;
    }
});
