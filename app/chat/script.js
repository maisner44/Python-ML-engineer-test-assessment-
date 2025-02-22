document.getElementById('sendBtn').addEventListener('click', function() {
    const userInput = document.getElementById('userInput').value.trim();
    if (!userInput) return;

    const chatOutput = document.getElementById('chatOutput');
    const loadingDiv = document.getElementById('loading');

    chatOutput.innerHTML += `<p class="user"><strong>You:</strong> ${userInput}</p>`;
    document.getElementById('userInput').value = '';

    loadingDiv.style.display = 'block';

    fetch('http://127.0.0.1:8000/query', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ question: userInput })
    })
    .then(response => response.json())
    .then(data => {
      loadingDiv.style.display = 'none';
      const formattedAnswer = data.answer.replace(/\n/g, '<br>');
      chatOutput.innerHTML += `<p class="advisor"><strong>Advisor:</strong> ${formattedAnswer}</p>`;
    })
    .catch(error => {
      console.error('Error:', error);
      loadingDiv.style.display = 'none';
      chatOutput.innerHTML += `<p class="advisor"><strong>Error:</strong> ${error}</p>`;
    });
  });
