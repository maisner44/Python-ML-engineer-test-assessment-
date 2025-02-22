function sendMessage() {
    const userInputElement = document.getElementById('userInput');
    const userInput = userInputElement.value.trim();
    if (!userInput) return;

    const chatOutput = document.getElementById('chatOutput');
    const loadingDiv = document.getElementById('loading');

    chatOutput.innerHTML += `<p class="user"><strong>You:</strong> ${userInput}</p>`;

    userInputElement.value = '';

    loadingDiv.style.display = 'block';

    fetch('/query', {
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

    fetch('/memory', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ content: userInput })
    })
    .then(response => response.json())
    .then(data => {
      chatOutput.innerHTML += `<p class="memory"><strong>Memory:</strong> ${data.status}: ${data.content}</p>`;
    })
    .catch(error => {
      console.error('Error storing memory:', error);
      chatOutput.innerHTML += `<p class="memory"><strong>Memory Error:</strong> ${error}</p>`;
    });
  }

  document.getElementById('sendBtn').addEventListener('click', sendMessage);

  document.getElementById('userInput').addEventListener('keypress', function(event) {
    if (event.key === 'Enter') {
      sendMessage();
    }
  });
