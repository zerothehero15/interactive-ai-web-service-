function sendMessage() {
    const userInput = document.getElementById('userInput').value;
    if (!userInput) return;

    const messages = document.getElementById('messages');
    messages.innerHTML += `<p><strong>You:</strong> ${userInput}</p>`;

    fetch('/api/respond', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ user_input: userInput })
    })
    .then(response => response.json())
    .then(data => {
        messages.innerHTML += `<p><strong>AI:</strong> ${data.response}</p>`;
        document.getElementById('userInput').value = '';
    });
}
