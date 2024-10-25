const socket = io.connect("http://localhost:5000");

document.getElementById("chat-form").addEventListener("submit", (event) => {
    event.preventDefault();
    const messageContent = document.getElementById("message").value;
    const messageType = "text";  // Default to text message

    if (messageContent) {
        const messageData = { content: messageContent, type: messageType };
        socket.emit("send_message", messageData);
        document.getElementById("message").value = "";
    }
});

// Load chat history when the user connects
socket.on("load_history", (messages) => {
    const messagesContainer = document.getElementById("messages");
    messagesContainer.innerHTML = "";  // Clear existing messages
    messages.forEach((msg) => {
        const messageElement = document.createElement("p");
        messageElement.textContent = `${msg.username}: ${msg.content}`;
        messagesContainer.appendChild(messageElement);
    });
});

// Display incoming messages
socket.on("receive_message", (message) => {
    const messagesContainer = document.getElementById("messages");
    const newMessageElement = document.createElement("p");
    newMessageElement.textContent = `${message.username}: ${message.content}`;
    messagesContainer.appendChild(newMessageElement);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;  // Auto-scroll to the latest message
});
